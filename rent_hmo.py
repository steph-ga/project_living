import pandas as pd
import numpy as np

import time
import requests
from bs4 import BeautifulSoup

# Load data
data_london = pd.read_csv('data_london.csv')

# Load sample data
sample_data = pd.read_csv('data_gross_yields.csv')
sample_postcode = sample_data.postcode.to_list()

# Print trial postcodes
print("Analysing postcodes: {}".format(sample_postcode))

# API inputs
api_key = 'HIDDEN'

# Initialise empty lists
double_ensuite = []
double = []
single_ensuite = []
single = []

for i in sample_postcode:
    rents_url = 'https://api.propertydata.co.uk/rents-hmo?key={}&postcode={}'.format(
                api_key,
                i)
    result = requests.get(rents_url).json()
    print(result)
    if result['status'] == 'success' and result['data']['double-ensuite']['points_analysed'] != 'Insufficient data':
        double_ensuite.append(result['data']['double-ensuite']['average'])
        double.append(result['data']['double-shared-bath']['average'])
        single_ensuite.append(result['data']['single-ensuite']['average'])
        single.append(result['data']['single-shared-bath']['average'])
    else:
        double_ensuite.append(0)
        double.append(0)
        single_ensuite.append(0)
        single.append(0)
    time.sleep(3)

rents_data = list(zip(sample_postcode, double_ensuite, double, single_ensuite, single))
rents_df = pd.DataFrame(rents_data, columns=['postcode','double_ensuite_rent','double_rent','single_ensuite_rent','single_rent'])

print("Saving data...")

rents_df.to_csv("data_rents.csv", index=False)

print("Data saved successfully!")