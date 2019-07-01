def run(location, Name):

        import numpy as np

        """
        drop files
        file save type
        naming
        """

        # Save in cloud
        with open(Name,'wb') as File:
                File.write(bytes(location,"UTF-8"))
        
        # Parse data
        import xlrd

        File = xlrd.open_workbook(location)
        File = File.sheet_by_index(0)

        Elements,Results = [],[]

        def TryFloat(In):
                try:
                        return float(In)
                except:
                        return float(In[1:])

        for x in range(6,18):
                Elements.append(File.cell(x, 1).value)
                # Percent
                if File.cell(x, 3).value == "mg/kg":
                        Results.append(TryFloat(File.cell(x, 4).value)/(10**6))
                else:
                        Results.append(TryFloat(File.cell(x, 4).value))

        return np.array(Results), np.array(Elements)

# print(run(r"C:\Users\henryro\OneDrive - Ballarat Grammar School\2019 Software\ProjectB\ExcelFiles\Compost 15mm 2018.xlsx","Soil"))
