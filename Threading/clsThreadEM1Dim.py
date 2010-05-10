#!/usr/bin/env python
import sys
from PyQt4 import QtCore, QtGui
#import supportClasses.ClassificationEM as EM
import numpy as Npy
import math as Math

class clsThreadEM1Dim(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.probs = None
        self.mu = None
        self.sigma = None
        self.liklihood = None
        self.Probabilities = None
        self.qvalues = None
        self.rank = None
        self.mblSuccess = False
        self.stopped = False
        self.mutex = QtCore.QMutex()
        self.completed = False
        self.niter = 0

    def Initialize(self, X, mintNumGaus, Pk, Mu, Sig, ltol, maxiter):
        self.Data = X
        self.nGauss = mintNumGaus
        self.Pk = Pk
        self.Mu = Mu
        self.Sig = Sig
        self.tol = ltol
        self.maxIter = maxiter


    def run(self):
        self.probs, self.mu, self.sigma, self.liklihood = self.PerformEM(self.Data, \
                                                        self.nGauss, self.Pk, self.Mu, \
                                                        self.Sig, self.tol, self.maxIter)
#        self.emit(QtCore.SIGNAL("progress(int)"), self.niter+1)
#        self.Probabilities = self.GetProbabilities(self.Data, self.probs, self.mu, self.sigma)
#        self.emit(QtCore.SIGNAL("progress(int)"), self.niter+2)
#        self.qvalues, self.rank = self.GetqValues(self.Probabilities)
        self.mblSuccess = True
        self.emit(QtCore.SIGNAL("finished(bool)"), self.mblSuccess)
        #self.stop()

    def GetResults(self):
        return self.probs, self.mu, self.sigma, self.liklihood#, self.Probabilities, self.qvalues, self.rank

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

    def whichmax(self, a_list):
        max_val, max_index = max((x, i) for i, x in enumerate(a_list))
        return max_index

    def Expectation(self, X, k, p, mu, Sig): # E-Step
        EPS = 0.00000001
        n = len(X)
        E = Npy.zeros((n, k))

        k1 = (2*Math.pi)**(0.5)

        for i in range(0, n):
            for j in range(0, k):
                dXM = X[i] - mu[j]
                gs = Math.exp(-0.5*dXM**2/(Sig[j])**2) / (k1*Sig[j])
                E[i, j] = p[j] * gs
            sumE = sum(E[i, :])
            if sumE != 0:
                E[i, :] = E[i, :] / sumE
        return E

    def Classification(self, X, E): # C-Step
        n, d = E.shape
        Class = Npy.zeros((n, d))
        maxColIdx = map(self.whichmax, E)
        for i in range(0, len(maxColIdx)):
            Class[i, maxColIdx[i]] = 1
        return Class


    def Maximization(self, X, Class): # M-Step
        k = len(Class[0])
        n = len(X)
        mu = Npy.zeros(k)
        Sig = Npy.zeros(k)

        colSumC = Npy.array([sum(Class[:, col]) for col in range(0, len(Class[0]))])
        p = colSumC/n
        XC = X*Class.transpose()
        XC = XC.transpose()
        colSumXC = Npy.array([sum(XC[:, col]) for col in range(0, len(XC[0]))])
        mu = colSumXC / colSumC

        for i in range(0, k):
            V = 0
            for j in range(0, n):
                dXM = X[j] - mu[i]
                V = V + Class[j, i]*dXM*dXM
            Sig[i] = Math.sqrt(V/colSumC[i])

        return p, mu, Sig

    def Likelihood(self, X, k, Sig, Class): # Compute Likelihood value.
        n = len(X)
        L = 0

        for i in range(0, k):
            Xk = X[Class[:, i]==1]
            nk = len(Xk)
            mu = sum(Xk) / nk
            L = L + nk*Npy.log(Sig[i]) + 0.5*sum((Xk-mu)**2) / Sig[i]**2
        return L

    def PerformEM(self, X, k, Pk, M, V, ltol, maxiter): # EM algorithm
        E = self.Expectation(X, k, Pk, M, V)
        Cl = self.Classification(X, E)
        Ln = self.Likelihood(X, k, V, Cl) # Initialize log likelihood
        Lo = 2*Ln
        self.niter = 0

        while ((abs(100*(Ln-Lo)/Lo)>ltol) and (self.niter<=maxiter)):
            #print niter
            self.emit(QtCore.SIGNAL("progress(int)"), self.niter)
            E = self.Expectation(X, k, Pk, M, V) # E-step
            Cl = self.Classification(X, E)
            Pk, M, V = self.Maximization(X, Cl)  # M-step
            Lo = Ln
            Ln = self.Likelihood(X, k, V, Cl)
            self.niter = self.niter + 1
            #print Lo
            #print Ln
        return Pk, M, V, Ln

    def GaussianDist1D(self, X, k, mu, Sig): # Gaussians
        EPS = 0.00000001
        n = len(X)
        E = Npy.zeros((n, k))

        k1 = (2*Math.pi)**(0.5)

        for i in range(0, n):
            for j in range(0, k):
                dXM = X[i] - mu[j]
                gs = Math.exp(-0.5*dXM**2/(Sig[j])**2) / (k1*Sig[j])
                E[i, j] = gs

        return E

    def GaussianDist1DSingle(self, X, mu, Sig): # Gaussians
        EPS = 0.00000001
        n = len(X)
        E = Npy.zeros(n)

        k1 = (2*Math.pi)**(0.5)

        for i in range(0, n):
            dXM = X[i] - mu
            gs = Math.exp(-0.5*dXM**2/(Sig)**2) / (k1*Sig)
            E[i] = gs

        return E

    def GetProbabilities1(self, X, Pk, M, Sig):
        muF = M[0]
        sigF = Sig[0]
        idx1 = (X<muF).nonzero()
        Dist = self.GaussianDist1DSingle(X, muF, sigF)
        Dist = Dist / sum(Dist)
        #if len(idx1)>0:
        #    Dist[idx1] = 0
        pvalue = Npy.array([sum(Dist[(Dist <= Dist[i]).nonzero()]) for i in xrange(len(Dist))])
        if len(idx1)>0:
            pvalue[idx1] = 1

        return pvalue

    def GetProbabilities(self, X, Pk, M, Sig):
        muF = M[0]
        sigF = Sig[0]
        idx1 = (X<muF).nonzero()
        Dist = self.GaussianDist1DSingle(X, muF, sigF)
        Dist = Dist / sum(Dist)
        pvalue = Npy.array([sum(Dist[(X >= X[i]).nonzero()]) for i in xrange(len(Dist))])

        return pvalue

    def GetProbabilitiesBayes(self, X, Pk, M, Sig):
        Dist = self.GaussianDist1D(X, 2, M, Sig)
        first = Pk[0]*Dist[:, 0]
        second = Pk[1]*Dist[:, 1]
        probabilities = first / (second + first)
        return probabilities

    def GetqValues(self, probs):
        Total = len(probs)
        sProbs = sorted(probs)
        rank = [sProbs.index(probs[i])+1 for i in xrange(len(probs))]
        #qVal = [min((Total-rank[i])*probs[i]/(rank[i]*(1-probs[i])), 1) for i in xrange(len(probs))]
        qVal = [min(Total*probs[i]/rank[i], 1) for i in xrange(len(probs))]
        return qVal, rank





