# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Ashoka\EclipseProjects\fdr_mix_model\src\epicUIelements\dlgNormalize.ui'
#
# Created: Sun Oct 26 21:48:46 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_mdlgNormalize(object):
    def setupUi(self, mdlgNormalize):
        mdlgNormalize.setObjectName("mdlgNormalize")
        mdlgNormalize.resize(408, 564)
        self.buttonBox = QtGui.QDialogButtonBox(mdlgNormalize)
        self.buttonBox.setGeometry(QtCore.QRect(140, 520, 241, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.line = QtGui.QFrame(mdlgNormalize)
        self.line.setGeometry(QtCore.QRect(10, 30, 381, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_8 = QtGui.QLabel(mdlgNormalize)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 301, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.line_2 = QtGui.QFrame(mdlgNormalize)
        self.line_2.setGeometry(QtCore.QRect(10, 500, 381, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.groupBox = QtGui.QGroupBox(mdlgNormalize)
        self.groupBox.setGeometry(QtCore.QRect(40, 105, 351, 177))
        self.groupBox.setObjectName("groupBox")
        self.mchkBoxSp = QtGui.QCheckBox(self.groupBox)
        self.mchkBoxSp.setGeometry(QtCore.QRect(20, 152, 201, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mchkBoxSp.setFont(font)
        self.mchkBoxSp.setChecked(True)
        self.mchkBoxSp.setObjectName("mchkBoxSp")
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(40, 30, 301, 91))
        self.label_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setMargin(3)
        self.label_4.setObjectName("label_4")
        self.mchkBoxDelCn2 = QtGui.QCheckBox(self.groupBox)
        self.mchkBoxDelCn2.setGeometry(QtCore.QRect(20, 128, 241, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mchkBoxDelCn2.setFont(font)
        self.mchkBoxDelCn2.setChecked(True)
        self.mchkBoxDelCn2.setObjectName("mchkBoxDelCn2")
        self.mchkBoxXCorr = QtGui.QCheckBox(self.groupBox)
        self.mchkBoxXCorr.setGeometry(QtCore.QRect(20, 10, 321, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mchkBoxXCorr.setFont(font)
        self.mchkBoxXCorr.setCheckable(True)
        self.mchkBoxXCorr.setChecked(True)
        self.mchkBoxXCorr.setObjectName("mchkBoxXCorr")
        self.groupBox_2 = QtGui.QGroupBox(mdlgNormalize)
        self.groupBox_2.setGeometry(QtCore.QRect(40, 320, 351, 70))
        self.groupBox_2.setObjectName("groupBox_2")
        self.mchkBoxHyperS = QtGui.QCheckBox(self.groupBox_2)
        self.mchkBoxHyperS.setGeometry(QtCore.QRect(20, 10, 321, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mchkBoxHyperS.setFont(font)
        self.mchkBoxHyperS.setCheckable(True)
        self.mchkBoxHyperS.setChecked(True)
        self.mchkBoxHyperS.setObjectName("mchkBoxHyperS")
        self.mchkBoxDeltaCn2 = QtGui.QCheckBox(self.groupBox_2)
        self.mchkBoxDeltaCn2.setGeometry(QtCore.QRect(20, 40, 311, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mchkBoxDeltaCn2.setFont(font)
        self.mchkBoxDeltaCn2.setChecked(True)
        self.mchkBoxDeltaCn2.setObjectName("mchkBoxDeltaCn2")
        self.mrBtnSequest = QtGui.QRadioButton(mdlgNormalize)
        self.mrBtnSequest.setGeometry(QtCore.QRect(20, 80, 201, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mrBtnSequest.setFont(font)
        self.mrBtnSequest.setChecked(True)
        self.mrBtnSequest.setObjectName("mrBtnSequest")
        self.mrBtnXTandem = QtGui.QRadioButton(mdlgNormalize)
        self.mrBtnXTandem.setEnabled(True)
        self.mrBtnXTandem.setGeometry(QtCore.QRect(20, 293, 211, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mrBtnXTandem.setFont(font)
        self.mrBtnXTandem.setObjectName("mrBtnXTandem")
        self.mrBtnSkip = QtGui.QRadioButton(mdlgNormalize)
        self.mrBtnSkip.setGeometry(QtCore.QRect(20, 50, 161, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mrBtnSkip.setFont(font)
        self.mrBtnSkip.setObjectName("mrBtnSkip")
        self.mrBtnSpectrumMill = QtGui.QRadioButton(mdlgNormalize)
        self.mrBtnSpectrumMill.setEnabled(True)
        self.mrBtnSpectrumMill.setGeometry(QtCore.QRect(20, 400, 211, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mrBtnSpectrumMill.setFont(font)
        self.mrBtnSpectrumMill.setObjectName("mrBtnSpectrumMill")
        self.groupBox_3 = QtGui.QGroupBox(mdlgNormalize)
        self.groupBox_3.setGeometry(QtCore.QRect(40, 426, 351, 70))
        self.groupBox_3.setObjectName("groupBox_3")
        self.mchkBoxSMScore = QtGui.QCheckBox(self.groupBox_3)
        self.mchkBoxSMScore.setGeometry(QtCore.QRect(20, 10, 321, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mchkBoxSMScore.setFont(font)
        self.mchkBoxSMScore.setCheckable(True)
        self.mchkBoxSMScore.setChecked(True)
        self.mchkBoxSMScore.setObjectName("mchkBoxSMScore")
        self.mchkBoxSMDelta = QtGui.QCheckBox(self.groupBox_3)
        self.mchkBoxSMDelta.setGeometry(QtCore.QRect(20, 40, 311, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mchkBoxSMDelta.setFont(font)
        self.mchkBoxSMDelta.setChecked(True)
        self.mchkBoxSMDelta.setObjectName("mchkBoxSMDelta")

        self.retranslateUi(mdlgNormalize)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), mdlgNormalize.reject)
        QtCore.QMetaObject.connectSlotsByName(mdlgNormalize)

    def retranslateUi(self, mdlgNormalize):
        mdlgNormalize.setWindowTitle(QtGui.QApplication.translate("mdlgNormalize", "Normalizing Data", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("mdlgNormalize", "Normalize Data:", None, QtGui.QApplication.UnicodeUTF8))
        self.mchkBoxSp.setText(QtGui.QApplication.translate("mdlgNormalize", "Z : Normalized Sp = ln(Sp)/10", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("mdlgNormalize", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" font-weight:600;\">Peptide Length</span> is calculated by first trimming the leading </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">and trailing residues and then removing all characters that </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">do not correspond to an amino acid.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Ex: <span style=\" font-weight:600;\">R.IYEVSQ*LAK.A </span>will become <span style=\" font-weight:600;\">IYEVSQLAK </span>and </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">the length will be <span style=\" font-weight:600;\">9.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; font-weight:600;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.mchkBoxDelCn2.setText(QtGui.QApplication.translate("mdlgNormalize", "Y : Normalized DelCn2 = √(DelCn2)", None, QtGui.QApplication.UnicodeUTF8))
        self.mchkBoxXCorr.setText(QtGui.QApplication.translate("mdlgNormalize", "X : Normalized XCorr = ln(XCorr)/ln(Peptide Length)", None, QtGui.QApplication.UnicodeUTF8))
        self.mchkBoxHyperS.setText(QtGui.QApplication.translate("mdlgNormalize", "X : Normalized Hyperscore = ln(Hyperscore)", None, QtGui.QApplication.UnicodeUTF8))
        self.mchkBoxDeltaCn2.setText(QtGui.QApplication.translate("mdlgNormalize", "Y : Normalized DeltaCn2 = DeltaCn2 (no change)", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnSequest.setText(QtGui.QApplication.translate("mdlgNormalize", "Normalize Sequest Scores", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnXTandem.setText(QtGui.QApplication.translate("mdlgNormalize", "Normalize X!Tandem Scores", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnSkip.setText(QtGui.QApplication.translate("mdlgNormalize", "Do Not Alter Data", None, QtGui.QApplication.UnicodeUTF8))
        self.mrBtnSpectrumMill.setText(QtGui.QApplication.translate("mdlgNormalize", "Normalize Spectrum Mill Scores", None, QtGui.QApplication.UnicodeUTF8))
        self.mchkBoxSMScore.setText(QtGui.QApplication.translate("mdlgNormalize", "X : Normalized Score = √(Score)", None, QtGui.QApplication.UnicodeUTF8))
        self.mchkBoxSMDelta.setText(QtGui.QApplication.translate("mdlgNormalize", "Y : Normalized ΔFwdRev = √|ΔFwdRev|", None, QtGui.QApplication.UnicodeUTF8))

