import numpy as np
from xlutils.save import save
import xlrd
import os

def run(path):

        if path == "":
                return [] , []

        File = xlrd.open_workbook(path)
        File = File.sheet_by_index(0)   

        Elements,Results = [],[]

        def TryFloat(In):
                try:
                        return float(In)
                except:
                        # >5
                        return float(In[1:])

        G_SQM = 133000
        for x in range(6,19):
                Elements.append(File.cell(x, 1).value)

                # To percent by weight
                measure = File.cell(x, 3).value
                value = TryFloat(File.cell(x, 4).value)
                if measure == "mg/kg":
                        Results.append(value/(10**6))
                elif measure == "g/sqm":
                        Results.append(value/G_SQM)
                elif measure == "%":
                        Results.append(value/100)
                else:
                        print("No measure - use mg/kg, g/sqm or %")

        return np.asarray(Results), np.asarray(Elements)