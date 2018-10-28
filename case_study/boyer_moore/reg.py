#!/usr/bin/python
import re

line = "delta1[1333] == 344";

searchObj = re.search( r'delta[1,2]\[[1-9]+\] == [0-9]+', line, re.M|re.I)

if searchObj:
   print "searchObj.group() : ", searchObj.group()
   # print "searchObj.group(1) : ", searchObj.group(1)
   # print "searchObj.group(2) : ", searchObj.group(2)
else:
   print "Nothing found!!"
