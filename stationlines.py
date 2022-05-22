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
"""

import inspect
import os
import sys

from qgis.core import QgsApplication

# Import StationLinesProvider
from .stationlines_provider import StationLinesProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class StationLinesPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = None

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = StationLinesProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        # Processing provider
        self.initProcessing()


    def unload(self):
        # Processing provider
        QgsApplication.processingRegistry().removeProvider(self.provider)
