import numpy as Npy
from PyQt4 import QtGui, QtCore

from epicUIelements.ui_dlgXYPlots import Ui_mdlgXYPlot

class clsXYPlotOptions(QtGui.QDialog):
    def __init__(self, mblNormed, mblSp):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_mdlgXYPlot()
        self.ui.setupUi(self)
        icon = QtGui.QIcon(":/epic.png")
        self.setWindowIcon(icon)

        if not mblSp:
            self.ui.mrBtnSpDelCn2.setEnabled(False)
            self.ui.mrBtnXCorrSp.setEnabled(False)
        if mblNormed:
            self.ui.mrBtnXCorrDelCn2.setText("Normalized XCorr vs. Normalized DelCn2")
            self.ui.mrBtnSpDelCn2.setText("Normalized Sp vs. Normalized DelCn2")
            self.ui.mrBtnXCorrSp.setText("Normalized XCorr vs. Normalized Sp")

        self.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.OK)

    def OK(self):
        self.accept()

    def GetXYParameters(self):
        if self.ui.mrBtnXCorrDelCn2.isChecked():
            plotVar = "XCorrDelCn2"
        elif self.ui.mrBtnSpDelCn2.isChecked():
            plotVar = "SpDelCn2"
        elif self.ui.mrBtnXCorrSp.isChecked():
            plotVar = "XCorrSp"

        return plotVar

