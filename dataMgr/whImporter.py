#! /usr/bin/python

import os
import fileinput
import importer as IMPORT

class WenhuaImport(IMPORT.Import):
	def __init__ (self, dataFile, dataTable, database='futures'):
		IMPORT.Import.__init__(self, dataFile, dataTable, database)	
		return
	
	def __exit__ (self):
		IMPORT.Import.__exit__(self)
		return
	
	#def wenhuaImport (self, tFrom, tTo):
	def wenhuaNewImport (self):
		self.prepareImport(self.dataTable)
		
		for line in fileinput.input(self.dataFile):
			cmdStr = 'echo %s | awk \'BEGIN {FS=","} {OFS=","} END {print $1}\'' % line.strip()
			res = os.popen(cmdStr)
			values = '"' + res.read().strip() + '"'
			cmdStr = 'echo %s | awk \'BEGIN {FS=","} {OFS=","} END {print $2, $3, $4, $5, $6, $7, $8}\'' % line.strip()
			res = os.popen(cmdStr)
			values = values + ',' + res.read().strip()
			values = values + ', Null' + ', Null'
			#print values
			self.db.insert(self.dataTable, values)
	