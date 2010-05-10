import numpy as Npy
from PyQt4 import QtGui, QtCore
from supportClasses.clsPlotParameters import clsPlotParameters

from epicUIelements.ui_dlgHistogramPlotOptions import Ui_dlgHistogramPlotOptions

markerColors = dict(Blue = 'b',\
                    Green = 'g',\
                    Red = 'r',\
                    Cyan = 'c',\
                    Magenta = 'm',\
                    Yellow = 'y',\
                    Black = 'k',\
                    White = 'w')

class clsHistogramPlotOptions(QtGui.QDialog):
    def __init__(self, mblNormed, mblSp):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_dlgHistogramPlotOptions()
        self.ui.setupUi(self)
        icon = QtGui.QIcon(":/epic.png")
        self.setWindowIcon(icon)
        self.nbins = 100
        self.mcolor = "#35cc1b"
        self.connect(self.ui.mtoolBtnColor, QtCore.SIGNAL("colorChanged(QColor)"), self.setMColor)

        self.populate_dialog()
        if not mblSp:
            self.ui.mrBtnSp.setEnabled(False)
            self.ui.mrBtnSpN.setEnabled(False)
        if not mblNormed:
            self.ui.mrBtnDelCn2N.setEnabled(False)
            self.ui.mrBtnXCorrN.setEnabled(False)
            self.ui.mrBtnSpN.setEnabled(False)

        self.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.OK)

    def setMColor(self, QColor):
        self.mcolor = str(QColor.name())#need to set value to str as it is QString

    def populate_dialog(self):
        self.ui.mtoolBtnColor.setColor(QtGui.QColor(self.mcolor))

    def OK(self):
        try:
            self.nbins = int(self.ui.mlEditBins.text())
        except:
            QtGui.QMessageBox.warning(self, "Invalid bin value", "Invalid bin number detected. Enter an integer.")
            self.reject()
        else:
            self.accept()

    def GetHistParameters(self):
        self.nbins = int(self.ui.mlEditBins.text())

        if self.ui.mrBtnXCorr.isChecked():
            plotVar = "XCorr"
        elif self.ui.mrBtnXCorrN.isChecked():
            plotVar = "XCorrN"
        elif self.ui.mrBtnDelCn2.isChecked():
            plotVar = "DelCn2"
        elif self.ui.mrBtnDelCn2N.isChecked():
            plotVar = "DelCn2N"
        elif self.ui.mrBtnSp.isChecked():
            plotVar = "Sp"
        elif self.ui.mrBtnSpN.isChecked():
            plotVar = "SpN"

        return self.mcolor, plotVar, self.nbins

