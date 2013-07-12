#! /usr/bin/python

'''
Emulation subsystem is capable of running a set of regression tests 
parallelly which could be better simulate real Future trading.

Ruan Zhengwang (ruan.zhengwang@gmail.com)
'''

import sys
sys.path.append('..')
import thread
import time
import strategy.turt1 as turt1
import tick
import runstat

# Log management.
class Log:
	def __init__ (self, logName):
		self.logName = logName
		try:
			self.logObj = open(logName, 'w')
		except:
			print "Open log file '%s' failed!" % logName
			return
		return
	
	def __exit__ (self):
		self.logObj.close()
		return
	
	# Append a log at the end of log file.
	def append (self, logs):
		try:
			self.logObj.write('%s\n' % logs)
		except:
			print "Writing log to '%s' failed!" % self.logName
			return
		
	# Close the log file.
	def close (self):
		self.logObj.close()
			
# Common attributes used for strategy to do regression. 
class CommonAttrs:
	def __init__ (self, maxAddPos, minPos, minPosIntv, priceUnit):
		self.maxAddPos = maxAddPos
		self.minPos = minPos
		self.minPosIntv = minPosIntv
		self.priceUnit = priceUnit
		return

# Core run time conntrol block between main thread and child thread.
class RunControl:
	def __init__ (self, acted, lock, tick, attrs, applied):
		self.acted = acted		# 'True' means child thread has taken action, 'False' 
						# means waitting for child thread to take action.
		self.lock = lock		# Lock to protect control attributes from changing.
		self.tick = tick		# Any time when tick varies, child thread needs checking
						# if should take actions.
		self.attrs = attrs		# Common attributes used for strategy to do regression.
		self.applied = applied		# 'True' means this control block is occupied by a thread.
		self.log = None			# Log object if not None, which helps manage logs in regression.
		return
	
	# Judge if self.tick matches a time tick.
	def tickMatch (self, timeTick):
		#print self.tick, timeTick
		t1 = time.strptime(self.tick, '%Y-%m-%d')
		t2 = time.strptime(timeTick, '%Y-%m-%d')
		
		return t1 == t2
		
	# Judge if self.tick is leg behind a time tick.
	def tickBehind (self, timeTick):
		#print self.tick, timeTick
		t1 = time.strptime(self.tick, '%Y-%m-%d')
		t2 = time.strptime(timeTick, '%Y-%m-%d')
		
		return t1 < t2
			
	# Do a micro HLT operation.
	def tinyHltLoop (self):
		#time.sleep(0.01)
		return
	
	# Judge if a tick is ready for a strategy to take actions.
	def tickIsReady (self, timeTick):
		self.lock.acquire()
		if self.acted:
			self.lock.release()
			self.tinyHltLoop()
			return False
		elif self.tickBehind(timeTick):
			self.acted = True
			self.lock.release()
			self.tinyHltLoop()
			return False
		elif self.tickMatch(timeTick):
			self.lock.release()
			return True
		else:
			print "# Exception #: Ticks '%s' are over time tick '%s' in thread, causing never ending..." % (self.tick, timeTick)
	
	# Set acted noticing main thread actions have been taken.
	def setActed (self):
		self.lock.acquire()
		self.acted = True
		self.lock.release()
		
	# Enable storing logs.
	def enableStoreLogs(self, logObj):
		self.log = logObj
		
# Run Time Control Block Set containing a set of Run Control blocks, 
# necessary for an emulation.
class RunCtrlSet:
	def __init__ (self, maxAllowedPos, tickSrc):
		self.num = 0
		self.set = []
		self.maxAllowedPos = maxAllowedPos
		self.tickSrc = tickSrc
		return
	
	def __exit__ (self):
		return
	
	def nrRunCtrl (self):
		return len(self.set)
		
	# Append a Run Control block.	
	def add (self, attr):
		#if self.nrRunCtrl() < self.num:
		self.set.append(attr)
		self.num += 1
		return self.nrRunCtrl()
	
	# Acquire the protection lock for run control block indexed by @index.
	def acquireLock (self, index):
		self.set[index].lock.acquire()
		
	# Release the protection lock for run control block indexed by @index.
	def releaseLock (self, index):
		self.set[index].lock.release()
		
	# Acquire protection locks for all run control blocks.
	def acquireAllLocks (self):
		i = 0
		while (i < self.num):
			self.set[i].lock.acquire()
			i += 1
			
	# Release protection locks for all run control blocks.
	def releaseAllLocks (self):
		i = 0
		while (i < self.num):
			self.set[i].lock.release()
			i += 1
		
	# Return if a run control block is occupied.
	def isApplied (self, index):
		return self.set[index].applied
	
	# Set a run control block occupied.
	def setApplied (self, index):
		self.set[index].applied = True
		
	# Clear a run control block occupied.
	def clearApplied (self, index):
		self.set[index].applied = False
		
	# Return if all child threads are stopped.
	# Note, this will acquire all protection locks.
	def ifAllStoppedWithLocks (self):
		self.acquireAllLocks()
		allStopped = True
		i = 0
		while (i < self.num):
			if self.isApplied(i):
				allStopped = False
				break
			i += 1
		self.releaseAllLocks()
		return allStopped
				
	# Return if a child thread has taken actions after tick varied.
	def isActed (self, index):
		return self.set[index].acted
	
	# Set acted noticing main thread actions have been taken.
	def setActed (self, index):
		self.set[index].acted = True
			
	# Clear all acted tag for running threads (applied == True).
	def clearActedIfApplied (self):
		i = 0
		while (i < self.num):
			if self.set[i].applied:
				self.set[i].acted = False
			else:
				self.set[i].acted = True
			i += 1
			
	# Judge if all child threads have taken actions after tick varied.
	def ifAllActed (self):
		#self.acquireAllLocks()
		allActed = True
		i = 0
		while (i < self.num):
			if not self.isActed(i):
				allActed = False
				break
			i += 1
		#self.releaseAllLocks()
		return allActed
		
	# New a tick and set for all child threads.	
	def setNewTicks (self):
		newTick = self.tickSrc.tickNext()
		i = 0
		while (i < self.num):
			self.set[i].tick = newTick
			i += 1
		
	# Set a tick for all child threads.
	def setTick (self, timeTick):
		i = 0
		while (i < self.num):
			self.set[i].tick = timeTick
			i += 1
			
