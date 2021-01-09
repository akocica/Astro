#!/usr/bin/python3
# -*- coding: ascii -*-

import cgi
import cgitb; cgitb.enable()

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
<head>
</head>
<body>
"""
)

def getWeatherStation(id, creds):
	url = 'https://api.weather.gov/stations/'+id+'/observations/current'
	d = json.loads(requests.get(url, headers=creds).text)['properties']
	ds = {}
	ds['Timestamp'] = d['timestamp'][:16][-5:]
	ds[' Conditions'] = d['textDescription']
	try:
		ds['   Temperature'] = round(float(d['temperature']['value'])* 9/5.0 + 32, 1)
	except:
		ds['   Temperature'] = ""

	try:
		ds['Wind DSG'] = str(int(d['windDirection']['value'])) + "/"
	except:
		ds['Wind DSG'] = "/"
		
	try:
		ds['Wind DSG'] = ds['Wind DSG'] + str(int(d['windSpeed']['value'])) + "/"
	except:
		ds['Wind DSG'] = ds['Wind DSG'] + "/"
		
	try:
		ds['Wind DSG'] = ds['Wind DSG'] + str(int(d['windGust']['value']))
	except:
		pass

	try:
		ds['Barometer'] = d['barometricPressure']['value']
	except:
		ds['Barometer'] = ""
	#try:
	#	ds['Pressure'] = d['seaLevelPressure']['value']
	#except:
	#	ds['Pressure'] = ""
	try:
		ds['Visibility'] = d['visibility']['value']
	except:
		ds['Visibility'] = ""
	try:
		ds['  Humidity'] = round(float(d['relativeHumidity']['value']),1)
	except:
		ds['  Humidity'] = ""

	return ds


def getWeather(lon, lat):
	pos = str(lat) + ',' + str(lon)
	creds = dict(token=token)
	url = "https://api.weather.gov//points/"+pos+"/stations"
	r = requests.get(url, headers=creds)
	data = {}
	n = 4
	rn = range(0,n)
	for k in json.loads(r.text)['features'][:n]:
		id = k['properties']['stationIdentifier']
		data[id] = getWeatherStation(id, creds)
	sd = sorted(list(data.keys()))
	s = '<tr><th></th>\n'
	for d in [sd[r] for r in rn]:
		s = s + '<th>{0}</th>\n'.format(d)
	s = s + '</tr>\n'
	for p in sorted(list(data[sd[0]].keys())):
		sy = ''
		if p == ' Conditions':
			sy = " class='n' align=right"
		s = s + '<tr><th>{0}</th>\n'.format(p)
		for d in [data[sd[r]][p] for r in rn]:
			s = s + '<td'+sy+' width=20% align=right>{0}</td>\n'.format(d)
	s = s + '</tr>\n'
	s = '\n<table width=100% height=100% cellspacing=10>\n{0}</table>\n'.format(s)
	return s

###############################################################################


args = cgi.FieldStorage()

lat_arg, lon_arg = AL.getLocation(args)
try:
	print(getWeather(lon_arg, lat_arg))
except:
	print("<P>NO DATA</P>")
print("</body>")
print("</html>")
