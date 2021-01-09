#!/usr/bin/python3
# -*- coding: ascii -*-

import cgi
import cgitb; cgitb.enable()

from datetime import datetime
from dateutil import parser
import ephem
import ephem.stars
import io
import json
import math
import requests
import sys
import pytz

import location as AL

print("Content-type: text/html;charset=utf-8")
print("""
<html>
<head>
<title>Almanac</title>
</head>
<body>
"""
)

dtz = pytz.timezone("America/New_York")

########################################

def body_to_row(obs, n, b):
	alt = 180*float(repr(b.alt))/(math.pi)
	az =  180*float(repr(b.az))/(math.pi)
	mag = b.mag
	phase = b.phase

	down = ephem.localtime(obs.next_setting(b, start=obs.date))
	down = pytz.utc.localize(down)
	down = down.astimezone(dtz).strftime("%I:%M%p")[:-1]
	down = (" " + down[1:] if down[0] == "0" else down )

	up = ephem.localtime(obs.next_rising(b, start=obs.date))
	up = pytz.utc.localize(up)
	up = up.astimezone(dtz).strftime("%I:%M%p")[:-1]
	up = (" " + up[1:] if up[0] == "0" else up )

	s = "<tr><th>{}</th><td class='f'>{:+.1f}</td><td class='f'>{:.1f}</td><td class='f'>{:+.1f}</td>".format(n, alt, az, mag)
	s = s + "<td class='f'>{}</td><td class='f'>{}</td><td class='f'>{:.0f}</td></tr>\n".format(up, down, phase)
	return s

def get_almanac(obs):
	s =  ""
	s = s + "<tr><th></th><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}</th><th>{4}</th><th>{5}</th></tr>\n".format("ALT","AZ","MAG","RISE","SET","%")
	s = s + body_to_row(obs, "Sun", ephem.Sun(obs))
	s = s + body_to_row(obs, "Moon", ephem.Moon(obs))
	s = s + body_to_row(obs, "Venus", ephem.Venus(obs))
	s = s + body_to_row(obs, "Mars", ephem.Mars(obs))
	s = s + body_to_row(obs, "Jupiter", ephem.Jupiter(obs))
	s = s + body_to_row(obs, "Saturn", ephem.Saturn(obs))
	s = s + body_to_row(obs, "Uranus", ephem.Uranus(obs))
	s = s + body_to_row(obs, "Neptune", ephem.Neptune(obs))
	return "<table width=100% height=100% cellpadding=20>{0}</table>\n".format(s)

########################################


args = cgi.FieldStorage()

lat_arg, lon_arg = AL.getLocation(args)

dt = pytz.utc.localize(datetime.utcnow())

obs = ephem.Observer()
obs.date = dt
obs.lon = lon_arg
obs.lat = lat_arg
obs.elevation = 0

sun_alt = str(int(180*float(repr(ephem.Sun(obs).alt))/(math.pi)))
sun_az =  str(int(180*float(repr(ephem.Sun(obs).az) )/(math.pi)))

ds = dt.astimezone(dtz).strftime("%b %y")
tm = dt.astimezone(dtz).strftime("%I:%M%p")[:-1]
lat_str = "{:.2f}".format(float(lat_arg))
lon_str = "{:.2f}".format(float(lon_arg))

print("<div width=100% height=100%>")
print("<table width=100% height=100%>")
print("<tr>")
print("	<td class='b'>"+ds+"</td>")
print("	<td class='b'>"+lat_str+"</td>")
print("	<td class='b'>"+sun_alt+"</td>")
print("</tr>")
print("<tr>")
print("	<td class='b'>"+tm+"</td>")
print("	<td class='b'>"+lon_str+"</td>")
print("	<td class='b'>"+sun_az+"</td>")
print("</tr>")
print("</table>")
print(get_almanac(obs))
print("</div>")
print("</body>")
print("</html>")
