from PyQt4 import QtCore, QtGui
from epicUIelements.ui_dlgAbout import Ui_mdlgAbout

class clsAboutEpic(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_mdlgAbout()
        self.ui.setupUi(self)
        icon = QtGui.QIcon(":/epic.png")
        self.setWindowIcon(icon)

        image = QtGui.QImage(":/logo2.png")
        #imageS = image.scaled(self.ui.mlabelLogo.width(), self.ui.mlabelLogo.height())
        self.ui.mlabelLogo.setPixmap(QtGui.QPixmap.fromImage(image))
        self.ui.mlabelLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.mlabelAbout.setText("<p><b>epic v0.3</b> ( <u>E</u>stimating <u>P</u>eptide <u>I</u>dentification <u>C</u>onfidence)</p>"
                "Developed in Python and Qt by Ashoka Polpitiya  for the US Department of Energy.<br>PNNL, Richland, WA, USA.<br>"
                "Copyright 2008, Battelle Memorial Institute.  All Rights Reserved.<br>"
                "Please keep in mind that the entire effort is very much a"
                " work in progress."
                "<p><u>Acknowledgements:</u><br>"
                "Daniel Lopez-Ferrer<br>Navdeep Jaitly<br>Brian Clowers")