#!/usr/bin/python3
# -*- coding: ascii -*-

import cgi
import cgitb; cgitb.enable()

from datetime import datetime
from dateutil import parser
import io
import json
import requests
import sys

import location as AL

token = 'LbbQscqzokEOBnKqoXEURWNJHLdboNdC'
creds = dict(token=token)

print("Content-type: text/html;charset=utf-8")
print("""
<html>
</head>
<body>
<div style="width:100%; height:100%;">
"""
)

imgList = ["chanceflurries","chancerain","chancesleet","chancesnow","chancetstorms","clear","cloudy","flurries","fog", "hazy","mostlycloudy","mostlysunny","partlycloudy","partlysunny","rain","sleet","snow","sunny","tstorms"]

def getImage(s):
	ss = s.replace(' ','').strip().lower()
	if not ss in imgList:
		r = 'unknown'
		if ss.find('clear') > -1:
			r = 'mostlysunny'
		if ss.find('snow') > -1:
			r = 'snow'
		if ss.find('rain')> -1:
			r = 'rain'
		if ss.find('sleet') > -1:
			r = 'sleet'
	else:
		r = ss
	return "<img style='width:40px;height:40px;' src='/svg/{0}.svg' alt='{0}'>".format(r)

def getSooner(jf):
	s = ""
	try:
		for r in jf['properties']['periods'][0:7]:
			pd = parser.parse(r['startTime']).strftime("%a")
			pt = parser.parse(r['startTime']).strftime("%p")
			t = str(r['temperature'])+r['temperatureUnit']
			f = r['detailedForecast']
			img = getImage(r['shortForecast'])
			s = s + "<tr> <td>{0} {1}</td> <td align=center><b>{4}</b></td> <td>{2}</td> <td class='n'>{3}</td> </tr>".format(pd, pt, img, f, t)
			#s = s + "<tr>  </tr>".format(t)
	except Exception as e:
		s = "<tr><th>NO DATA</th></tr>"
	html = "<table>{0}</table>".format(s)
	return html

def getLater(jf):
	s = ""
	try:
		for r in jf['properties']['periods'][8:]:
			pd = parser.parse(r['startTime']).strftime("%a")
			pt = parser.parse(r['startTime']).strftime("%p")
			t = str(r['temperature'])+r['temperatureUnit']
			f = r['shortForecast']
			img = getImage(r['shortForecast'])
			s = s + "<tr> <td>{0} {1}</td> <td><b>{2}</b></td> <td>{4}</td>  <td class='n'>{3}</td> </tr>".format(pd, pt, t, f, img)
	except Exception as e:
		s = "<tr><th>NO DATA</th></tr>"
	html = "<table>{0}</table>".format(s)
	return html


def getForecast(lon, lat):
	pos = str(lat) + ',' + str(lon)
	try:
		url = 'https://api.weather.gov//points/'+pos
		r = requests.get(url, headers=creds)
		j = json.loads(r.text)

		rf = requests.get(j['properties']['forecast'], headers=creds)
		jf = json.loads(rf.text)
		a = getSooner(jf)
		b = getLater(jf)
	except:
		a = "NO DATA"
		b = "NO DATA"
	html = ("<table><tr><td valign=top>{0}</td><td valign=top>{1}</td></tr></table>").format(a, b)
	return html


###############################################################################


args = cgi.FieldStorage()

lat_arg, lon_arg = AL.getLocation(args)

print(getForecast(lon_arg, lat_arg))
print("</div>")
print("</body>")
print("</html>")
