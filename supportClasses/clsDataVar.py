#!/usr/bin/env python
import numpy as Npy

class clsDataVar:
    def __init__(self, name, epiclabel, data):
        self.name = name
        self.epicLabel = epiclabel
        self.data = data
        self.mblNormed = False
        self.dataN = []

    def SetParameters(self, name, epiclabel, data):
        self.name = name
        self.epicLabel = epiclabel
        self.data = data