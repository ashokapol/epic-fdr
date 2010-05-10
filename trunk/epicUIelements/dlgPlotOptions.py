#!/usr/bin/env python

import numpy as Npy
from PyQt4 import QtGui, QtCore
from supportClasses.clsPlotParameters import clsPlotParameters

from epicUIelements.ui_dlgPlotOptions import Ui_dlgPlotOptions
#[ '-' | '--' | '-.' | ':' | 'steps' | 'None' | ' ' | '' ]
lineStyles = dict(solid_line = '-',\
                  dashed_line = '--', \
                  dash_dot_line = '-.',\
                  dotted_line = ':',\
                  points = ':',\
                  steps = 'steps',\
                  none = 'None')

"""
ACCEPTS: [ '+' | ',' | '.' | '1' | '2' | '3' | '4'
                 | '<' | '>' | 'D' | 'H' | '^' | '_' | 'd'
                 | 'h' | 'o' | 'p' | 's' | 'v' | 'x' | '|'
                 | TICKUP | TICKDOWN | TICKLEFT | TICKRIGHT
                 | 'None' | ' ' | '' ]
"""
markerSytles = dict(circles = 'o',\
                    triangle_up = '^',\
                    triangle_down  = 'v',\
                    triangle_left  = '<',\
                    triangle_right  = '>',\
                    square  = 's',\
                    plus  = '+',\
                    cross  = 'x',\
                    diamond  = 'D',\
                    thin_diamond  = 'd',\
                    tripod_down  = '1',\
                    tripod_up  = '2',\
                    tripod_left  = '3',\
                    tripod_right  = '4',\
                    hexagon  = 'h',\
                    rotated_hexagon  = 'H',\
                    pentagon  = 'p',\
                    vertical_line  = '|',\
                    horizontal_line  = '_')

lineWidths = Npy.arange(.5,5.5,.5)
markerSizes = range(1,11)

