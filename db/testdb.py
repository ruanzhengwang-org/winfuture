#! /usr/bin/python
# coding=gbk

import sys
import mysqldb as sql

db = sql.MYSQL ('localhost', 'root', '19851117', 'futures')

db.connect()
db.setDefTable('futures')
#res = db.search('Oid >= 2', 'Price')
ret = db.search('trading', 'Oid >= 2')
print "ret: %d" % ret
res = db.fetch(1)
#print res.decode('utf-8')
print res

db.insert('trading', "'', 'm1305', '2012-12-28 14:37:48', 'duo', 1, 3368, 1, 0.09, 0, 0, 'tupo m10', 'python'")

db.update('trading', 'Oid = 12', "Reason='tu po M10', Comments='Python DB5'")

ret = db.search('trading', 'Oid > 10', 'Oid, TradeDate, Price, Times')
print "ret: %d" % ret
print db.fetch(0)

#db.remove('trading', 'Oid > 20')

db.close()


#import voice

#v = voice.Voice ("Dog is runing")
#v.Yield ()
            
#t = CAnimal()
#t.Say()