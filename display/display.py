#!/usr/bin/python
"""
0  All attributes off  default
1  Bold (or Bright) 
4  Underline 
5  Blink 
7  Invert 
30 Black text
31 Red text
32 Green text
33 Yellow text
34 Blue text
35 Purple text
36 Cyan text
37 White text
40 Black background
41 Red background
42 Green background
43 Yellow background
44 Blue background
45 Purple background
46 Cyan background
47 White background
"""
import sys, os

colorTxt={
	#Colors for text
	"bl":'30',	#black
	"r" :'31',	#red
	"g" :'32',	#green
	"y" :'33',	#yellow
	"b" :'34',	#blue
	"p" :'35',	#purple
	"c" :'36',	#cyan
	"w" :'37'	#white
}

colorBg={
	#Colors for background
	"bl":'40',	#black
	"r" :'41',	#red
	"g" :'42',	#green
	"y" :'43',	#yellow
	"b" :'44',	#blue
	"p" :'45',	#purple
	"c" :'46',	#cyan
	"w" :'47'	#white
}
colorAttr={
#Colors for attribute
	"def":'0',	#default
	"bld":'1',	#blod
	"und":'4',	#underline
	"bli":'5',	#blink
	"inv":'7'	#invert
}


class COLORS:

	def __init__(self):
		self.templete={"def":"0;;"}

	def addTemplete(self, keyword, attr='0', text='', background=''):
		self.templete[keyword]= ';'.join([attr, text, background])
        
        
class PrintColor(COLORS):

	def __init__(self):
		COLORS.__init__(self)
		if sys.platform.find("win") != -1:
			self.start = "%s"
			self.end=''
		else:
			self.start = "\x1B[%sm"
			self.end = "\x1B[0m"

	def printColor(self, *args):
		output = ''
		try:
			for (key,value) in args:
			#	print key+value
				form = self.templete[key]
				value_formed = self.start % form
				output += value_formed+str(value)
			output += self.end

		except KeyError, e:
			print "Error: %d, %s" % (e.args[0], e.args[1])
			print "There is no keyword %s in the templete, please check" % key
			sys.exit(1) 
		finally:
			print output

def testColors():
	""" """
	for atrr in iter([0,1,4,5,7]):
		print "attribute %d ------------------------------" % atrr
		for fore in [30,31,32,33,34,35,36,37]:
			for back in [40,41,42,43,44,45,46,47]:
				color = "\033[%d;%d;%dm" % (atrr,fore,back)
				print "%s %d-%d-%d\033[0m" % (color,atrr,fore,back),
			print ""

                        
if __name__ == "__main__":
	""" """
	#testColors()
	dis=PrintColor()
	dis.addTemplete("dgw",colorAttr['def'],colorTxt['g'],colorBg['w'])
	dis.addTemplete("drw",colorAttr['def'],colorTxt['r'],colorBg['w'])
	dis.addTemplete("dbbl",colorAttr['def'],colorTxt['b'],colorBg['bl'])
	print dis.templete
	args=[]
	args.append(('dgw','dgw'))
	args.append(('drw','drw'))
	args.append(('dbbl','dbbl'))
	args.append(('dbbl','abcd'))
	#args.append(('wrong','wrong'))
	print args
	dis.printColor(*args)

