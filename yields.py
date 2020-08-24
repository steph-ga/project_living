import pandas as pd
import numpy as np
import time

import requests
from bs4 import BeautifulSoup

# Load data
data_london = pd.read_csv('data_london.csv')

# Extract sample postcodes for the trial period, max 30 each time
num_of_sample = int(input("Enter the number of postcodes to search (max 30): "))
sample_data = data_london[:num_of_sample]
sample_postcode = sample_data.postcode.to_list()

# Print trial postcodes
print("Analysing postcodes: {}".format(sample_postcode))
print("Assuming 2 bedroom properties, retrieving gross yields...")

# API inputs
api_key = 'HIDDEN'

# Initialise an empty list
gross_yields = []
num_of_bedrooms = input("Average gross yields for properties with how many bedrooms? Enter the number of bedrooms: ")

for i in sample_postcode:
    yield_url = "https://api.propertydata.co.uk/yields?key=HIY0FWQYTH&postcode={}&bedrooms={}".format(i, num_of_bedrooms)
    result = requests.get(yield_url).json()
    print (result)
    if result['status'] == 'success':
        gross_yield = result['data']['long_let']['gross_yield']
        gross_yields.append(gross_yield)
    else:
        gross_yields.append(0)
    time.sleep(3)

yields_data = list(zip(sample_postcode, gross_yields))
yields_df = pd.DataFrame(yields_data, columns=['postcode','gross_yield'])

print("Saving data...")

yields_df.to_csv("data_gross_yields.csv", index=False)

print("Data saved successfully!")