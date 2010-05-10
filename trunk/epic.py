#!/usr/bin/env python
"""
epic : Estimating Peptide Identification Confidence
Fits a mixture of Gaussians to MS/MS database search scores (ex: XCorr/DelCn2) using
Expectation Maximization algorithm. There are placeholders for X!Tandem which will be added in a
future release.

Steps:
------
1. Load a Sequest Synopsis/First hit file.
2. Select scores to be used as variables (upto 3 variables can be used)
3. Normalize the scores(Process -> Normalize)
    This will transform Xcorr and DelCn2 to normalized values.
4. Fit a Gaussian Mixture (Process -> Fit Gaussian Mixture)
    This will fit a mixture of two Gaussians and create two new columns in the data table
    denoting the p-values and q-values that a peptide is coming from the False distribution
    (lower, the better).
Plot menu: Plotting commands are available for visualizing the data and the fitting.

Source: https://prismsvn.pnl.gov/idl/projects/epic/Tags/version_SEQ_2D

------------------------------
Developed by: Ashoka Polpitiya
(ashoka@tgen.org)
"""
import sys
import os.path as OS
if sys.platform == 'win32':
    import winpaths as WinPaths
from PyQt4 import QtCore, QtGui, Qt
import numpy as Npy
import random
import csv
import time
import pickle
import math
import pylab as Py
from matplotlib.widgets import SpanSelector

from epicUIelements.epicTableModel import epicTableModel

from epicUIelements.ui_epic import Ui_mMainWindowEpic
from epicUIelements.dlgPlotOptions import PlotOptions
from epicUIelements.dlgEMparameters import clsdlgEMparameters
from epicUIelements.dlgNormalize import clsdlgNormalizePara
from epicUIelements.dlgHistogramPlotOptions import clsHistogramPlotOptions
from epicUIelements.dlgXYPlots import clsXYPlotOptions
from epicUIelements.dlgSelectVars import clsSelectVars
from epicUIelements.dlgSequestPara import clsSelectSequestVars
from epicUIelements.dlgXTandemPara import clsSelectXTandemVars
from epicUIelements.dlgSpectrumMillPara import clsSelectSpectrumMillVars

import supportClasses.clsDataVar as clsDataVar
import supportClasses.DataPreProcess as ProcData
from supportClasses.clsPlotParameters import clsPlotParameters
from supportClasses.clsSynFhtPara import extractColumnsFromSyn
import supportClasses.fileIOroutines as fileIO
import supportClasses.NormalizationRoutines as normalize
import supportClasses.ClassificationEM as EM
from supportClasses.clsEMInitPara import clsEMInitPara

import Threading.clsReadFiles as clsReadFiles
import Threading.clsThreadEM as clsThreadEM
import Threading.clsThreadEM1Dim as clsThreadEM1Dim
import Threading.clsGetqValues as clsThreadqVal

from extraNiceties.Splash import SplashScreen
from epicUIelements.dlgAbout import clsAboutEpic

import qrc_epicResources

open_file_filters = 'Synopsis Files (*_syn.txt);;First Hit Files (*_fht.txt);;X!Tandem Files (*_xt.txt);;' +\
                'Spectrum Mill Files (*.ssv);;Text TSV (*.txt);;CSV (*.csv);;All Files (*.*)'
save_file_filters = 'Text TSV (*.txt);;CSV (*.csv);;All Files (*.*)'
fig_file_filters = 'PNG (*.png);;PDF (*.pdf);;PS (*.ps);;EPS (*.eps);;SVG (*.svg)'

###########################################
# Main Class
###########################################
class Main_Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_mMainWindowEpic()
        self.ui.setupUi(self)

        self.mstrMessages = []
        self.lstMessageModel = QtGui.QStringListModel()

        self.Data, self.DataHeader = [], []

        if sys.platform == 'win32':
            self.MyDocs = WinPaths.get_my_documents()
        else:
            self.MyDocs = '.'
        self.marrFiles = []

        self.LayoutStatusBar()
        self.ToggleProgressBar(False)
        self.AddMessage2Tab('epic started.')

        self.Init()
        self.InitVars()
        self.mblDataLoaded = False

        self.statusBar().showMessage("")

        # tracking persistence
        self.mdictAppSettings = {}
        self.mdictPlotParameters = {}

        # Save/retrieve application settings
        self.settingsFile = QtGui.QApplication.applicationDirPath() + '/epic.pkl'
        if OS.isfile(self.settingsFile):
            f1 = file(self.settingsFile, 'rb')
            self.mdictAppSettings = pickle.load(f1)
            f1.close()
        else:
            self.mdictAppSettings = dict(fopen='.', fsynopen='.', fsave='.')


    def InitVars(self):
        # Variables related to files and raw data
        self.VarHeader = []
        self.mclsXvar = clsDataVar.clsDataVar("", "", [])
        self.mclsYvar = clsDataVar.clsDataVar("", "", [])
        self.mclsZvar = clsDataVar.clsDataVar("", "", [])
        self.mdictNormedData = {}
        self.mblX, self.mblY, self.mblZ, self.mblCS, self.mblTryptSt = False, False, False, False, False
        self.Peptides = []

        # Analysis and EM related variables
        self.mblVarsSelected = False
        self.mblNormalized = False
        self.Xem = []
        self.strArrEMvars = None
        self.probs = None
        self.qvalues = None
        self.rank = None
        self.mu = None
        self.sigma = None
        self.liklihood = None
        self.probabilities = None
        self.worker = None
        self.mblModelFitted = False
        self.dimEM = 2
        self.mblpqDone = False

        # Plotting related variables
        self.mblShowGrid = True
        self.matplotHandle = None
        self.selectHandle = None
        self.textHandle = None
        self.clsPlotParaCurr = {}
        self._connectionIDplot = []
        self.mblPickPoints = False
        self.histBars = []
        self.histColor = ""
        self.mblIsHZoom = False
        self.mstrPlotVars = "" # XY, YZ, XZ
        self.mstrPlotType = "" # Scatter, Histogram, Contour
        self.mstrPlotData = "Raw" # So far "Raw" and "Normed"
        self.ShowVars("Not selected", "Not selected", "Not selected")


    def Init(self):
        self.ui.mnuAutoScale = QtGui.QAction("Auto Scale", self)
        self.ui.mnuAutoScale.setShortcut("Ctrl+Shift+A")
        self.ui.matplotlibWidget.addAction(self.ui.mnuAutoScale)
        self.ui.mnuPlotOptions = QtGui.QAction("Plot Options", self)
        self.ui.matplotlibWidget.addAction(self.ui.mnuPlotOptions)
        self.ui.mnuSelectPoints = QtGui.QAction("Select Points", self)
        self.ui.mnuSelectPoints.setCheckable(True)
        self.ui.mnuSelectPoints.setChecked(False)
        self.ui.matplotlibWidget.addAction(self.ui.mnuSelectPoints)
