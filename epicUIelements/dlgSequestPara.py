from PyQt4 import QtCore, QtGui
from os.path import basename
from epicUIelements.ui_dlgSequestPara import Ui_mdlgSequestPara
import qrc_epicResources


class clsSelectSequestVars(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_mdlgSequestPara()
        self.ui.setupUi(self)
        icon = QtGui.QIcon(":/epic.png")
        self.setWindowIcon(icon)

        self.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.OK)

    def OK(self):
        try:
            tmp1 = float(self.ui.mlineEditDelCn2threh.text())
        except:
            QtGui.QMessageBox.warning(self, "Invalid entries", "Invalid entry detected. Check all entries again.")
        else:
            self.accept()

    def GetVars(self):
        boolListCS = [self.ui.mchkBoxCS1.isChecked(), self.ui.mchkBoxCS2.isChecked(), \
                                   self.ui.mchkBoxCS3.isChecked(), self.ui.mchkBoxCS4.isChecked(),
                                   self.ui.mchkBoxCS5.isChecked(), self.ui.mchkBoxCSother.isChecked()]
        boolListTryp = [self.ui.mchkBoxNone.isChecked(), self.ui.mchkBoxPartial.isChecked(), \
                                   self.ui.mchkBoxFull.isChecked()]
        mintMaxXC = int(self.ui.mspinBoxMaxXc.value())
        mfltDCcth = float(self.ui.mlineEditDelCn2threh.text())
        mblBypass = self.ui.mchkBoxByPass.isChecked()

        return boolListCS, boolListTryp, mintMaxXC, mfltDCcth, mblBypass

