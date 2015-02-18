# -*- coding: utf-8 -*-
"""
/***************************************************************************
 iir
                                 A QGIS plugin
 py plugin for iir
                             -------------------
        begin                : 2015-01-14
        copyright            : (C) 2015 by Jus Beall, Travis Caruth
        email                : beall008@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load iir class from file iir.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .py_iir import iir
    return iir(iface)
