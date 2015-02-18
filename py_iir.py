# credit to orignal pyIIR to Travis Caruth https://github.com/tcaruth/pyiir/blob/master/iir.py

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from py_iir_dialog import   iirDialog
import sys
import os
import os.path
from os import listdir
from os.path import isfile, join
import subprocess
import requests
import re


class iir:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'iir_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = iirDialog()
        self.dlg.connect(self.dlg.toolBrowse,SIGNAL("clicked()"), self.select_file)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&IIR')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'iir')
        self.toolbar.setObjectName(u'iir')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('iir', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):


        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/iir/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'IIR'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&IIR'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # v15.17.2.1713
            home = os.path.expanduser("~")
            error = open(home + '/' + 'iirerror.log','wb')
            def calcvar(url):
                error.write('143 calculating variables\n')
                x = filter(lambda x: 'x0' in x, url)
                x = float(x[0].lstrip('x0='))
                y = filter(lambda y: 'y0' in y, url)
                y = float(y[0].lstrip('y0='))
                width = filter(lambda width: 'pwidth' in width, url)
                width = int(width[0].lstrip('pwidth='))
                height = filter(lambda height: 'pheight' in height, url)
                height = int(height[0].lstrip('pheight='))
                zoomurl = url[0].split('?')
                zoom = filter(lambda zoom: 'zoom' in zoom, zoomurl)
                zoom = int(zoom[0].lstrip('zoom='))
                bbox1 = str(x - width)
                bbox2 = str(y - height)
                bbox3 = str(x + width)
                bbox4 = str(y + height)
                bbox = bbox1 + ',' + bbox2 + ',' + bbox3 + ',' + bbox4
                x = int(x - width)
                y = int(y - height)
                urlparam = [ url, x, y, width, height, zoom, bbox ]
                #                 0   1  2   3        4         5        6
                error.write('161 done\n')
                error.write(str(urlparam[1]))
                error.write('\n')
                error.write(str(urlparam[2]))
                error.write('\n')
                error.write(str(urlparam[3]))
                error.write('\n')
                error.write(str(urlparam[4]))
                error.write('\n')
                error.write(str(urlparam[5]))
                error.write('\n')
                error.write(str(urlparam[6]))
                error.write('\n')
                return urlparam
            def serverError( status, reason, i, url ): # where we're going, we dont need errors. if needed, add in a messagebox with the following stuff, or similar
                print 'Server returned error ' + str(jpg.status_code) + ' with reason "' + str(jpg.reason) + '" for file "' + i + '".'
                print 'URL: ' + jpg.url
                print ''
            def getjgwjpg(): # urlparam = [ url, x, y, width, height, zoom, bbox ]
                error.write('168 started getjgwjpg()\n')
                for i in layerstenminuscodes:
                    jgw = open(filename + i + '.jgw', 'w')
                    jgw.write(str(urlparam[5]) + "\n0.0\n0.0\n-" + str(urlparam[5]) + "\n" + str(urlparam[1]) + "\n" + str(urlparam[2]))
                    jgw.close()
                    curval = layerstenminuscodes.get(i)
                    layersdata['layers'] = curval
                    jpg = requests.get(layerstenminusurl, params=layersdata)
                    if int(jpg.status_code) == 200:
                        f = open(filename + i + '.jpg', 'wb', 0)
                        f.write(jpg.content)
                        f.close()
                    # else: serverError(jpg.status_code,jpg.reason,i,jpg.url)
                error.write('181 layerstenminuscodes complete\n')
                for i in layerstenpluscodes:
                    jgw = open(filename + i + '.jgw', 'w')
                    jgw.write(str(urlparam[5]) + "\n0.0\n0.0\n-" + str(urlparam[5]) + "\n" + str(urlparam[2]) + "\n" + str(urlparam[3]))
                    jgw.close()
                    if i == 'S2014C':  # workaround until we see if 2015 has the same server
                        jpg = requests.get('http://gis.apfo.usda.gov/arcgis/services/NAIP/Iowa_2014_1m_NC/ImageServer/WMSServer?layers='
                                        + str(layerstenpluscodes.get(i)), params=layersdata)
                        print 'Using workaround for ' + str(jpg.url)
                        if int(jpg.status_code) == 200:
                            f = open(filename + i + '.jpg', 'wb', 0)
                            f.write(jpg.content)
                            f.close()
                        # else: serverError(jpg.status_code,jpg.reason,i,jpg.url)
                    else:
                        curval = layerstenminuscodes.get(i)
                        layersdata['layers'] = curval
                        jpg = requests.get(layerstenplusurl[0] + str(layerstenpluscodes.get(i)) + layerstenplusurl[1], params=layersdata)
                        if int(jpg.status_code) == 200:
                            f = open(filename + i + '.jpg', 'wb', 0)
                            f.write(jpg.content)
                            f.close()
                        # else: serverError(jpg.status_code,jpg.reason,i,jpg.url)
                error.write('204 layerstenpluscodes complete\n')

            error.write('206 pulling urlEdit text\n')
            rawurl = self.dlg.urlEdit.text()
            url = re.sub('[" \']{,}', '', rawurl)
            url = url.split('&')
            rawfilename = self.dlg.clientEdit.text()
            filename = re.sub("(\.\w{3}){,}", '', rawfilename)
            filename = str( self.dlg.browseEdit.text() + "/" + filename + "_" )
            error.write('212 urlEdit: ' + rawurl + '\n')
            error.write('213 filename: ' + filename + '\n')

            # urlparam = [[urlsplit], x, y, width, height, zoom, bbox]
            urlparam = calcvar(url)


            layerstenpluscodes = {
                'S2014C': 'naip_2014_nc',
                'S2013IR': 'naip_2013_cir',
                'S2013C': 'naip_2013_nc',
                'S2011IR': 'naip_2011_cir',
                'S2011C': 'naip_2011_nc',
                'S2010IR': 'naip_2010_cir',
                'S2010C': 'naip_2010_nc',
                'SP2010IR': 'naip_2010_cir',
                'SP2010C': 'ortho_2010_nc',
                }
            layerstenminuscodes = {
                'S2009C': 'naip_2009',
                'S2008C': 'naip_2008',
                'S2007C': 'naip_2007',
                'S2006C': 'naip_2006',
                'S2005C': 'naip_2005',
                'S2004C': 'naip_2004',
                'SP2002IR': 'cir',
                'ELEV': 'lidar_hs',
                '1990s': 'doqqs',
                }
            layersdata = {
                'wmtver': '1.0',
                'request': 'map',
                'format': 'jpeg',
                'srs': 'EPSG:26915',
                'styles': '',
                }
            layersdata['bbox'] = urlparam[6]  # bbox
            layersdata['width'] = urlparam[3]  # width
            layersdata['height'] = urlparam[4]  # height
            layerstenminusurl = 'http://ortho.gis.iastate.edu/server.cgi?'
            layerstenplusurl = [ 'http://ags.gis.iastate.edu/arcgisserver/services/Ortho/', '/ImageServer/WMSServer?' ]

            # do work
            error.write('255 attempting to call getjgwjpg()\n')
            getjgwjpg()
            error.close()

    def select_file(self):
        dirname = QFileDialog.getExistingDirectory(None, u"Select directory",options=QFileDialog.DontUseNativeDialog,)
        self.dlg.browseEdit.setText(dirname)