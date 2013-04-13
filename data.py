#! /usr/bin/python

import db.mysqldb as sql

class Data:
	def __init__ (self, database):
		self.db = sql.MYSQL("localhost", "root", "19851117", database)
		self.db.connect()
		return
	
	def __exit__ (self):
		self.db.close()
		return 
	
	def sum (self, data):
		i = 0
		sum = 0
		#print data[0], data[0][0], len(data)

		while i < len(data):
			sum = sum + data[i][0]
			i = i + 1
			
		return sum

	def avg (self, data, count):
		return self.sum(data) / count
	
	def M (self, table, date, filed='Close', days=1):
		cond = 'Time <= "%s" order by Time desc limit %d' % (date, days)
		#print cond
		num = self.db.search(table, cond, filed)
		res = self.db.fetch('all')
		#print res
		#print res[0][0]

		return self.avg(res, num)
	
	def M5 (self, table, date, filed='Close'):
		return self.M(table, date, filed, 5)
	
	def M10 (self, table, date, filed='Close'):
		return self.M(table, date, filed, 10)
	
	def M20 (self, table, date, filed='Close'):
		return self.M(table, date, filed, 20)
	
	def M40 (self, table, date, filed='Close'):
		return self.M(table, date, filed, 40)
	
	def M60 (self, table, date, filed='Close'):
		return self.M(table, date, filed, 60)
	