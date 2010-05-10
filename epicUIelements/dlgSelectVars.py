from PyQt4 import QtCore, QtGui
from epicUIelements.ui_dlgSelectVars import Ui_mdlgSelectVars
import qrc_epicResources

class clsSelectVars(QtGui.QDialog):
    def __init__(self, columns):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_mdlgSelectVars()
        self.ui.setupUi(self)
        icon = QtGui.QIcon(":/epic.png")
        self.setWindowIcon(icon)

        self.ui.mListViewCols.addItems(columns)
        self.ui.mListViewCols.SelectionMode = 1
        #self.TestFill(columns)

        #color = QtGui.QColor("yellow")
        palette1 = self.ui.mLineEditX.palette()
        palette2 = self.ui.mLineEditPepSeq.palette()
        #palette3 = self.ui.mLineEditY.palette()
        palette1.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(255, 250, 205, 127))
        palette2.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(255, 250, 205, 127))
        #palette3.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(255, 250, 205, 127))


        self.connect(self.ui.mBtnPepSeq, QtCore.SIGNAL("clicked()"), self.SelectPepSeq)
        self.connect(self.ui.mBtnY, QtCore.SIGNAL("clicked()"), self.SelectY)
        self.connect(self.ui.mBtnX, QtCore.SIGNAL("clicked()"), self.SelectX)
        self.connect(self.ui.mBtnZ, QtCore.SIGNAL("clicked()"), self.SelectZ)
        self.connect(self.ui.mBtnCS, QtCore.SIGNAL("clicked()"), self.SelectCS)
        self.connect(self.ui.mBtnTrypState, QtCore.SIGNAL("clicked()"), self.SelectTrSt)
        self.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.OK)

        self.mblX = False
        self.mblY = False
        self.mblZ = False
        self.mblCS = False
        self.mblTryptSt = False

        self.ui.mchkBoxCS1.setEnabled(False)
        self.ui.mchkBoxCS2.setEnabled(False)
        self.ui.mchkBoxCS3.setEnabled(False)
        self.ui.mchkBoxCSother.setEnabled(False)
        self.ui.mchkBoxFull.setEnabled(False)
        self.ui.mchkBoxNone.setEnabled(False)
        self.ui.mchkBoxPartial.setEnabled(False)

    def OK(self):
        if self.ui.mLineEditPepSeq.text().isEmpty() or self.ui.mLineEditX.text().isEmpty():
            #self.ui.mLineEditProt.text().isEmpty() or self.ui.mLineEditScanN.text().isEmpty() or \
            QtGui.QMessageBox.warning(self, "Empty Selections", "Not All required columns selected.")
        else:
            self.accept()

    def IsUsed(self, colName):
        if self.ui.mLineEditPepSeq.text() == colName or self.ui.mLineEditY.text() == colName or \
            self.ui.mLineEditCS.text() == colName  or self.ui.mLineEditX.text() == colName:
            return True
        else:
            return False

    def SelectPepSeq(self):
        selectedItem = self.ui.mListViewCols.currentItem()
        if selectedItem != None and not self.IsUsed(selectedItem.text()):
            self.ui.mLineEditPepSeq.setText(selectedItem.text())
            self.PepSeq = selectedItem.text()

    def SelectY(self):
        selectedItem = self.ui.mListViewCols.currentItem()
        if selectedItem != None and not self.IsUsed(selectedItem.text()):
            self.ui.mLineEditY.setText(selectedItem.text())
            self.Y = selectedItem.text()
            self.mblY = True

    def SelectX(self):
        selectedItem = self.ui.mListViewCols.currentItem()
        if selectedItem != None and not self.IsUsed(selectedItem.text()):
            self.ui.mLineEditX.setText(selectedItem.text())
            self.X = selectedItem.text()

    def SelectZ(self):
        selectedItem = self.ui.mListViewCols.currentItem()
        if selectedItem != None and not self.IsUsed(selectedItem.text()):
            self.ui.mLineEditZ.setText(selectedItem.text())
            self.Z = selectedItem.text()
            self.mblZ = True

    def SelectCS(self):
        selectedItem = self.ui.mListViewCols.currentItem()
        if selectedItem != None and not self.IsUsed(selectedItem.text()):
            self.ui.mLineEditCS.setText(selectedItem.text())
            self.CS = selectedItem.text()
            self.mblCS = True
            self.ui.mchkBoxCS1.setEnabled(True)
            self.ui.mchkBoxCS2.setEnabled(True)
            self.ui.mchkBoxCS3.setEnabled(True)
            self.ui.mchkBoxCSother.setEnabled(True)

    def SelectTrSt(self):
        selectedItem = self.ui.mListViewCols.currentItem()
        if selectedItem != None and not self.IsUsed(selectedItem.text()):
            self.ui.mLineEditTrypState.setText(selectedItem.text())
            self.TryptSt = selectedItem.text()
            self.mblTryptSt = True
            self.ui.mchkBoxFull.setEnabled(True)
            self.ui.mchkBoxNone.setEnabled(True)
            self.ui.mchkBoxPartial.setEnabled(True)

    def GetVars(self):
        h = [str(self.PepSeq), str(self.X)]
        if self.mblY:
            h.append(str(self.Y))
        else:
            h.append("NA")
        if self.mblZ:
            h.append(str(self.Z))
        else:
            h.append("NA")
        if self.mblCS:
            h.append(str(self.CS))
        else:
            h.append("NA")
        if self.mblTryptSt:
            h.append(str(self.TryptSt))
        else:
            h.append("NA")
        boolListData = [self.mblY, self.mblZ, self.mblCS, self.mblTryptSt]
        boolListCS = [self.mblCS and self.ui.mchkBoxCS1.isChecked(), self.mblCS and self.ui.mchkBoxCS2.isChecked(),\
                      self.mblCS and self.ui.mchkBoxCS3.isChecked(), self.mblCS and self.ui.mchkBoxCSother.isChecked()]
        boolListTryp = [self.mblTryptSt and self.ui.mchkBoxNone.isChecked(), self.mblTryptSt and self.ui.mchkBoxPartial.isChecked(),
                         self.mblTryptSt and self.ui.mchkBoxFull.isChecked()]
        """
        boolListCS = [mblCS1, mblCS2, mblCS3, mblCSrest]
        boolListTryp = [mblNone, mblPartial, mblFull]
        """
        return h, boolListData, boolListCS, boolListTryp



