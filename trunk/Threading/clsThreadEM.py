#!/usr/bin/env python
import sys
from PyQt4 import QtCore, QtGui
#import supportClasses.ClassificationEM as EM
import numpy as Npy
import math as Math

class clsThreadEM(QtCore.QThread):

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
        #self.emit(QtCore.SIGNAL("progress(int)"), self.niter+1)
        #self.Probabilities = self.GetProbabilities(self.Data, self.probs, self.mu, self.sigma)
        #self.emit(QtCore.SIGNAL("progress(int)"), self.niter+2)
        #self.qvalues, self.rank = self.GetqValues(self.Probabilities)
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
                E[i, j] = p[j] * gs
            E[i, :] = E[i, :] / sum(E[i, :])
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
        n, d = X.shape
        mu = Npy.zeros((d, k))
        Sig = Npy.zeros((k, d, d))
        V = Npy.zeros((d, d))

        rowSumC = Npy.array([sum(Class[:, col]) for col in range(0, len(Class[0]))])
        p = rowSumC/n
        XtimesC = Npy.dot(X.transpose(), Class)
        mu = XtimesC / Npy.tile(rowSumC, (d, 1))

        for i in range(0, k):
            V = Npy.zeros((d, d))
            for j in range(0, n):
                dXM = Npy.mat(X[j, :] - mu[:, i])
                V = V + Class[j, i]*Npy.dot(dXM.T, dXM)
            Sig[i] = V/rowSumC[i]

        return p, mu, Sig

    def Likelihood(self, X, k, Sig, Class): # Compute Likelihood value.
        n, d = X.shape

        L = 0

        for i in range(0, k):
            iSig = Npy.linalg.inv(Sig[i])
            Xk = X[Class[:, i]==1, :]
            nk = len(Xk)
            Wk = nk*Npy.cov(Xk.T)

            L = L + nk*(Npy.log(Npy.linalg.det(Sig[i]))) + \
                  sum(Npy.diag(Npy.dot(iSig, Wk)))
        return L

    def PerformEM(self, X, k, Pk, M, V, ltol, maxiter): # EM algorithm
        """
        k: number of Gaussians
        Pk: weights on the Gaussians
        M: Means
        V: Covariance matrices
        ltol: tolerance %
        maxiter: Maximum number of iterations
        """
        E = self.Expectation(X, k, Pk, M, V)
        Cl = self.Classification(X, E)
        Ln = self.Likelihood(X, k, V, Cl) # Initialize log likelihood
        Lo = 2*Ln
        self.niter = 0

        while ((abs(100*(Ln-Lo)/Lo)>ltol) and (self.niter<=maxiter)):
            E = self.Expectation(X, k, Pk, M, V) # E-step
            Cl = self.Classification(X, E)
            Pk, M, V = self.Maximization(X, Cl)  # M-step
            Lo = Ln
            Ln = self.Likelihood(X, k, V, Cl)
            self.niter = self.niter + 1
            self.emit(QtCore.SIGNAL("progress(int)"), self.niter)
        return Pk, M, V, Ln

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

    def GaussianDistSingle(self, X, mu, Sig): # Gaussians
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

    def GetProbabilities1(self, X, Pk, M, Sig):
        muF = M[:,0]
        sigF = Sig[0]
        idx1 = (X[:,0]<muF[0]).nonzero()
        idx2 = (X[:,1]<muF[1]).nonzero()
        Dist = self.GaussianDistSingle(X, muF, sigF)
        Dist = Dist / sum(Dist)
        if len(idx1)>0:
            Dist[idx1] = 1
        if len(idx2)>0:
            Dist[idx2] = 1
        pvalue = Npy.array([sum(Dist[(Dist <= Dist[i]).nonzero()]) for i in xrange(len(Dist))])

        return pvalue

    def GetProbabilities(self, X, Pk, M, Sig):
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

        pvalue = Npy.array([sum(Dist[(Dist <= Dist[i]).nonzero()]) for i in xrange(len(Dist))])

        if len(idx1)>0:
            pvalue[idx1] = 1
        if len(idx2)>0:
            pvalue[idx2] = 1

        return pvalue

    def GetProbabilities_old(self, X, Pk, M, Sig):
        muF = M[:,0]
        sigF = Sig[0]
        Dist = self.GaussianDistSingle(X, muF, sigF)
        Dist = Dist / sum(Dist)
        pvalue = Npy.array([sum(Dist[(Dist <= Dist[i]).nonzero()]) for i in xrange(len(Dist))])
        idx1 = (X[:,0]<muF[0]).nonzero()
        idx2 = (X[:,1]<muF[1]).nonzero()
        if len(idx1)>0:
            pvalue[idx1] = 1
        if len(idx2)>0:
            pvalue[idx2] = 1

        return pvalue

    def GetProbabilitiesBayes(self, X, Pk, M, Sig):
        Dist = self.GaussianDist(X, 2, M, Sig)
        falseD = Pk[0]*Dist[:, 0]
        trueD = Pk[1]*Dist[:, 1]
        probabilities = falseD / (trueD + falseD)
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





