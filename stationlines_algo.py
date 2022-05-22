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

import math

from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterDistance,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QVariant

class StationLinesAlg(QgsProcessingAlgorithm):
    
    INPUT = "INPUT"
    DISTANCE = "DISTANCE"
    LENGTH = "LENGTH"
    ANGLE = "ANGLE"
    SIDE = "SIDE"
    IGNORE_EXISTING_VERTICES = "IGNORE_EXISTING_VERTICES"
    OUTPUT = "OUTPUT"
    
    SIDES = [["Left", "Right", "Both"], ["left", "right", "both"]]
    
    def initAlgorithm(self, config=None):  # pylint: disable=unused-argument
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Line(s)",
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterDistance(
                self.DISTANCE,
                "Fixed distance between transects",
                parentParameterName=self.INPUT,
                defaultValue=50.0,
                minValue=0.001,
            )
        )
        
        self.addParameter(
            QgsProcessingParameterDistance(
                self.LENGTH,
                "Length of the transect",
                parentParameterName=self.INPUT,
                defaultValue=5.0,
                minValue=0,
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ANGLE,
                "Angle in degrees from the original line at the vertices",
                QgsProcessingParameterNumber.Double,
                defaultValue=90,
                minValue=0,
                maxValue=360,
            )
        )
        
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SIDE,
                "Side to create the transects",
                options=self.SIDES[0],
                allowMultiple=False,
                defaultValue=2
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                "Transects",
                QgsProcessing.TypeVectorLine,
                createByDefault=True,
                defaultValue=None,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        linesLayer = self.parameterAsSource(parameters, self.INPUT, context)
        distance = self.parameterAsDouble(parameters, self.DISTANCE, context)
        length = self.parameterAsDouble(parameters, self.LENGTH, context)
        angle = self.parameterAsDouble(parameters, self.ANGLE, context)
        side = self.SIDES[1][self.parameterAsEnum(parameters, self.SIDE, context)]
        
        fields = linesLayer.fields()
        fields.append(QgsField("TR_FID", QVariant.Int, "", 20))
        fields.append(QgsField("TR_ID", QVariant.Int, "", 20))
        fields.append(QgsField("TR_SEGMENT", QVariant.Int, "", 20))
        fields.append(QgsField("TR_ANGLE", QVariant.Double, "", 5, 2))
        fields.append(QgsField("TR_LENGTH", QVariant.Double, "", 20, 6))
        fields.append(QgsField("TR_ORIENT", QVariant.String, "", 1))
        
        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields, QgsWkbTypes.LineString, linesLayer.sourceCrs()
        )
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))
        
        current = 0
        number = 0
        total = 100.0 / linesLayer.featureCount() if linesLayer.featureCount() else 0
        linesFeatures = linesLayer.getFeatures()
        for feat in linesFeatures:
            current += 1
            if feedback.isCanceled():
                break
            
            if not feat.hasGeometry():
                continue
            
            feedback.setProgress(int(current * total))
            
            featGeom = feat.geometry()
            if featGeom.isMultipart():
                multiLine = featGeom.asMultiPolyline()
            else:
                multiLine =[featGeom.asPolyline()]
            for linestring in multiLine:
                line = QgsGeometry().fromPolylineXY(linestring)
                d = 0
                
                while(d <= line.length()):
                    transectPoint = line.interpolate(d).asPoint()
                    transectAngle = angle + line.interpolateAngle(d) * 180 / math.pi
                    outFeat = QgsFeature()
                    
                    attrs = feat.attributes()
                    attrs.extend([current, number, number+1, angle, length, self.SIDES[1].index(side)])
                    outFeat.setAttributes(attrs)
                    outFeat.setGeometry(calcTransect(transectPoint, transectAngle, length, side))
                    if not sink.addFeature(outFeat, QgsFeatureSink.FastInsert):
                        raise QgsProcessingException(self.writeFeatureError(sink.get(), parameters, self.OUTPUT))
                    d += distance
                    number += 1
        
        return {self.OUTPUT: dest_id}

    def name(self):
        return "stationlines"

    def displayName(self):
        return "Transect at fixed distance"

    def createInstance(self):
        return StationLinesAlg()

def calcTransect(point, angle, length, side):
    line = []

    if side == "right" or side == "both":
        pLeft = point.project(length, angle)
        if side != "both":
            pRight = point

    if side == "left" or side == "both":
        pRight = point.project(-length, angle)
        if side != "both":
            pLeft = point

    line.append(pLeft)
    line.append(pRight)
    return QgsGeometry().fromPolylineXY(line)
