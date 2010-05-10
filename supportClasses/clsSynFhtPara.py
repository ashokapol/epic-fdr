#!/usr/bin/env python
from supportClasses.fileIOroutines import read_CSV, read_CSV_header
import numpy as Npy

class clsSynFhtParameters:
    def __init__(self, mblCS1, mblCS2, mblCS3, mblCSrest,\
                 mblNoneTr, mblPartialTr, mblFullyTr, \
                 mintMaxXCorrRank, mflDelCn2Th, mblBypass, \
                 synFiles):

        self.mblCS1 = mblCS1
        self.mblCS2 = mblCS2
        self.mblCS3 = mblCS3
        self.mblCSrest = mblCSrest

        self.mblNoneTr = mblNoneTr
        self.mblPartialTr = mblPartialTr
        self.mblFullyTr = mblFullyTr

        self.mintMaxXCorrRank = mintMaxXCorrRank
        self.mflDelCn2Th = float(mflDelCn2Th)
        self.mblBypass = mblBypass

        self.Files = synFiles

def extractColumnsFromSyn(self, para):
    Data = []
    synHeader = read_CSV_header(self, para.Files[0])
    for synFile in para.Files:
        currData = read_CSV(self, synFile)
        Data.extend(currData)
    if not para.mblBypass:
        XCorr = Npy.array([float(Data[i][5]) for i in range(0,len(Data))])
        CS = Npy.array([int(Data[i][3]) for i in range(0,len(Data))])
        DelCn2 = Npy.array([float(Data[i][11]) for i in range(0,len(Data))])
        Sp = Npy.array([float(Data[i][7]) for i in range(0,len(Data))])
        TrypSt = Npy.array([int(Data[i][18]) for i in range(0,len(Data))])
        RankXc = Npy.array([int(Data[i][13]) for i in range(0,len(Data))])

        tmpidx = Npy.ones(len(CS))
        idxCS = (tmpidx == 0)

        if para.mblCS1:
            idxCS = idxCS | (CS == 1)
        if para.mblCS2:
            idxCS = idxCS | (CS == 2)
        if para.mblCS3:
            idxCS = idxCS | (CS == 3)
        if para.mblCSrest:
            idxCS = idxCS | (CS > 3)

        idxDCn = (DelCn2 >= para.mflDelCn2Th)
        idxXCr = (RankXc <= int(para.mintMaxXCorrRank))
        idx = idxCS & idxDCn & idxXCr

        tmpidx = Npy.ones(len(TrypSt))
        idxTr = (tmpidx == 0)

        if para.mblFullyTr:
            idxTr = idxTr | (TrypSt == 2)
        if para.mblPartialTr:
            idxTr = idxTr | (TrypSt == 1)
        if para.mblNoneTr:
            idxTr = idxTr | (TrypSt == 0)

        mboolIdx = idx & idxTr
        x = Npy.array(range(len(Data)))
        nIdx = x[mboolIdx]
    else:
        nIdx = range(len(Data))

    headerIdx = [10,5,11,7,3,1,8] # [PepSeq, XCorr, DelCn2, Charge State, ScanN, ProteinName]
    DataHeader = [synHeader[i] for i in headerIdx]
    Data = [[Data[row][col] for col in headerIdx] for row in nIdx]

    return DataHeader, Data

