def run(path = None):

        import numpy as np
        from xlutils.save import save
        import xlrd
        import os

        File = xlrd.open_workbook(path)
        File = File.sheet_by_index(0)   
        
        Elements,Results = [],[]

        def TryFloat(In):
                try:
                        return float(In)
                except:
                        return float(In[1:])

        for x in range(6,19):
                Elements.append(File.cell(x, 1).value)
                # Percent
                if File.cell(x, 3).value == "mg/kg":
                        Results.append(TryFloat(File.cell(x, 4).value)/(10**6))
                else:
                        Results.append(TryFloat(File.cell(x, 4).value))

        return np.array(Results), np.array(Elements)