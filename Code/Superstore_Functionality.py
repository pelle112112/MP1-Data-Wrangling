import pandas as pd
import numpy as np
import xlrd
import matplotlib.pyplot as mpl

# Read the data from the excel file. The method returns a dataframe containing the data. 
def readExcelData(path):
    return pd.read_excel(path, index_col=None, na_values=['NA'])

# Method which takes a dataframe as parameter and returns the sum of missing values from each feature.
def findMissingvalues(dataFrame):
    return dataFrame.isnull().sum()

# Method which will clean the a feature from a dataframe. 
# You have to provide the method with the dataframe itself, 
# the name of the feature you want to clean 
# and a boolean expression: True will insert the mean of the data at the missing positions; False will delete the rows with missing values.
def cleanMissingValues(dataFrame, missingValue, insertMean):
    if insertMean:
        mean_value = dataFrame[missingValue].mean()
        dataFrame[missingValue] = dataFrame[missingValue].fillna(mean_value)
        return dataFrame
    else:
        return dataFrame[missingValue].dropna()

# Method which returns the names of the features in a dataframe
def getFeatures(dataFrame):
    return dataFrame.columns

# Method focused on removing data which can be used for identifying people. 
def anonymiseDataFrame(dataFrame):
    return dataFrame.drop(['Customer Name', 'Customer ID'], axis=1)

# Method that removes all redundant columns, leaving columns related to customer segments and profits. 
def getProfitBySegment(dataFrame):
    anonymizedDataFrame = anonymiseDataFrame(dataFrame)
    return anonymizedDataFrame.drop([
        'Sales',
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

# Method that removes all redundant columns, leaving columns related to customer segments and sales. 
def getSalesBySegment(dataFrame):
    anonymizedDataFrame = anonymiseDataFrame(dataFrame)
    return anonymizedDataFrame.drop([
        'Profit',
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

# Method which can visualize a dataframe. It takes the dataframe as parameter, aswell as the name of the feature you want your graph to be grouped by and the kind of graph you want. 
def visualizeDataframe(dataFrame, desiredDataX, visualizationStyle):
    if visualizationStyle == 'pie':
        dataFrame.groupby(by=desiredDataX).sum().plot(kind=visualizationStyle, subplots=True, legend=False, autopct='%1.1f%%', explode=(0, 0, 0, 0.1), shadow=True)
    else:
        dataFrame.groupby(by=desiredDataX).sum().plot(kind=visualizationStyle)
    mpl.show()

# Read the excel file.
dataFrame = readExcelData('Data\superstore.xls')
# Print the dataframe to the console.
print(dataFrame)
# Print the features of the dataframe.
print(getFeatures(dataFrame))
# Find the missing values of the dataframe - in this specific case only the feature 'Product Base Margin' has missing values. 
print(findMissingvalues(dataFrame))
# Handling the missing values. In this case because it is so few that are missing, 
# and because the result of these few would not skew the overall result, 
# I have decided to replace the misisng values with the mean of the feature.
cleanedDataFrame = cleanMissingValues(dataFrame, 'Product Base Margin', True)
# Checking that there is no longer any missing values. 
print(findMissingvalues(cleanedDataFrame))
# Printing the cleaned dataframe after grouping it by customer segment, and adding the profits together. This is done to see which segment provides the store with the highest profit. 
print(getProfitBySegment(cleanedDataFrame).groupby(by='Customer Segment').sum())
# Visualize the dataframe in a pie diagram for easier visualization of how much of the companies profits is belongs to the different customer segments.
visualizeDataframe(getProfitBySegment(cleanedDataFrame), 'Customer Segment', 'pie')
# Visualizing the dataframe with focus on sales instead to see if there is a connection between profits and sales.
# Interestingly the small businesses segment provides the store with the highest profit, even though they provide the lowest amount of total sales. 
visualizeDataframe(getSalesBySegment(cleanedDataFrame), 'Customer Segment', 'pie')