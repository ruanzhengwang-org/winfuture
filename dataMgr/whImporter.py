#! /usr/bin/python

import os
import fileinput
import importer as IMPORT

class WenhuaImport(IMPORT.Import):
	def __init__ (self, database='futures'):
		#IMPORT.Import.__init__(self, dataFile, dataTable, database)
		IMPORT.Import.__init__(self, database)
		return
	
	def __exit__ (self):
		IMPORT.Import.__exit__(self)
		return
	
	#def wenhuaImport (self, tFrom, tTo):
	def newImport (self, dataFile, dataTable):
		self.prepareImport(dataTable)
		
		for line in fileinput.input(dataFile):
			cmdStr = 'echo %s | awk \'BEGIN {FS=","} {OFS=","} END {print $1}\'' % line.strip()
			res = os.popen(cmdStr)
			values = '"' + res.read().strip() + '"'
			cmdStr = 'echo %s | awk \'BEGIN {FS=","} {OFS=","} END {print $2, $3, $4, $5, $6, $7, $8}\'' % line.strip()
			res = os.popen(cmdStr)
			values = values + ',' + res.read().strip()
			values = values + ', Null' + ', Null'
			#print values
			self.db.insert(dataTable, values)
			
	# Get the Time (the first) field from records file.
	def getRecordTime(self, record):
		return self.getRecordField(record, 1)
	
	# Get the Time (the second) field from records file.
	def getRecordData(self, record):
		return self.getRecordField(record, 2)
	
	# Import data records from a directory to database.
	def importFromDir (self, directory, dataTable):
		self.prepareImport(dataTable)
		
		oFile = open('%s/o.txt' % (directory))
		hFile = open('%s/h.txt' % (directory))
		lFile = open('%s/l.txt' % (directory))
		cFile = open('%s/c.txt' % (directory))
		
		for oLine in oFile:
			oLine = oLine.strip()
			hLine = hFile.readline().strip()
			lLine = lFile.readline().strip()
			cLine = cFile.readline().strip()
			
			#print oLine
			#print hLine
			#print lLine
			#print cLine	
			
			Time = self.getRecordTime(oLine)
			Open = self.getRecordData(oLine)
			Highest = self.getRecordData(hLine)
			Lowest = self.getRecordData(lLine)
			Close = self.getRecordData(cLine)
			
			values = '"%s", %s, %s, %s, %s, 0, Null, Null, Null, Null' % (Time, Open, Highest, Lowest, Close)
			
			#print values
			
			self.db.insert(dataTable, values)
		
		oFile.close()
		hFile.close()
		lFile.close()
		cFile.close()
		
	