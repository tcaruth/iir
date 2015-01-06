# IIR

# test url
# http://ortho.gis.iastate.edu/client_pls.cgi?zoom=2&x0=663692&y0=4642601&layer=naip_2013_cir&action=pan&pwidth=500&pheight=500
import urllib2
import requests
import os

cwd = os.getcwd()
url = raw_input('Paste URL from any one page <No Quotes>: ')
filename = raw_input('Please type the desired filename: ')
client = raw_input('Please type a client name. Leave blank for same as filename: ')
if client == '':
	client = filename
# url = "http://ortho.gis.iastate.edu/client_pls.cgi?zoom=2&x0=663692&y0=4642601&layer=naip_2013_cir&action=pan&pwidth=500&pheight=500"
url = url.split('&')
print "Processing" # the user has no idea if anything is happening otherwise

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
x = filter(lambda x: 'x0' in x, url)
x = int(x[0].lstrip('x0='))
# pick out y0, strip it to just the value
y = filter(lambda y: 'y0' in y, url)
y = int(y[0].lstrip('y0='))
# pwidth
width = filter(lambda width: 'pwidth' in width, url)
width = int(width[0].lstrip('pwidth='))
# pheight
height = filter(lambda height: 'pheight' in height, url)
height = int(height[0].lstrip('pheight='))
# zoom
zoomurl = url[0].split('?')
zoom = filter(lambda zoom: 'zoom' in zoom, zoomurl)
zoom = int(zoom[0].lstrip('zoom='))
#calc bbox
bbox1 = str(x - width)
bbox2 = str(y - height)
bbox3 = str(x + width)
bbox4 = str(y + height)
bbox = bbox1 + ',' + bbox2 + ',' + bbox3 + ',' + bbox4

#layers
layerstenplusurl = ["http://ags.gis.iastate.edu/arcgisserver/services/Ortho/","/ImageServer/WMSServer?wmtver=1.0&request=map&layers=","&format=jpeg&srs=EPSG:26915&styles="]
layerstenpluscodes = {
'S2013IR':"naip_2013_cir",
'S2013C':"naip_2013_nc",
'S2011C':"naip_2011_nc",
'S2011IR':"naip_2011_cir",
'S2010C':"naip_2010_nc",
'S2010IR':"naip_2010_cir",
'SP2010C':"ortho_2010_nc",
'SP2010IR':"naip_2010_cir"
}
layerstenminusurl = ["http://ortho.gis.iastate.edu/server.cgi?wmtver=1.0&request=map&layers=","&format=jpeg&srs=EPSG:26915&styles="]
layerstenminuscodes = {'S2009C':"naip_2009",'S2008C':"naip_2008",'S2007C':"naip_2007",'S2006C':"naip_2006",'S2005C':"naip_2005",'S2004C':"naip_2004",'SP2002IR':"cir",'ELEV':"lidar_hs",'1990s':"doqqs"}

# # layers
# layerstenplusurl = ["http://ags.gis.iastate.edu/arcgisserver/services/Ortho/","/ImageServer/WMSServer"]
# layerstenpluscodes = {'S2013IR':"naip_2013_cir",'S2013C':"naip_2013_nc",'S2011C':"naip_2011_nc",'S2011IR':"naip_2011_cir",'S2010C':"naip_2010_nc",'S2010IR':"naip_2010_cir",'SP2010C':"ortho_2010_nc",'SP2010IR':"naip_2010_cir"}
layerstenplusdata = {'wmtver':'1.0','request':'map','format':'jpeg','srs':'EPSG:26915','styles':''} 
# need to add layers still, not sure how that works. maybe a for loop that goes over the list, with layerstenplusdata['layer'] = layerstenpluscodes[i]
# note that the layer is also in the url, so the request has to be going through the dictionary anyways


# layerstenminusurl = ["http://ortho.gis.iastate.edu/server.cgi"]
layerstenminusdata = {'wmtver':'1.0','request':'map','format':'jpeg','srs':'EPSG:26915','styles':''}
# layerstenminuscodes = {'S2009C':"naip_2009",'S2008C':"naip_2008",'S2007C':"naip_2007",'S2006C':"naip_2006",'S2005C':"naip_2005",'S2004C':"naip_2004",'SP2002IR':"cir",'ELEV':"lidar_hs",'1990s':"doqqs"}

# #download layers. should look at using requests instead of urllib2.
# for i in layerstenminuscodes:
    # jpgreq = urllib2.Request(layerstenminusurl[0] + str(layerstenminuscodes.get(i)) + layerstenminusurl[1] + "&bbox=" + str(bbox) + "&width=" + str(width) + "&height=" + str(height))
    # jgwfile = open(i + '.jgw', 'w')
    # jgwfile.write(str(zoom) + "\n0.0\n0.0\n-" + str(zoom) + "\n" + str(x) + "\n" + str(y))
    # jgwfile.close()
    # f = open(i + ".jpg","wb",0)
    # #jpgresponse = urllib2.urlopen(jpgreq)
    # f.write(urllib2.urlopen(jpgreq).read())
    # f.close()


for i in layerstenminuscodes:
    jpgreq = urllib2.Request(layerstenminusurl[0] + str(layerstenminuscodes.get(i)) + layerstenminusurl[1] + "&bbox=" + str(bbox) + "&width=" + str(width) + "&height=" + str(height))
    cleartextjpgreq = layerstenminusurl[0] + str(layerstenminuscodes.get(i)) + layerstenminusurl[1] + "&bbox=" + str(bbox) + "&width=" + str(width) + "&height=" + str(height)
    print cleartextjpgreq
    jgwfile = open(i + '.jgw', 'w')
    jgwfile.write(str(zoom) + "\n0.0\n0.0\n-" + str(zoom) + "\n" + str(x) + "\n" + str(y))
    jgwfile.close()
    f = open(i + ".jpg","wb",0)
    #jpgresponse = urllib2.urlopen(jpgreq)
    f.write(urllib2.urlopen(jpgreq).read())
    f.close()
for i in layerstenpluscodes:
    jpgreq = urllib2.Request(layerstenplusurl[0] + str(layerstenpluscodes.get(i)) + layerstenplusurl[1] + str(layerstenpluscodes.get(i)) + layerstenplusurl[2] + "&bbox=" + str(bbox) + "&width=" + str(width) + "&height=" + str(height))
    cleartextjpgreq = layerstenplusurl[0] + str(layerstenpluscodes.get(i)) + layerstenplusurl[1] + str(layerstenpluscodes.get(i)) + layerstenplusurl[2] + "&bbox=" + str(bbox) + "&width=" + str(width) + "&height=" + str(height)
    print cleartextjpgreq
    jgwfile = open(i + '.jgw', 'w')
    jgwfile.write(str(zoom) + "\n0.0\n0.0\n-" + str(zoom) + "\n" + str(x) + "\n" + str(y))
    jgwfile.close()
    f = open(i + ".jpg", "wb", 0)
    #jpgresponse = urllib2.urlopen(jpgreq)
    f.write(urllib2.urlopen(jpgreq).read())
    f.close()


print "Finished!"
os.chdir(cwd)