#        self.ui.mnuHZoom = QtGui.QAction("Horizontal Zoom", self)
#        self.ui.mnuHZoom.setShortcut("Ctrl+Shift+Z")
#        self.ui.mnuHZoom.setCheckable(True)
#        self.ui.mnuHZoom.setChecked(False)
#        self.ui.matplotlibWidget.addAction(self.ui.mnuHZoom)
        self.ui.matplotlibWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ui.mtabWidget.setCurrentIndex(0)

        self.ui.mnuCtxtSaveMsgs = QtGui.QAction("Save Messages", self)
        self.ui.mlstViewMessages.addAction(self.ui.mnuCtxtSaveMsgs)
        self.ui.mlstViewMessages.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.span = SpanSelector(self.ui.matplotlibWidget.canvas.ax, self.onselect, 'horizontal',
                                 useblit=True, rectprops=dict(alpha=0.5, facecolor='#C6DEFF') )#There is a bug in mpl 0.91 'blue' is red and 'red' is blue
        self.span.visible = False

        # SIGNALS/SLOTS
        self.connect(self.ui.mnuOpenFile, QtCore.SIGNAL("triggered()"), self.OpenFiles)
        self.connect(self.ui.mnuSaveData, QtCore.SIGNAL("triggered()"), self.saveData)
        self.connect(self.ui.mnuSaveMessages, QtCore.SIGNAL("triggered()"), self.saveMessages)
        self.connect(self.ui.mnuCtxtSaveMsgs, QtCore.SIGNAL("triggered()"), self.saveMessages)

        self.connect(self.ui.mnuSelectVars, QtCore.SIGNAL("triggered()"), self.SelectVarsGeneric)
        self.connect(self.ui.mnuSelectVarsSEQUEST, QtCore.SIGNAL("triggered()"), self.SelectSequestVars)
        self.connect(self.ui.mnuSelectVarsXTandem, QtCore.SIGNAL("triggered()"), self.SelectXTandemVars)
        self.connect(self.ui.mnuSelectVarsSpectrumMill, QtCore.SIGNAL("triggered()"), self.SelectSpectrumMillVars)
        self.connect(self.ui.mnuNormalize, QtCore.SIGNAL("triggered()"), self.normalizeData)
        self.connect(self.ui.mnuFitMixed, QtCore.SIGNAL("triggered()"), self.fitMixModel)
        self.connect(self.ui.mnuCompute_q_vals, QtCore.SIGNAL("triggered()"), self.getpvalNoCov)
        self.connect(self.ui.mnupBayes, QtCore.SIGNAL("triggered()"), self.getpvalBayes)
        self.connect(self.ui.mnupGVol, QtCore.SIGNAL("triggered()"), self.getpvalGVol)
        self.connect(self.ui.mnupGVolC, QtCore.SIGNAL("triggered()"), self.getpvalGVolC)

        self.connect(self.ui.mnuRawX_vs_Y, QtCore.SIGNAL("triggered()"), self.ScatterPlot)
        self.connect(self.ui.mnuRawX_vs_Z, QtCore.SIGNAL("triggered()"), self.ScatterPlot)
        self.connect(self.ui.mnuRawY_vs_Z, QtCore.SIGNAL("triggered()"), self.ScatterPlot)

        self.connect(self.ui.mbtnX_vs_Y, QtCore.SIGNAL("clicked()"), self.ScatterPlot)
        self.connect(self.ui.mbtnX_vs_Z, QtCore.SIGNAL("clicked()"), self.ScatterPlot)
        self.connect(self.ui.mbtnY_vs_Z, QtCore.SIGNAL("clicked()"), self.ScatterPlot)

        self.connect(self.ui.mnuNormX_vs_Y, QtCore.SIGNAL("triggered()"), self.ScatterPlot)
        self.connect(self.ui.mnuNormX_vs_Z, QtCore.SIGNAL("triggered()"), self.ScatterPlot)
        self.connect(self.ui.mnuNormY_vs_Z, QtCore.SIGNAL("triggered()"), self.ScatterPlot)

        self.connect(self.ui.mnuAutoScale, QtCore.SIGNAL("triggered()"), self.autoscalePlot)
        self.connect(self.ui.mnuPlotOptions, QtCore.SIGNAL("triggered()"), self.plottingOptions)
        self.connect(self.ui.mnuSelectPoints, QtCore.SIGNAL("triggered()"), self.SelectPoints)
        #self.connect(self.ui.mnuHZoom, QtCore.SIGNAL("triggered()"), self.HorizontalZoomToggle)

        self.connect(self.ui.mnuRawHistX, QtCore.SIGNAL("triggered()"), self.PlotHistogram)
        self.connect(self.ui.mnuRawHistY, QtCore.SIGNAL("triggered()"), self.PlotHistogram)
        self.connect(self.ui.mnuRawHistZ, QtCore.SIGNAL("triggered()"), self.PlotHistogram)
        self.connect(self.ui.mnuNormHistX, QtCore.SIGNAL("triggered()"), self.PlotHistogram)
        self.connect(self.ui.mnuNormHistY, QtCore.SIGNAL("triggered()"), self.PlotHistogram)
        self.connect(self.ui.mnuNormHistZ, QtCore.SIGNAL("triggered()"), self.PlotHistogram)
        self.connect(self.ui.mbtnHistX, QtCore.SIGNAL("clicked()"), self.PlotHistogram)
        self.connect(self.ui.mbtnHistY, QtCore.SIGNAL("clicked()"), self.PlotHistogram)
        self.connect(self.ui.mbtnHistZ, QtCore.SIGNAL("clicked()"), self.PlotHistogram)

        self.connect(self.ui.mnuContourSurfOnly, QtCore.SIGNAL("triggered()"), self.PlotContours)
        self.connect(self.ui.mnuContourSurfPoints, QtCore.SIGNAL("triggered()"), self.PlotContours)
        self.connect(self.ui.mnuContourLinesOnly, QtCore.SIGNAL("triggered()"), self.PlotContours)
        self.connect(self.ui.mnuContourLinesPoints, QtCore.SIGNAL("triggered()"), self.PlotContours)
        self.connect(self.ui.mbtnContours, QtCore.SIGNAL("clicked()"), self.PlotContours)
        self.connect(self.ui.mnuFDRPerformance, QtCore.SIGNAL("triggered()"), self.ShowFDRPerformance)
        self.connect(self.ui.mbtnFDRregions, QtCore.SIGNAL("clicked()"), self.ShowFDRpoints)
        self.connect(self.ui.mnuFDRregions, QtCore.SIGNAL("triggered()"), self.ShowFDRpoints)
        self.connect(self.ui.mbtnSaveFigure, QtCore.SIGNAL("clicked()"), self.SaveFigure)
        self.ui.mnuPlot.addAction(self.ui.dockWidget.toggleViewAction())
        #self.connect(self.ui.mnuTogglePlotBtns, QtCore.SIGNAL("triggered()"), self.ui.dockWidget.toggleViewAction)
        #self.connect(self.ui.mnuFDRregions, QtCore.SIGNAL("triggered()"), self.PlotSurface)
        #self._connectionIDplot = self.ui.matplotlibWidget.canvas.mpl_connect('move_event', self.)
        self.connect(self.ui.mnuAbout, QtCore.SIGNAL("triggered()"), self.about_eFDR)



    def LayoutStatusBar(self):
        self.xQLabel = QtGui.QLabel("X : ")
        self.xQLabel.setMinimumSize(self.xQLabel.sizeHint())
        #self.statusLabel.setAlignment(QtGui.QLabel.AlignCenter)
        self.xQLabel.setText("X : ")
        self.ui.statusbar.addPermanentWidget(self.xQLabel)

        self.yQLabel = QtGui.QLabel("Y : ")
        self.yQLabel.setMinimumSize(self.yQLabel.sizeHint())
        #self.statusLabel.setAlignment(QtGui.QLabel.AlignCenter)
        self.yQLabel.setText("Y : ")
        self.ui.statusbar.addPermanentWidget(self.yQLabel)

        self.zQLabel = QtGui.QLabel("Z : ")
        self.zQLabel.setMinimumSize(self.zQLabel.sizeHint())
        #self.statusLabel.setAlignment(QtGui.QLabel.AlignCenter)
        self.zQLabel.setText("Z : ")
        self.ui.statusbar.addPermanentWidget(self.zQLabel)

        self.statusLabel = QtGui.QLabel("Ready")
        self.statusLabel.setMinimumSize(self.statusLabel.sizeHint())
        #self.statusLabel.setAlignment(QtGui.QLabel.AlignCenter)
        self.statusLabel.setText("Ready")
        self.ui.statusbar.addPermanentWidget(self.statusLabel)

        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setTextVisible(False)
        self.progressBar.setRange(0,100)
        self.progressBar.setValue(0)
        self.progressBar.setFixedHeight(15)
        self.progressBar.setFixedWidth(100)
        self.ui.statusbar.addWidget(self.progressBar)

    def SetStatusLabel(self, text):
        self.statusLabel.setText(text)

    def ShowVars(self, X, Y, Z):
        self.xQLabel.setText("X : " + X)
        self.yQLabel.setText("Y : " + Y)
        self.zQLabel.setText("Z : " + Z)

    def ShowStatusMessage(self, text, stime):
        self.statusBar().showMessage(text, stime)

    def SetProgressValue(self, val):
        self.progressBar.setValue(val)

    def ToggleProgressBar(self, toggle):
        self.progressBar.setVisible(toggle)

    def AddMessage2Tab(self, message):
        self.mstrMessages.append(message)
        self.lstMessageModel.setStringList(self.mstrMessages)
        self.ui.mlstViewMessages.setModel(self.lstMessageModel)

    def Splash(self):
        splash = SplashScreen()
        splash.showMessage(self.tr('Initializing...'))
        time.sleep(1)
