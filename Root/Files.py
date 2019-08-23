import numpy as np
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
        # opening files and creating variables
        File = xlrd.open_workbook(path).sheet_by_index(0)
        Results, Elements = [],[]
        contains_errors = False

        # conversions
        for x in range(6,19):
                try:
                        Elements.append(File.cell(x, 1).value)
                        units = File.cell(x, 3).value
                        value = return_float(File.cell(x, 4).value)     
                except:
                        # print("\nvalues missing in", path)
                        Elements.append("None")
                        Results.append(0.0)
                        contains_errors = True
                        continue

                if units.lower() == "mg/kg":
                        Results.append(value/(10**6))
                elif units.lower() == "g/sqm":
                        Results.append(value/133000)
                elif units == "%":
                        Results.append(value/100)
                else:
                        # print("\nmissing valid units in", path)
                        # print("use mg/kg, g/sqm or %")
                        Results.append(0.0)
                        contains_errors = True
                        continue

                # range checking
                if -1 < x < 1:
                        Results[-1] = 0.0

        return np.array(Results), np.array(Elements), contains_errors
        