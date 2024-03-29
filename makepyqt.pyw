#!/usr/bin/env python
# Copyright (c) 2007 Qtrac Ltd. All rights reserved.

import os
import platform
import stat
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

__version__ = "1.0.1"


class OptionsForm(QDialog):

    def __init__(self, parent=None):
        super(OptionsForm, self).__init__(parent)

        settings = QSettings()
        pyuic4Label = QLabel("pyuic4")
        self.pyuic4Label = QLabel(
                settings.value("pyuic4", QVariant(PYUIC4)).toString())
        self.pyuic4Label.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        pyuic4Button = QPushButton("py&uic4...")
        pyrcc4Label = QLabel("pyrcc4")
        self.pyrcc4Label = QLabel(
                settings.value("pyrcc4", QVariant(PYRCC4)).toString())
        self.pyrcc4Label.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        pyrcc4Button = QPushButton("pyr&cc4...")
        pylupdate4Label = QLabel("pylupdate4")
        self.pylupdate4Label = QLabel(
                settings.value("pylupdate4",
                        QVariant(PYLUPDATE4)).toString())
        self.pylupdate4Label.setFrameStyle(QFrame.StyledPanel|
                                           QFrame.Sunken)
        pylupdate4Button = QPushButton("py&lupdate4...")
        lreleaseLabel = QLabel("lrelease")
        self.lreleaseLabel = QLabel(
                settings.value("lrelease",
                        QVariant("lrelease")).toString())
        self.lreleaseLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        lreleaseButton = QPushButton("l&release...")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                     QDialogButtonBox.Cancel)

        layout = QGridLayout()
        layout.addWidget(pyuic4Label, 0, 0)
        layout.addWidget(self.pyuic4Label, 0, 1)
        layout.addWidget(pyuic4Button, 0, 2)
        layout.addWidget(pyrcc4Label, 1, 0)
        layout.addWidget(self.pyrcc4Label, 1, 1)
        layout.addWidget(pyrcc4Button, 1, 2)
        layout.addWidget(pylupdate4Label, 2, 0)
        layout.addWidget(self.pylupdate4Label, 2, 1)
        layout.addWidget(pylupdate4Button, 2, 2)
        layout.addWidget(lreleaseLabel, 3, 0)
        layout.addWidget(self.lreleaseLabel, 3, 1)
        layout.addWidget(lreleaseButton, 3, 2)
        layout.addWidget(buttonBox, 4, 0, 1, 3)
        self.setLayout(layout)

        self.connect(pyuic4Button, SIGNAL("clicked()"),
                lambda: self.setPath("pyuic4"))
        self.connect(pyrcc4Button, SIGNAL("clicked()"),
                lambda: self.setPath("pyrcc4"))
        self.connect(pylupdate4Button, SIGNAL("clicked()"),
                lambda: self.setPath("pylupdate4"))
        self.connect(lreleaseButton, SIGNAL("clicked()"),
                lambda: self.setPath("lrelease"))
        self.connect(buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(buttonBox, SIGNAL("rejected()"), self.reject)

        self.setWindowTitle("Make PyQt - Tool Paths")


    def accept(self):
        settings = QSettings()
        settings.setValue("pyuic4", QVariant(self.pyuic4Label.text()))
        settings.setValue("pyrcc4", QVariant(self.pyrcc4Label.text()))
        settings.setValue("pylupdate4",
                QVariant(self.pylupdate4Label.text()))
        settings.setValue("lrelease", QVariant(self.lreleaseLabel.text()))
        QDialog.accept(self)


    def setPath(self, tool):
        if tool == "pyuic4":
            label = self.pyuic4Label
        elif tool == "pyrcc4":
            label = self.pyrcc4Label
        elif tool == "pylupdate4":
            label = self.pylupdate4Label
        elif tool == "lrelease":
            label = self.lreleaseLabel
        path = QFileDialog.getOpenFileName(self,
                "Make PyQt - Set Tool Path", label.text())
        if path:
            label.setText(QDir.toNativeSeparators(path))


class Form(QMainWindow):

    def __init__(self):
        super(Form, self).__init__(None)

        pathLabel = QLabel("Path:")
        self.pathLabel = QLabel(sys.argv[1] \
                if len(sys.argv) > 1 and os.access(sys.argv[1], os.F_OK) \
                else os.getcwd())
        self.pathLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        self.pathLabel.setToolTip("The relative path; all actions will "
                "take place here,<br>and in this path's subdirectories "
                "if the Recurse checkbox is checked")
        self.pathButton = QPushButton("&Path...")
        self.pathButton.setToolTip(self.pathLabel.toolTip().replace(
                "The", "Sets the"))
        self.recurseCheckBox = QCheckBox("&Recurse")
        self.recurseCheckBox.setToolTip("Clean or build all the files "
                "in the path directory,<br>and all its subdirectories, "
                "as deep as they go.")
        self.transCheckBox = QCheckBox("&Translate")
        self.transCheckBox.setToolTip("Runs <b>pylupdate4</b> on all "
                "<tt>.py</tt> and <tt>.pyw</tt> files in conjunction "
                "with each <tt>.ts</tt> file.<br>Then runs "
                "<b>lrelease</b> on all <tt>.ts</tt> files to produce "
                "corresponding <tt>.qm</tt> files.<br>The "
                "<tt>.ts</tt> files must have been created initially by "
                "running <b>pylupdate4</b><br>directly on a <tt>.py</tt> "
                "or <tt>.pyw</tt> file using the <tt>-ts</tt> option.")
        self.debugCheckBox = QCheckBox("&Dry Run")
        self.debugCheckBox.setToolTip("Shows the actions that would "
                "take place but does not do them.")
        self.logBrowser = QTextBrowser()
        self.logBrowser.setLineWrapMode(QTextEdit.NoWrap)
        self.buttonBox = QDialogButtonBox()
        menu = QMenu(self)
        toolsAction = menu.addAction("&Tool paths...")
        aboutAction = menu.addAction("&About")
        moreButton = self.buttonBox.addButton("&More",
                QDialogButtonBox.ActionRole)
        moreButton.setMenu(menu)
        moreButton.setToolTip("Use <b>More-&gt;Tool paths</b> to set the "
                "paths to the tools if they are not found by default")
        self.buildButton = self.buttonBox.addButton("&Build",
                QDialogButtonBox.ActionRole)
        self.buildButton.setToolTip("Runs <b>pyuic4</b> on all "
                "<tt>.ui</tt> "
                "files and <b>pyrcc4</b> on all <tt>.qrc</tt> files "
                "that are out-of-date.<br>Also runs <b>pylupdate4</b> "
                "and <b>lrelease</b> if the Translate checkbox is "
                "checked.")
        self.cleanButton = self.buttonBox.addButton("&Clean",
                QDialogButtonBox.ActionRole)
        self.cleanButton.setToolTip("Deletes all <tt>.py</tt> files that "
                "were generated from <tt>.ui</tt> and <tt>.qrc</tt> "
                "files,<br>i.e., all files matching <tt>qrc_*.py</tt> "
                " and <tt>ui_*.py.")
        quitButton = self.buttonBox.addButton("&Quit",
                QDialogButtonBox.RejectRole)

        topLayout = QHBoxLayout()
        topLayout.addWidget(pathLabel)
        topLayout.addWidget(self.pathLabel, 1)
        topLayout.addWidget(self.pathButton)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.recurseCheckBox)
        bottomLayout.addWidget(self.transCheckBox)
        bottomLayout.addWidget(self.debugCheckBox)
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addWidget(self.logBrowser)
        layout.addLayout(bottomLayout)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.connect(aboutAction, SIGNAL("triggered()"), self.about)
        self.connect(toolsAction, SIGNAL("triggered()"), self.setToolPaths)
        self.connect(self.pathButton, SIGNAL("clicked()"), self.setPath)
        self.connect(self.buildButton, SIGNAL("clicked()"), self.build)
        self.connect(self.cleanButton, SIGNAL("clicked()"), self.clean)
        self.connect(quitButton, SIGNAL("clicked()"), self.close)

        self.setWindowTitle("Make PyQt")


    def about(self):
        QMessageBox.about(self, "About Make PyQt",
                """<b>Make PyQt</b> v %s
                <p>Copyright &copy; 2007 Qtrac Ltd. 
                All rights reserved.
                <p>This application can be used to build PyQt
                applications.
                It runs pyuic4, pyrcc4, pylupdate4, and lrelease as
                required, although pylupdate4 must be run directly to
                create the initial .ts files.
                <p>Python %s - Qt %s - PyQt %s on %s""" % (
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))


    def setPath(self):
        path = QFileDialog.getExistingDirectory(self,
                "Make PyQt - Set Path", self.pathLabel.text())
        if path:
            self.pathLabel.setText(QDir.toNativeSeparators(path))


    def setToolPaths(self):
        dlg = OptionsForm(self)
        dlg.exec_()


    def build(self):
        self.updateUi(False)
        self.logBrowser.clear()
        recurse = self.recurseCheckBox.isChecked()
        path = unicode(self.pathLabel.text())
        self._apply(recurse, self._build, path)
        if self.transCheckBox.isChecked():
            self._apply(recurse, self._translate, path)
        self.updateUi(True)


    def clean(self):
        self.updateUi(False)
        self.logBrowser.clear()
        recurse = self.recurseCheckBox.isChecked()
        path = unicode(self.pathLabel.text())
        self._apply(recurse, self._clean, path)
        self.updateUi(True)


    def updateUi(self, enable):
        for widget in (self.buildButton, self.cleanButton,
                self.pathButton, self.recurseCheckBox,
                self.transCheckBox, self.debugCheckBox):
            widget.setEnabled(enable)
        if not enable:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        else:
            QApplication.restoreOverrideCursor()
            self.buildButton.setFocus()


    def _apply(self, recurse, function, path):
        if not recurse:
            function(path)
        else:
            for root, dirs, files in os.walk(path):
                for dir in sorted(dirs):
                    function(os.path.join(root, dir))


    def _build(self, path):
        settings = QSettings()
        pyuic4 = unicode(settings.value("pyuic4",
                                        QVariant(PYUIC4)).toString())
        pyrcc4 = unicode(settings.value("pyrcc4",
                                        QVariant(PYRCC4)).toString())
        prefix = unicode(self.pathLabel.text())
        if not prefix.endswith(os.sep):
            prefix += os.sep
        failed = 0
        process = QProcess()
        for name in os.listdir(path):
            source = os.path.join(path, name)
            target = None
            if source.endswith(".ui"):
                target = os.path.join(path,
                                    "ui_" + name.replace(".ui", ".py"))
                command = pyuic4
            elif source.endswith(".qrc"):
                target = os.path.join(path,
                                    "qrc_" + name.replace(".qrc", ".py"))
                command = pyrcc4
            if target is not None:
                if not os.access(target, os.F_OK) or (
                   os.stat(source)[stat.ST_MTIME] > \
                   os.stat(target)[stat.ST_MTIME]):
                    args = ["-o", target, source]
                    msg = "converted <font color=darkblue>" + source + \
                          "</font> to <font color=blue>" + target + \
                          "</font>"
                    if self.debugCheckBox.isChecked():
                        msg = "<font color=green># " + msg + "</font>"
                    else:
                        process.start(command, args)
                        if not process.waitForFinished(2 * 60 * 1000):
                            msg = "<font color=red>FAILED: %s</font>" % \
                                command
                            failed += 1
                    self.logBrowser.append(msg.replace(prefix, ""))
                else:
                    self.logBrowser.append("<font color=green>"
                            "# %s is up-to-date</font>" % \
                            source.replace(prefix, ""))
                QApplication.processEvents()
        if failed:
            QMessageBox.information(self, "Make PyQt - Failures",
                    "Try manually setting the paths to the tools "
                    "using <b>More-&gt;Tool paths</b>")


    def _clean(self, path):
        prefix = unicode(self.pathLabel.text())
        if not prefix.endswith(os.sep):
            prefix += os.sep
        deletelist = []
        for name in os.listdir(path):
            target = os.path.join(path, name)
            source = None
            if target.endswith(".py") or target.endswith(".pyc") or \
               target.endswith(".pyo"):
                if name.startswith("ui_") and not name[-1] in "oc":
                    source = os.path.join(path, name[3:-3] + ".ui")
                elif name.startswith("qrc_"):
                    if target[-1] in "oc":
                        source = os.path.join(path, name[4:-4] + ".qrc")
                    else:
                        source = os.path.join(path, name[4:-3] + ".qrc")
                elif target[-1] in "oc":
                    source = target[:-1]
                if source is not None:
                    if os.access(source, os.F_OK):
                        if self.debugCheckBox.isChecked():
                            self.logBrowser.append("<font color=green>"
                                    "# delete %s</font>" % \
                                    target.replace(prefix, ""))
                        else:
                            deletelist.append(target)
                    else:
                        self.logBrowser.append("<font color=darkred>"
                                "will not remove "
                                "'%s' since `%s' not found</font>" % (
                                target.replace(prefix, ""),
                                source.replace(prefix, "")))
        if not self.debugCheckBox.isChecked():
            for target in deletelist:
                self.logBrowser.append("deleted "
                        "<font color=red>%s</font>" % \
                        target.replace(prefix, ""))
                os.remove(target)
                QApplication.processEvents()


    def _translate(self, path):
        prefix = unicode(self.pathLabel.text())
        if not prefix.endswith(os.sep):
            prefix += os.sep
        files = []
        tsfiles = []
        for name in os.listdir(path):
            if name.endswith((".py", ".pyw")):
                files.append(os.path.join(path, name))
            elif name.endswith(".ts"):
                tsfiles.append(os.path.join(path, name))
        if not tsfiles:
            return
        settings = QSettings()
        pylupdate4 = unicode(settings.value("pylupdate4",
                             QVariant(PYLUPDATE4)).toString())
        lrelease = unicode(settings.value("lrelease",
                           QVariant(LRELEASE)).toString())
        process = QProcess()
        failed = 0
        for ts in tsfiles:
            qm = ts[:-3] + ".qm"
            command1 = pylupdate4
            args1 = files + ["-ts", ts]
            command2 = lrelease
            args2 = ["-silent", ts, "-qm", qm]
            msg = "updated <font color=blue>%s</font>" % \
                    ts.replace(prefix, "")
            if self.debugCheckBox.isChecked():
                msg = "<font color=green># %s</font>" % msg
            else:
                process.start(command1, args1)
                if not process.waitForFinished(2 * 60 * 1000):
                    msg = "<font color=red>FAILED: %s</font>" % command1
                    failed += 1
            self.logBrowser.append(msg)
            msg = "generated <font color=blue>%s</font>" % \
                    qm.replace(prefix, "")
            if self.debugCheckBox.isChecked():
                msg = "<font color=green># %s</font>" % msg
            else:
                process.start(command2, args2)
                if not process.waitForFinished(2 * 60 * 1000):
                    msg = "<font color=red>FAILED: %s</font>" % command2
                    failed += 1
            self.logBrowser.append(msg)
            QApplication.processEvents()
        if failed:
            QMessageBox.information(self, "Make PyQt - Failures",
                    "Try manually setting the paths to the tools "
                    "using <b>More-&gt;Tool paths</b>")


app = QApplication(sys.argv)
PATH = unicode(app.applicationDirPath())
PYUIC4 = os.path.join(PATH, "pyuic4")
PYRCC4 = os.path.join(PATH, "pyrcc4")
PYLUPDATE4 = os.path.join(PATH, "pylupdate4")
LRELEASE = "lrelease"
if platform.system() == "Windows":
    PYUIC4 = PYUIC4.replace("/", "\\") + ".bat"
    PYRCC4 = PYRCC4.replace("/", "\\") + ".exe"
    PYLUPDATE4 = PYLUPDATE4.replace("/", "\\") + ".exe"
app.setOrganizationName("Qtrac Ltd.")
app.setOrganizationDomain("qtrac.eu")
app.setApplicationName("Make PyQt")
form = Form()
form.show()
app.exec_()

# 1.0.1 Fixed bug reported by Brian Downing where paths that contained
#       spaces were not handled correctly.