#        splash.showMessage(self.tr('Test 1...'))
#        time.sleep(0.4)

        splash.close()

    def closeEvent(self, event):
        if self.okToExit():
            f1 = file(self.settingsFile, 'wb')
            pickle.dump(self.mdictAppSettings, f1, True)
            f1.close()
        else:
            event.ignore()

    def okToExit(self):
        reply = QtGui.QMessageBox.question(self, "Confirm Quit", "Exit epic now?",\
                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            return True
        else:
            return False

    def program_close(self):
        sys.exit()

    def UpdateDataView(self):
        # Updates the two tabs on Data table and scatter plot
        self.tablemodel = epicTableModel(self.Data, self.DataHeader, self)
        self.ui.mTableView.setModel(self.tablemodel)
        self.ui.mTableView.setSortingEnabled(True)
        self.SetStatusLabel("%d rows and %d columns" %(len(self.Data), len(self.Data[0])))
        self.AddMessage2Tab("%d rows and %d columns" %(len(self.Data), len(self.Data[0])))
        #self.ScatterPlot()

    def OpenFiles(self):
        try:
            rootFolder = self.mdictAppSettings['fopen']
        except (KeyError):
            rootFolder = self.MyDocs
        self.marrFiles = QtGui.QFileDialog.getOpenFileNames(self,"Open Data Files",\
                                   rootFolder,\
                                   open_file_filters)
        self.marrFiles = [str(self.marrFiles[i]) for i in range(0,len(self.marrFiles))]
        if self.marrFiles:
            self.InitVars()
            self.mblDataLoaded = False
            self.clear_plot()
            self.mdictAppSettings['fopen'] = OS.dirname(str(self.marrFiles[0]))
            if fileIO.filesCompatible(self, self.marrFiles):
                self.ToggleProgressBar(True)
                self.worker = None
                self.worker = clsReadFiles.clsThreadReadFiles()
                self.worker.Initialize(self.marrFiles)
                self.connect(self.worker, QtCore.SIGNAL("progress(int)"), self.UpdateFileReadProgress)
                self.connect(self.worker, QtCore.SIGNAL("finished(bool)"), self.FileReadDone)
                self.AddMessage2Tab('Reading Files : ')
                self.worker.start()
            else:
                QtGui.QMessageBox.warning(self, "epic - Error", "File error. If multiple files, they are not the same type")

    def UpdateFileReadProgress(self, progVal):
        self.SetStatusLabel("Reading Files : %d Files Done." % progVal)
        self.SetProgressValue((progVal*10)%100 + 10)
        self.AddMessage2Tab("  %d Files Done." % progVal)

    def FileReadDone(self, mblSuccess):
        self.ToggleProgressBar(False)
        self.DataHeader, self.Data = self.worker.GetResults()
        self.mblDataLoaded = mblSuccess
        self.worker.wait()
        if mblSuccess:
            self.UpdateDataView()
            for i in xrange(len(self.marrFiles)):
                self.AddMessage2Tab('File : ' + self.marrFiles[i] + ' loaded.')
        else:
            QtGui.QMessageBox.warning(self, "epic - Error", "Unknown file error.")

    def saveData(self):
        if len(self.Data) > 0:
            self.savefilename = QtGui.QFileDialog.getSaveFileName(self,
                                                          "Save data",
                                                          self.mdictAppSettings['fsave'],
                                                          save_file_filters)
            if not (self.savefilename.isNull() or self.savefilename.isEmpty()):
                self.mdictAppSettings['fsave'] = OS.dirname(str(self.savefilename))
                try:
                    writer = csv.writer(open(self.savefilename, "wb"))
                    writer.writerow(self.DataHeader)
                    writer.writerows(self.Data)
                    self.AddMessage2Tab('Data saved to : ' + self.savefilename + '.')
                except (csv.Error), e:
                    QtGui.QMessageBox.warning(self, "epic - Save Error",
                        "Failed to load %s: %s" % (self.savefilename, e))
        else:
            self.SetStatusLabel("No data yet.")

    def saveMessages(self):
        if (len(self.mstrMessages) > 0):
            self.savefilename = QtGui.QFileDialog.getSaveFileName(self,
                                                          "Save Messages",
                                                          self.mdictAppSettings['fsave'],
                                                          save_file_filters)
            if not (self.savefilename.isNull() or self.savefilename.isEmpty()):
                self.mdictAppSettings['fsave'] = OS.dirname(str(self.savefilename))
                try:
                    writer = csv.writer(open(self.savefilename, "w"), delimiter='\n')
                    writer.writerow(self.mstrMessages)
                except (csv.Error), e:
                    QtGui.QMessageBox.warning(self, "epic - Save Error",
                        "Failed to save %s: %s" % (self.savefilename, e))
        else:
            self.SetStatusLabel("No messages yet.")

    def SelectSequestVars(self):
        if self.mblDataLoaded and not self.mblVarsSelected:
            mdlgSelectSEQVars = clsSelectSequestVars()
            if mdlgSelectSEQVars.exec_():
                self.InitVars()
                boolListCS, boolListTryp, mintMaxXC, mfltDCcth, mblBypass = mdlgSelectSEQVars.GetVars()
                try:
                    idxPepSeq = self.DataHeader.index("Peptide")
                    xIdx = self.DataHeader.index("XCorr")
                    yIdx = self.DataHeader.index("DelCn2")
                    zIdx = self.DataHeader.index("Sp")
                    idxCS = self.DataHeader.index("ChargeState")
                    idxTryptSt = self.DataHeader.index("NumTrypticEnds")
                    idxRankXc = self.DataHeader.index("RankXc")
                except (ValueError):
                    QtGui.QMessageBox.warning(self, "File error", "This file does not appear to be a Sequest Synopsys" + \
                                              "/First Hit file")

                    return None
                try:
                    CS = Npy.array([int(self.Data[i][idxCS]) for i in range(0,len(self.Data))]) # Charge state column
                    TrypSt = Npy.array([int(self.Data[i][idxTryptSt]) for i in range(0,len(self.Data))]) # Tryptic ends column
                    DelCn2 = Npy.array([float(self.Data[i][yIdx]) for i in range(0,len(self.Data))])
                    RankXc = Npy.array([int(self.Data[i][idxRankXc]) for i in range(0,len(self.Data))])
                except ValueError:
                    return None

                mblDataIdx = ProcData.extractDataSEQ(CS, TrypSt, DelCn2, RankXc, boolListCS, boolListTryp,\
                                                     mfltDCcth, mintMaxXC, mblBypass)
                if mblDataIdx != None:
                    x = Npy.array(range(len(self.Data)))
                    nIdx = x[mblDataIdx]
                    if len(nIdx) > 0:
                    # Subset data
                        self.Data = [self.Data[row][:] for row in nIdx]
                        self.UpdateDataView()
                    else:
                        self.mblVarsSelected = False
                        QtGui.QMessageBox.warning(self, "Error", "No matching data found.")
                        return None
                else:
                    QtGui.QMessageBox.warning(self, "Error", "Error in extracting data.")
                    return None

                self.Peptides = [self.Data[i][idxPepSeq] for i in xrange(len(self.Data))]
                x = [self.Data[i][xIdx] for i in xrange(len(self.Data))]
                y = [self.Data[i][yIdx] for i in xrange(len(self.Data))]
                z = [self.Data[i][zIdx] for i in xrange(len(self.Data))]
                self.mblX, self.mblY, self.mblZ = True, True, True
                self.mclsXvar.SetParameters("XCorr", "X", x)
                self.mclsYvar.SetParameters("DelCn2", "Y", y)
                self.mclsZvar.SetParameters("Sp", "Z", z)
                self.mblNormalized = False
                self.ShowVars(self.mclsXvar.name, self.mclsYvar.name, self.mclsZvar.name)
                self.AddMessage2Tab('Variables selected -> X : %s, Y : %s, Z : %s' % \
                                    (self.mclsXvar.name, self.mclsYvar.name, self.mclsZvar.name))
                self.mblVarsSelected = True
        else:
            QtGui.QMessageBox.warning(self, "Oops!", "Either data is not yet loaded or variables already selected.")

    def SelectXTandemVars(self):
        if self.mblDataLoaded and not self.mblVarsSelected:
            mdlgSelectXTVars = clsSelectXTandemVars()
            if mdlgSelectXTVars.exec_():
                self.InitVars()
                boolListCS, mfltDCcth, mblBypass = mdlgSelectXTVars.GetVars()
                try:
                    idxPepSeq = self.DataHeader.index("Peptide_Sequence")
                    xIdx = self.DataHeader.index("Peptide_Hyperscore")
                    yIdx = self.DataHeader.index("DeltaCn2")
                    idxCS = self.DataHeader.index("Charge")
                except (ValueError):
                    QtGui.QMessageBox.warning(self, "File error", "This file does not appear to be a X!Tandem file")
                    return None
                try:
                    CS = Npy.array([int(self.Data[i][idxCS]) for i in range(0,len(self.Data))]) # Charge state column
                    DelCn2 = Npy.array([float(self.Data[i][yIdx]) for i in range(0,len(self.Data))])
                except ValueError:
                    return None

                mblDataIdx = ProcData.extractDataXTandem(CS, DelCn2, boolListCS, mfltDCcth, mblBypass)
                if mblDataIdx != None:
                    x = Npy.array(range(len(self.Data)))
                    nIdx = x[mblDataIdx]
                    if len(nIdx) > 0:
                    # Subset data
                        self.Data = [self.Data[row][:] for row in nIdx]
                        self.UpdateDataView()
                    else:
                        self.mblVarsSelected = False
                        QtGui.QMessageBox.warning(self, "Error", "No matching data found.")
                        return None
                else:
                    QtGui.QMessageBox.warning(self, "Error", "Error in extracting data.")
                    return None

                self.Peptides = [self.Data[i][idxPepSeq] for i in xrange(len(self.Data))]
                x = [self.Data[i][xIdx] for i in xrange(len(self.Data))]
                y = [self.Data[i][yIdx] for i in xrange(len(self.Data))]
                self.mblX, self.mblY = True, True
                self.mclsXvar.SetParameters("Hyperscore", "X", x)
                self.mclsYvar.SetParameters("DeltaCn2", "Y", y)
                #self.mclsYvar.SetParameters("Not selected", "Z", [])
                self.mblNormalized = False
                self.ShowVars(self.mclsXvar.name, self.mclsYvar.name, "Not selected")
                self.AddMessage2Tab('Variables selected -> X : %s, Y : %s, Z : %s' % \
                                    (self.mclsXvar.name, self.mclsYvar.name, "Not selected"))
                self.mblVarsSelected = True
        else:
            QtGui.QMessageBox.warning(self, "Oops!", "Either data is not yet loaded or variables already selected.")

    def SelectSpectrumMillVars(self):
        if self.mblDataLoaded and not self.mblVarsSelected:
            mdlgSelectSMVars = clsSelectSpectrumMillVars()
            if mdlgSelectSMVars.exec_():
                self.InitVars()
                boolListCS, mfltDCcth, mblBypass = mdlgSelectSMVars.GetVars()
                try:
                    idxPepSeq = self.DataHeader.index("sequence")
                    xIdx = self.DataHeader.index("score")
                    yIdx = self.DataHeader.index("deltaForwardReverseScore")
                    idxCS = self.DataHeader.index("parent_charge")
                except (ValueError):
                    QtGui.QMessageBox.warning(self, "File error", "This file does not appear to be a Spectrum Mill file")
                    return None
                try:
                    CS = Npy.array([int(self.Data[i][idxCS]) for i in range(0,len(self.Data))]) # Charge state column
                    DelCn2 = Npy.array([float(self.Data[i][yIdx]) for i in range(0,len(self.Data))])
                except ValueError:
                    return None

                mblDataIdx = ProcData.extractDataXTandem(CS, DelCn2, boolListCS, mfltDCcth, mblBypass)
                if mblDataIdx != None:
                    x = Npy.array(range(len(self.Data)))
                    nIdx = x[mblDataIdx]
                    # Subset data
                    self.Data = [self.Data[row][:] for row in nIdx]
                    self.UpdateDataView()
                else:
                    QtGui.QMessageBox.warning(self, "Error", "Error in extracting data.")
                    return None

                self.Peptides = [self.Data[i][idxPepSeq] for i in xrange(len(self.Data))]
                x = [self.Data[i][xIdx] for i in xrange(len(self.Data))]
                y = [self.Data[i][yIdx] for i in xrange(len(self.Data))]
                self.mblX, self.mblY = True, True
                self.mclsXvar.SetParameters("Score", "X", x)
                self.mclsYvar.SetParameters("DeltaFwdRev", "Y", y)
                #self.mclsYvar.SetParameters("Not selected", "Z", [])
                self.mblNormalized = False
                self.ShowVars(self.mclsXvar.name, self.mclsYvar.name, "Not selected")
                self.AddMessage2Tab('Variables selected -> X : %s, Y : %s, Z : %s' % \
                                    (self.mclsXvar.name, self.mclsYvar.name, "Not selected"))
                self.mblVarsSelected = True
        else:
            QtGui.QMessageBox.warning(self, "Oops!", "Either data is not yet loaded or variables already selected.")

    def SelectVarsGeneric(self):
        if self.mblDataLoaded and not self.mblVarsSelected:
            mdlgSelectVars = clsSelectVars(self.DataHeader)
            if mdlgSelectVars.exec_():
                self.InitVars()
                self.VarHeader, boolListData, boolListCS, boolListTryp = mdlgSelectVars.GetVars()
                """
                boolListData = [mblY, mblZ, mblCS, mblTryptSt]
                boolListCS = [mblCS1, mblCS2, mblCS3, mblCSrest]
                boolListTryp = [mblNone, mblPartial, mblFull]
                """
                self.mblX, self.mblY, self.mblZ, self.mblCS, self.mblTryptSt = False, False, False, False, False
                self.mblY, self.mblZ, self.mblCS, self.mblTryptSt = boolListData[0], boolListData[1], \
                                                                        boolListData[2], boolListData[3]
                self.mblX = True
                xlabel = self.VarHeader[1]
                ylabel = "Not selected" if not self.mblY else self.VarHeader[2]
                zlabel = "Not selected" if not self.mblZ else self.VarHeader[3]

                idxPepSeq = self.DataHeader.index(self.VarHeader[0])
                idxX = self.DataHeader.index(self.VarHeader[1])
                idxY = None if not self.mblY else self.DataHeader.index(self.VarHeader[2])
                idxZ = None if not self.mblZ else self.DataHeader.index(self.VarHeader[3])
                idxCS = None if sum(boolListCS) == 0 else self.DataHeader.index(self.VarHeader[4])
                idxTryptSt = None if sum(boolListTryp) == 0 else self.DataHeader.index(self.VarHeader[5])

                CS, TrypSt = None, None
                nIdx = range(len(self.Data))
                mblDataIdx = None
                if idxCS != None:
                    try:
                        CS = Npy.array([int(self.Data[i][idxCS]) for i in range(0,len(self.Data))]) # Charge state column
                    except ValueError:
                        return None
                if  idxTryptSt != None:
                    try:
                        TrypSt = Npy.array([int(self.Data[i][idxTryptSt]) for i in range(0,len(self.Data))]) # Tryptic ends column
                    except ValueError:
                        return None

                mblDataIdx = ProcData.extractDataGeneric(CS, TrypSt, idxCS, idxTryptSt, boolListCS, boolListTryp)

                if mblDataIdx != None:
                    x = Npy.array(range(len(self.Data)))
                    nIdx = x[mblDataIdx]
                    # Subset data
                    self.Data = [self.Data[row][:] for row in nIdx]
                    self.UpdateDataView()

                self.Peptides = [self.Data[i][idxPepSeq] for i in xrange(len(self.Data))]
                x = [self.Data[i][idxX] for i in xrange(len(self.Data))]
                self.mclsXvar.SetParameters(xlabel, "X", x)
                if idxY != None:
                    y = [self.Data[i][idxY] for i in xrange(len(self.Data))]
                    self.mclsYvar.SetParameters(ylabel, "Y", y)
                if idxZ != None:
                    z = [self.Data[i][idxZ] for i in xrange(len(self.Data))]
                    self.mclsZvar.SetParameters(zlabel, "Z", z)

                self.mblNormalized = False
                self.ShowVars(self.mclsXvar.name, self.mclsYvar.name, self.mclsZvar.name)
                self.AddMessage2Tab('Variables selected -> X : %s, Y : %s, Z : %s' % \
                                    (self.mclsXvar.name, self.mclsYvar.name, self.mclsZvar.name))
                self.mblVarsSelected = True
        else:
            QtGui.QMessageBox.warning(self, "Oops!", "Either data is not yet loaded or variables already selected.")

    def normalizeData(self):
        if not self.mblX:
            QtGui.QMessageBox.warning(self, "No variables found.", "Select scores as variables before normalizing!")
        else:
            mdlgNormPara = clsdlgNormalizePara(self.mblY, self.mblZ)
            if mdlgNormPara.exec_():
                mblX, mblY, mblZ, mblSEQ, mblXT, mblSpecMill, mblSkip = mdlgNormPara.GetNormParameters()
                if mblSkip:
                    self.AddMessage2Tab('Skipping normalization...')
                    xN, yN, zN, self.mblNormalized = normalize.NormalizeSkip(self.Peptides,\
                                                            [] if not self.mblX else self.mclsXvar.data,\
                                                            [] if not self.mblY else self.mclsYvar.data,\
                                                            [] if not self.mblZ else self.mclsZvar.data)
                elif mblSEQ:
                    self.AddMessage2Tab('Normalizing for SEQUEST settings...')
                    xN, yN, zN, self.mblNormalized = normalize.NormalizeSEQ(self.Peptides,\
                                                            [] if not mblX else self.mclsXvar.data,\
                                                            [] if not mblY else self.mclsYvar.data,\
                                                            [] if not mblZ else self.mclsZvar.data)
                elif mblXT:
                    self.AddMessage2Tab('Normalizing for X!Tandem settings...')
                    xN, yN, zN, self.mblNormalized = normalize.NormalizeXTandem(self.Peptides,\
                                                            [] if not mblX else self.mclsXvar.data,\
                                                            [] if not mblY else self.mclsYvar.data)
                elif mblSpecMill:
                    self.AddMessage2Tab('Normalizing for Spectrum Mill settings...')
                    xN, yN, zN, self.mblNormalized = normalize.NormalizeSpectrumMill(self.Peptides,\
                                                            [] if not mblX else self.mclsXvar.data,\
                                                            [] if not mblY else self.mclsYvar.data)

                if self.mblNormalized:
                    if len(xN) > 0:
                        self.mclsXvar.dataN = Npy.array(xN)
                        self.mclsXvar.mblNormed = True
                        self.mdictNormedData[self.mclsXvar.name] = self.mclsXvar
                        self.AddDataColumn("Normalized_" + self.mclsXvar.name, xN)
                        self.AddMessage2Tab('X variable normalized.')
                    if len(yN) > 0:
                        self.mclsYvar.dataN = Npy.array(yN)
                        self.mclsYvar.mblNormed = True
                        self.mdictNormedData[self.mclsYvar.name] = self.mclsYvar
                        self.AddDataColumn("Normalized_" + self.mclsYvar.name, yN)
                        self.AddMessage2Tab('Y variable normalized.')
                    if len(zN) > 0:
                        self.mclsZvar.dataN = Npy.array(zN)
                        self.mclsZvar.mblNormed = True
                        self.mdictNormedData[self.mclsZvar.name] = self.mclsZvar
                        self.AddDataColumn("Normalized_" + self.mclsZvar.name, zN)
                        self.AddMessage2Tab('Z variable normalized.')
                    if self.mblNormalized:
                        self.AddMessage2Tab('... done.')
                        self.tablemodel = epicTableModel(self.Data, self.DataHeader, self)
                        self.ui.mTableView.setModel(self.tablemodel)
                        self.ui.mTableView.setSortingEnabled(True)
                        self.SetStatusLabel("%d rows and %d columns" %(len(self.Data), len(self.Data[0])))
                        self.AddMessage2Tab("%d rows and %d columns" %(len(self.Data), len(self.Data[0])))
                    else:
                        QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")


    ####################################################################
    # Fit a mixture of two Gaussian distributions using the
    # Expectation Maximization (EM) algorithm.
    # Classification EM (CEM) was used with some performance gains.
    ####################################################################
    def GuessInitMeans4EM(self):
        muxF, muyF, muzF, muxT, muyT, muzT = 0.2, 0.2, 0.3, 0.55, 0.75, 0.6
        varX, varY, varZ = None, None, None
        if self.mclsXvar.mblNormed:
            Xrange = Npy.linspace(self.mclsXvar.dataN.min(), self.mclsXvar.dataN.max(),10)
            muxF, muxT =Xrange[2], Xrange[7]
            varX = clsEMInitPara(self.mclsXvar.name, muxF, muxT, 0.71, 0.45)
        if self.mclsYvar.mblNormed:
            Yrange = Npy.linspace(self.mclsYvar.dataN.min(), self.mclsYvar.dataN.max(),10)
            muyF, muyT =Yrange[2], Yrange[7]
            varY = clsEMInitPara(self.mclsYvar.name, muyF, muyT, 0.32, 0.55)
        if self.mclsZvar.mblNormed:
            Zrange = Npy.linspace(self.mclsZvar.dataN.min(), self.mclsZvar.dataN.max(),10)
            muzF, muzT =Zrange[2], Zrange[7]
            varZ = clsEMInitPara(self.mclsZvar.name, muzF, muzT, 0.51, 0.35)
        return varX, varY, varZ

    def fitMixModel(self):
        if not self.mblX:
            QtGui.QMessageBox.warning(self, "No variables found.", "Select scores to fit the model!")
        else:
            if not self.mblNormalized:
                QtGui.QMessageBox.warning(self, "Normalize..", "You need to normalize the data first!")
            else:
                if self.worker != None :
                    if self.worker.isRunning():
                        QtGui.QMessageBox.warning(self, "Running...", "Model fitting is being done. Wait until it finishes.")
                        return
                else:
                    self.Xem = None
                    mdlgEMpara = clsdlgEMparameters()
                    # Init
                    Pk, M, V, ltol, maxiter = [], [], [], [], []
                    varX, varY, varZ = self.GuessInitMeans4EM()
                    mdlgEMpara.SetInitParameters(varX,\
                                                 None if not self.mclsYvar.mblNormed else varY,\
                                                 None if not self.mclsZvar.mblNormed else varZ)
                    if mdlgEMpara.exec_():
                        self.dimEM = mdlgEMpara.GetEMmodelDimension()
                        if self.dimEM == 1:
                            Pk, M, V, ltol, maxiter, varSel =mdlgEMpara.GetInitParameters1D()
                            self.strArrEMvars = [varSel] # keep track for plotting
                            mclsX = self.mdictNormedData[varSel]
                            self.Xem = mclsX.dataN
                        if self.dimEM == 2:
                            Pk, M, V, ltol, maxiter, varX, varY =mdlgEMpara.GetInitParameters2D()
                            self.strArrEMvars = [varX, varY] # keep track for plotting
                            mclsX = self.mdictNormedData[varX]
                            mclsY = self.mdictNormedData[varY]
                            self.Xem = Npy.transpose(Npy.array([mclsX.dataN, mclsY.dataN]))
                        if self.dimEM == 3:
                            Pk, M, V, ltol, maxiter =mdlgEMpara.GetInitParameters3D()
                            # keep track for plotting
                            self.strArrEMvars = [self.mclsXvar.name, self.mclsYvar.name, self.mclsZvar.name]
                            self.Xem = Npy.transpose(Npy.array([self.mclsXvar.dataN, self.mclsYvar.dataN, self.mclsZvar.dataN]))

                        mintNumGaus = 2
                        self.ToggleProgressBar(True)
                        if self.dimEM == 1:
                            self.worker = clsThreadEM1Dim.clsThreadEM1Dim()
                            self.worker.Initialize(self.Xem, mintNumGaus, Pk, M, V, ltol, maxiter)
                            self.connect(self.worker, QtCore.SIGNAL("progress(int)"), self.UpdateEMprogress)
                            self.connect(self.worker, QtCore.SIGNAL("finished(bool)"), self.EMdone)
                            self.AddMessage2Tab('EM fitting : ')
                            self.worker.start()
                        else:
                            self.worker = clsThreadEM.clsThreadEM()
                            self.worker.Initialize(self.Xem, mintNumGaus, \
                                                    Pk, M, V, ltol, maxiter)
                            self.connect(self.worker, QtCore.SIGNAL("progress(int)"), self.UpdateEMprogress)
                            self.connect(self.worker, QtCore.SIGNAL("finished(bool)"), self.EMdone)
                            self.AddMessage2Tab('EM fitting : ')
                            self.worker.start()

    def EMdone(self, mblSuccess):
        self.mblModelFitted = True
        headTitle = "p_values"
        #self.probs, self.mu, self.sigma, self.liklihood, self.probabilities, self.qvalues, self.rank = \
        #                                                            self.worker.GetResults()
        self.probs, self.mu, self.sigma, self.liklihood = self.worker.GetResults()
        self.mblSuccess = mblSuccess
        self.worker.wait()
        # Update the datatable
        #self.AddDataColumn("p_values", self.probabilities)
        #self.AddDataColumn("q_values", self.qvalues)

#        self.tablemodel = epicTableModel(self.Data, self.DataHeader, self)
#        self.ui.mTableView.setModel(self.tablemodel)
#        self.ui.mTableView.setSortingEnabled(True)
        self.SetProgressValue(100)
        self.ToggleProgressBar(False)
        self.worker = None
        if self.dimEM == 1:
            self.AddMessage2Tab('EM model was fitted.')
            self.AddMessage2Tab('Mean for False hits : ' + str(self.mu[0]))
            self.AddMessage2Tab('Standard Deviation for False hits :' + str(self.sigma[0]))
            self.AddMessage2Tab('Mean for True hits : ' + str(self.mu[1]))
            self.AddMessage2Tab('Standard Deviation for True hits :' + str(self.sigma[1]))
            self.AddMessage2Tab('Weights on True and False Distributions: ' + str(self.probs))
        else:
            self.AddMessage2Tab('EM model was fitted.')
            self.AddMessage2Tab('Means for False hits : ' + str(self.mu[:,0]))
            self.AddMessage2Tab('Covariance matrix for False hits :')
            self.AddMessage2Tab(str(self.sigma[0,:,:]))
            self.AddMessage2Tab('Means for True hits : ' + str(self.mu[:,1]))
            self.AddMessage2Tab('Covariance matrix for True hits :')
            self.AddMessage2Tab(str(self.sigma[1,:,:]))
            self.AddMessage2Tab('Weights on True and False Distributions: ' + str(self.probs))
        self.SetStatusLabel("%d rows and %d columns" %(len(self.Data), len(self.Data[0])))
        self.AddMessage2Tab("%d rows and %d columns" %(len(self.Data), len(self.Data[0])))


    def UpdateEMprogress(self, progVal):
        self.SetStatusLabel("EM fitting: %d Iterations Done." % progVal)
        self.SetProgressValue((progVal*10)%100 + 10)
        self.AddMessage2Tab("  %d Iterations Done." % progVal)

    def getpvalBayes(self):
        self.Calculate_qvalues(1)

    def getpvalGVol(self):
        self.Calculate_qvalues(2)

    def getpvalGVolC(self):
        self.Calculate_qvalues(3)

    def getpvalNoCov(self):
        self.Calculate_qvalues(4)

    def Calculate_qvalues(self, mintMethod):
        if self.mblModelFitted:
            self.ToggleProgressBar(True)
            self.worker = None
            self.worker = clsThreadqVal.clsGetqValues()
            self.worker.Initialize(self.Xem, self.probs, self.mu, self.sigma, mintMethod, self.dimEM)
            self.AddMessage2Tab('Calculating q-values...')
            self.connect(self.worker, QtCore.SIGNAL("progress(int)"), self.UpdateqValueProgress)
            self.connect(self.worker, QtCore.SIGNAL("finished(bool)"), self.qValueDone)
            self.worker.start()
        else:
            QtGui.QMessageBox.warning(self, "epic - Error", "No mixture model parameters found")

    def qValueDone(self, mblSuccess):
        self.mblpqDone = True
        headTitle = "p_values"
        self.probabilities, self.qvalues, self.rank = self.worker.GetResults()
        self.mblSuccess = mblSuccess
        self.worker.wait()
        #Update the datatable
        self.AddDataColumn("p_values", self.probabilities)
        self.AddDataColumn("q_values", self.qvalues)

        self.tablemodel = epicTableModel(self.Data, self.DataHeader, self)
        self.ui.mTableView.setModel(self.tablemodel)
        self.ui.mTableView.setSortingEnabled(True)
        self.SetProgressValue(100)
        self.ToggleProgressBar(False)
        self.worker = None
        self.AddMessage2Tab('q-values are calculated.')
        self.SetStatusLabel("%d rows and %d columns" %(len(self.Data), len(self.Data[0])))
        self.AddMessage2Tab("%d rows and %d columns" %(len(self.Data), len(self.Data[0])))

    def UpdateqValueProgress(self, progVal):
        #n, d = self.Xem.shape
        self.SetStatusLabel("Calculating q_values: %d" % progVal)
        self.SetProgressValue(progVal%100)
        #self.AddMessage2Tab("  %d rows Done." % progVal)

    def AddDataColumn(self, headTitle, dataColumn):
        # Update the datatable
        try:
            idx = self.DataHeader.index(headTitle)
        except ValueError:
            idx = -1 # no match
        if (idx == -1):
            self.Data = [self.Data[i] + [dataColumn[i]] for i in range(0, len(self.Data))]
            self.DataHeader.append(headTitle)
        else:
            for i in range(0, len(self.Data)):
                self.Data[i][idx] = dataColumn[i]


    ####################################################################
    # Plotting related methods start here
    ####################################################################
    def SaveFigure(self):
        try:
            rootFolder = self.mdictAppSettings['fsave']
        except (KeyError):
            rootFolder = self.MyDocs

        if (len(self.Data) > 0):
            figfilename = QtGui.QFileDialog.getSaveFileName(self,
                                                          "Save Figure",
                                                          rootFolder,
                                                          fig_file_filters)
            if not (figfilename.isNull() or figfilename.isEmpty()):
                self.mdictAppSettings['fsave'] = OS.dirname(str(figfilename))
                (filepath, filename) = OS.split(str(figfilename))
                (shortname, extension) = OS.splitext(filename)
                fformat = extension.split('.')[1]
                try:
                    self.ui.matplotlibWidget.canvas.fig.savefig(str(figfilename), dpi=200, format=fformat)
                except Exception, reason:
                    QtGui.QMessageBox.warning(self, "epic - Save Error",
                        "Failed to Save Figure. Error: %s" % (reason))
        else:
            self.SetStatusLabel("No data yet.")

    def ShowFDRPerformance(self):
        if not self.mblpqDone:
            QtGui.QMessageBox.warning(self, "No q-values", \
                                      "q-values aren't calculated yet.\nProcess -> Compute q-values")
            return
        else:
            self.clear_plot()
            #idx1 = Npy.sort((self.qvalues <= 0.2).nonzero())
            #idx1 = max(idx1)
            xx = Npy.array([self.qvalues, self.rank])
            #xx = xx.T
            #xx = xx[xx[:,1].argsort(),]
            #xx = xx.T
            self.ui.matplotlibWidget.canvas.ax.plot(xx[0,:], xx[1,:], "o", ms=2)
            self.ui.matplotlibWidget.canvas.ax.grid(True)
            self.ui.matplotlibWidget.canvas.PlotTitle = "FDR Performance"
            self.ui.matplotlibWidget.canvas.xtitle = "FDR"
            self.ui.matplotlibWidget.canvas.ytitle = "Count"
            self.ui.matplotlibWidget.canvas.format_labels()
            self.ui.matplotlibWidget.canvas.draw()
            #self.init_xyplot(self.qvalues, self.rank, "FDR Performance", "FDR", "Count", "Normed", '#FF0000', '-')
            self.ui.mtabWidget.setCurrentIndex(1)

    def ShowFDRpoints(self):
        if not self.mblpqDone:
            QtGui.QMessageBox.warning(self, "No q-values", \
                                      "q-values aren't calculated yet.\nProcess -> Compute q-values")
            return
        elif self.dimEM == 1:
            QtGui.QMessageBox.warning(self, "Not supported", "This feature is not available for 1-D models")
            return
        else:
            if self.mstrPlotType !="" or self.mstrPlotType != "Histogram":
                mblOK = False
                fdr, mblOK = QtGui.QInputDialog.getDouble(self, "FDR Cutoff", "Enter FDR cutoff (0-100%):", 10.0, 0, 100, 4)
                if mblOK:
                    title = "FDR = " + str(fdr) + "%"
                    fdr = fdr / 100
                    idx = self.DataHeader.index("q_values")
                    qvalues = [self.Data[i][idx] for i in xrange(len(self.Data))]
                    qvalues = Npy.array(qvalues)
                    idxfdr = (qvalues <= fdr).nonzero()
                    if self.dimEM == 2:
                        x, y = self.ContourPlotting(False, False)
                    else:
                        x, y = self.ShowFDRPoints3DModel()
                    xx = [x[i] for i in idxfdr[0]]
                    yy = [y[i] for i in idxfdr[0]]
                    self.init_xyplot(x, y, title, self.strArrEMvars[0], self.strArrEMvars[1],\
                                     "Normed", '#00FF00', 'o', False, 1)
                    self.ui.matplotlibWidget.canvas.ax.plot(xx, yy, "go", ms=2)
                    self.ui.matplotlibWidget.canvas.PlotTitle = title
                    self.ui.matplotlibWidget.canvas.format_labels()
                    self.ui.matplotlibWidget.canvas.draw()
                    self.mstrPlotType = "Contour"


    def PlotContours(self):
        if not self.mblModelFitted:
            QtGui.QMessageBox.warning(self, "No Model", "Mixture model not fitted yet.")
            return
        elif self.dimEM != 2:
            QtGui.QMessageBox.warning(self, "Not a 2D Model?", "Contours can be plotted only for 2D models.")
            return
        else:
            self.mstrPlotType = "Contour"
            sender = self.sender() # menuname and check if it has "Plot"
            sender = str(sender.objectName())
            mblSurf = (sender.find("ContourSurf")>-1)
            mblPoints = (sender.find("Points")>-1)
            if sender.find("mbtnContours")>-1:
                mblSurf, mblPoints = True, True
            self.ContourPlotting(mblSurf, mblPoints)


    def ContourPlotting(self, mblSurf, mblPoints):
        clsX = self.mdictNormedData[self.strArrEMvars[0]]
        clsY = self.mdictNormedData[self.strArrEMvars[1]]
        xx = clsX.dataN
        yy = clsY.dataN
        xlab = clsX.epicLabel
        ylab = clsY.epicLabel

        delta = (max(xx) - min(xx))/50
        x = Npy.arange(min(xx)-2*delta, max(xx)+2*delta, delta)
        y = Npy.arange(min(yy)-2*delta, max(yy)+2*delta, delta)
        X, Y = Npy.meshgrid(x, y)
        Zf = EM.GaussianGrid(X, Y, self.mu[:,0], self.sigma[0,:,:])
        Zt = EM.GaussianGrid(X, Y, self.mu[:,1], self.sigma[1,:,:])
        Zf = Zf*self.probs[0]
        Zt = Zt*self.probs[1]
        Z = Zf + Zt
        levelsF = Npy.linspace(Zf.min(), Zf.max(), 3)
        levelsT = Npy.linspace(Zt.min(), Zt.max(), 10)
        levels = Npy.unique(Npy.concatenate((levelsF, levelsT)))

        self.clear_plot()
        if mblPoints:
            #self.ui.matplotlibWidget.canvas.ax.plot(xx, yy, "ro", ms=1)
            self.init_xyplot(xx, yy, "", self.strArrEMvars[0], self.strArrEMvars[1], "Normed", '#FF0000', 'o')
            self.matplotHandle.set_markersize(1)
        self.mstrPlotVars = xlab + ylab # make a 'XY', 'YZ', 'XZ' plot type
        if not mblSurf:
            #ZZ = Npy.ma.masked_less_equal(Z, levels[1], copy=True)
            self.ui.matplotlibWidget.canvas.ax.contour(X,Y,Z,levels,colors = 'g')
        else:
            self.ui.matplotlibWidget.canvas.ax.contourf(X,Y,Z,10,cmap=Py.cm.YlOrRd)
        self.ui.matplotlibWidget.canvas.PlotTitle = "Model Fit"
        self.ui.matplotlibWidget.canvas.ax.grid(self.mblShowGrid)
        self.ui.matplotlibWidget.canvas.xtitle = self.strArrEMvars[0]
        self.ui.matplotlibWidget.canvas.ytitle = self.strArrEMvars[1]
        self.ui.matplotlibWidget.canvas.format_labels()
        self.ui.mtabWidget.setCurrentIndex(1)
        return xx, yy

    def ShowFDRPoints3DModel(self):
        clsX = self.mdictNormedData[self.strArrEMvars[0]]
        clsY = self.mdictNormedData[self.strArrEMvars[1]]
        xx = clsX.dataN
        yy = clsY.dataN
        xlab = clsX.epicLabel
        ylab = clsY.epicLabel

        self.clear_plot()
        self.init_xyplot(xx, yy, "", self.strArrEMvars[0], self.strArrEMvars[1], "Normed", '#FF0000', 'o')
        self.matplotHandle.set_markersize(1)
        self.mstrPlotVars = xlab + ylab # make a 'XY', 'YZ', 'XZ' plot type
        self.ui.matplotlibWidget.canvas.PlotTitle = "Model Fit"
        self.ui.matplotlibWidget.canvas.ax.grid(self.mblShowGrid)
        self.ui.matplotlibWidget.canvas.xtitle = self.strArrEMvars[0]
        self.ui.matplotlibWidget.canvas.ytitle = self.strArrEMvars[1]
        self.ui.matplotlibWidget.canvas.format_labels()
        self.ui.mtabWidget.setCurrentIndex(1)
        return xx, yy

    def PlotSurface(self):
        if self.mblModelFitted:
            delta = (max(self.xN) - min(self.xN))/50
            x = Npy.arange(min(self.xN)-2*delta, max(self.xN)+2*delta, delta)
            y = Npy.arange(min(self.yN)-2*delta, max(self.yN)+2*delta, delta)
            X, Y = Npy.meshgrid(x, y)
            Zf = EM.GaussianGrid(X, Y, self.mu[:,0], self.sigma[0,:,:])
            Zt = EM.GaussianGrid(X, Y, self.mu[:,1], self.sigma[1,:,:])
            Zf = Zf*self.probs[0]
            Zt = Zt*self.probs[1]
            Z = Zf + Zt
            self.clear_plot()
            self.ui.matplotlibWidget.canvas.ax.plot_surface(X,Y,Z)
            self.ui.matplotlibWidget.canvas.draw()
            self.ui.mtabWidget.setCurrentIndex(1)

    def PlotHistogram(self):
        if self.mblX:
            self.mstrPlotType = "Histogram"
            sender = self.sender() # menuname and check if it has "Plot"
            sender = str(sender.objectName())

            mblRawSelected = self.ui.mrBtnRawPlots.isChecked()
            mblNormSelected = self.ui.mrBtnNormedPlots.isChecked()
            mblRawHistX = (sender.find("RawHistX")>-1 or (sender.find("mbtnHistX")>-1 and mblRawSelected))
            mblNormHistX = (sender.find("NormHistX")>-1 or (sender.find("mbtnHistX")>-1 and mblNormSelected))
            mblRawHistY = (sender.find("RawHistY")>-1 or (sender.find("mbtnHistY")>-1 and mblRawSelected))
            mblNormHistY = (sender.find("NormHistY")>-1 or (sender.find("mbtnHistY")>-1 and mblNormSelected))
            mblRawHistZ = (sender.find("RawHistZ")>-1 or (sender.find("mbtnHistZ")>-1 and mblRawSelected))
            mblNormHistZ = (sender.find("NormHistZ")>-1 or (sender.find("mbtnHistZ")>-1 and mblNormSelected))

            mblPlotmodelFit = False

            if mblRawHistX and self.mblX:
                X = self.mclsXvar.data
                title = "Histogram of " + self.mclsXvar.name
                xtitle = self.mclsXvar.name
            elif mblNormHistX and self.mblX and self.mclsXvar.mblNormed:
                X = self.mclsXvar.dataN
                title = "Histogram of Normalized " + self.mclsXvar.name
                xtitle = "Normalized " + self.mclsXvar.name
                if self.mblModelFitted and self.dimEM == 1 and self.strArrEMvars[0].find(self.mclsXvar.name) > -1:
                    muF = self.mu[0]
                    muT = self.mu[1]
                    sigmaF = self.sigma[0]
                    sigmaT = self.sigma[1]
                    mblPlotmodelFit = True
            elif mblRawHistY and self.mblY:
                X = self.mclsYvar.data
                title = "Histogram of " + self.mclsYvar.name
                xtitle = self.mclsYvar.name
            elif mblNormHistY and self.mblY and self.mclsYvar.mblNormed:
                X = self.mclsYvar.dataN
                title = "Histogram of Normalized " + self.mclsYvar.name
                xtitle = "Normalized " + self.mclsYvar.name
                if self.mblModelFitted and self.dimEM == 1 and self.strArrEMvars[0].find(self.mclsYvar.name) > -1:
                    muF = self.mu[0]
                    muT = self.mu[1]
                    sigmaF = self.sigma[0]
                    sigmaT = self.sigma[1]
                    mblPlotmodelFit = True
            elif mblRawHistZ and self.mblZ:
                X = self.mclsZvar.data
                title = "Histogram of " + self.mclsZvar.name
                xtitle = self.mclsZvar.name
            elif mblNormHistZ and self.mblZ and self.mclsZvar.mblNormed:
                X = self.mclsZvar.dataN
                title = "Histogram of Normalized " + self.mclsZvar.name
                xtitle = "Normalized " + self.mclsZvar.name
                if self.mblModelFitted and self.dimEM == 1 and self.strArrEMvars[0].find(self.mclsZvar.name) > -1:
                    muF = self.mu[0]
                    muT = self.mu[1]
                    sigmaF = self.sigma[0]
                    sigmaT = self.sigma[1]
                    mblPlotmodelFit = True
            else:
                QtGui.QMessageBox.warning(self, "No variables", "Either this variable is not selected or\n" +\
                                           "data not normalized if you were trying to plot normalized data.")
                return
            if sender.find("mbtn")>-1 or self.ui.mtabWidget.currentIndex() == 1:
                try:
                    nbins = int(self.ui.mlineEdBins.text())
                except ValueError:
                    QtGui.QMessageBox.warning(self, "Invalid Bins", "Bins should be an integer number.")
                    return
            else:
                nbins = 100
            pcolor = '#00CC00'
            Xn = [float(X[i]) for i in range(0, len(X))]

            self.clear_plot()
            n, bins = Npy.histogram(Xn, nbins, normed=True, new=True)
            width = 0.9*(bins[1]-bins[0])

            if mblPlotmodelFit:
                yF = self.probs[0]*Py.normpdf(bins, muF, sigmaF)
                yT = self.probs[1]*Py.normpdf(bins, muT, sigmaT)
                self.ui.matplotlibWidget.canvas.ax.plot(bins, yF, 'r-')
                self.ui.matplotlibWidget.canvas.ax.plot(bins, yT, 'b-')
                self.ui.matplotlibWidget.canvas.ax.plot(bins, yF+yT, 'k--')

            self.histBars = self.ui.matplotlibWidget.canvas.ax.bar(bins[0:-1], n, width=width, color=pcolor)
            self.plotax = self.ui.matplotlibWidget.canvas.ax
            self.histColor = self.histBars[0].get_facecolor()

            self.ui.matplotlibWidget.canvas.ax.grid(True)
            self.ui.matplotlibWidget.canvas.PlotTitle = title
            self.ui.matplotlibWidget.canvas.xtitle = xtitle
            self.ui.matplotlibWidget.canvas.ytitle = "Frequency"
            self.ui.matplotlibWidget.canvas.format_labels()
            self.ui.matplotlibWidget.canvas.draw()
            self.ui.mtabWidget.setCurrentIndex(1)
            self.mstrPlotVars = "Histogram"


    def ScatterPlot(self):
        numVars = self.mblX + self.mblY + self.mblZ
        if numVars >= 2:
            self.mstrPlotType = "Scatter"
            sender = self.sender() # menuname and check if it has "Plot"
            sender = str(sender.objectName())

            mblRawSelected = self.ui.mrBtnRawPlots.isChecked()
            mblNormSelected = self.ui.mrBtnNormedPlots.isChecked()
            mblXY = (sender.find("X_vs_Y")>-1 or sender.find("mbtnX_vs_Y")>-1)
            mblXZ = (sender.find("X_vs_Z")>-1 or sender.find("mbtnX_vs_Z")>-1)
            mblYZ = (sender.find("Y_vs_Z")>-1 or sender.find("mbtnY_vs_Z")>-1)

            X, Y, Z = [], [], []
            if (sender.find("Raw")>-1) or mblRawSelected:
                X, Y, Z = self.mclsXvar.data, self.mclsYvar.data, self.mclsZvar.data
                plotType = "Raw"
                Title = "Raw Data"
            elif (sender.find("Norm")>-1 or mblNormSelected) and self.mblNormalized:
                X, Y, Z = self.mclsXvar.dataN, self.mclsYvar.dataN, self.mclsZvar.dataN
                plotType = "Normed"
                Title = "Normalized Data"
            else:
                QtGui.QMessageBox.warning(self, "Invalid", "No normalized data found.")
                return

            if mblXY and self.mblX and self.mblY:
                x, y = X, Y
                xlab, ylab = self.mclsXvar.name, self.mclsYvar.name
                self.mstrPlotVars = "XY"
            elif mblXZ and self.mblX and self.mblZ:
                x, y = X, Z
                xlab, ylab = self.mclsXvar.name, self.mclsZvar.name
                self.mstrPlotVars = "XZ"
            elif mblYZ and self.mblY and self.mblZ:
                x, y = Y, Z
                xlab, ylab = self.mclsYvar.name, self.mclsZvar.name
                self.mstrPlotVars = "YZ"
            else:
                QtGui.QMessageBox.warning(self, "Data insufficient", "No matches found for your selection.")
                return

            if (len(x) > 0) and (len(y) > 0):
                self.init_xyplot(x, y, Title, xlab, ylab, plotType, '#FF0000', 'o')
                self.ui.mtabWidget.setCurrentIndex(1)
            else:
                QtGui.QMessageBox.warning(self, "Data insufficient", "No matches found for your selection.")
        else:
            QtGui.QMessageBox.warning(self, "Data insufficient",\
                                      "No matches found for your selection.\nNeed at least two variables.")



    def PlotXY(self, X, Y, title, xlab, ylab, plotType, plotStr):
        self.init_xyplot(X, Y, title, xlab, ylab, plotType, '#FF0000', 'o')
        self.mstrPlotVars = plotStr

    def SelectPoints(self):
        """
        This method will be called from the plot context menu for
        selecting points
        """
        if self.mblX and self.mstrPlotType != "Histogram" and self.selectHandle != None:
            if not self.mblPickPoints:
                self._connectionIDplot = self.ui.matplotlibWidget.canvas.mpl_connect('pick_event', self.OnPick)
                self.mblPickPoints = True
                self.ui.mnuSelectPoints.setChecked(True)
                #self.ui.mnuSelectPoints.setIcon(ico1)
            else:
                self.ui.matplotlibWidget.canvas.mpl_disconnect(self._connectionIDplot)
                self.mblPickPoints = False
                self.selectHandle.set_visible(False)
                self.textHandle.set_text('')
                self.ui.matplotlibWidget.canvas.draw()
                self.ui.mnuSelectPoints.setChecked(False)

    def OnPick(self, event):
        """
        This is the pick_event handler for matplotlib
        This method will get the coordinates of the mouse pointer and
        finds the closest point and retrieves the corresponding peptide sequence.
        Also draws a yellow circle around the point.
        """
        if self.mblX and self.mstrPlotType != "Histogram":
            #if event.artist!=line: return True
            N1 = len(event.ind)
            if not N1: return True
            # the click locations
            xc = event.mouseevent.xdata
            yc = event.mouseevent.ydata

            X, Y, Z = self.mclsXvar.data, self.mclsYvar.data, self.mclsZvar.data

            if self.mstrPlotData == 'Normed':
                X, Y, Z = self.mclsXvar.dataN, self.mclsYvar.dataN, self.mclsZvar.dataN
            elif self.mstrPlotData == 'Raw':
                X, Y, Z = self.mclsXvar.data, self.mclsYvar.data, self.mclsZvar.data

            if self.mstrPlotVars == "XY" or self.mstrPlotVars == "YX":
                x, y = X, Y
            if self.mstrPlotVars == "YZ" or self.mstrPlotVars == "ZY":
                x, y = Y, Z
            if self.mstrPlotVars == "XZ" or self.mstrPlotVars == "ZX":
                x, y = X, Z

            x = [float(x[i]) for i in range(0, len(x))]
            y = [float(y[i]) for i in range(0, len(y))]

            x = Npy.array(x)
            y = Npy.array(y)

            distances = Npy.hypot(xc-x[event.ind], yc-y[event.ind])
            indmin = distances.argmin()
            dataind = event.ind[indmin]

            showText = self.Peptides[dataind]
            if self.mblX:
                showText = showText + "\n" + self.mclsXvar.name + " = " + str(self.mclsXvar.data[dataind])
            if self.mblY:
                showText = showText + "\n" + self.mclsYvar.name + " = " + str(self.mclsYvar.data[dataind])
            if self.mblZ:
                showText = showText + "\n" + self.mclsZvar.name + " = " + str(self.mclsZvar.data[dataind])

            # show yellow circle
            self.selectHandle.set_visible(True)
            self.selectHandle.set_data(x[dataind], y[dataind])
            #print x[dataind], y[dataind]
            self.textHandle.set_text(showText)
            self.ui.matplotlibWidget.canvas.draw()

    def MotionOnPlot(self, event):
        """Called during mouse motion over figure"""
        if self.mblX:
            if event.xdata != None and event.ydata != None: # mouse is inside the axes
                tip1 = 'x=%f\ny=%f' % (event.xdata, event.ydata)
                tip2 = 'x=%f\ty=%f' % (event.xdata, event.ydata)
                self.setToolTip(tip1) # update the tooltip
                self.statusBar().showMessage(tip2)
            else: # mouse is outside the axes
                self.statusBar().showMessage(" ")

    def HorizontalZoomToggle(self):
        if self.mblIsHZoom:
            self.mblIsHZoom = False
            self.span.visible = False
            self.ui.mnuHZoom.setChecked(False)
        else:
            self.mblIsHZoom = True
            self.span.visible = True
            self.ui.mnuHZoom.setChecked(True)

    def onselect(self,  xmin, xmax):
        if self.mblIsHZoom:
            self.ui.matplotlibWidget.canvas.ax.set_xlim(xmin,  xmax)
            self.ui.matplotlibWidget.canvas.draw()


    def clear_plot(self):
        self.ui.matplotlibWidget.canvas.ax.cla()
        self.ui.matplotlibWidget.canvas.format_labels()
        self.ui.matplotlibWidget.canvas.draw()
        self.mblHistPlot = False

    def autoscale_plot(self):
        self.ui.matplotlibWidget.canvas.ax.autoscale_view(tight = False, scalex=True, scaley=True)
        self.ui.matplotlibWidget.canvas.draw()

    def init_xyplot(self, x, y, title="Data", xtitle="XCorr", ytitle="DelCn2", plotType="Raw",
                  col='#FF0000', symb='o', mblClear=True, ms=2):
        self.mstrPlotData = plotType
        if mblClear:
            self.clear_plot()
        self.matplotHandle, = self.ui.matplotlibWidget.canvas.ax.plot(x, y, symb, picker=5)
        self.matplotHandle.set_markerfacecolor(col)
        self.selectHandle, = self.ui.matplotlibWidget.canvas.ax.plot([x[0]], [y[0]], 'o', \
                                        ms=8, alpha=.4, color='yellow', visible=False)
        self.textHandle = self.ui.matplotlibWidget.canvas.ax.text(0.02, 0.98, '', fontsize=7, \
                                        bbox=dict(facecolor='yellow', alpha=0.2), \
                                        transform=self.ui.matplotlibWidget.canvas.ax.transAxes, va='top')
        self.plotax = self.ui.matplotlibWidget.canvas.ax

        #if plotType not in self.mdictPlotParameters:
        self.matplotHandle.set_markersize(ms)
        self.ui.matplotlibWidget.canvas.ax.grid(self.mblShowGrid)
        self.ui.matplotlibWidget.canvas.PlotTitle = title
        self.ui.matplotlibWidget.canvas.xtitle = xtitle
        self.ui.matplotlibWidget.canvas.ytitle = ytitle
        self.clsPlotParaCurr = clsPlotParameters(self.matplotHandle, \
                                                           self.mblShowGrid, \
                                                           self.plotax.get_xlim(), \
                                                           self.plotax.get_ylim(), \
                                                           self.plotax.get_xscale(), \
                                                           self.plotax.get_yscale(), \
                                                           self.ui.matplotlibWidget.canvas.PlotTitle, \
                                                           self.ui.matplotlibWidget.canvas.xtitle, \
                                                           self.ui.matplotlibWidget.canvas.ytitle, \
                                                           self.histColor, \
                                                           self._connectionIDplot, self.mblPickPoints)
        self.mdictPlotParameters[plotType] = self.clsPlotParaCurr

        #self.updatePlot(self.mdictPlotParameters[plotType])
        self.ui.matplotlibWidget.canvas.format_labels()
        self.ui.matplotlibWidget.canvas.draw()

    def updatePlot(self, clsPlotParam):
        if self.matplotHandle is not None:
            self.matplotHandle.set_markersize(clsPlotParam.mflMarkerSize)
            self.matplotHandle.set_marker(clsPlotParam.mstrMarkerStyle)
            self.matplotHandle.set_markerfacecolor(clsPlotParam.mstrColor)
            self.matplotHandle.set_linestyle(clsPlotParam.mstrLineStyle)
            self.matplotHandle.set_linewidth(clsPlotParam.mflLineWidth)
        self.mblShowGrid = clsPlotParam.mblShowGrid
        self.ui.matplotlibWidget.canvas.ax.grid(self.mblShowGrid)
        self.ui.matplotlibWidget.canvas.ax.set_xlim((clsPlotParam.mflXmin, clsPlotParam.mflXmax))
        self.ui.matplotlibWidget.canvas.ax.set_ylim((clsPlotParam.mflYmin, clsPlotParam.mflYmax))
        self.ui.matplotlibWidget.canvas.ax.set_xscale(clsPlotParam.mstrXscale)
        self.ui.matplotlibWidget.canvas.ax.set_yscale(clsPlotParam.mstrYscale)
        if len(self.histBars) >0:
            for bar in self.histBars:
                bar.set_facecolor(clsPlotParam.mstrColor)
        self.ui.matplotlibWidget.canvas.PlotTitle = clsPlotParam.mstrTitle
        self.ui.matplotlibWidget.canvas.xtitle = clsPlotParam.mstrXlabel
        self.ui.matplotlibWidget.canvas.ytitle = clsPlotParam.mstrYlabel
        self.ui.matplotlibWidget.canvas.format_labels()
        self.ui.matplotlibWidget.canvas.draw()

    def plottingOptions(self):
        if self.mblX:
            if len(self.histBars) > 0:
                self.histColor = self.histBars[0].get_facecolor()
            self.plotOptDialog = PlotOptions(clsPlotParameters(self.matplotHandle, \
                                                           self.mblShowGrid, \
                                                           self.plotax.get_xlim(), \
                                                           self.plotax.get_ylim(), \
                                                           self.plotax.get_xscale(), \
                                                           self.plotax.get_yscale(), \
                                                           self.ui.matplotlibWidget.canvas.PlotTitle, \
                                                           self.ui.matplotlibWidget.canvas.xtitle, \
                                                           self.ui.matplotlibWidget.canvas.ytitle,\
                                                           self.histColor,\
                                                           self._connectionIDplot, self.mblPickPoints))
            if self.plotOptDialog.exec_():
                mclsPlotpara = self.plotOptDialog.GetPlotParamters()
                self.mdictPlotParameters[self.mstrPlotData] = mclsPlotpara
                self.updatePlot(mclsPlotpara)

    def autoscalePlot(self):
        self.ui.matplotlibWidget.canvas.ax.autoscale_view(tight = False, scalex=True, scaley=True)
        self.ui.matplotlibWidget.canvas.draw()
    ####################################################################
    # Plotting related methods end here
    ####################################################################

    def about_eFDR(self):
        dlgAboutEpic = clsAboutEpic()
        dlgAboutEpic.exec_()


# end Main_Window class

################################################
# Main Program
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    Main_Window().Splash()

    myapp = Main_Window()
    icon = QtGui.QIcon(":/epic.png")
    myapp.setWindowIcon(icon)
    #### Speed up ###
    #import psyco
    #psyco.full()
    #################
    myapp.show()
    sys.exit(app.exec_())
## End of Main Program
################################################




