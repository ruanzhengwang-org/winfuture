#! /usr/bin/python

import db.mysqldb as sql

class Import:
	def __init__ (self, dataFile, dataTable, database='futures'):
		self.db = sql.MYSQL("localhost", 'win', 'winfwinf', database)
		self.db.connect()
		self.dataFile = dataFile
		self.dataTable = dataTable
		return
	
	def __exit__ (self):
		self.db.close()
		return
	
	def setAttrs (self, dataFile, dataTable):
		self.dataFile = dataFile
		self.dataTable = dataTable
		return
		
	# Prepare to import records from $self.dataFile to $self.dataTable.
	# If $self.dataTable does not exist, create it using template.
	def prepareImport(self, table, tableType='dayk'):
		if self.db.ifTableExist(table):
			return True
		
		if tableType == 'dayk':
			template = 'templateDayk'
			
		self.db.createTableTemplate(table, template)
		
	# Newly import data records from $self.dataFile to $self.dataTable
	def newImport (self):
		return
	
	# Reimport to records between date $Tfrom to date $tTo from 
	# self.table to new $table
	def partReimportTo(self, table, tFrom, tTo=None):
		if self.db.ifTableExist(self.dataTable) == False:
			return
		
		self.prepareImport(table)
		
		if (tTo is None):
			sqls = 'insert %s (select * from %s where Time >= \'%s\' order by Time asc)' % (table, self.dataTable, tFrom)
		else:
			sqls = 'insert %s (select * from %s where Time >= \'%s\' and Time <= \'%s\' order by Time asc)' % (table, self.dataTable, tFrom, tTo)
		
		res = self.db.execSql(sqls)
		
		#print 'partReimportTo'
		return res
		