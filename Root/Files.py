import numpy as np
import xlrd

# type checking
def return_float(value):
        # try avoids errors with unrecognized symbols
        try:
                return float(value)
        except:
                try:
                        # >5
                        return float(value[1:])
                except:
                        return 0

def values(path):
        # opening files and creating variables
        excel_file = xlrd.open_workbook(path).sheet_by_index(0)
        values, nutrients = [],[]
        contains_errors = False

        # conversions
        for x in range(6,19):
                try:
                        nutrients.append(excel_file.cell(x, 1).value)
                        units = excel_file.cell(x, 3).value
                        value = return_float(excel_file.cell(x, 4).value)     
                except:
                        # print("\nvalues missing in", path)
                        nutrients.append("None")
                        values.append(0.0)
                        contains_errors = True
                        continue

                if units.lower() == "mg/kg":
                        values.append(value/(10**6))
                elif units.lower() == "g/sqm":
                        values.append(value/133000)
                elif units == "%":
                        values.append(value/100)
                else:
                        # print("\nmissing valid units in", path)
                        # print("use mg/kg, g/sqm or %")
                        values.append(0.0)
                        contains_errors = True
                        continue

                # range checking
                if -1 < x < 1:
                        values[-1] = 0.0

        return np.array(values), np.array(nutrients), contains_errors
        