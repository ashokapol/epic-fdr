#!/usr/bin/env python
import math as Math
from PyQt4 import QtCore, QtGui
import numpy as Npy

def whichmax(a_list):
    max_val, max_index = max((x, i) for i, x in enumerate(a_list))
    return max_index

def Expectation(X, k, p, mu, Sig): # E-Step
    EPS = 0.00000001
    n, d = X.shape
    sqdtS = Npy.zeros(k)
    E = Npy.zeros((n,k))
    iSig = Npy.array([Npy.zeros((d, d)), Npy.zeros((d, d))])

    k1 = (2*Math.pi)**(0.5*d)

    for j in range(0,k):
        if Npy.alltrue(Sig[j]==Npy.zeros((d,d))):
            Sig[j] = EPS * Npy.ones(d, d)
        sqdtS[j] = Math.sqrt(Npy.linalg.det(Sig[j]))
        iSig[j] = Npy.linalg.inv(Sig[j])

    for i in range(0,n):
        for j in range(0,k):
            dXM = X[i,:] - mu[:,j]
            rh1 = -0.5*Npy.dot(Npy.dot(dXM,iSig[j]), dXM.transpose())
            gs = Math.exp(rh1) / (k1*sqdtS[j])
            E[i,j] = p[j] * gs
        E[i,:] = E[i,:] / sum(E[i,:])
    return E

def Classification(X, E): # C-Step
    n, d = E.shape
    Class = Npy.zeros((n, d))
    maxColIdx = map(whichmax, E)
    for i in range(0, len(maxColIdx)):
        Class[i, maxColIdx[i]] = 1
    return Class


def Maximization(X, Class): # M-Step
    k = len(Class[0])
    n, d = X.shape
    mu = Npy.zeros((d, k))
    Sig = Npy.zeros((k, d, d))
    V = Npy.zeros((d, d))

    rowSumC = Npy.array([sum(Class[:, col]) for col in range(0, len(Class[0]))])
    p = rowSumC/n
    XtimesC = Npy.dot(X.transpose(), Class)
    mu = XtimesC / Npy.tile(rowSumC, (d,1))

    for i in range(0, k):
        for j in range(0,n):
            dXM = Npy.mat(X[j,:] - mu[:,i])
            V = V + Class[j,i]*Npy.dot(dXM.T, dXM)
        Sig[i] = V/rowSumC[i]

    return p, mu, Sig

def Likelihood(X, k, Sig, Class): # Compute Likelihood value.
    n, d = X.shape

    L = 0

    for i in range(0,k):
        iSig = Npy.linalg.inv(Sig[i])
        Xk = X[Class[:,i]==1,:]
        nk = len(Xk)
        Wk = nk*Npy.cov(Xk.T)

        L = L + nk*(Npy.log(Npy.linalg.det(Sig[i]))) + \
              sum(Npy.diag(Npy.dot(iSig, Wk)))
    return L

def PerformEM(X, k, Pk, M, V, ltol, maxiter): # EM algorithm
    E = Expectation(X, k, Pk, M, V)
    Cl = Classification(X, E)
    Ln = Likelihood(X, k, V, Cl) # Initialize log likelihood
    Lo = 2*Ln
    niter = 0

    while ((abs(100*(Ln-Lo)/Lo)>ltol) and (niter<=maxiter)):
        #print niter
        emit(QtCore.SIGNAL("progress(int)"), niter)
        E = Expectation(X, k, Pk, M, V) # E-step
        Cl = Classification(X, E)
        Pk, M, V = Maximization(X, Cl)  # M-step
        Lo = Ln
        Ln = Likelihood(X, k, V, Cl)
        niter = niter + 1
        #print Lo
        #print Ln
    return Pk, M, V, Ln

def GaussianDist(X, k, mu, Sig): # Gaussians
    EPS = 0.00000001
    n, d = X.shape
    sqdtS = Npy.zeros(k)
    E = Npy.zeros((n,k))
    iSig = Npy.array([Npy.zeros((d, d)), Npy.zeros((d, d))])

    k1 = (2*Math.pi)**(0.5*d)

    for j in range(0,k):
        if Npy.alltrue(Sig[j]==Npy.zeros((d,d))):
            Sig[j] = EPS * Npy.ones(d, d)
        sqdtS[j] = Math.sqrt(Npy.linalg.det(Sig[j]))
        iSig[j] = Npy.linalg.inv(Sig[j])

    for i in range(0,n):
        for j in range(0,k):
            dXM = X[i,:] - mu[:,j]
            rh1 = -0.5*Npy.dot(Npy.dot(dXM,iSig[j]), dXM.transpose())
            gs = Math.exp(rh1) / (k1*sqdtS[j])
            E[i,j] = gs

    return E

def GaussianGrid(X,Y,mu,Sig):
    X = Npy.array(X)
    Y = Npy.array(Y)
    EPS = 0.00000001
    n, d = X.shape
    Z = Npy.zeros((n,d))
    iSig = Npy.linalg.inv(Sig)
    sqdtS = Math.sqrt(Npy.linalg.det(Sig))

    k1 = 2*Math.pi

    for i in range(0,n):
        for j in range(0,d):
            x = Npy.array([X[i,j], Y[i,j]])
            dXM = x - mu
            rh1 = -0.5*Npy.dot(Npy.dot(dXM,iSig), dXM.transpose())
            gs = Math.exp(rh1) / (k1*sqdtS)
            Z[i,j] = gs

    return Z

def GetProbabilities(X, Pk, M, Sig):
    Dist = GaussianDist(X, 2, M, Sig)
    first = Pk[0]*Dist[:,0]
    second = Pk[1]*Dist[:,1]
    probabilities = second / (second + first)
    return probabilities





