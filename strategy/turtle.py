#! /usr/bin/python

import sys
sys.path.append("..")

import data
import trade

class Turtle:
	def __init__ (self, future, maxPos, direc, dataTable):
		self.future = future
		self.maxPos = maxPos
		self.direc = direc
		self.data = data.Data('futures', dataTable)
		
		#print "Turtle initialized!"
		return
	
	def __exit__ (self):
		return
	
	def atr (self):
		return
	
	def openPosition (self):
		return
	
	def closePosition (self):
		return
	
	def breakThrough (self):
		return
	
	def query (self):
		return
	
	def set (self):
		return 
	