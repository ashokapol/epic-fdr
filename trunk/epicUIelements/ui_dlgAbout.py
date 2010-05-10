# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Ashoka\EclipseProjects\fdr_mix_model\src\epicUIelements\dlgAbout.ui'
#
# Created: Sun Jun 08 00:38:02 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_mdlgAbout(object):
    def setupUi(self, mdlgAbout):
        mdlgAbout.setObjectName("mdlgAbout")
        mdlgAbout.resize(QtCore.QSize(QtCore.QRect(0,0,476,326).size()).expandedTo(mdlgAbout.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mdlgAbout.sizePolicy().hasHeightForWidth())
        mdlgAbout.setSizePolicy(sizePolicy)

        self.hboxlayout = QtGui.QHBoxLayout(mdlgAbout)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")

        self.mlabelLogo = QtGui.QLabel(mdlgAbout)
        self.mlabelLogo.setObjectName("mlabelLogo")
        self.vboxlayout.addWidget(self.mlabelLogo)

        self.mlabelAbout = QtGui.QLabel(mdlgAbout)
        self.mlabelAbout.setObjectName("mlabelAbout")
        self.vboxlayout.addWidget(self.mlabelAbout)

        self.buttonBox = QtGui.QDialogButtonBox(mdlgAbout)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.retranslateUi(mdlgAbout)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),mdlgAbout.accept)
        QtCore.QMetaObject.connectSlotsByName(mdlgAbout)

    def retranslateUi(self, mdlgAbout):
        mdlgAbout.setWindowTitle(QtGui.QApplication.translate("mdlgAbout", "About epic", None, QtGui.QApplication.UnicodeUTF8))
        self.mlabelLogo.setText(QtGui.QApplication.translate("mdlgAbout", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.mlabelAbout.setText(QtGui.QApplication.translate("mdlgAbout", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

