import numpy as np
from xlutils.save import save
import xlrd

# type checking
def return_float(In):
        # try avoids errors with unrecognized symbols
        try:
                return float(In)
        except:
                try:
                        # >5
                        return float(In[1:])
                except:
                        return 0

def values(path):
        print(path)
        # opening files and creating variables
        File = xlrd.open_workbook(path, ragged_rows=True).sheet_by_index(0)
        Elements,Results = [],[]

        # conversions
        for x in range(6,19):
                Elements.append(File.cell(x, 1).value)

                # To percent by weight
                measure = File.cell(x, 3).value
                value = return_float(File.cell(x, 4).value)
                if measure == "mg/kg":
                        Results.append(value/(10**6))
                elif measure == "g/sqm":
                        Results.append(value/133000)
                elif measure == "%":
                        Results.append(value/100)
                else:
                        Results.append(0)

        # range checking
        for i, x in enumerate(Results):
                if not -1 < x < 1:
                        Results[i] = 0

        return np.array(Results), np.array(Elements)
