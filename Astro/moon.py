#!/usr/bin/python3
# -*- coding: ascii -*-

import cgi
import cgitb; cgitb.enable()

import ephem

map = [2,25,5,17,7,10,26,9,4,13,15,23,24,14,8,11,16,21,19,22,6,18,20,1,0,12]
print("Content-type: text/html;charset=utf-8")
print("""
<html>
<head>
<title>Moon</title>
</head>
<body>""")
d = int((ephem.now() - ephem.previous_new_moon(ephem.now()))/1.00)
if d > 25:
	d =  25;
dd = map[d]
print("<img style='height:100px;' src='/svg/{0}.svg' alt='{1} days old'> ".format(dd,d))
print("</body>")
print("</html>")
