#!/usr/bin/env python
import math as Math
from PyQt4 import QtGui
import numpy as Npy
#from scipy import optimize

aminoResidues = "ARNDCEQGHILKMFPSTWYVBZJX"

def NormalizeSEQ(Peptides, X, Y, Z):
    mblSuccess = True
    XN, YN, ZN = [], [], []

    strippedSeqList = [StripNonAminoChars(Peptides[i]) for i in range(0, len(Peptides))]
    seqLength = [len(strippedSeqList[i]) for i in range(0, len(strippedSeqList))]

    if len(X) > 0:
        try:
            XN = [Math.log(float(X[i]))/Math.log(seqLength[i]) for i in range(0, len(X))]
        except ZeroDivisionError:
            QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")
            mblSuccess = False
    if len(Y) > 0:
        try:
            YN = [Math.sqrt(float(Y[i])) for i in range(0, len(Y))]
        except ValueError:
            QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")
            mblSuccess = False
    if len(Z) > 0:
        try:
            ZN = [Math.log(float(Z[i]))/10 for i in range(0, len(Z))]
        except ValueError:
            QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")
            mblSuccess = False
    return XN, YN, ZN, mblSuccess

def NormalizeXTandem(Peptides, X, Y):
    mblSuccess = True
    XN, YN, ZN = [], [], []

    #strippedSeqList = [StripNonAminoChars(Peptides[i]) for i in range(0, len(Peptides))]
    #seqLength = [len(strippedSeqList[i]) for i in range(0, len(strippedSeqList))]

    if len(X) > 0:
        try:
            XN = [Math.log(float(X[i])) for i in range(0, len(X))]
            #XN = [Math.log(float(X[i]))/Math.log(seqLength[i]) for i in range(0, len(X))]
        except (TypeError, ValueError):
            QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")
            mblSuccess = False
    if len(Y) > 0:
        try:
            YN = [float(Y[i]) for i in range(0, len(Y))]
        except ValueError:
            QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")
            mblSuccess = False
    return XN, YN, [], mblSuccess

def NormalizeSpectrumMill(Peptides, X, Y):
    mblSuccess = True
    XN, YN, ZN = [], [], []

    #strippedSeqList = [StripNonAminoChars(Peptides[i]) for i in range(0, len(Peptides))]
    #seqLength = [len(strippedSeqList[i]) for i in range(0, len(strippedSeqList))]

    if len(X) > 0:
        try:
            XN = [Math.sqrt(float(X[i])) for i in range(0, len(X))]
            #XN = [Math.log(float(X[i]))/Math.log(seqLength[i]) for i in range(0, len(X))]
        except (TypeError, ValueError):
            QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")
            mblSuccess = False
    if len(Y) > 0:
        try:
            YN = [Math.sqrt(Math.fabs(float(Y[i]))) for i in range(0, len(Y))]
        except ValueError:
            QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")
            mblSuccess = False
    return XN, YN, [], mblSuccess

def NormalizeSkip(Peptides, X, Y, Z):
    mblSuccess = True
    XN, YN, ZN = [], [], []

    if len(X) > 0:
        try:
            XN = [float(X[i]) for i in range(0, len(X))]
        except ValueError:
            QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")
            mblSuccess = False
    if len(Y) > 0:
        try:
            YN = [float(Y[i]) for i in range(0, len(Y))]
        except ValueError:
            QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")
            mblSuccess = False
    if len(Z) > 0:
        try:
            ZN = [float(Z[i]) for i in range(0, len(Z))]
        except ValueError:
            QtGui.QMessageBox.warning(self, "epic - Error", "Failed to normalize")
            mblSuccess = False
    return XN, YN, ZN, mblSuccess

def StripNonAminoChars(str):
    strSplitted = str.split('.')
    if (len(strSplitted) == 3):
        str = strSplitted[1]
    else:
        str = strSplitted[0]
    return ''.join([c for c in str if ord(c) >= 65 and ord(c) <= 90])

def MixedLL2D_Org(x, Z):
    mux1, muy1, sigmax1, sigmay1, mux2, muy2, sigmax2, sigmay2, rho1, rho2, p = x

    OneMinusRho1Sq = 1 - rho1*rho1
    OneMinusRho2Sq = 1 - rho2*rho2
    z1 = (Z[:,0]-mux1)**2/(sigmax1*sigmax1)+(Z[:,1]-muy1)**2/(sigmay1*sigmay1) - 2*rho1 * (Z[:,0]-mux1) * (Z[:,1]-muy1)/(sigmax1 * sigmay1)
    z2 = (Z[:,0]-mux2)**2/(sigmax2*sigmax2)+(Z[:,1]-muy2)**2/(sigmay2*sigmay2) - 2*rho2 * (Z[:,0]-mux2) * (Z[:,1]-muy2)/(sigmax2 * sigmay2)
    first, second = -z1/(2*OneMinusRho1Sq), -z2/(2*OneMinusRho2Sq)
    first = Npy.array([p*Math.exp(first[i])/(2*Math.pi*sigmax1*sigmay1*Math.sqrt(OneMinusRho1Sq)) for i in range(0,len(first))])
    second = Npy.array([(1-p)*Math.exp(second[i])/(2*Math.pi*sigmax2*sigmay2*Math.sqrt(OneMinusRho2Sq)) for i in range(0,len(second))])
    sum2 = first + second
    sum2 = Npy.array([Math.log(sum2[i]) for i in range(0,len(sum2))])
    MixNormNegLL = -sum2.sum()
    return MixNormNegLL

def FitMixedDistributions_Org(self, X):
    x0 = [0.2, 0.2, .1, .1, .4, .6, .1, .1, 0, .5, 0.3]
    xopt = optimize.fmin(MixedLL2D_Org, x0, args=(X,))
    return xopt





