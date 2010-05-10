import numpy as Npy
from PyQt4 import QtGui, QtCore

from epicUIelements.ui_dlgEMvars import Ui_mdlgEMvars

class clsXYPlotOptions(QtGui.QDialog):
    def __init__(self, mblSp):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_mdlgEMvars()
        self.ui.setupUi(self)
        icon = QtGui.QIcon(":/epic.png")
        self.setWindowIcon(icon)

        if not mblSp:
            self.ui.mchkBoxSp.setEnabled(False)

        self.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.OK)

    def OK(self):
        mblnumChecked = self.ui.mchkBoxXC.isChecked() + self.ui.mchkBoxDCn.isChecked() + self.ui.mchkBoxSp.isChecked()
        if (mblnumChecked > 1):
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, "Fewer choices", "Check at least two variables to be normalized.")
            self.reject()

    def GetEMVars(self):
        return self.ui.mchkBoxXC.isChecked(), self.ui.mchkBoxDCn.isChecked(), self.ui.mchkBoxSp.isChecked()

