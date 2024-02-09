# import librabries and tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets, preprocessing, metrics

# Columns i wish to remove from the csv
columnsToDrop = [

    'Estimated mortality of TB cases who are HIV-positive, per 100 000 population, high bound',
    'Estimated number of deaths from TB in people who are HIV-positive, low bound',
    'Estimated number of deaths from TB in people who are HIV-positive, high bound',
    'Estimated number of incident cases (all forms), low bound',
    'Estimated number of incident cases (all forms), high bound',
    'Estimated HIV in incident TB (percent), low bound',
    'Estimated HIV in incident TB (percent), high bound',
    'Estimated incidence of TB cases who are HIV-positive per 100 000 population, low bound',
    'Estimated incidence of TB cases who are HIV-positive per 100 000 population, high bound',
    'Estimated incidence of TB cases who are HIV-positive, low bound',
    'Estimated incidence of TB cases who are HIV-positive, high bound',
    'Case detection rate (all forms), percent, low bound',
    'Case detection rate (all forms), percent, high bound',
    'Estimated mortality of TB cases (all forms, excluding HIV), per 100 000 population, low bound',
    'Estimated mortality of TB cases (all forms, excluding HIV), per 100 000 population, high bound',
    'Estimated number of deaths from TB (all forms, excluding HIV), low bound',
    'Estimated number of deaths from TB (all forms, excluding HIV), high bound',
    'Estimated mortality of TB cases who are HIV-positive, per 100 000 population, low bound',
    'Estimated incidence (all forms) per 100 000 population, low bound',
    'Estimated incidence (all forms) per 100 000 population, high bound',
    'Estimated prevalence of TB (all forms) per 100 000 population, low bound',
    'Estimated prevalence of TB (all forms) per 100 000 population, high bound',
    'Estimated prevalence of TB (all forms), low bound',
    'Estimated prevalence of TB (all forms), high bound'
]

#Load the Csv data
def loadCsv():
    csv = pd.read_csv ('../data/TB_Burden_Country.csv', index_col=None, na_values=['NA'])
    return csv

#print info of the csv
def printCsvInfo(csv):
    print()
    print(csv.shape)
    print()
    print(csv.count())
    print()
    
    
csv = loadCsv()

print(csv.isnull().sum())
print()
print(csv.columns)
print()
csv_sorted = csv.sort_values(by='Estimated prevalence of TB (all forms) per 100 000 population', ascending=False)
#print out the top 10 countries with the highest estimated prevalence of TB (all forms) per 100 000 population
print(csv_sorted.head(10))


def newCsvTable(csv):
# drop unnecessary columns
    processedCsv = csv.drop(columnsToDrop, axis=1)
    return processedCsv


newCsv= newCsvTable(csv)

print(newCsv.count())
print()


# Top 50 countries with the prevalence of TB per 100.000 indbyggere
def top50CountriesWithTBPrevalence(newCsv):
    csv['Year'] = pd.to_datetime(newCsv['Year'], format='%Y')
    # Sort the DataFrame by 'Country or territory name' and 'Year', then keep the latest year for each country
    latest_data = csv.sort_values(by=['Country or territory name', 'Year'], ignore_index=True).groupby('Country or territory name').tail(1)

    # Display all countries sorted by Estimated prevalence of TB
    sorted_by_prevalence = latest_data.sort_values(by='Estimated prevalence of TB (all forms) per 100 000 population', ascending=False)

    # Top 50 countries with the prevalence of TB per 100.000 indbyggere
    print(sorted_by_prevalence.head(50))
    print()
    return latest_data


# Prevalence by region
def TBPrevalenceByRegion(newCsv, latest_data = top50CountriesWithTBPrevalence):
    # Group by region and aggregate data for each region
    aggregated_data_by_region = latest_data.groupby('Region').agg({
    'Estimated total population number': 'sum',
    'Estimated prevalence of TB (all forms) per 100 000 population': 'mean',
    'Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population':'mean',
    'Estimated mortality of TB cases who are HIV-positive, per 100 000 population':'mean',
    # Add other columns you want to aggregate
    }).reset_index()

    # Round the aggregated values to two decimals
    aggregated_data_by_region = aggregated_data_by_region.round(2)

    # Sort the DataFrame by 'Estimated prevalence of TB (all forms) per 100 000 population' in descending order
    sorted_by_prevalence_by_region = aggregated_data_by_region.sort_values(by='Estimated prevalence of TB (all forms) per 100 000 population', ascending=False)

    # Show all regions (6) with the prevalence of TB per 100.000 indbyggere
    print(sorted_by_prevalence_by_region.head(6))
    plt.show()
    print()
    return sorted_by_prevalence_by_region



# Graph of prevalence by region including mortality
def graphOfprevalenceByRegionInklMortallity(newCsv, sorted_by_prevalence_by_region):
    # Extracting data from the DataFrame
    regions = sorted_by_prevalence_by_region['Region']
    prevalence_data = sorted_by_prevalence_by_region['Estimated prevalence of TB (all forms) per 100 000 population']
    mortality_data = sorted_by_prevalence_by_region['Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population']
    hiv_mortality_data = sorted_by_prevalence_by_region['Estimated mortality of TB cases who are HIV-positive, per 100 000 population']

    bar_width = 0.4
    opacity = 0.7

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10, 6))

    # Transparent lightblue bar for Estimated prevalence of TB
    rects1 = ax.bar(regions, prevalence_data, bar_width, alpha=opacity, color='lightblue', label='Prevalence')

    # Calculate positions for the red and green bars (half the size of light blue bar)
    bar_positions = [np.arange(len(regions)) - bar_width / 4, np.arange(len(regions)) + bar_width / 4]

    # Red bar for Estimated mortality of TB cases (excluding HIV)
    rects2 = ax.bar(bar_positions[0], mortality_data, bar_width / 2, alpha=opacity, color='red', label='Mortality (TB)')

    # Green bar for Estimated mortality of TB cases with HIV
    rects3 = ax.bar(bar_positions[1], hiv_mortality_data, bar_width / 2, alpha=opacity, color='green', label='Mortality (HIV)')

    # Adding labels
    ax.set_xlabel('Region')
    ax.set_ylabel('Values per 100,000 population')
    ax.set_title('TB Metrics by Region')
    ax.legend()

    #Display the plot
    plt.show()
    print()

#Run methods   
top50CountriesWithTBPrevalence(newCsv)    
TBPrevalenceByRegion(newCsv, top50CountriesWithTBPrevalence(newCsv))
graphOfprevalenceByRegionInklMortallity(newCsv, sorted_by_prevalence_by_region = TBPrevalenceByRegion(newCsv, top50CountriesWithTBPrevalence(newCsv)))