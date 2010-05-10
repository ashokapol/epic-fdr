# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Ashoka\EclipseProjects\fdr_mix_model\src\epicUIelements\dlgEMvars.ui'
#
# Created: Sat Oct 18 08:50:52 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_mdlgEMvars(object):
    def setupUi(self, mdlgEMvars):
        mdlgEMvars.setObjectName("mdlgEMvars")
        mdlgEMvars.resize(314, 296)
        self.buttonBox = QtGui.QDialogButtonBox(mdlgEMvars)
        self.buttonBox.setGeometry(QtCore.QRect(90, 250, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.line_2 = QtGui.QFrame(mdlgEMvars)
        self.line_2.setGeometry(QtCore.QRect(10, 230, 291, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line = QtGui.QFrame(mdlgEMvars)
        self.line.setGeometry(QtCore.QRect(10, 30, 291, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.mlblTitle = QtGui.QLabel(mdlgEMvars)
        self.mlblTitle.setGeometry(QtCore.QRect(10, 10, 241, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.mlblTitle.setFont(font)
        self.mlblTitle.setObjectName("mlblTitle")
        self.frame = QtGui.QFrame(mdlgEMvars)
        self.frame.setGeometry(QtCore.QRect(70, 70, 141, 121))
        self.frame.setFrameShape(QtGui.QFrame.WinPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.mchkBoxSp = QtGui.QCheckBox(self.frame)
        self.mchkBoxSp.setGeometry(QtCore.QRect(20, 90, 72, 18))
        self.mchkBoxSp.setObjectName("mchkBoxSp")
        self.mchkBoxXC = QtGui.QCheckBox(self.frame)
        self.mchkBoxXC.setGeometry(QtCore.QRect(20, 10, 72, 18))
        self.mchkBoxXC.setChecked(True)
        self.mchkBoxXC.setObjectName("mchkBoxXC")
        self.mchkBoxDCn = QtGui.QCheckBox(self.frame)
        self.mchkBoxDCn.setGeometry(QtCore.QRect(20, 50, 72, 18))
        self.mchkBoxDCn.setChecked(True)
        self.mchkBoxDCn.setObjectName("mchkBoxDCn")
        self.mrBtn2DEM = QtGui.QRadioButton(mdlgEMvars)
        self.mrBtn2DEM.setGeometry(QtCore.QRect(20, 50, 141, 18))
        self.mrBtn2DEM.setChecked(True)
        self.mrBtn2DEM.setObjectName("mrBtn2DEM")
        self.mrBtn3DEM = QtGui.QRadioButton(mdlgEMvars)
        self.mrBtn3DEM.setGeometry(QtCore.QRect(20, 210, 161, 18))
        self.mrBtn3DEM.setObjectName("mrBtn3DEM")

        self.retranslateUi(mdlgEMvars)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), mdlgEMvars.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), mdlgEMvars.reject)
        QtCore.QMetaObject.connectSlotsByName(mdlgEMvars)

    def retranslateUi(self, mdlgEMvars):
        mdlgEMvars.setWindowTitle(QtGui.QApplication.translate("mdlgEMvars", "Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.mlblTitle.setText(QtGui.QApplication.translate("mdlgEMvars", "Select Variables for Model Fitting:", None, QtGui.QApplication.UnicodeUTF8))
        self.mchkBoxSp.setText(QtGui.QApplication.translate("mdlgEMvars", "Sp", None, QtGui.QApplication.UnicodeUTF8))
        self.mchkBoxXC.setText(QtGui.QApplication.translate("mdlgEMvars", "XCorr", None, QtGui.QApplication.UnicodeUTF8))
        self.mchkBoxDCn.setText(QtGui.QApplication.translate("mdlgEMvars", "DelCn2", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtn2DEM.setText(QtGui.QApplication.translate("mdlgEMvars", "2 Dimensional Model", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtn3DEM.setText(QtGui.QApplication.translate("mdlgEMvars", "3 Dimensional Model", None, QtGui.QApplication.UnicodeUTF8))

