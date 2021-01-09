#!/usr/bin/python3
# -*- coding: ascii -*-

import cgi
import cgitb; cgitb.enable()
from datetime import datetime
import ephem as E
import ephem.stars as ES
import math
import pytz
import location as AL

print("Content-type: text/html;charset=utf-8")
print("""
<html>
<head>
<title>Sky</title>
</head>
<body>
"""
)

dtz = pytz.timezone("America/New_York")

args = cgi.FieldStorage()

lat_arg, lon_arg = AL.getLocation(args)

dt = pytz.utc.localize(datetime.utcnow())

obs = E.Observer()
obs.date = datetime.utcnow()
obs.lon = lon_arg
obs.lat = lat_arg
obs.elevation = 0

ds = dt.astimezone(dtz).strftime("%b %y")
tm = dt.astimezone(dtz).strftime("%I:%M%p")[:-1]


P = [{"e":E.Sun(obs),    "nm":"Sun",     "c":"yellow", 	"v":20},\
     {"e":E.Moon(obs),   "nm":"Moon",    "c":"blue", 	"v":16},\
     {"e":E.Venus(obs),  "nm":"Venus",   "c":"lightblue", 	"v":8},\
     {"e":E.Mars(obs),   "nm":"Mars",    "c":"red", 	"v":6},\
     {"e":E.Jupiter(obs),"nm":"Jup", "c":"green", 	"v":8},\
     {"e":E.Saturn(obs), "nm":"Sat",  "c":"orange", 	"v":6} ]
B = []

for p in P:
	p["e"].compute(obs)
	if p["e"].alt > 0:
		B.append(p)

for star in ES.db.split("\n"):
    n = star.split(",")[0]
    if len(n) > 0:
        es = E.star(n)
        es.compute(obs)
        if es.mag < 4 and es.alt > 0:
            sd = {"e":es,"nm":n}
            B.append(sd)
for b in B:
    if "v" not in b:
        n = int(float(repr(b['e'].mag)) + 2)
        if n > 5:
            n = 5
        b["v"] = [6, 5, 4, 3, 1.5, 1.0, 0.5, 0.25, 0.1][n]

print("<svg height='360' width='360' version='1.1' viewBox='-24 -24 384 384'  xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>")
print("<rect width='100%' height='100%' fill='#000033'/>")
print("<g stroke='#58D68D' stroke-width='1.25' fill='#000033' opacity='0.25'>")
p = """<g><circle cx='180' cy='180' r='180' />
<circle cx='180' cy='180' r='120'/>
<circle cx='180' cy='180' r='60' /></g>
<g><line x1='180' y1='0' x2='180' y2='360' />
<line x1='0' y1='180' x2='360' y2='180' /></g>
<g transform = 'translate(180, 180) rotate(45) translate(-180, -180)'>
<line x1='180' y1='0' x2='180' y2='360' />
<line x1='0' y1='180' x2='360' y2='180' /></g>"""
print(p)

print("</g>")
print("<g stroke='gray' stroke-width='0.5' fill='white' opacity='0.75'>")
for b in B:
    r = (math.pi/2 - b['e'].alt)/(math.pi/2.0)
    theta =  b['e'].az - math.pi/2.0
    x = r * math.cos(theta) * 180.0 + 180
    y = r * math.sin(theta) * 180.0 + 180
    sc = ("" if "c" not in b else " fill='{}'".format(b["c"]) )
    s = "\t<circle cx='{:.4f}' cy='{:.4f}' r='{:.2f}'{}/>".format(x, y, b["v"], sc)
    print(s)
print("</g>")

print("<g fill='yellow' style='direction:rtl;font-family:Sans,Arial;font-size:11;'>")
for b in B:
    if b['e'].mag < 1.6 or b['nm'] == "Polaris":
        r = (math.pi/2.0 - b['e'].alt)/(math.pi/2.0)
        theta =  b['e'].az - math.pi/2.0
        a = (12 if b["v"] > 5 else 8)
        a = (0 if b["v"] > 10 else a)
        x = (r * math.cos(theta) * 180.0 + 180) + (len(b["nm"]) * 3.2)
        y = (r * math.sin(theta) * 180.0 + 180) - a
        s = "\t<text x='{:.2f}' y='{:.2f}'>{}</text>".format(x,y,b["nm"])
        print(s)
print("</g>")
print("</svg>")

print("</body>")
print("</html>")
