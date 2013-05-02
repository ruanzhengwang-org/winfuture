#!/usr/bin/python

import sys
sys.path.append("..")
from display.output import *

def test_output():
	#testColors()
	dis=PrintColor()
	dis.addTemplete("dgw",colorAttr['def'],colorTxt['g'],colorBg['w'])
	dis.addTemplete("drw",colorAttr['def'],colorTxt['r'],colorBg['w'])
	dis.addTemplete("dbbl",colorAttr['def'],colorTxt['b'],colorBg['bl'])
	print dis.templete
	args=[]
	args.append(('dgw', 'attr:default, text:green, backgraound:white',))
	args.append(('drw', 'attr:default, text:red, backgraound:white'))
	args.append(('dbbl','attr:default, text:blue, backgraound:black'))
	
	#args.append(('wrong','wrong'))
	print args
	dis.printColor(*args)
	
if __name__ == "__main__":
	test_output()
