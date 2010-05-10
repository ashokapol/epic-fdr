#!/usr/bin/env python
import sys
from PyQt4 import QtCore, QtGui
#import supportClasses.ClassificationEM as EM
import numpy as Npy
import math as Math
from supportClasses.fileIOroutines import read_CSV, read_CSV_header

mdictFileFormats = {'.csv':',', '.txt':'\t', '.ssv':';'}

class clsThreadReadFiles(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.header = []
        self.Data = []
        self.mblSuccess = False
        self.marrFiles = None

    def Initialize(self, marrF):
        self.marrFiles = marrF

    def run(self):
        niter = 0
        currData = []
        self.header = read_CSV_header(self, self.marrFiles[0])
        if self.header is not None:
            for fname in self.marrFiles:
                niter = niter + 1
                currData = read_CSV(self, fname)
                if len(currData)>0:
                    self.mblSuccess = True
                    self.Data.extend(currData)
                    self.emit(QtCore.SIGNAL("progress(int)"), niter)
        self.emit(QtCore.SIGNAL("finished(bool)"), self.mblSuccess)

    def GetResults(self):
        return self.header, self.Data

    def stop(self):
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()


    def isStopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()


