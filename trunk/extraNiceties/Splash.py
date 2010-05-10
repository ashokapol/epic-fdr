#!/usr/bin/env python
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QPixmap, QSplashScreen, QColor
import qrc_epicResources

class SplashScreen(QSplashScreen):
	"""
	Class implementing a splashscreen for eric4.
	"""
	def __init__(self):
		"""
		Constructor
		"""
		ericPic = QPixmap(":/logo2.png")
		self.labelAlignment = \
			Qt.Alignment(Qt.AlignBottom | Qt.AlignRight | Qt.AlignAbsolute)
		QSplashScreen.__init__(self, ericPic)
		self.show()
		QApplication.flush()

	def showMessage(self, msg):
		"""
		Public method to show a message in the bottom part of the splashscreen.

		@param msg message to be shown (string or QString)
		"""
		QSplashScreen.showMessage(self, msg, self.labelAlignment, QColor(Qt.black))
		QApplication.processEvents()

	def clearMessage(self):
		"""
		Public method to clear the message shown.
		"""
		QSplashScreen.clearMessage(self)
		QApplication.processEvents()
