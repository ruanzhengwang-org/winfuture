#!/usr/bin/python
import sys
sys.path.append("..")
import data

def test_data():
	"""
	$ python test_data.py
	3439.4
	3439.4
	3400.5
	3416.7
	3000.0
	3000.0
	3340.8
	"""
	dat = data.Data('futures', 'm1305_day_k')
	res = dat.M('2012-12-20', 'Close', 5)
	print res
	res = dat.M5('2012-12-20', 'Close')
	print res
	res = dat.M('2012-12-20', 'Open', 2)
	print res
	res = dat.M('2012-12-20', 'Close', 10)
	print res
	res = dat.M('2012-05-31', 'Close', 2)
	print res
	res = dat.M5('2012-05-31', 'Close')
	print res

	res = dat.M5('2013-01-11 14:55', 'Close')
	print res

if __name__ =='__main__':
	test_data()