import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, preprocessing, metrics
import geopandas as gpd


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

# We have the possibility of removing the MBTI Personality Column, but it says something about the personality traits of the influencers.

printDataframe(newDF)

# Create a visualization of the data. Age as x-axis and the amount of influencers as y-axis
# First i need to calculate the amount of influencers in each age group
def ageVisualization(data):
    age = data['Age']
    age = age.value_counts()
    age = age.sort_index()
    age.plot(kind='bar')
    plt.show()
    
# Visualization of the education level for the influencers
def educationVisualization(data):
    education = data['Education Level']
    education = education.value_counts()
    education = education.sort_index()
    education.plot(kind='bar')
    plt.show()
    
ageVisualization(newDF)
educationVisualization(newDF)

