# IIR

# this whole thing is really messy, but i can't see any repeating patterns where it would make sense ( or shorter ) to use functions
import requests
import os
import re

def calcvar(url):
	# pick out x0, strip it to just the value
	x = filter(lambda x: "x0" in x, url)
	x = int(x[0].lstrip("x0="))
	# pick out y0, strip it to just the value
	y = filter(lambda y: "y0" in y, url)
	y = int(y[0].lstrip("y0="))
	# pwidth
	width = filter(lambda width: "pwidth" in width, url)
	width = int(width[0].lstrip("pwidth="))
	# pheight
	height = filter(lambda height: "pheight" in height, url)
	height = int(height[0].lstrip("pheight="))
	# zoom
	zoomurl = url[0].split("?")
	zoom = filter(lambda zoom: "zoom" in zoom, zoomurl)
	zoom = int(zoom[0].lstrip("zoom="))
	#calc BoundingBOX
	bbox1 = str(x - width)
	bbox2 = str(y - height)
	bbox3 = str(x + width)
	bbox4 = str(y + height)
	bbox = bbox1 + "," + bbox2 + "," + bbox3 + "," + bbox4
	urlparams = [url, x, y, width, height, zoom, bbox]
	return urlparams

rawurl = self.dlg.urlEdit.currentText()
url = re.sub("[\" \']{,}","",rawurl)
url = url.split("&")
rawfilename = self.dlg.clientEdit.currentText()
filename = re.sub("(\.\w{3}){,}","",rawfilename)

urlparams = calcvar(url)
# urlparams = [[urlsplit], x, y, width, height, zoom, bbox]

layerstenpluscodes = {
"S2014C":"naip_2014_nc",
"S2013IR":"naip_2013_cir",
"S2013C":"naip_2013_nc",
"S2011IR":"naip_2011_cir",
"S2011C":"naip_2011_nc",
"S2010IR":"naip_2010_cir",
"S2010C":"naip_2010_nc",
"SP2010IR":"naip_2010_cir",
"SP2010C":"ortho_2010_nc"
}
layerstenminuscodes = {
"S2009C":"naip_2009",
"S2008C":"naip_2008",
"S2007C":"naip_2007",
"S2006C":"naip_2006",
"S2005C":"naip_2005",
"S2004C":"naip_2004",
"SP2002IR":"cir",
"ELEV":"lidar_hs",
"1990s":"doqqs"
}
layersdata = {"wmtver":"1.0","request":"map","format":"jpeg","srs":"EPSG:26915","styles":""}
layersdata['bbox'] = urlparams[6] # bbox
layersdata['width'] = urlparams[3] # width
layersdata['height'] = urlparams[4] # height
layerstenminusurl = "http://ortho.gis.iastate.edu/server.cgi?"
layerstenplusurl = ["http://ags.gis.iastate.edu/arcgisserver/services/Ortho/","/ImageServer/WMSServer?"]

def serverError(status,reason,i,url):
	 print "Server returned error " + str(jpg.status_code) + " with reason \"" + str(jpg.reason) + "\" for file \"" + i + "\"." 
	 print "URL: " + jpg.url
	 print ""
	
for i in layerstenminuscodes:
	jgw = open(str(self.browseEdit.currentText()) + i + ".jgw", "w")
	jgw.write(str(zoom) + "\n0.0\n0.0\n-" + str(zoom) + "\n" + str(x) + "\n" + str(y))
	jgw.close()
	curval = layerstenminuscodes.get(i)
	layersdata['layers'] = curval
	jpg = requests.get(layerstenminusurl, params=layersdata)
	if int(jpg.status_code) == 200:
		f = open(str(self.browseEdit.currentText()) + i + ".jpg","wb",0)
		f.write(jpg.content)
		f.close()
	#else: serverError(jpg.status_code,jpg.reason,i,jpg.url)
for i in layerstenpluscodes:
	jgw = open(str(self.browseEdit.currentText()) + i + ".jgw", "w")
	jgw.write(str(zoom) + "\n0.0\n0.0\n-" + str(zoom) + "\n" + str(x) + "\n" + str(y))
	jgw.close()
	if i == "S2014C": #workaround until we see if 2015 has the same server
		jpg = requests.get("http://gis.apfo.usda.gov/arcgis/services/NAIP/Iowa_2014_1m_NC/ImageServer/WMSServer?layers=" + str(layerstenpluscodes.get(i)), params=layersdata)
		print "Using workaround for " + str(jpg.url)
		if int(jpg.status_code) == 200:
			f = open(str(self.browseEdit.currentText()) + i + ".jpg","wb",0)
			f.write(jpg.content)
			f.close()
		#else: serverError(jpg.status_code,jpg.reason,i,jpg.url)
	else:
		curval = layerstenminuscodes.get(i)
		layersdata['layers'] = curval
		jpg = requests.get(layerstenplusurl[0] + str(layerstenpluscodes.get(i)) + layerstenplusurl[1], params=layersdata)
		if int(jpg.status_code) == 200:
			f = open(str(self.browseEdit.currentText()) + i + ".jpg","wb",0)
			f.write(jpg.content)
			f.close()
		#else: serverError(jpg.status_code,jpg.reason,i,jpg.url)