#! /usr/bin/python

import sys
sys.path.append("..")

import data
import trade
import date as DATE
import db.mysqldb as sql
import futures as FUT


class TurtData:
	def __init__ (self, database, table):
		self.db = sql.MYSQL("localhost", 'win', 'winfwinf', database)
		self.table = table
		self.db.connect()
		return
		
	def __exit__ (self):
		self.db.close()
		return
		
	def updateTr (self, time, ltr):
		cond = 'Time=\'%s\'' % (time)
		value = 'Tr=%s' % (ltr)
		#print cond, value
		self.db.update(self.table, cond, value)
		return
	
	def updateAtr (self, time, atr):
		cond = 'Time=\'%s\'' %(time)
		value = 'Atr=%s' % (atr)
		#print cond, value
		self.db.update(self.table, cond, value)
		return


class Turtle(FUT.Futures):
	def __init__ (self, futName, dataTable, tradeTable, database='futures'):
		self.futName = futName
		self.database = database
		self.dataTable = dataTable
		self.data = data.Data(database, dataTable)
		self.dateSet = DATE.Date(database, dataTable)
		self.tradeTable = tradeTable
		self.tradeRec = trade.Trade(database, tradeTable)
		self.maxPos = None
		self.minPos = None
		self.minPosIntv = None
		self.pList = []
		self.profit = 0	
		#print "Turtle initialized!"
		return
	
	def __exit__ (self):
		return
	
	# Helper
	def __updateTr (self, table, time, ltr):
		#print time, 'ltr', ltr
		turtDat = TurtData(self.database, table)
		return turtDat.updateTr(time, ltr)
		
	def __updateAtr (self, table, time, atr):
		#print time, '                          atr', atr
		turtDat = TurtData(self.database, table)
		return turtDat.updateAtr(time, atr)
	
	def __updateAtrFromTo (self, table, tFrom, tTo, atr):
		lcDateSet = DATE.Date(self.database, table)
		time = tFrom	
		lcDateSet.setCurDate(tFrom)
		
		while time is not None and time != tTo:
			self.__updateAtr(table, time, atr)
			time = lcDateSet.getSetNextDate()
			
		self.__updateAtr(table, tTo, atr)
	
	#def updateAtrFromTo (self, table, tFrom, tTo, atr):
		#return self.__updateAtrFromTo (table, tFrom, tTo, atr)
	
	def tr (self, time):
		t = '%s' % (time)
		if self.dateSet.isFirstDate(t):
			#print self.data.getHighest(t), self.data.getLowest(t)
			ltr = self.data.getHighest(t) - self.data.getLowest(t)
		else:
			prevClose = self.data.getClose(self.dateSet.prevDate(t))
			highest = self.data.getHighest(t)
			lowest = self.data.getLowest(t)
			
			#print prevClose, highest, lowest
			#print highest-lowest, highest - prevClose, prevClose - lowest
			ltr = max(highest-lowest, highest - prevClose, prevClose - lowest)

		return ltr
		
	def atr (self, table=None):
		if table is None:
			table = self.dataTable
	
		i = 0
		atr = 0
		prevAtr = 0
		lcDateSet = DATE.Date(self.database, table)
		time = lcDateSet.firstDate()
		firstDate = time
		
		while time is not None:
			ltr = self.tr(time)
			#print 'ltr', ltr, 'prevAtr', prevAtr
			self.__updateTr(table, time, ltr)
			
			# For the beginning 20 dates, atr = (tr1 + tr2 + ... + tr20)/20
			if i < 20:
				atr = atr + ltr
				if i == 19:
					atr = atr/20
					self.__updateAtrFromTo(table, firstDate, time, atr)
					prevAtr = atr
				i = i + 1
				time= lcDateSet.getSetNextDate()
				continue
				
			# From the 21st time, atr = (prevAtr * 19 + ltr)/20
			atr = round((prevAtr * 19 + ltr)/20)
			self.__updateAtr(table, time, atr)
			#print 'atr', atr
			prevAtr = atr
			time= lcDateSet.getSetNextDate()
	
		return
	
	def query (self):
		return
	
	def setAttrs (self, maxPos, minPos, minPosIntv):
		self.maxPos = maxPos
		self.minPos = minPos
		self.minPosIntv = minPosIntv
		return
		
	def checkAttrs (self):
		if self.maxPos is None:
			return False
		elif self.minPos is None:
			return False
		elif self.minPosIntv is None:
			return False
		else:
			return True
	
	def doShort (self, dateSet, date):
		return
		
	def doLong (self, dateSet, date):
		return
	
	def hitShortSignal (self, date):
		return
		
	def hitLongSignal (self, date):
		return
		
	def run (self):
		if self.checkAttrs() is False:
			print """
			Key attributss must be set before run strategy, which could be 
			simply made calling setAttrs().
			"""
			return
		
		lcDateSet = DATE.Date(self.database, self.dataTable)
		#lcDateSet = self.dateSet
		time = lcDateSet.firstDate()
		
		while time is not None:
			if self.hitShortSignal(time):
				self.doShort(lcDateSet, time);
			elif self.hitLongSignal(time):
				self.doLong(lcDateSet, time);

			time= lcDateSet.getSetNextDate()
	
	# Get the 'lowest' in $days before $date.
	def lowestByDate (self, date, days, field='Close'):
		return self.data.lowestByDate(date, days, field)
		
	# Get the 'highest' in $days before $date.
	def highestByDate (self, date, days, field='Close'):
		return self.data.highestByDate(date, days, field)
	
	def showProfit (self):
		print "		****** Total profit %s ******" % (self.profit)	
	
	# Position Management Methods.
	def curPostion (self):
		return len(self.pList)
	
	def emptyPostion (self):
		self.pList = []
	
	def openShortPostion (self, price):
		if len(self.pList) >= self.maxPos:
			return
		self.pList.append(price)
		print "		-->> Open: %s, poses %s <<--" % (price, len(self.pList))
		return len(self.pList)
		
	def openLongPostion (self, price):
		if len(self.pList) >= self.maxPos:
			return
		self.pList.append(price)
		print "		-->> Open: %s, poses %s <<--" % (price, len(self.pList))
		return len(self.pList)
		
	def closeShortPostion (self, price):
		if len(self.pList) == 0:
			return
		profit = self.pList.pop() - price
		self.profit = self.profit + profit
		print "		<<-- Close: profit %s, poses %s -->>" % (profit, len(self.pList))
		if len(self.pList) == 0:
			self.showProfit()
			
		return len(self.pList)
	
	def closeLongPostion (self, price):
		if len(self.pList) == 0:
			return
		profit = price - self.pList.pop()
		self.profit = self.profit + profit
		print "		<<-- Close: profit %s, poses %s -->>" % (profit, len(self.pList))
		if len(self.pList) == 0:
			self.showProfit()
			
		return len(self.pList)
		
	def closeAllPostion (self, price, short):
		while len(self.pList):
			if short is 'short':
				poses = self.closeShortPostion(price)
			else:
				poses = self.closeLongPostion(price)
					
		return len(self.pList)
			
	def closeMultPostion (self, poses, price, short):
		i = 0
		while len(self.pList) and i < poses:
			if short is 'short':
				poses = self.closeShortPostion(price)
			else:
				poses = self.closeLongPostion(price)
			i = i + 1
		
		return len(self.pList)
		