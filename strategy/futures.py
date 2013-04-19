#! /usr/bin/python

import strategy as STRT

#
# Futures strategy super class which defines the most common methods 
# used to do futures business. Any futures strategy must inherit this 
# class so that the main framework could know how to interact with 
# a certain strategy.
#

class Futures(STRT.Strategy):
	def openPosition (self):
		return
	
	def openShortPostion (self):
		return
		
	def openLongPostion (self):
		return
			
	def closePosition (self):
		return
	
	def isBreakThrough (self):
		return
	