# End call for an emulation thread.
def emulationThreadEnd (runCtrl):
	# Be careful, need to set 'acted' as True before exit an emulation thread, 
	# because it is possible to be set False by clearActedIfApplied() while 
	# competing to acquie the lock.
	runCtrl.lock.acquire()
	runCtrl.applied = False
	#print 'emulationThread acted %d' % runCtrl.acted
	runCtrl.acted = True
	runCtrl.lock.release()
	
	if runCtrl.log:
		runCtrl.log.close()
		
	thread.exit_thread()
	return

# Entry for an emulation thread.
def emulationThreadStart (strategy, futCode, runCtrl):
	strt1 = None
	runStat = runstat.RunStat(futCode)
	
	if strategy == 'turt1':
		strt1 = turt1.Turt1 (futCode, '%s_dayk' % futCode, 'dummy', 'history', runStat)
	else:
		print "Bad strategy, only supports 'turt1' right now..."
		emulationThreadEnd(runCtrl)
		return
		
	# Enable storing logs.
	logTemp = 'logs/%s.log' % futCode	
	futLog = Log(logTemp)
	runCtrl.enableStoreLogs(futLog)
	
	strt1.setAttrs(runCtrl.attrs.maxAddPos, runCtrl.attrs.minPos, 
			runCtrl.attrs.minPosIntv, runCtrl.attrs.priceUnit)
			
	# Enable emulation mode for strategy.	
	strt1.enableEmulate(runCtrl)
	strt1.run()
	if strt1.runStat is not None:
		strt1.runStat.showStat()
		
	emulationThreadEnd(runCtrl)

# Emulation Core.
class Emulate:
	def __init__ (self, strategy, ctrlSet, futList):
		self.strategy = strategy
		self.ctrlSet = ctrlSet
		self.futList = futList
		return
	
	def __exit__ (self):
		return
			
	def run (self):
		#lock = thread.allocate_lock()
		
		# At this point, no threads are running, so directly set current tick with no lockings.
		self.ctrlSet.setTick(self.ctrlSet.tickSrc.curTick())
		
		# Exits loop only when Futures list is empty and all child threads are stopped.
		while len(self.futList) != 0 or not self.ctrlSet.ifAllStoppedWithLocks():
			# if Futures list is not empty, allocate a run control block for the 
			# top Future and emulate it in a thread.
			if len(self.futList) != 0:
				i = 0
				while i < self.ctrlSet.num:
					self.ctrlSet.acquireLock(i)
					if not self.ctrlSet.isApplied(i):
						#lock.acquire()
						if len(self.futList) == 0:
							self.ctrlSet.setActed(i)
							self.ctrlSet.releaseLock(i)
							i += 1
							continue
						futCode = self.futList.pop()
						#lock.release()
						self.ctrlSet.setApplied(i)
						self.ctrlSet.releaseLock(i)
						
						print 'Thread %d:' % i
						thread.start_new_thread(emulationThreadStart, 
								(self.strategy, futCode, self.ctrlSet.set[i]))
					else:
						self.ctrlSet.releaseLock(i)
					i += 1
			
			# Check if all child threads have taken actions after tick varied previously.
			# If all acted, set next tick and notice child threads to continue.
			
			#time.sleep(0.01)
			self.ctrlSet.acquireAllLocks()
			allActed = self.ctrlSet.ifAllActed()
			if allActed:
				self.ctrlSet.setNewTicks()
				self.ctrlSet.clearActedIfApplied()
			
			self.ctrlSet.releaseAllLocks()
		
if __name__ == '__main__':
	#futList = ['m0401', 'm0501', 'm0601', 'm0701', 'm0801']
	futList = ['m0401', 'm0501']
	futList.reverse()
	comAttr = CommonAttrs(4, 1, 40, 10)
	runCtrl1 = RunControl(False, thread.allocate_lock(), None, comAttr, False)
	runCtrl2 = RunControl(False, thread.allocate_lock(), None, comAttr, False)
	
	tickSrc = tick.Tick(2003, 1, 1)
	
	runCtrlSet = RunCtrlSet(6, tickSrc)
	runCtrlSet.add(runCtrl1)
	runCtrlSet.add(runCtrl2)
	
	emu = Emulate('turt1', runCtrlSet, futList)
	emu.run()
	
	