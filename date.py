#!/usr/bin/python

import db.mysqldb as sql

class Date:
	def __init__ (self, database, table):
		self.db = sql.MYSQL("localhost", "root", "19851117", database)
		self.db.connect()
		self.fillDates(table)
		return
	
	def __exit__ (self):
		self.db.close()
		return
	
	def fillDates (self, table):
		sqls = 'select Time from %s order by %s asc' % (table, 'Time')
		#self.db.search(table, None, 'Day')
		self.db.execSql(sqls)
		self.dateSet = self.db.fetch('all')
		self.dateIndex = 0
		self.indexBound = len(self.dateSet)
		#print self.indexBound
		#print self.dateSet
		return
	
	def curDate (self):
		if self.dateIndex >= 0 and self.dateIndex < self.indexBound:
			return self.dateSet[self.dateIndex][0]
		return None
	
	def nextDate (self):
		if self.dateIndex + 1 < self.indexBound:
			return self.dateSet[self.dateIndex + 1][0]
		return None
		
	def setCurDate (self, day):
		#print day
		#time = '%s' % (self.dateSet[0][0])
		#print time
		i = 0
		while i < self.indexBound:
			time = '%s' % (self.dateSet[i][0])
			if time == day:
				self.dateIndex = i
				return i
			i = i + 1
			
		return None
	
	def getSetNextDate (self):
		if self.dateIndex + 1 < self.indexBound:
			self.dateIndex = self.dateIndex + 1
			return self.dateSet[self.dateIndex][0]
		else:
			return None
	