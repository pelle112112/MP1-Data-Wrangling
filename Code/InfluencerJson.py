import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, preprocessing, metrics


# Load the data with a function
def loadJson():
    jsonPath = '../Data/influencer_data.jsonl'
    return pd.read_json(jsonPath, lines=True)



# Print the Dataframe info
def printDataframe(data):
    print(data)
    print(data.shape)
    print(data.count)


df = loadJson()


# Check which columns are in the dataframe
print(df.columns)

# Check for missing data
print(df.isnull().sum())

# anomyzing the data and removing Backstory
# Changing sex to numeral values
def preprocessor(df):
    processed_df = df.copy()
    le = preprocessing.LabelEncoder()
    processed_df['Sex'] = le.fit_transform(df['Sex'])
    processed_df = processed_df.drop(['Name','Backstory'], axis=1)
    return processed_df

newDF = preprocessor(df)

printDataframe(newDF)


