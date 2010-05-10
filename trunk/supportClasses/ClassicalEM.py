#!/usr/bin/env python
import math as Math
from PyQt4 import QtGui
import numpy as Npy

def Expectation(X, k, p, mu, Sig): # E-Step
    EPS = 0.00000001
    n, d = X.shape
    #n = len(X)
    #d = len(X[0])
    sqdtS = Npy.zeros(k)
    E = Npy.zeros((n,k))
    iSig = Sig

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
            #gs = Npy.array([map(Math.exp,rh1[idx,:]) for idx in range(0,len(rh1))]) / (k1*sqdtS[j])
            gs = Math.exp(rh1) / (k1*sqdtS[j])
            E[i,j] = p[j] * gs
        E[i,:] = E[i,:] / sum(E[i,:])
    return E

def Maximization(X, k, E): # M-Step
    n, d = X.shape
    #n = len(X)
    #d = len(X[0])
    mu = Npy.zeros((d, k))
    Sig = Npy.zeros((k, d, d))
    V = Npy.zeros((d, d))

    rowSumE = Npy.array([sum(E[:, col]) for col in range(0, len(E[0]))])
    XtimesE = Npy.dot(X.transpose(), E)
    mu = XtimesE / Npy.tile(rowSumE, (d,1))

    for i in range(0, k):
        for j in range(0,n):
            dXM = Npy.mat(X[j,:] - mu[:,i])
            V = V + E[j,i]*Npy.dot(dXM.T, dXM)
        Sig[i] = V/rowSumE[i]
    p = rowSumE/n

    return p, mu, Sig

def Likelihood(X, k, p, mu, Sig): # Compute Likelihood value.
    n, d = X.shape
    #n = len(X)
    #d = len(X[0])

    Xbar = X.mean(axis=0) #colMeans(X)
    V = Npy.cov(X.T) #cov(X)
    L = 0

    for i in range(0,k):
        iSig = Npy.linalg.inv(Sig[i])
        dXbM = Xbar - mu[:,i]
        L = L + p[i]*(-0.5)*n*(Npy.log(Npy.linalg.det(Sig[i])) + \
              sum(Npy.diag(Npy.dot(iSig, V))) + \
                         Npy.dot(Npy.dot(dXbM.transpose(), iSig), dXbM))
    return L

def PerformEM(X, k, Pk, M, V, ltol, maxiter): # EM algorithm
    Ln = Likelihood(X,k,Pk,M,V) # Initialize log likelihood
    Lo = 2*Ln
    niter = 0

    while ((abs(100*(Ln-Lo)/Lo)>ltol) and (niter<=maxiter)):
        print niter
        E = Expectation(X,k,Pk,M,V) # E-step
        Pk, M, V = Maximization(X,k,E)  # M-step
        Lo = Ln
        Ln = Likelihood(X, k, Pk, M, V)
        niter = niter + 1
        print Lo
        print Ln
    return Pk, M, V



