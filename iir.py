# IIR

# this whole thing is really messy, but i can't see any repeating patterns where it would make sense ( or shorter ) to use functions
import requests
import os
import re

cwd = os.getcwd()
rawurl = raw_input("Paste URL from any one page: ")
url = re.sub("[\" \']{,}","",rawurl)
if rawurl == "":
	url = "http://ortho.gis.iastate.edu/client.cgi?zoom=1&x0=480176&y0=4707155&layer=naip_2014_nc&action=pan&pwidth=500&pheight=500"
rawfilename = raw_input("Please type the desired filename: ")
filename = re.sub("(\.\w{3}){,}","",rawfilename)
if filename == "":
	filename = "test"
client = raw_input("Please type a client name. Leave blank for same as filename: ")
if client == "":
	client = filename
url = url.split("&")

#setup client and file folder
try:
    os.mkdir(client)
    os.chdir(client)
except:
    os.chdir(client)
try:
    os.mkdir(filename)
    os.chdir(filename)
except:
    os.chdir(filename)
    print "This filename is already in use. Overwriting with new downloads."

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

#layers
newavailablelayers = {
 # for use below, 
 # S = summer
 # SP = spring
 # C = natural color
 # IR = color infrared
 # so we have Summer2014naturalColor
 # S2014C
 # S2013IR
 # S2013C 
 # S2011C 
 # S2011IR 
 # S2010C 
 # S2010IR 
 # SP2010C
 # SP2010IR
 }
oldavailablelayers = {
 # SP2009C 
 # SP2009IR 
 # SP2007C 
 # SP2007IR 
 # S2009C 
 # S2008C 
 # S2007C 
 # S2006C 
 # S2005C 
 # S2004C 
 # S2002CIR 
 # S2002IR
 # 2002 Orthophotos - IGIC (gray-scale) 
 # 1990s Orthophotos - USGS 
 # 1980s Aerial Photos - USDA 
 # 1970s Aerial Photos - USDA 
 # 1960s Aerial Photos - USDA 
 # 1950s Aerial Photos - USDA 
 # 1930s Aerial Photos - USDA Full extent 
 # 24K Topographic Maps - USGS 
 # 100K Topographic Maps - USGS 
 # 250K Topographic Maps - USGS 
 # Hillshade from 1-meter LiDAR Full extent 
 # Hillshade from 10-meter DEM - USGS 
 # Hillshade from 30-meter DEM - USGS 
 # Color Hillshade 30m DEM Legend 
 # General Land Office Survey 1836-1859 
 # Andreas Atlas 1875 
 # 1800s Historic Vegetation - ISU Legend Info 
 # 2002 Landcover - IGSB Legend 
 # 1992 Landcover - Iowa Gap Legend Info 
 # 1992 Landcover - USGS NLCD Legend
 }
 
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

# at this point, both wms servers use the same parameters. we'll split them later if we have to
layersdata = {"wmtver":"1.0","request":"map","format":"jpeg","srs":"EPSG:26915","styles":""}
layersdata['bbox'] = bbox
layersdata['width'] = width
layersdata['height'] = height

layerstenminusurl = "http://ortho.gis.iastate.edu/server.cgi?"
layerstenplusurl = ["http://ags.gis.iastate.edu/arcgisserver/services/Ortho/","/ImageServer/WMSServer?"]
# sigh.. 2014 uses a new server. i need to find a way to interact directly with wms, rather than just image grabbing. for now, we'll do a little workaround with the tenpluscodes
# http://gis.apfo.usda.gov/arcgis/services/NAIP/Iowa_2014_1m_NC/ImageServer/WMSServer?wmtver=1.0&request=map&bbox=455582,4667655,505582,4717655&width=500&height=500&layers=naip_2014_nc&format=jpeg&srs=EPSG:26915&styles=

progy,progx = 0,0
def progress(progy):
	progy += 1
	progress = str(progy)
	print progress + " / " + str(len(layerstenminuscodes) + len(layerstenpluscodes)) + " - " + i
	return progy

# download layers
for i in layerstenminuscodes:
	progx = progress(progx) # hacky sort of progress bar
	jgw = open(i + ".jgw", "w")
	jgw.write(str(zoom) + "\n0.0\n0.0\n-" + str(zoom) + "\n" + str(x) + "\n" + str(y))
	jgw.close()
	curval = layerstenminuscodes.get(i)
	layersdata['layers'] = curval
	jpg = requests.get(layerstenminusurl, params=layersdata)
	if int(jpg.status_code) == 200:
		f = open(i + ".jpg","wb",0)
		f.write(jpg.content)
		f.close()
	else:
		print "Server returned error " + str(jpg.status_code) + " with reason \"" + str(jpg.reason) + "\" for file \"" + i + "\"."
		print "URL: " + jpg.url
		print ""
for i in layerstenpluscodes:
	progx = progress(progx)
	jgw = open(i + ".jgw", "w")
	jgw.write(str(zoom) + "\n0.0\n0.0\n-" + str(zoom) + "\n" + str(x) + "\n" + str(y))
    # holds the following
    # 2 (zoom)
    # 0.0 (x skew)
    # 0.0 (y skew)
    # -2 (neg zoom)
    # 479677 (x)
    # 4707654 (y)
	jgw.close()
	if i == "S2014C": #workaround until we see if 2015 has the same server
		jpg = requests.get("http://gis.apfo.usda.gov/arcgis/services/NAIP/Iowa_2014_1m_NC/ImageServer/WMSServer?layers=" + str(layerstenpluscodes.get(i)), params=layersdata)
		print "Using workaround for " + str(jpg.url)
		if int(jpg.status_code) == 200:
			f = open(i + ".jpg","wb",0)
			f.write(jpg.content)
			f.close()
		else:
			print "Server returned error " + str(jpg.status_code) + " with reason \"" + str(jpg.reason) + "\" for file \"" + i + "\"." 
			print "URL: " + jpg.url
			print ""
	else:
		curval = layerstenminuscodes.get(i)
		layersdata['layers'] = curval
		jpg = requests.get(layerstenplusurl[0] + str(layerstenpluscodes.get(i)) + layerstenplusurl[1], params=layersdata)
		if int(jpg.status_code) == 200:
			f = open(i + ".jpg","wb",0)
			f.write(jpg.content)
			f.close()
		else:
			print "Server returned error " + str(jpg.status_code) + " with reason \"" + str(jpg.reason) + "\" for file \"" + i + "\"." 
			print "URL: " + jpg.url
			print ""

print "Finished!"
os.chdir(cwd)