# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Research\Python\fdr_mix_model\src\epicUIelements\dlgHistogramPlotOptions.ui'
#
# Created: Wed Oct 15 17:22:08 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgHistogramPlotOptions(object):
    def setupUi(self, dlgHistogramPlotOptions):
        dlgHistogramPlotOptions.setObjectName("dlgHistogramPlotOptions")
        dlgHistogramPlotOptions.resize(315, 280)
        self.buttonBox = QtGui.QDialogButtonBox(dlgHistogramPlotOptions)
        self.buttonBox.setGeometry(QtCore.QRect(70, 240, 231, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.line = QtGui.QFrame(dlgHistogramPlotOptions)
        self.line.setGeometry(QtCore.QRect(10, 30, 291, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_8 = QtGui.QLabel(dlgHistogramPlotOptions)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 301, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.mrBtnXCorr = QtGui.QRadioButton(dlgHistogramPlotOptions)
        self.mrBtnXCorr.setGeometry(QtCore.QRect(20, 50, 83, 18))
        self.mrBtnXCorr.setChecked(True)
        self.mrBtnXCorr.setObjectName("mrBtnXCorr")
        self.mrBtnDelCn2 = QtGui.QRadioButton(dlgHistogramPlotOptions)
        self.mrBtnDelCn2.setGeometry(QtCore.QRect(20, 80, 83, 18))
        self.mrBtnDelCn2.setObjectName("mrBtnDelCn2")
        self.mrBtnXCorrN = QtGui.QRadioButton(dlgHistogramPlotOptions)
        self.mrBtnXCorrN.setGeometry(QtCore.QRect(20, 140, 121, 18))
        self.mrBtnXCorrN.setObjectName("mrBtnXCorrN")
        self.mrBtnDelCn2N = QtGui.QRadioButton(dlgHistogramPlotOptions)
        self.mrBtnDelCn2N.setGeometry(QtCore.QRect(20, 170, 121, 18))
        self.mrBtnDelCn2N.setObjectName("mrBtnDelCn2N")
        self.label_7 = QtGui.QLabel(dlgHistogramPlotOptions)
        self.label_7.setGeometry(QtCore.QRect(190, 90, 82, 20))
        self.label_7.setObjectName("label_7")
        self.label_9 = QtGui.QLabel(dlgHistogramPlotOptions)
        self.label_9.setGeometry(QtCore.QRect(190, 170, 82, 20))
        self.label_9.setObjectName("label_9")
        self.mlEditBins = QtGui.QLineEdit(dlgHistogramPlotOptions)
        self.mlEditBins.setGeometry(QtCore.QRect(190, 190, 110, 20))
        self.mlEditBins.setObjectName("mlEditBins")
        self.mtoolBtnColor = ColorButton(dlgHistogramPlotOptions)
        self.mtoolBtnColor.setEnabled(True)
        self.mtoolBtnColor.setGeometry(QtCore.QRect(190, 110, 111, 21))
        self.mtoolBtnColor.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mtoolBtnColor.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.mtoolBtnColor.setObjectName("mtoolBtnColor")
        self.line_2 = QtGui.QFrame(dlgHistogramPlotOptions)
        self.line_2.setGeometry(QtCore.QRect(10, 220, 291, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.mrBtnSp = QtGui.QRadioButton(dlgHistogramPlotOptions)
        self.mrBtnSp.setGeometry(QtCore.QRect(20, 110, 83, 18))
        self.mrBtnSp.setObjectName("mrBtnSp")
        self.mrBtnSpN = QtGui.QRadioButton(dlgHistogramPlotOptions)
        self.mrBtnSpN.setGeometry(QtCore.QRect(20, 200, 101, 18))
        self.mrBtnSpN.setObjectName("mrBtnSpN")

        self.retranslateUi(dlgHistogramPlotOptions)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dlgHistogramPlotOptions.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dlgHistogramPlotOptions.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgHistogramPlotOptions)

    def retranslateUi(self, dlgHistogramPlotOptions):
        dlgHistogramPlotOptions.setWindowTitle(QtGui.QApplication.translate("dlgHistogramPlotOptions", "Histograms", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "Plot Histograms:", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnXCorr.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "XCorr", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnDelCn2.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "DelCn2", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnXCorrN.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "XCorr (normalized)", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnDelCn2N.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "DelCn2 (normalized)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "Marker Color:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "Number of Bins:", None, QtGui.QApplication.UnicodeUTF8))
        self.mlEditBins.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "100", None, QtGui.QApplication.UnicodeUTF8))
        self.mtoolBtnColor.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "Select Color...", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnSp.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "Sp", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnSpN.setText(QtGui.QApplication.translate("dlgHistogramPlotOptions", "Sp (normalized)", None, QtGui.QApplication.UnicodeUTF8))

from colorbutton import ColorButton
