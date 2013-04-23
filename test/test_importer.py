#! /usr/bin/python

import sys
sys.path.append("..")
#import dataMgr.importer as IMPORT
#imp = IMPORT.Import('../tmp/dayk/rb09.txt', 'rb09_dayk')

import dataMgr.whImporter as IMPORT
imp = IMPORT.WenhuaImport('../tmp/dayk/rb09.txt', 'rb09_dayk')
imp.wenhuaNewImport()
imp.partReimportTo('rb09_test', '2013-02-04', '2013-03-08')

