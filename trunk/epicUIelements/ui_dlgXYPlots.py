# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Ashoka\EclipseProjects\fdr_mix_model\src\epicUIelements\dlgXYPlots.ui'
#
# Created: Wed Oct 15 23:14:06 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_mdlgXYPlot(object):
    def setupUi(self, mdlgXYPlot):
        mdlgXYPlot.setObjectName("mdlgXYPlot")
        mdlgXYPlot.resize(317, 200)
        self.buttonBox = QtGui.QDialogButtonBox(mdlgXYPlot)
        self.buttonBox.setGeometry(QtCore.QRect(80, 150, 221, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.line_2 = QtGui.QFrame(mdlgXYPlot)
        self.line_2.setGeometry(QtCore.QRect(10, 130, 291, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line = QtGui.QFrame(mdlgXYPlot)
        self.line.setGeometry(QtCore.QRect(10, 30, 291, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.mlblTitle = QtGui.QLabel(mdlgXYPlot)
        self.mlblTitle.setGeometry(QtCore.QRect(10, 10, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.mlblTitle.setFont(font)
        self.mlblTitle.setObjectName("mlblTitle")
        self.mrBtnXCorrDelCn2 = QtGui.QRadioButton(mdlgXYPlot)
        self.mrBtnXCorrDelCn2.setGeometry(QtCore.QRect(30, 50, 271, 18))
        self.mrBtnXCorrDelCn2.setChecked(True)
        self.mrBtnXCorrDelCn2.setObjectName("mrBtnXCorrDelCn2")
        self.mrBtnSpDelCn2 = QtGui.QRadioButton(mdlgXYPlot)
        self.mrBtnSpDelCn2.setGeometry(QtCore.QRect(30, 80, 271, 18))
        self.mrBtnSpDelCn2.setObjectName("mrBtnSpDelCn2")
        self.mrBtnXCorrSp = QtGui.QRadioButton(mdlgXYPlot)
        self.mrBtnXCorrSp.setGeometry(QtCore.QRect(30, 110, 271, 18))
        self.mrBtnXCorrSp.setObjectName("mrBtnXCorrSp")

        self.retranslateUi(mdlgXYPlot)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), mdlgXYPlot.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), mdlgXYPlot.reject)
        QtCore.QMetaObject.connectSlotsByName(mdlgXYPlot)

    def retranslateUi(self, mdlgXYPlot):
        mdlgXYPlot.setWindowTitle(QtGui.QApplication.translate("mdlgXYPlot", "XY Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.mlblTitle.setText(QtGui.QApplication.translate("mdlgXYPlot", "XY Plot:", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnXCorrDelCn2.setText(QtGui.QApplication.translate("mdlgXYPlot", "XCorr vs. DelCn2", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnSpDelCn2.setText(QtGui.QApplication.translate("mdlgXYPlot", "Sp vs. DelCn2", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnXCorrSp.setText(QtGui.QApplication.translate("mdlgXYPlot", "XCorr vs. Sp", None, QtGui.QApplication.UnicodeUTF8))

