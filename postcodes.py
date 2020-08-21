#%% 
# Import libraries

import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup

from geopy.geocoders import Nominatim
import folium

import matplotlib.pyplot as plt
from matplotlib import cm, colors

print('All libraries are successfully imported!')

# %% 
# Extract postcodes in London from: www.worldpostalcode.com

url = "https://worldpostalcode.com/united-kingdom/england/greater-london"
html = requests.get(url).text
soup = BeautifulSoup(html)
bs = BeautifulSoup(html).prettify()

# %% 
# Extract place names
place_names = []
for item in soup.find_all('div', class_='place'):
    place_names.append(item.get_text())

# Extract post codes
place_codes = []
for item in soup.find_all('div', class_='code'):
    place_codes.append(item.get_text())

# Create a dataframe
data = {'PostCode':place_codes, 'Areas':place_names}
london_locations = pd.DataFrame(data, columns=data.keys())

# %%
# Clean the data table 
# Unstack rows
temp = london_locations['PostCode'].str.split(' ')
london_locations = london_locations.reindex(london_locations.index.repeat(temp.apply(len)))
london_locations['Codes'] = np.hstack(temp)
london_locations.reset_index(drop=True, inplace=True)

# %%
london_locations.drop(columns=['PostCode'], inplace=True)
london_locations.drop_duplicates(inplace=True)

# %%
print("{} postcodes in Greater London retrieved.".format(london_locations.shape[0]))

# %%

postcode = pd.read_csv('postcode.csv')
postcode = postcode.iloc[:,1:]

# %%
# Merge two data sources
london_merged = pd.merge(london_locations, postcode, left_on='Codes', right_on='postcode', how='left')
# %%
# Rows without geolocation
print("{} postcodes without geo coordinates. removing...".format(len(london_merged[london_merged['latitude']==0])))

# %%
london_merged = london_merged[london_merged['latitude']!=0]
print("Postcodes removed are: {}".format(london_merged[london_merged['latitude']==0]['Codes'].to_list()))
# %%
# Drop one col of postcodes
london_merged.drop(columns=['Codes'], inplace=True)
# %%
# Check if there are outliers
import seaborn as sns

fig, ax = plt.subplots(2,1)
sns.boxplot(x=london_merged['latitude'], ax=ax[0])
sns.boxplot(x=london_merged['longitude'], ax=ax[1])
plt.show()

# %%
london_merged.to_csv('data_london.csv', index=False)
# %%
