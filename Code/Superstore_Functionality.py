import pandas as pd
import numpy as np
import xlrd

def readExcelData(path):
    return pd.read_excel(path, index_col=None, na_values=['NA'])

dataFrame = readExcelData('Data\superstore.xls')
print(dataFrame)
print(dataFrame.isnull().sum())