#!/usr/bin/env python
class clsPlotParameters:
    def __init__(self, plothandle, mblShowGrid, mflXlim, \
                 mflYlim, xscale, yscale, title, xlabel, ylabel, histColor, \
                 callbackID, mblPickPoints):

        self.plotHandle = plothandle if plothandle != None else None

        self.mstrMarkerStyle = plothandle.get_marker() if plothandle != None else None
        self.mstrColor = plothandle.get_markerfacecolor() if plothandle != None else None
        self.mstrLineStyle = plothandle.get_linestyle() if plothandle != None else None
        self.mflLineWidth = plothandle.get_linewidth() if plothandle != None else None
        self.mflMarkerSize = plothandle.get_markersize() if plothandle != None else None
        self.mblShowGrid = mblShowGrid
        self.mflXmin = mflXlim[0]
        self.mflXmax = mflXlim[1]
        self.mflYmin = mflYlim[0]
        self.mflYmax = mflYlim[1]
        self.mstrXscale = xscale
        self.mstrYscale = yscale
        self.mstrTitle = title
        self.mstrXlabel = xlabel
        self.mstrYlabel = ylabel
        self.histColor = histColor
        self.callbackID = callbackID
        self.mblPickPts = mblPickPoints