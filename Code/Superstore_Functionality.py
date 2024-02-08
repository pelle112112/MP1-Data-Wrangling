import pandas as pd
import numpy as np
import xlrd
import matplotlib.pyplot as mpl

def readExcelData(path):
    return pd.read_excel(path, index_col=None, na_values=['NA'])

def findMissingvalues(dataFrame):
    return dataFrame.isnull().sum()

def getFeatures(dataFrame):
    return dataFrame.columns

def anonymiseDataFrame(dataFrame):
    return dataFrame.drop(['Customer Name', 'Customer ID'], axis=1)

def getProfitBySegment(dataFrame):
    anonymizedDataFrame = anonymiseDataFrame(dataFrame)
    return anonymizedDataFrame.drop([
        'Row ID',
        'Order Priority', 
        'Discount',
        'Unit Price',
        'Shipping Cost',
        'Ship Mode',
        'Product Category',
        'Product Sub-Category',
        'Product Container',
        'Product Name',
        'Product Base Margin',
        'Country',
        'Region',
        'State or Province',
        'City',
        'Postal Code',
        'Order Date',
        'Ship Date',
        'Quantity ordered new',
        'Order ID'
        ], axis=1)

def visualizeDataframe(dataFrame, visualizationStyle, desiredData):
    desiredData = dataFrame[desiredData].value_counts().plot(kind=visualizationStyle)
    mpl.plot()

dataFrame = readExcelData('Data\superstore.xls')
print(dataFrame)
print(getFeatures(dataFrame))
print(findMissingvalues(dataFrame))
print(getProfitBySegment(dataFrame))
visualizeDataframe(dataFrame, 'bar', 'Profit')
# getProfitBySegment(dataFrame).boxplot(by='Customer Segment', column='Profit')
# getProfitBySegment(dataFrame)['Customer Segment'].value_counts().plot(kind='pie')
# mpl.plot([dataFrame['Customer Segment'], dataFrame['Profit']])
# mpl.ylabel('Profit')
# mpl.xlabel('Customer Segment')
# mpl.show()