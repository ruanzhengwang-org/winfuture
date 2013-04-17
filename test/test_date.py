#!/usr/bin/python
import sys
sys.path.append("..")
import date

def test_date():
	"""
	2012-05-31
	2012-06-01
	2012-06-01
	2012-06-04
	2012-06-05
	2012-06-06
	127
	2012-12-04
	2012-12-05
	"""
	time = date.Date('futures', 'm1305_day_k')
	res = time.curDate()
	print res
	res = time.nextDate()
	print res
	res = time.getSetNextDate()
	print res
	res = time.getSetNextDate()
	print res
	res = time.getSetNextDate()
	print res
	res = time.getSetNextDate()
	print res
	res = time.setCurDate('2012-12-04')
	print res
	res = time.curDate()
	print res
	res = time.nextDate()
	print res


if __name__=='__main__':
	test_date()