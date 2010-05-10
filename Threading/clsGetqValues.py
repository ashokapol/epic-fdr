#!/usr/bin/env python
import sys
from PyQt4 import QtCore, QtGui
#import supportClasses.ClassificationEM as EM
import numpy as Npy
import math as Math

class clsGetqValues(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.probs = None
        self.mu = None
        self.sigma = None
        self.liklihood = None
        self.pvalues = None
        self.qvalues = None
        self.rank = None
        self.mblSuccess = False
        self.stopped = False
        self.mutex = QtCore.QMutex()
        self.completed = False
        self.niter = 0
        self.dim = 2

    def Initialize(self, X, probs, mu, sigma, method, dim):
        self.Data = X
        self.sigma = sigma
        self.mu = mu
        self.probs = probs
        self.method = method
        self.dim = dim

    def run(self):
        if self.method == 1:
            if self.dim == 1:
                self.pvalues = self.GetProbabilities1D_Bayes(self.Data, self.probs, self.mu, self.sigma)
            else:
                self.pvalues = self.GetProbabilities_Bayes(self.Data, self.probs, self.mu, self.sigma)
        elif self.method == 2:
            if self.dim == 1:
                self.pvalues = self.GetProbabilities1D_GVol(self.Data, self.probs, self.mu, self.sigma)
            else:
                self.pvalues = self.GetProbabilities_GVol(self.Data, self.probs, self.mu, self.sigma)
        elif self.method == 3:
            if self.dim == 1:
                self.pvalues = self.GetProbabilities1D_GVolC(self.Data, self.probs, self.mu, self.sigma)
            else:
                self.pvalues = self.GetProbabilities_GVolC(self.Data, self.probs, self.mu, self.sigma)
        elif self.method == 4:
            if self.dim == 1:
                self.pvalues = self.GetProbabilities1D_GVolC(self.Data, self.probs, self.mu, self.sigma)
            else:
                self.pvalues = self.GetProbabilities_noCov(self.Data, self.probs, self.mu, self.sigma)
        else:
            self.pvalues = self.GetProbabilities_GVolC(self.Data, self.probs, self.mu, self.sigma)


        self.emit(QtCore.SIGNAL("progress(int)"), self.niter+1)
        self.qvalues, self.rank = self.GetqValues(self.pvalues)
        self.mblSuccess = True
        self.emit(QtCore.SIGNAL("finished(bool)"), self.mblSuccess)
        #self.stop()

    def GetResults(self):
        return self.pvalues, self.qvalues, self.rank

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

    def GaussianDist(self, X, k, mu, Sig): # Multiple (k) Gaussians
        EPS = 0.00000001
        n, d = X.shape
        sqdtS = Npy.zeros(k)
        E = Npy.zeros((n, k))
        iSig = Npy.array([Npy.zeros((d, d)), Npy.zeros((d, d))])

        k1 = (2*Math.pi)**(0.5*d)

        for j in range(0, k):
            if Npy.alltrue(Sig[j]==Npy.zeros((d, d))):
                Sig[j] = EPS * Npy.ones(d, d)
            sqdtS[j] = Math.sqrt(Npy.linalg.det(Sig[j]))
            iSig[j] = Npy.linalg.inv(Sig[j])

        for i in range(0, n):
            for j in range(0, k):
                dXM = X[i, :] - mu[:, j]
                rh1 = -0.5*Npy.dot(Npy.dot(dXM, iSig[j]), dXM.transpose())
                gs = Math.exp(rh1) / (k1*sqdtS[j])
                E[i, j] = gs

        return E

    def GaussianDistSingle(self, X, mu, Sig): # One Gaussian
        EPS = 0.00000001
        n, d = X.shape
        sqdtS = 0
        E = Npy.zeros(n)
        iSig = Npy.array([Npy.zeros((d, d)), Npy.zeros((d, d))])

        k1 = (2*Math.pi)**(0.5*d)

        if Npy.alltrue(Sig==Npy.zeros((d, d))):
            Sig = EPS * Npy.ones(d, d)
        sqdtS = Math.sqrt(Npy.linalg.det(Sig))
        iSig = Npy.linalg.inv(Sig)

        for i in range(0, n):
            dXM = X[i, :] - mu
            rh1 = -0.5*Npy.dot(Npy.dot(dXM, iSig), dXM.transpose())
            gs = Math.exp(rh1) / (k1*sqdtS)
            E[i] = gs

        return E

    def Calp_nocov2D(self, x, M, sig):
        t2 = ((x[0] - M[0])/sig[0])**2 + ((x[1] - M[1])/sig[1])**2
        p = Math.exp(-t2/2)
        return p

    def GetProbabilities_noCov(self, X, Pk, M, Sig): # Probabilities without using covariances
        n, d = X.shape
        muF = M[:,0]
        sigF = Sig[0]
        idx1 = (X[:,0]<muF[0]).nonzero()
        idx2 = (X[:,1]<muF[1]).nonzero()

        sigma = Npy.array([Npy.sqrt(sigF[0,0]), Npy.sqrt(sigF[1,1])])

        pvalue = Npy.array([self.Calp_nocov2D(X[i,], muF, sigma) for i in xrange(n)])

        if len(idx1)>0:
            pvalue[idx1] = 1
        if len(idx2)>0:
            pvalue[idx2] = 1

        return pvalue

    def GetProbabilities_GVolC(self, X, Pk, M, Sig): # Probabilities with a constraint
        muF = M[:,0]
        sigF = Sig[0]
        idx1 = (X[:,0]<muF[0]).nonzero()
        idx2 = (X[:,1]<muF[1]).nonzero()
        Dist = self.GaussianDistSingle(X, muF, sigF)
        Dist = Dist / sum(Dist)

        if len(idx1)>0:
            Dist[idx1] = 0
        if len(idx2)>0:
            Dist[idx2] = 0

        pvalue = Npy.zeros(len(Dist))
        for i in xrange(len(Dist)):
            pvalue[i] = sum(Dist[(Dist <= Dist[i]).nonzero()])
            self.niter = self.niter + 1
            self.emit(QtCore.SIGNAL("progress(int)"), self.niter)

        #pvalue = Npy.array([sum(Dist[(Dist <= Dist[i]).nonzero()]) for i in xrange(len(Dist))])

        if len(idx1)>0:
            pvalue[idx1] = 1
        if len(idx2)>0:
            pvalue[idx2] = 1

        return pvalue

    def GetProbabilities_GVol(self, X, Pk, M, Sig):
        muF = M[:,0]
        sigF = Sig[0]
        Dist = self.GaussianDistSingle(X, muF, sigF)
        Dist = Dist / sum(Dist)

        pvalue = Npy.zeros(len(Dist))
        for i in xrange(len(Dist)):
            pvalue[i] = sum(Dist[(Dist <= Dist[i]).nonzero()])
            self.niter = self.niter + 1
            self.emit(QtCore.SIGNAL("progress(int)"), self.niter)

        #pvalue = Npy.array([sum(Dist[(Dist <= Dist[i]).nonzero()]) for i in xrange(len(Dist))])
        idx1 = (X[:,0]<muF[0]).nonzero()
        idx2 = (X[:,1]<muF[1]).nonzero()
        if len(idx1)>0:
            pvalue[idx1] = 1
        if len(idx2)>0:
            pvalue[idx2] = 1

        return pvalue

    def GetProbabilities_Bayes(self, X, Pk, M, Sig):
        Dist = self.GaussianDist(X, 2, M, Sig)
        falseD = Pk[0]*Dist[:, 0]
        trueD = Pk[1]*Dist[:, 1]
        probabilities = falseD / (trueD + falseD)
        self.emit(QtCore.SIGNAL("progress(int)"), 10)
        return probabilities

    def GetqValues(self, probs):
        Total = len(probs)
        sProbs = sorted(probs)
        rank = [sProbs.index(probs[i])+1 for i in xrange(Total)]
        qVal = [min((Total-rank[i])*probs[i]/(rank[i]*(1-probs[i])), 1) for i in xrange(len(probs))]
        #qVal = [min(Total*probs[i]/rank[i], 1) for i in xrange(Total)]
        return qVal, rank

    def GetqValues1(self, probs):
        Total = len(probs)
        sProbs = sorted(probs)
        rank = [sProbs.index(probs[i])+1 for i in xrange(Total)]
        qVal = [min(Total*probs[i]/rank[i], 1) for i in xrange(Total)]
        return qVal, rank

    ####### 1D Model related ##############
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

    def GetProbabilities1D_GVolC(self, X, Pk, M, Sig):
        muF = M[0]
        sigF = Sig[0]
        idx1 = (X<muF).nonzero()
        Dist = self.GaussianDist1DSingle(X, muF, sigF)
        Dist = Dist / sum(Dist)
        if len(idx1)>0:
            Dist[idx1] = 0

        pvalue = Npy.zeros(len(Dist))
        for i in xrange(len(Dist)):
            pvalue[i] = sum(Dist[(Dist <= Dist[i]).nonzero()])
            self.niter = self.niter + 1
            self.emit(QtCore.SIGNAL("progress(int)"), self.niter)

        #pvalue = Npy.array([sum(Dist[(Dist <= Dist[i]).nonzero()]) for i in xrange(len(Dist))])
        if len(idx1)>0:
            pvalue[idx1] = 1

        return pvalue

    def GetProbabilities1D_GVol(self, X, Pk, M, Sig):
        muF = M[0]
        sigF = Sig[0]
        idx1 = (X<muF).nonzero()
        Dist = self.GaussianDist1DSingle(X, muF, sigF)
        Dist = Dist / sum(Dist)

        pvalue = Npy.zeros(len(Dist))
        for i in xrange(len(Dist)):
            pvalue[i] = sum(Dist[(Dist <= Dist[i]).nonzero()])
            self.niter = self.niter + 1
            self.emit(QtCore.SIGNAL("progress(int)"), self.niter)

        #pvalue = Npy.array([sum(Dist[(X >= X[i]).nonzero()]) for i in xrange(len(Dist))])

        return pvalue

    def GetProbabilities1D_Bayes(self, X, Pk, M, Sig):
        Dist = self.GaussianDist1D(X, 2, M, Sig)
        first = Pk[0]*Dist[:, 0]
        second = Pk[1]*Dist[:, 1]
        probabilities = first / (second + first)
        self.emit(QtCore.SIGNAL("progress(int)"), 10)
        return probabilities

    def GetProbabilities1D_noCov(self, X, Pk, M, Sig): # Probabilities without using covariances
        muF = M[:,0]
        sigF = Sig[0]

        pvalue = Npy.array([sum(Dist[(Dist <= Dist[i]).nonzero()]) for i in xrange(len(Dist))])

        return pvalue




