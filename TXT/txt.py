import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
from sklearn import datasets, preprocessing, metrics
import os
import re

nutritional_info = {
    'shrimp': {'calories': 99},
    'avocado': {'calories': 160},
    'flour': {'calories': 364},
    'sugar': {'calories': 387},
    'almonds': {'calories': 579},
    'cocoa': {'calories': 228},
    'milk': {'calories': 42},
    # Add more ingredients and their nutritional info here
}


# Define the function to extract ingredients and their quantities
def extract_ingredients(content):
    ingredient_pattern = re.compile(r'(\d+)\s(cups?|tablespoons?|teaspoons?|pounds?|ounces?|grams?|liters?|milliliters?)\s(of)?\s(\w+)', re.IGNORECASE)
    matches = ingredient_pattern.findall(content)
    ingredients = {}
    for quantity, unit, _, ingredient in matches:
        if ingredient.lower() in nutritional_info:
            ingredients[ingredient.lower()] = int(quantity)  # Simplified logic
    return ingredients


measurement_pattern = re.compile(r'\b(cups?|tablespoons?|teaspoons?|pounds?|ounces?|grams?|liters?|milliliters?)\b', re.IGNORECASE)

doc_directory = 'C:/Users/techn/OneDrive/Skrivebord/BI py/DataWrangling/MP1-Data-Wrangling/Data/txt'
filtered_documents = []

for i in range(1, 101):  # Assuming there are 100 documents
    file_path = os.path.join(doc_directory, f'food_{i}.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Extract ingredients
            ingredients = extract_ingredients(content)
            filtered_documents.append((i, content, ingredients))  # Corrected append
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        filtered_documents.append((i, "", {}))  # Append with placeholders if file not found

recipe_nutrition = []
for recipe_id, _, ingredients in filtered_documents:
    total_calories = 0
    print(f"Recipe ID: {recipe_id}")
    for ingredient, quantity in ingredients.items():
        print(f"Ingredient: {ingredient}, Quantity: {quantity}")
        if ingredient in nutritional_info:
            ingredient_calories_per_100g = nutritional_info[ingredient]['calories']
            print(f"Calories per 100g: {ingredient_calories_per_100g}")
            total_calories += ingredient_calories_per_100g * (quantity / 100)
        else:
            print(f"No nutritional information found for: {ingredient}")
    print(f"Total Calories for Recipe {recipe_id}: {total_calories}")
    recipe_nutrition.append((recipe_id, total_calories))

df_nutrition = pd.DataFrame(recipe_nutrition, columns=['Recipe ID', 'Total Calories'])
print(df_nutrition.head())  # Check the first few rows to ensure it's populated correctly
print(df_nutrition.columns)

# Simple bar plot of total calories per recipe
plt.figure(figsize=(15, 10))  # Adjust figure size

# Assuming you're creating a bar plot
sns.barplot(x=df_nutrition.index, y='Total Calories', data=df_nutrition)
plt.title('Total Calories per Recipe')
plt.xlabel('Recipe Index')  # Update x-axis label
plt.ylabel('Total Calories')  # Update y-axis label
plt.xticks(rotation=45, fontsize=10)  # Rotate x-axis labels and adjust font size
plt.yticks(fontsize=10)
plt.tight_layout()  # Adjust layout

# Debugging statements
print("Minimum Total Calories:", df_nutrition['Total Calories'].min())
print("Maximum Total Calories:", df_nutrition['Total Calories'].max())
print("Plot Limits (y-axis):", plt.gca().get_ylim())

plt.show()


from collections import Counter

#Flatten all content into a single string for analysis

all_content = " ".join([content for _, content, _ in filtered_documents])

# Find all matcges of measurement terms
all_measurements = measurement_pattern.findall(all_content)

# Count occurences
measurement_counts = Counter(all_measurements)

# Convcert to DataFrame for easier visualization
measurement_df = pd.DataFrame(measurement_counts.items(), columns=['Measurement', 'Count'])

# Simple var plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Count', y='Measurement', data=measurement_df.sort_values('Count', ascending=False))
plt.title('Frequency of Measurements Terms in Recipes')
plt.show()