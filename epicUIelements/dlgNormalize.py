#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
from os.path import basename
from epicUIelements.ui_dlgNormalize import Ui_mdlgNormalize
import qrc_epicResources

class clsdlgNormalizePara(QtGui.QDialog):
    def __init__(self, mblY, mblZ):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_mdlgNormalize()
        self.ui.setupUi(self)
        icon = QtGui.QIcon(":/epic.png")
        self.setWindowIcon(icon)

        if not mblY:
            self.ui.mchkBoxDelCn2.setChecked(False)
            self.ui.mchkBoxDelCn2.setEnabled(False)
        if not mblZ:
            self.ui.mchkBoxSp.setChecked(False)
            self.ui.mchkBoxSp.setEnabled(False)
        self.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.OK)

    def OK(self):
        varSelected = 0
        if self.ui.mrBtnSequest.isChecked():
            varSelected = self.ui.mchkBoxXCorr.isChecked() + self.ui.mchkBoxDelCn2.isChecked() +\
                        self.ui.mchkBoxSp.isChecked()
            if (varSelected > 0):
                self.accept()
            else:
                QtGui.QMessageBox.warning(self, "Fewer choices", "Check at least two variables to be normalized.")
        elif self.ui.mrBtnXTandem.isChecked():
            varSelected = self.ui.mchkBoxHyperS.isChecked() + self.ui.mchkBoxDeltaCn2.isChecked()
            if (varSelected > 0):
                self.accept()
            else:
                QtGui.QMessageBox.warning(self, "Fewer choices", "Check at least two variables to be normalized.")
        elif self.ui.mrBtnSpectrumMill.isChecked():
            varSelected = self.ui.mchkBoxSMScore.isChecked() + self.ui.mchkBoxSMDelta.isChecked()
            if (varSelected > 0):
                self.accept()
            else:
                QtGui.QMessageBox.warning(self, "Fewer choices", "Check at least two variables to be normalized.")
        elif self.ui.mrBtnSkip.isChecked():
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, "Error", "Select wisely...")


    def SetInitParameters(self, sub):
        self.ui.mchkBoxXCorr.setChecked()
        self.ui.mchkBoxDelCn2.setChecked()

    def GetNormParameters(self):
        mblSEQ, mblXT, mblSpecMill = False, False, False
        if self.ui.mrBtnSkip.isChecked():
            return False, False, False, False, False, False, True
        if self.ui.mrBtnSequest.isChecked():
            mblSEQ = True
            mblX = self.ui.mchkBoxXCorr.isChecked()
            mblY = self.ui.mchkBoxDelCn2.isChecked()
            mblZ = self.ui.mchkBoxSp.isChecked()
            mblSkip = False
            return mblX, mblY, mblZ, mblSEQ, mblXT, mblSpecMill, mblSkip
        elif self.ui.mrBtnXTandem.isChecked():
            mblXT = True
            mblX = self.ui.mchkBoxHyperS.isChecked()
            mblY = self.ui.mchkBoxDeltaCn2.isChecked()
            mblZ = False
            mblSkip = False
            return mblX, mblY, mblZ, mblSEQ, mblXT, mblSpecMill, mblSkip
        elif self.ui.mrBtnSpectrumMill.isChecked():
            mblSpecMill = True
            mblX = self.ui.mchkBoxSMScore.isChecked()
            mblY = self.ui.mchkBoxSMDelta.isChecked()
            mblZ = False
            mblSkip = False
            return mblX, mblY, mblZ, mblSEQ, mblXT, mblSpecMill, mblSkip
        else:
            return False, False, False, False, False, False, False

