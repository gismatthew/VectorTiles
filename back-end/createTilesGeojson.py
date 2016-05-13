import math
import urllib
import os

def getR():
	return 6378137

def getResolution(zoom):
	return 2 * math.pi * getR() / 256 / 2**zoom

def getOrigShift():
	return 2 * math.pi * getR() / 2

def convertPixelToMeters(px, py, zoom):
	res = getResolution(zoom)
	origShift = getOrigShift()
	x = px * res - origShift
	y = py * res - origShift
	return [x, y]

def convertMetersToLatLng(mx, my):
	origShift = getOrigShift()
	lng = mx / origShift * 180
	lat = my / origShift * 180
	lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
 	return [lng, lat]

def convertTileToLatLng(x, y, zoom):
	mp = convertPixelToMeters(x*256, y*256, zoom)
	return convertMetersToLatLng(mp[0], mp[1])

def convertTileToLatLngBounds(x, y, z):
	p1 = convertTileToLatLng(x, y, z)
	p2 = convertTileToLatLng(x+1, y+1, z)
	return [p1, p2]

def convertTileToMeters(x, y, zoom):
	return convertPixelToMeters(x*256, y*256, zoom)

def convertTileToMeterBounds(x, y, z):
	p1 = convertTileToMeters(x, y, z)
	p2 = convertTileToMeters(x+1, y+1, z)
	return [p1, p2]

def createTilesGeojson(zoom1, zoom2):
	total_file = 0
	cur_file = 0
	for z in xrange(zoom1, zoom2+1):
		n = 2**z
		total_file += n*n
	for z in xrange(zoom1, zoom2+1):
		n = 2**z
		dir0 = 'tiles_geojson/' + str(z)
		if not os.path.exists(dir0):
			os.makedirs(dir0)
		for x in xrange(0, n):
			dir0 = 'tiles_geojson/' + str(z) + '/' + str(x)
			if not os.path.exists(dir0):
				os.makedirs(dir0)
			for y in xrange(0, n):
				file0 = 'tiles_geojson/' + str(z) + '/' + str(x) + '/' + str(y) + '.geojson'
				# if not os.path.isfile(file0):
				# bbox = convertTileToLatLngBounds(x, y, z)
				bbox = convertTileToMeterBounds(x, y, z)
				bbox = str(bbox[0][0]) + ',' + str(bbox[0][1]) + ',' + str(bbox[1][0]) + ',' + str(bbox[1][1])
				dl = urllib.URLopener()
				# url = 'http://localhost:8080/geoserver/gwc/service/wms?LAYERS=matt:demo-world&FORMAT=application/json;type=geojson&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&SRS=EPSG:4326&BBOX=' + bbox + '&WIDTH=256&HEIGHT=256'
				url = 'http://localhost:8080/geoserver/gwc/service/wms?LAYERS=matt:demo-world&FORMAT=application/json;type=geojson&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&SRS=EPSG:900913&BBOX=' + bbox + '&WIDTH=256&HEIGHT=256'

				# print url
				# print "Saving to " + file0

				try:
					dl.retrieve(url, file0)
				except:
					print "fail to retrieve: " + url
				
				# update the progress
				cur_file += 1
				p = round(cur_file * 100.0 / total_file, 1)
				print 'Progress: ' + str(p) + '% (' + str(cur_file) + '/' + str(total_file) + ')'
	
	print 'Done!'

def createTilesTopojson(zoom1, zoom2):
	total_file = 0
	cur_file = 0
	for z in xrange(zoom1, zoom2+1):
		n = 2**z
		total_file += n*n
	for z in xrange(zoom1, zoom2+1):
		n = 2**z
		dir0 = 'tiles_topojson/' + str(z)
		if not os.path.exists(dir0):
			os.makedirs(dir0)
		for x in xrange(0, n):
			dir0 = 'tiles_topojson/' + str(z) + '/' + str(x)
			if not os.path.exists(dir0):
				os.makedirs(dir0)
			for y in xrange(0, n):
				file0 = 'tiles_topojson/' + str(z) + '/' + str(x) + '/' + str(y) + '.topojson'
				# if not os.path.isfile(file0):
				# bbox = convertTileToLatLngBounds(x, y, z)
				bbox = convertTileToMeterBounds(x, y, z)
				bbox = str(bbox[0][0]) + ',' + str(bbox[0][1]) + ',' + str(bbox[1][0]) + ',' + str(bbox[1][1])
				dl = urllib.URLopener()
				# url = 'http://localhost:8080/geoserver/gwc/service/wms?LAYERS=matt:demo-world&FORMAT=application/json;type=geojson&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&SRS=EPSG:4326&BBOX=' + bbox + '&WIDTH=256&HEIGHT=256'
				url = 'http://localhost:8080/geoserver/gwc/service/wms?LAYERS=matt:demo-world&FORMAT=application/json;type=topojson&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&SRS=EPSG:900913&BBOX=' + bbox + '&WIDTH=256&HEIGHT=256'
				
				# print url
				# print "Saving to " + file0
				
				try:
					dl.retrieve(url, file0)
				except:
					print "fail to retrieve: " + url
				
				# update the progress
				cur_file += 1
				p = round(cur_file * 100.0 / total_file, 1)
				print 'Progress: ' + str(p) + '% (' + str(cur_file) + '/' + str(total_file) + ')'
	
	print 'Done!'

def createTilesPBF(zoom1, zoom2, tms):
	total_file = 0
	cur_file = 0
	if (tms):
		dirName = 'tiles_pbf_tms/'
	else:
		dirName = 'tiles_pbf/'
	for z in xrange(zoom1, zoom2+1):
		n = 2**z
		total_file += n*n
	for z in xrange(zoom1, zoom2+1):
		n = 2**z
		dir0 = dirName + str(z)
		if not os.path.exists(dir0):
			os.makedirs(dir0)
		for x in xrange(0, n):
			dir0 = dirName + str(z) + '/' + str(x)
			if not os.path.exists(dir0):
				os.makedirs(dir0)
			for y in xrange(0, n):
				if (tms):
					file0 = dirName + str(z) + '/' + str(x) + '/' + str(y) + '.pbf'
				else:
					file0 = dirName + str(z) + '/' + str(x) + '/' + str(n-y-1) + '.pbf'
				
				# if not os.path.isfile(file0):
				# bbox = convertTileToLatLngBounds(x, y, z)
				bbox = convertTileToMeterBounds(x, y, z)
				bbox = str(bbox[0][0]) + ',' + str(bbox[0][1]) + ',' + str(bbox[1][0]) + ',' + str(bbox[1][1])
				dl = urllib.URLopener()
				url = 'http://localhost:8080/geoserver/gwc/service/wms?LAYERS=matt:imm_country&FORMAT=application/x-protobuf;type=mapbox-vector&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&SRS=EPSG:900913&BBOX=' + bbox + '&WIDTH=256&HEIGHT=256'
				
				# print url
				# print "Saving to " + file0
				
				try:
					dl.retrieve(url, file0)
				except:
					print "fail to retrieve: " + url
				
				# update the progress
				cur_file += 1
				p = round(cur_file * 100.0 / total_file, 1)
				print 'Progress: ' + str(p) + '% (' + str(cur_file) + '/' + str(total_file) + ')'
	
	print 'Done!'

createTilesPBF(0,2,False)