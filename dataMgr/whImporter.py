#! /usr/bin/python

import os
import sys
sys.path.append('..')

import fileinput
import importer as IMPORT
import date

class WenhuaImport(IMPORT.Import):
	def __init__ (self, database='futures'):
		IMPORT.Import.__init__(self, database)
		return
	
	def __exit__ (self):
		IMPORT.Import.__exit__(self)
		return
	
	# Support 2 types of time formats, "yyyy-mm-dd" and "mm/dd/yyyy", in data files, 
	# but only "yyyy-mm-dd" is allowed to insert into database.
	def _formatTime (self, time):
		if time.find('-') != -1:
			return time
		elif time.find('/') != -1:
			sep = time.split('/')
			#print sep
			return '%s-%s-%s' % (sep[2], sep[0], sep[1])
		else:
			print 'Wrong time format found!'
			exit()
	
	# Import all records from a file into a datatable.
	def newImport (self, dataFile, dataTable):
		self.prepareImport(dataTable)
		
		for line in fileinput.input(dataFile):
			cmdStr = 'echo %s | awk \'BEGIN {FS=","} {OFS=","} END {print $1}\'' % line.strip()
			res = os.popen(cmdStr)
			values = '"' + self._formatTime(res.read().strip()) + '"'
			cmdStr = 'echo %s | awk \'BEGIN {FS=","} {OFS=","} END {print $2, $3, $4, $5, $6, $7, $8}\'' % line.strip()
			res = os.popen(cmdStr)
			values = values + ',' + res.read().strip()
			values = values + ', Null' + ', Null'
			#print values
			self.db.insert(dataTable, values)
	
	# Check if a record exists in a datatable.
	# Existed, return 1, otherwise return 0.
	def recordExistInTable (self, record, dataTable):
		time = self.getRecordFieldSepByComma(record, 1)
		
		sqls = 'select * from %s where Time = "%s"' % (dataTable, time)
		res = self.db.execSql(sqls)
		#print res
		return res
	
	# Insert a record into a datatable.
	def insertRecord (self, record, dataTable):
		time = self._formatTime(self.getRecordFieldSepByComma(record, 1))
		oPrice = self.getRecordFieldSepByComma(record, 2)
		hPrice = self.getRecordFieldSepByComma(record, 3)
		lPrice = self.getRecordFieldSepByComma(record, 4)
		cPrice = self.getRecordFieldSepByComma(record, 5)
		avgPrice = self.getRecordFieldSepByComma(record, 6)
		sellVol = self.getRecordFieldSepByComma(record, 7)
		buyVol = self.getRecordFieldSepByComma(record, 8)
		
		#print time, oPrice, hPrice, lPrice, cPrice, avgPrice, sellVol, buyVol
		
		values = '"%s", %s, %s, %s, %s, %s, %s, %s, Null, Null' % (time, oPrice, hPrice, lPrice, cPrice, avgPrice, sellVol, buyVol)
		self.db.insert(dataTable, values)
		
		return True
		
	# Append a record at the end of a datatable.
	def appendRecord (self, record, dataTable, date):
		time = self._formatTime(self.getRecordFieldSepByComma(record, 1))
		
		if time <= date:
			return False
		
		return self.insertRecord(record, dataTable)
		
	# Omit all records which exist in datatable, only append the records which does not 
	# exist at the end of datatable from a file.
	def appendRecordsFromFile (self, dataFile, dataTable):
		self.prepareImport(dataTable)
		
		dataSet = date.Date(self.database, dataTable)
		
		for line in fileinput.input(dataFile):
			self.appendRecord(line.strip(), dataTable, dataSet.lastDate())
			
	# Append all records files stored in a directory to database omitting all
	# records which exist in datatable.
	def appendRecordsFromDir (self, diretory):
		fList = os.listdir(diretory)
		
		while len(fList) > 0:
			#tableName = fList.pop().split('.')[0] + '_dayk'
			#print tableName
			fName = fList.pop()
			tableName = fName.split('.')[0] + '_dayk'

			if self.db.ifTableExist(tableName):
				print "Appending '%s' to '%s'..." % (fName, tableName)
				
				file = diretory + '/' + fName
				self.appendRecordsFromFile(file, tableName)
		
	# Append and possibly update a record in datatable. If the record does not 
	# exist, append it, othewise, update this record in datatable as passed $record.
	def updateToTable (self, record, dataTable):
		if self.recordExistInTable(record, dataTable) == 0:
			return self.insertRecord(record, dataTable)
		
		# Record exists in datatable, update it.
		time = self._formatTime(self.getRecordFieldSepByComma(record, 1))
		oPrice = self.getRecordFieldSepByComma(record, 2)
		hPrice = self.getRecordFieldSepByComma(record, 3)
		lPrice = self.getRecordFieldSepByComma(record, 4)
		cPrice = self.getRecordFieldSepByComma(record, 5)
		avgPrice = self.getRecordFieldSepByComma(record, 6)
		sellVol = self.getRecordFieldSepByComma(record, 7)
		buyVol = self.getRecordFieldSepByComma(record, 8)
		
		#print time, oPrice, hPrice, lPrice, cPrice, avgPrice, sellVol, buyVol
		
		values = 'Open=%s,' % oPrice
		values += 'Highest=%s,' % hPrice
		values += 'Lowest=%s,' % lPrice
		values += 'Close=%s,' % cPrice
		values += 'Avg=%s,' % avgPrice
		values += 'SellVol=%s,' % sellVol
		values += 'BuyVol=%s' % buyVol
		
		cond = 'Time="%s"' % time

		self.db.update(dataTable, cond, values)
		
	# Insert and possibly update all the records in dataFile to datatable.
	def updateRecordsFromFile (self, dataFile, dataTable):
		self.prepareImport(dataTable)
		for line in fileinput.input(dataFile):
			self.updateToTable(line.strip(), dataTable)
		
	# Get the Time (the first) field from records file.
	def getDirRecordTime (self, record):
		return self.getRecordFieldSepBySpace(record, 1)
	
	# Get the Time (the second) field from records file.
	def getDirRecordData (self, record):
		return self.getRecordFieldSepBySpace(record, 2)
	
	# Import data records in a directory to database.
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
			
			time = self._formatTime(self.getDirRecordTime(oLine))
			oPrice = self.getDirRecordData(oLine)
			hPrice = self.getDirRecordData(hLine)
			lPrice = self.getDirRecordData(lLine)
			cPrice = self.getDirRecordData(cLine)
			
			values = '"%s", %s, %s, %s, %s, 0, Null, Null, Null, Null' % (time, oPrice, hPrice, lPrice, cPrice)
			
			#print values
			
			self.db.insert(dataTable, values)
		
		oFile.close()
		hFile.close()
		lFile.close()
		cFile.close()
		
	# processRawRecords should ONLY be used combined with importFromDir(), 
	# which aims to remove the uesless header and descriptions on the top 
	# of data records imported from WenHua.
	def processRawRecords (self, directory, lines=43):
		oFile = '%s/o.txt' % (directory)
		hFile = '%s/h.txt' % (directory)
		lFile = '%s/l.txt' % (directory)
		cFile = '%s/c.txt' % (directory)
		
		cmdStr = 'sed -i "1,%sd" %s' % (lines, oFile)
		os.popen(cmdStr)
		cmdStr = 'sed -i "1,%sd" %s' % (lines, hFile)
		os.popen(cmdStr)
		cmdStr = 'sed -i "1,%sd" %s' % (lines, lFile)
		os.popen(cmdStr)
		cmdStr = 'sed -i "1,%sd" %s' % (lines, cFile)
		os.popen(cmdStr)
		
	