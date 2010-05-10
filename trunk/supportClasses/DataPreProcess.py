#!/usr/bin/env python
import numpy as Npy

"""
CS: Data column of charge states
TrypSt: Data column with Tryptic ends
"""
def extractDataGeneric(CS, TrypSt, indexCS, indexTr, mblLstCS, mblLstTryp):
    idxCS, idxTr = None, None
    mboolIdx = None

    if indexCS != None:
        mblCS1, mblCS2, mblCS3, mblCSother = mblLstCS[0], mblLstCS[1], mblLstCS[2], mblLstCS[3]

        tmpidx = Npy.ones(len(CS))
        idxCS = (tmpidx == 0)

        if mblCS1:
            idxCS = idxCS | (CS == 1)
        if mblCS2:
            idxCS = idxCS | (CS == 2)
        if mblCS3:
            idxCS = idxCS | (CS == 3)
        if mblCSother:
            idxCS = idxCS | (CS > 3)

    if indexTr != None:
        mblNoneTr, mblPartialTr, mblFullyTr = mblLstTryp[0], mblLstTryp[1], mblLstTryp[2]

        tmpidx = Npy.ones(len(TrypSt))
        idxTr = (tmpidx == 0)

        if mblFullyTr:
            idxTr = idxTr | (TrypSt == 2)
        if mblPartialTr:
            idxTr = idxTr | (TrypSt == 1)
        if mblNoneTr:
            idxTr = idxTr | (TrypSt == 0)

    if (idxCS == None) and (idxTr == None):
        return None
    elif idxTr == None:
        mboolIdx = idxCS
    elif idxCS == None:
        mboolIdx = idxTr
    else:
        mboolIdx = idxTr & idxCS

    return mboolIdx



def extractDataSEQ(CS, TrypSt, DelCn2, RankXc, mblLstCS, mblLstTryp, mflDelCn2Th, mintMaxXCorrRank, mblBypass):
    mboolIdx = None
    if not mblBypass:
        mblCS1, mblCS2, mblCS3, mblCS4, mblCS5, mblCSother = mblLstCS[0], mblLstCS[1], mblLstCS[2], mblLstCS[3], mblLstCS[4], mblLstCS[5]

        tmpidx = Npy.ones(len(CS))
        idxCS = (tmpidx == 0)
        idxTr = (tmpidx == 0)

        if mblCS1:
            idxCS = idxCS | (CS == 1)
        if mblCS2:
            idxCS = idxCS | (CS == 2)
        if mblCS3:
            idxCS = idxCS | (CS == 3)
        if mblCS4:
            idxCS = idxCS | (CS == 4)
        if mblCS5:
            idxCS = idxCS | (CS == 5)
        if mblCSother:
            idxCS = idxCS | (CS > 6)

        mblNoneTr, mblPartialTr, mblFullyTr = mblLstTryp[0], mblLstTryp[1], mblLstTryp[2]

        if mblFullyTr:
            idxTr = idxTr | (TrypSt == 2)
        if mblPartialTr:
            idxTr = idxTr | (TrypSt == 1)
        if mblNoneTr:
            idxTr = idxTr | (TrypSt == 0)

        idxDCn = (DelCn2 >= mflDelCn2Th)
        idxXCr = (RankXc <= mintMaxXCorrRank)

        mboolIdx = idxCS & idxTr & idxDCn & idxXCr
    else:
        tmpidx = Npy.ones(len(CS))
        mboolIdx = (tmpidx == 1)

    return mboolIdx

def extractDataXTandem(CS, DelCn2, mblLstCS, mflDelCn2Th, mblBypass):
    mboolIdx = None
    if not mblBypass:
        mblCS1, mblCS2, mblCS3, mblCS4, mblCS5, mblCSother = mblLstCS[0], mblLstCS[1], mblLstCS[2], mblLstCS[3], mblLstCS[4], mblLstCS[5]

        tmpidx = Npy.ones(len(CS))
        idxCS = (tmpidx == 0)
        idxTr = (tmpidx == 0)

        if mblCS1:
            idxCS = idxCS | (CS == 1)
        if mblCS2:
            idxCS = idxCS | (CS == 2)
        if mblCS3:
            idxCS = idxCS | (CS == 3)
        if mblCS4:
            idxCS = idxCS | (CS == 4)
        if mblCS5:
            idxCS = idxCS | (CS == 5)
        if mblCSother:
            idxCS = idxCS | (CS > 6)

        idxDCn = (DelCn2 >= mflDelCn2Th)

        mboolIdx = idxCS & idxDCn
    else:
        tmpidx = Npy.ones(len(CS))
        mboolIdx = (tmpidx == 1)

    return mboolIdx

