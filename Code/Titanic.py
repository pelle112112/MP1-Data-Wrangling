# import pandas for structuring the data
import pandas as pd

# import numpy for numerical analysis
import numpy as np

# import libs for diagrams inline with the text
import matplotlib.pyplot as plt
import seaborn as sns
import xlrd


# other utilities
from sklearn import datasets, preprocessing, metrics

# Reading the file: Titanic.xls
df = pd.read_excel('Titanic.xls', index_col=None, na_values=['NA'])

print(df.shape)
print(df.columns)
print(list(df))
print(df.head())

# Data cleaning
df.isnull().sum()
df = df.drop(['body', 'cabin', 'boat'], axis=1)
print(df.shape)
#replace the missing age with the average age
mean_age = df.age.mean()
df['age'] = df['age'].fillna(mean_age)
#print the count
print("Current numbers of data: \n", df.count())
df["home.dest"] = df["home.dest"].fillna("NA")
print(df.head())
# See current state of null values:
print(df.isnull().sum())
mean_fare = df.fare.mean()
print(mean_fare)
df['Fare'] = df['fare'].fillna(mean_fare)


# Replace with mode
mode_emb = df.embarked.mode()
print(mode_emb)
df['embarked']=df['embarked'].fillna('S')

# Creating a function to change female and male values to 0 and 1
def preprocessor(df):
    processed_df = df.copy()
    le = preprocessing.LabelEncoder()
    processed_df['sex'] = le.fit_transform(df['sex'])
    processed_df['embarked'] = le.fit_transform(df['embarked'])
    processed_df = processed_df.drop(['name','ticket','home.dest'], axis=1)
    return processed_df

# Running the function
dfp = preprocessor(df)
# Checking the data
print(dfp.head)
print(dfp.shape)
print(np.all(np.isfinite(dfp)))
print(np.any(np.isnan(dfp)))

# 3
# A What type of error have been checked for?
# We have checked for missing age, missing fare, missing home dest, missing embarked and finally removed high missing values which includes "boat", "body" and "cabin"

# B Has this type of error been found?
# Yes. All of the errors have been found and fixed.

# C If it has been found, how has it been recovered?
# The missing age has been changed to average age. Missing fare to average fare. Missing destination changed to 'NA'. Missing embarked changed to 'S'. The data from the last 3 columns have been removed

# D do you suggest any other alternative way of data reparation?
# The missing values for age and fare could be changed to 0 instead of average.