class PlotOptions(QtGui.QDialog):
    def __init__(self, ppara):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_dlgPlotOptions()
        self.ui.setupUi(self)
        icon = QtGui.QIcon(":/epic.png")
        self.setWindowIcon(icon)

        #self.connect(self.btn_SelectColor, SIGNAL("clicked()"), self.getColor)
        self.connect(self.ui.mtoolBtnColor, QtCore.SIGNAL("colorChanged(QColor)"), self.setMColor)
        self.mcolor = ""
        self._cid = ppara.callbackID
        self._mblPickPts = ppara.mblPickPts
        self.populate_dialog(ppara)


    def setMColor(self, QColor):
        self.mcolor = str(QColor.name())#need to set value to str as it is QString

    def populate_dialog(self, plotParam):
        self.ui.mlineEditTitle.setText(plotParam.mstrTitle)

        self.ui.mlineEditXmin.setText(str(plotParam.mflXmin))
        self.ui.mlineEditXmax.setText(str(plotParam.mflXmax))
        self.ui.mlineEditXlabel.setText(plotParam.mstrXlabel)

        self.ui.mlineEditYmin.setText(str(plotParam.mflYmin))
        self.ui.mlineEditYmax.setText(str(plotParam.mflYmax))
        self.ui.mlineEditYlabel.setText(plotParam.mstrYlabel)

        self.ui.mchkBoxGrid.setChecked(plotParam.mblShowGrid)
        self.ui.mchkBoxLogX.setChecked(plotParam.mstrXscale == 'log')
        self.ui.mchkBoxLogY.setChecked(plotParam.mstrYscale == 'log')

        plotHandle = plotParam.plotHandle

        # Fill and set Combo boxes
        markerStyleList = [x for x in markerSytles]
        lineStyleList = [x for x in lineStyles]
        lineWidthList = [str(x) for x in lineWidths]
        markerSizeList = [str(x) for x in markerSizes]

        try:
            currMarkerIdx = markerStyleList.index(self.GetDictKey(markerSytles, plotHandle.get_marker()))
        except AttributeError:
            currMarkerIdx = 0
        try:
            currLineStyIdx = lineStyleList.index(self.GetDictKey(lineStyles, plotHandle.get_linestyle()))
        except AttributeError:
            currLineStyIdx = 0

        try:
            self.mcolor = plotHandle.get_markerfacecolor()
        except AttributeError:
            self.mcolor = '#FF0000'
        if plotParam.histColor != "":
            self.mcolor = plotParam.histColor

        try:
            currLineWIdx = lineWidthList.index(str(plotHandle.get_linewidth()))
        except ValueError:
            lineWidthList.append(str(plotHandle.get_linewidth()))
            currLineWIdx = lineWidthList.index(str(plotHandle.get_linewidth()))
        except AttributeError:
            currLineWIdx = 0

        try:
            currMarkerSzIdx = markerSizeList.index(str(plotHandle.get_markersize()))
        except ValueError:
            markerSizeList.append(str(plotHandle.get_markersize()))
            currMarkerSzIdx = markerSizeList.index(str(plotHandle.get_markersize()))
        except AttributeError:
            currMarkerSzIdx = 0

        QtGui.QComboBox.addItems(self.ui.mcmbBMarkerStyle, markerStyleList)
        QtGui.QComboBox.setCurrentIndex(self.ui.mcmbBMarkerStyle, currMarkerIdx)

        QtGui.QComboBox.addItems(self.ui.mcmbBLineStyle, lineStyleList)
        QtGui.QComboBox.setCurrentIndex(self.ui.mcmbBLineStyle, currLineStyIdx)

        QtGui.QComboBox.addItems(self.ui.mcmbBLineW, lineWidthList)
        QtGui.QComboBox.setCurrentIndex(self.ui.mcmbBLineW, currLineWIdx)

        QtGui.QComboBox.addItems(self.ui.mcmbBMarkerSize, markerSizeList)
        QtGui.QComboBox.setCurrentIndex(self.ui.mcmbBMarkerSize, currMarkerSzIdx)

        self.ui.mtoolBtnColor.setColor(QtGui.QColor(self.mcolor))

        # end combo box filling

    def GetDictKey(self, dictionary, val):
        for key, value in dictionary.items():
            if value == val:
                return key

    def GetPlotParamters(self):
        param = clsPlotParameters(None, self.ui.mchkBoxGrid.isChecked(), \
                                  [float(self.ui.mlineEditXmin.text()), float(self.ui.mlineEditXmax.text())],\
                                  [float(self.ui.mlineEditYmin.text()), float(self.ui.mlineEditYmax.text())],\
                                  'log' if self.ui.mchkBoxLogX.isChecked() else 'linear',\
                                  'log' if self.ui.mchkBoxLogY.isChecked() else 'linear',\
                                  self.ui.mlineEditTitle.text(), self.ui.mlineEditXlabel.text(),\
                                  self.ui.mlineEditYlabel.text(),\
                                  "", None, None)
        param.mstrMarkerStyle = markerSytles[str(self.ui.mcmbBMarkerStyle.currentText())]
        #param.mstrColor = markerColors[str(self.ui.mcmbBCol.currentText())]
        param.mstrColor = self.mcolor
        param.mstrLineStyle = lineStyles[str(self.ui.mcmbBLineStyle.currentText())]
        param.mflLineWidth = float(self.ui.mcmbBLineW.currentText())
        param.mflMarkerSize = float(self.ui.mcmbBMarkerSize.currentText())
        param.callbackID = self._cid
        param.mblPickPts = self._mblPickPts

        return param

#class clsPlotParameters:
#    def __init__(self, plothandle, mblShowGrid, mflXlim, \
#                 mflYlim, xscale, yscale, title, xlabel, ylabel,\
#                 callbackID, mblPickPoints):
#
#        self.plotHandle = plothandle if plothandle != None else None
#
#        self.mstrMarkerStyle = plothandle.get_marker() if plothandle != None else None
#        self.mstrColor = plothandle.get_markerfacecolor() if plothandle != None else None
#        self.mstrLineStyle = plothandle.get_linestyle() if plothandle != None else None
#        self.mflLineWidth = plothandle.get_linewidth() if plothandle != None else None
#        self.mflMarkerSize = plothandle.get_markersize() if plothandle != None else None
#        self.mblShowGrid = mblShowGrid
#        self.mflXmin = mflXlim[0]
#        self.mflXmax = mflXlim[1]
#        self.mflYmin = mflYlim[0]
#        self.mflYmax = mflYlim[1]
#        self.mstrXscale = xscale
#        self.mstrYscale = yscale
#        self.mstrTitle = title
#        self.mstrXlabel = xlabel
#        self.mstrYlabel = ylabel
#        self.callbackID = callbackID
#        self.mblPickPts = mblPickPoints




