#!/usr/bin/python3
# -*- coding: ascii -*-


lats = {"Sunnyside":"40.7471690","Treadwell":"42.3681799","Riverhead":"40.9741481","Battery":"40.7019582"}
lons = {"Sunnyside":"-73.9199318","Treadwell":"-75.0707475","Riverhead":"-72.7162548","Battery":"-74.0163393"}

def getLocation(args):
	lat_arg = "40.7471690"
	lon_arg = "-73.9199318"
	if 'lon' in args and 'lat' in args:
		lon_arg = args["lon"].value
		lat_arg = args["lat"].value
	elif 'loc' in args:
		loc = args["loc"].value
		if loc in lats and loc in lons:
			lat_arg = lats[loc]
			lon_arg = lons[loc]
	return [lat_arg , lon_arg ]
