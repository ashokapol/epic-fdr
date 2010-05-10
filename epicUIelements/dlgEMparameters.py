#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
from os.path import basename
from epicUIelements.ui_dlgEMparameters import Ui_mdlgEMparameters
from supportClasses.clsEMInitPara import clsEMInitPara
import qrc_epicResources
import numpy as Npy

class clsdlgEMparameters(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_mdlgEMparameters()
        self.ui.setupUi(self)
        icon = QtGui.QIcon(":/epic.png")
        self.setWindowIcon(icon)

        self.X = ""
        self.Y = ""
        self.muYF = 0.2
        self.muYT = 0.6
        self.sigYF = 0.32
        self.sigYT = 0.55
        self.RhoT = 0.33
        self.pF = 0.6
        self.muXF = 0.2
        self.muXT = 0.7
        self.sigXF = 0.71
        self.sigXT = 0.45
        self.RhoF = 0.2
        self.pT = 1 - self.pF
        self.MaxIter = 1000
        self.Tol = 0.1

        self.varX, self.varY, self.varZ = None, None, None

        self.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.OK)
        self.connect(self.ui.mcmbBox1DX, QtCore.SIGNAL("currentIndexChanged(int)"), self.onIndexChanged1DX)
        self.connect(self.ui.mcmbBox2DX, QtCore.SIGNAL("currentIndexChanged(int)"), self.onIndexChanged2DX)
        self.connect(self.ui.mcmbBox2DY, QtCore.SIGNAL("currentIndexChanged(int)"), self.onIndexChanged2DY)

    def onIndexChanged1DX(self, index):
        if index == 0:
            muF = str(round(self.varX.muF,2))
            muT = str(round(self.varX.muT,2))
            sigF = str(round(self.varX.sigF,2))
            sigT = str(round(self.varX.sigT,2))
        if index == 1:
            muF = str(round(self.varY.muF,2))
            muT = str(round(self.varY.muT,2))
            sigF = str(round(self.varY.sigF,2))
            sigT = str(round(self.varY.sigT,2))
        if index == 2:
            muF = str(round(self.varZ.muF,2))
            muT = str(round(self.varZ.muT,2))
            sigF = str(round(self.varZ.sigF,2))
            sigT = str(round(self.varZ.sigT,2))
        self.ui.mLineEd1DmuF.setText(muF)
        self.ui.mLineEd1DmuT.setText(muT)
        self.ui.mLineEd1DsigF.setText(sigF)
        self.ui.mLineEd1DsigT.setText(sigT)

    def onIndexChanged2DX(self, index):
        if index == 0:
            muF = str(round(self.varX.muF,2))
            muT = str(round(self.varX.muT,2))
            sigF = str(round(self.varX.sigF,2))
            sigT = str(round(self.varX.sigT,2))
        if index == 1:
            muF = str(round(self.varY.muF,2))
            muT = str(round(self.varY.muT,2))
            sigF = str(round(self.varY.sigF,2))
            sigT = str(round(self.varY.sigT,2))
        if index == 2:
            muF = str(round(self.varZ.muF,2))
            muT = str(round(self.varZ.muT,2))
            sigF = str(round(self.varZ.sigF,2))
            sigT = str(round(self.varZ.sigT,2))
        self.ui.mLineEd2DmuXF.setText(muF)
        self.ui.mLineEd2DmuXT.setText(muT)
        self.ui.mLineEd2DsigXF.setText(sigF)
        self.ui.mLineEd2DsigXT.setText(sigT)

    def onIndexChanged2DY(self, index):
        if index == 0:
            muF = str(round(self.varX.muF,2))
            muT = str(round(self.varX.muT,2))
            sigF = str(round(self.varX.sigF,2))
            sigT = str(round(self.varX.sigT,2))
        if index == 1:
            muF = str(round(self.varY.muF,2))
            muT = str(round(self.varY.muT,2))
            sigF = str(round(self.varY.sigF,2))
            sigT = str(round(self.varY.sigT,2))
        if index == 2:
            muF = str(round(self.varZ.muF,2))
            muT = str(round(self.varZ.muT,2))
            sigF = str(round(self.varZ.sigF,2))
            sigT = str(round(self.varZ.sigT,2))
        self.ui.mLineEd2DmuYF.setText(muF)
        self.ui.mLineEd2DmuYT.setText(muT)
        self.ui.mLineEd2DsigYF.setText(sigF)
        self.ui.mLineEd2DsigYT.setText(sigT)

    def OK(self):
        if (self.ui.mstkWidgEM.currentIndex() == 0):
            try:
                if (self.ui.mcmbBox1DX.currentIndex() == -1):
                    raise Exception('Select a variable')
                self.X = str(self.ui.mcmbBox1DX.currentText())
                self.muXF = float(self.ui.mLineEd1DmuF.text())
                self.muXT = float(self.ui.mLineEd1DmuT.text())
                self.sigXF = float(self.ui.mLineEd1DsigF.text())
                self.sigXT = float(self.ui.mLineEd1DsigT.text())
                self.MaxIter = int(self.ui.mLineEd1DMaxIter.text())
                self.Tol = float(self.ui.mLineEd1DTol.text())
                self.pF = float(self.ui.mLineEd1DpF.text())
            except Exception, inst:
                QtGui.QMessageBox.warning(self, "Invalid entries", "Invalid entry detected." +\
                                          " Check all entries again.\nError: %s" % inst)
            else:
                self.accept()

        if (self.ui.mstkWidgEM.currentIndex() == 1):
            try:
                if (self.ui.mcmbBox2DX.currentText() == self.ui.mcmbBox2DY.currentText()):
                    raise Exception('Same Variable selected for X and Y')
                if ((self.ui.mcmbBox2DX.currentIndex() == -1) or (self.ui.mcmbBox2DY.currentIndex() == -1)):
                    raise Exception('Select Two variables')
                self.X = str(self.ui.mcmbBox2DX.currentText())
                self.Y = str(self.ui.mcmbBox2DY.currentText())
                self.muXF = float(self.ui.mLineEd2DmuXF.text())
                self.muXT = float(self.ui.mLineEd2DmuXT.text())
                self.RhoF = float(self.ui.mLineEd2DRhoF.text())
                self.RhoT = float(self.ui.mLineEd2DRhoT.text())
                self.sigXF = float(self.ui.mLineEd2DsigXF.text())
                self.sigXT = float(self.ui.mLineEd2DsigXT.text())
                self.MaxIter = int(self.ui.mLineEd2DMaxIter.text())
                self.Tol = float(self.ui.mLineEd2DTol.text())
                self.muYF = float(self.ui.mLineEd2DmuYF.text())
                self.muYT = float(self.ui.mLineEd2DmuYT.text())
                self.sigYF = float(self.ui.mLineEd2DsigYF.text())
                self.sigYT = float(self.ui.mLineEd2DsigYT.text())
                self.pF = float(self.ui.mLineEd2DpF.text())
            except Exception, inst:
                QtGui.QMessageBox.warning(self, "Invalid entries", "Invalid entry detected." +\
                                          " Check all entries again.\nError: %s" % inst)
            else:
                self.accept()

        if (self.ui.mstkWidgEM.currentIndex() == 2):
            try:
                self.muXF = float(self.ui.mLineEd3DmuXF.text())
                self.muXT = float(self.ui.mLineEd3DmuXT.text())
                self.MaxIter = int(self.ui.mLineEd3DMaxIter.text())
                self.Tol = float(self.ui.mLineEd3DTol.text())
                self.muYF = float(self.ui.mLineEd3DmuYF.text())
                self.muYT = float(self.ui.mLineEd3DmuYT.text())
                self.muZF = float(self.ui.mLineEd3DmuZF.text())
                self.muZT = float(self.ui.mLineEd3DmuZT.text())
                self.pF = float(self.ui.mLineEd3DpF.text())
            except Exception, inst:
                QtGui.QMessageBox.warning(self, "Invalid entries", "Invalid entry detected." +\
                                          " Check all entries again.\nError: %s" % inst)
            else:
                self.accept()

    def SetInitParameters(self, varX, varY, varZ):
        self.varX, self.varY, self.varZ = varX, varY, varZ
        vars = [varX.varname]
        if varY is not None:
            vars.append(varY.varname)
        if varZ is not None:
            vars.append(varZ.varname)
        self.ui.mcmbBox1DX.insertItems(0, vars)
        self.ui.mcmbBox2DX.insertItems(0, vars)
        self.ui.mcmbBox2DY.insertItems(0, vars)

        self.ui.mLineEd1DmuF.setText(str(round(varX.muF,2)))
        self.ui.mLineEd1DmuT.setText(str(round(varX.muT,2)))
        self.ui.mLineEd1DsigF.setText(str(round(varX.sigF,2)))
        self.ui.mLineEd1DsigT.setText(str(round(varX.sigT,2)))

        self.ui.mLineEd2DmuXF.setText(str(round(varX.muF,2)))
        self.ui.mLineEd2DmuXT.setText(str(round(varX.muT,2)))
        self.ui.mLineEd2DsigXF.setText(str(round(varX.sigF,2)))
        self.ui.mLineEd2DsigXT.setText(str(round(varX.sigT,2)))
        self.ui.mLineEd2DmuYF.setText('' if varY is None else str(round(varY.muF,2)))
        self.ui.mLineEd2DmuYT.setText('' if varY is None else str(round(varY.muT,2)))
        self.ui.mLineEd2DsigYF.setText('' if varY is None else str(round(varY.sigF,2)))
        self.ui.mLineEd2DsigYT.setText('' if varY is None else str(round(varY.sigT,2)))

        self.ui.mLineEd3DmuXF.setText(str(round(varX.muF,2)))
        self.ui.mLineEd3DmuXT.setText(str(round(varX.muT,2)))
        self.ui.mLineEd3DmuYF.setText('' if varY is None else str(round(varY.muF,2)))
        self.ui.mLineEd3DmuYT.setText('' if varY is None else str(round(varY.muT,2)))
        self.ui.mLineEd3DmuZF.setText('' if varZ is None else str(round(varZ.muF,2)))
        self.ui.mLineEd3DmuZT.setText('' if varZ is None else str(round(varZ.muT,2)))

        if len(vars) == 1:
            self.ui.page2D.setEnabled(False)
            self.ui.page3D.setEnabled(False)
        if len(vars) == 2:
            self.ui.page3D.setEnabled(False)
        try:
            iX = vars.index('XCorr')
            iY = vars.index('DelCn2')
            self.ui.mcmbBox2DX.setCurrentIndex(iX)
            self.ui.mcmbBox2DY.setCurrentIndex(iY)
        except ValueError:
            pass
        try:
            iX = vars.index('Hyperscore')
            iY = vars.index('DeltaCn2')
            self.ui.mcmbBox2DX.setCurrentIndex(iX)
            self.ui.mcmbBox2DY.setCurrentIndex(iY)
        except ValueError:
            pass
        try:
            iX = vars.index('Score')
            iY = vars.index('DeltaFwdRev')
            self.ui.mcmbBox2DX.setCurrentIndex(iX)
            self.ui.mcmbBox2DY.setCurrentIndex(iY)
        except ValueError:
            pass
        self.ui.mstkWidgEM.setCurrentIndex(0)
        self.ui.mcmbBoxDim.setCurrentIndex(0)

    def GetInitParameters1D(self):
        self.pT = 1 - self.pF
        Pk = Npy.array([self.pF, self.pT])
        M = Npy.array([self.muXF, self.muXT])
        V1 = self.sigXF
        V2 = self.sigXT
        V = Npy.array([V1,V2])
        return Pk, M, V, self.Tol, self.MaxIter, self.X

    def GetInitParameters2D(self):
        self.pT = 1 - self.pF
        Pk = Npy.array([self.pF, self.pT])
        M = Npy.array([[self.muXF, self.muXT], [self.muYF, self.muYT]])
        V1 = Npy.array([[self.sigXF**2, self.RhoF*self.sigXF*self.sigYF], \
                        [self.RhoF*self.sigXF*self.sigYF, self.sigYF**2]])
        V2 = Npy.array([[self.sigXT**2, self.RhoT*self.sigXT*self.sigYT], \
                        [self.RhoT*self.sigXT*self.sigYT, self.sigYT**2]])
        V = Npy.array([V1,V2])
        return Pk, M, V, self.Tol, self.MaxIter, self.X, self.Y

    def GetInitParameters3D(self):
        self.pT = 1 - self.pF
        Pk = Npy.array([self.pF, self.pT])
        M = Npy.array([[self.muXF, self.muXT], [self.muYF, self.muYT], [self.muZF, self.muZT]])
        V1 = Npy.array([[0.11, 0.01, 0.02], [0.03, 0.13, 0.01], [0.01, 0.03, 0.12]])
        V2 = Npy.array([[0.14, 0.01, 0.02], [0.03, 0.13, 0.01], [0.01, 0.03, 0.12]])
        V = Npy.array([V1,V2])
        return Pk, M, V, self.Tol, self.MaxIter

    def GetEMmodelDimension(self):
        if (self.ui.mstkWidgEM.currentIndex() == 0):
            return 1
        if (self.ui.mstkWidgEM.currentIndex() == 1):
            return 2
        if (self.ui.mstkWidgEM.currentIndex() == 2):
            return 3




