# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StationLines
                                 A QGIS plugin
 Create lines along a polyline with specifications (length, side, angle)
                             -------------------
        begin                : 2014-04-11
        copyright            : (C) 2014 by Loïc BARTOLETTI
        email                : l.bartoletti@free.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load StationLines class from file StationLines
    from .stationlines import StationLinesPlugin
    return StationLinesPlugin(iface)
