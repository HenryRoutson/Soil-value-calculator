import numpy as np
from xlutils.save import save
import xlrd
import os

def values(path):

        if path == "":
                print("no path")
                return [] , []

        File = xlrd.open_workbook(path)
        File = File.sheet_by_index(0)   

        Elements,Results = [],[]

        def TryFloat(In):
                try:
                        return abs(float(In))
                except:
                        try:
                                # >5
                                return abs(float(In[1:]))
                        except:
                                return 0

        for x in range(6,19):
                Elements.append(File.cell(x, 1).value)

                # To percent by weight
                measure = File.cell(x, 3).value
                value = TryFloat(File.cell(x, 4).value)
                if measure == "mg/kg":
                        Results.append(value/(10**6))
                elif measure == "g/sqm":
                        Results.append(value/133000)
                elif measure == "%":
                        Results.append(value/100)
                else:
                        Results.append(0)

        return np.array(Results), np.array(Elements)
