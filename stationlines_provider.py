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

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = "$Format:%H$"

import os

from processing.core.ProcessingConfig import ProcessingConfig, Setting
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .stationlines_algo import StationLinesAlg


class StationLinesProvider(QgsProcessingProvider):
    def __init__(self):
        QgsProcessingProvider.__init__(self)
        self.algs = []

    def id(self):
        return "stationlines"

    def name(self):
        return "Station Lines"

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "icon.png"))

    def longName(self):
        return self.name()

    def loadAlgorithms(self):
        self.addAlgorithm(StationLinesAlg())
