#!/usr/bin/env python
from PyQt4 import QtGui
import csv
import os
from matplotlib.mlab import load
import numpy as Npy

mdictFileFormats = {'.csv':',', '.txt':'\t', '.ssv':';'}

def read_CSV_org(self, filename):
    dirname, fname = os.path.split(str(filename))
    name, ext = os.path.splitext(fname)
    delim = mdictFileFormats[ext]
    f = open(filename, "rb")
    reader = csv.reader(f, delimiter=delim)
    DataArray = []
    try:
        reader.next() # skip header
        for row in reader:
            DataArray.append(row)
        f.close()
        return DataArray
    except (csv.Error, StopIteration), e:
        QtGui.QMessageBox.warning(self, "epic - Load Error",
                        "Failed to load %s: %s" % (filename, e))

def read_CSV(self, filename):
    dirname, fname = os.path.split(str(filename))
    name, ext = os.path.splitext(fname)
    if name.find("_DelCn2") > -1:
        name = name.split("_DelCn2")
        name = name[0]
    delim = mdictFileFormats[ext]
    f = open(filename, "rb")
    reader = csv.reader(f, delimiter=delim)
    DataArray = []
    try:
        reader.next() # skip header
        for row in reader:
            row = [name] + row
            DataArray.append(row)
        f.close()
        return DataArray
    except (csv.Error, StopIteration), e:
        QtGui.QMessageBox.warning(self, "epic - Load Error",
                        "Failed to load %s: %s" % (filename, e))

def read_CSV_mlab(self, filename):
    dirname, fname = os.path.split(str(filename))
    name, ext = os.path.splitext(fname)
    delim = mdictFileFormats[ext]
    DataArray = []
    try:
        DataArray = load(filename, delimiter=delim, skiprows=1, dtype=str)
        return DataArray.tolist()
    except:
        return []

def read_CSV_header(self, filename):
    dirname, fname = os.path.split(str(filename))
    name, ext = os.path.splitext(fname)
    delim = mdictFileFormats[ext]
    f = open(filename, "rb")
    reader = csv.reader(f, delimiter=delim)
    try:
        header = reader.next()
        if len(header) < 2:
            header = None
            raise Exception('Empty header. Possible extra line at top.')
    except (csv.Error, StopIteration), e:
        QtGui.QMessageBox.warning(self, "epic - Load Error",
                        "Failed to load %s: %s" % (filename, e))
    except Exception, inst:
        QtGui.QMessageBox.warning(self, "epic - Load Error", \
                                          " Check your file again.\nError: %s" % inst)
    else:
        header = [header[i].replace(" ", "") for i in xrange(len(header))]
    finally:
        f.close()
        header1 = ["DatasetName"] + header
        return header1

def read_CSV_header_org(self, filename):
    dirname, fname = os.path.split(str(filename))
    name, ext = os.path.splitext(fname)
    delim = mdictFileFormats[ext]
    f = open(filename, "rb")
    reader = csv.reader(f, delimiter=delim)
    try:
        header = [reader.next()]
        if len(header[0]) < 2:
            header = None
            raise Exception('Empty header. Possible extra line at top.')
    except (csv.Error, StopIteration), e:
        QtGui.QMessageBox.warning(self, "epic - Load Error",
                        "Failed to load %s: %s" % (filename, e))
    except Exception, inst:
        QtGui.QMessageBox.warning(self, "epic - Load Error", \
                                          " Check your file again.\nError: %s" % inst)
    else:
        header = header[0]
        header = [header[i].replace(" ", "") for i in xrange(len(header))]
    finally:
        f.close()
        return header

def filesCompatible(self, marrFiles):
    header = read_CSV_header(self, marrFiles[0])
    if header is not None:
        for fname in marrFiles:
            header_new = read_CSV_header(self, fname)
            if header != header_new:
                return False
        return True
    else:
        return False

def readMultipleCSVfiles(self, marrFiles):
    Data = []
    header = read_CSV_header(self, marrFiles[0])
    if header is not None:
        for fname in marrFiles:
            currData = read_CSV(self, fname)
            Data.extend(currData)
        return header, Data
    else:
        return [], []



