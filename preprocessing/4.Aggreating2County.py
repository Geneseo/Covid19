# Aggreating to county level
# loading package
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from collections import Counter
import nltk

import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
import pandas as pd
import numpy as np
import re as regex
import plotly
from plotly import graph_objs
from time import time
import gensim
from pathlib import Path

import seaborn as sns



import warnings
warnings.filterwarnings('ignore')

%matplotlib inline
plotly.offline.init_notebook_mode()

# Loading data

class TwitterData_Initialize():
    data = []
    processed_data = []
    wordlist = []

    data_model = None
    data_labels = None
    is_testing = False
    
    def initialize(self, csv_file, is_testing_set=False, from_cached=None):
        if from_cached is not None:
            self.data_model = pd.read_csv(from_cached)
            return
        
        self.data = pd.read_csv(csv_file,encoding='latin-1') # encoding must be done with latin-1 to avoid error
            
        self.processed_data = self.data.copy()
        self.wordlist = []
        self.data_model = None
        self.data_labels = None
        
data_geofips.to_csv("NRC_Vader_geo_compiled_reallast_CensusTract_last.csv", index=False)


# merge death and new cases
df_state = pd.read_csv('/Users/macbook/1Tweet_Sentiment/us_states.csv',encoding='latin-1')
df_county = pd.read_csv('/Users/macbook/1Tweet_Sentiment/us_counties.csv',encoding='latin-1')
df_us = pd.read_csv('/Users/macbook/1Tweet_Sentiment/us_cases.csv',encoding='latin-1')

data_geofips = pd.merge(data_geofips, df_state[['simplified_created_at_date','fips','state_cases','state_deaths']], how = 'left', on =['simplified_created_at_date','fips'])
data_geofips = pd.merge(data_geofips, df_county[['simplified_created_at_date','Fips_5','county_cases','county_deaths']], how = 'left', on =['simplified_created_at_date','Fips_5'])
data_geofips = pd.merge(data_geofips, df_us, how = 'left', on =['simplified_created_at_date'])

data_geofips[['state_cases']] = data_geofips[['state_cases']].fillna(value=0)
data_geofips[['state_deaths']] = data_geofips[['state_deaths']].fillna(value=0)
data_geofips[['county_deaths']] = data_geofips[['county_deaths']].fillna(value=0)
data_geofips[['county_cases']] = data_geofips[['county_cases']].fillna(value=0)


# group_by Fips5 = df_fips5 // Urban gotta be percentage by fips5. so no Urban 0,1 but County and State level pct
a = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['happiness_mean'].mean().reset_index()
#af = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['afinn_score'].mean().reset_index()
b = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['democrat'].mean().reset_index()
c = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['republican'].mean().reset_index()
d = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['fips'].mean().reset_index()
#e = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['PovertyRate'].mean().reset_index()

j = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['us_cases'].mean().reset_index()
k = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['state_cases'].mean().reset_index()
l = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['county_cases'].mean().reset_index()

n = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['us_deaths'].mean().reset_index()
m = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['state_deaths'].mean().reset_index()
o = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['county_deaths'].mean().reset_index()

p = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['simplified_created_number'].mean().reset_index()

q = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['White_pct'].mean().reset_index()
r = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['Black_pct'].mean().reset_index()
s = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['Asian_pct'].mean().reset_index()
t = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['Hispanic_pct'].mean().reset_index()
u = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['Seniors_pct'].mean().reset_index()
v = data_geofips.groupby(['Fips_5','simplified_created_at','state'])['Kids_pct'].mean().reset_index()

#n = data_geofips1.groupby(['Fips_5','simplified_created_at','state'])['Asian_pct'].mean().reset_index()

##Urbanization
Urban_county = pd.read_csv("Urban_county.csv")
Urban_state = pd.read_csv("Urban_state.csv")

## Govornor / rural classification
df_rural_classification = pd.read_csv('/Users/macbook/1Tweet_Sentiment/Urban_Rural_Classification_CDC.csv',encoding='latin-1')
df_govornor = pd.read_csv('/Users/macbook/1Tweet_Sentiment/govornor.csv',encoding='latin-1')

##Tweet_Count
df_county = data_geofips.groupby(['Fips_5', 'simplified_created_at']).fips.agg(county_tweet=len).reset_index()
df_state = data_geofips.groupby(['fips', 'simplified_created_at']).fips.agg(state_tweet=len).reset_index()

a = a.merge(b, on = ['Fips_5','simplified_created_at','state'])
#a = a.merge(af, on = ['Fips_5','simplified_created_at','state'])
a = a.merge(c, on = ['Fips_5','simplified_created_at','state'])
a = a.merge(d, on = ['Fips_5','simplified_created_at','state'])
#a = pd.merge(a, e, how = 'left', on = ['Fips_5','simplified_created_at','state'])
a = pd.merge(a, Urban_county, how = 'left', on = ['Fips_5'])
a = pd.merge(a, Urban_state, how = 'left', on = ['fips','state'])

a = a.merge(j, on = ['Fips_5','simplified_created_at','state'])
a = a.merge(k, on = ['Fips_5','simplified_created_at','state'])
a = a.merge(l, on = ['Fips_5','simplified_created_at','state'])

a = a.merge(n, on = ['Fips_5','simplified_created_at','state'])
a = a.merge(m, on = ['Fips_5','simplified_created_at','state'])
a = a.merge(o, on = ['Fips_5','simplified_created_at','state'])

a = a.merge(p, on = ['Fips_5','simplified_created_at','state'])

a= pd.merge(a, df_county, how = 'left', on = ['Fips_5','simplified_created_at'])
a= pd.merge(a, df_state, how = 'left', on = ['fips','simplified_created_at'])

a = pd.merge(a, df_govornor,how='left',on='state')
a = pd.merge(a, df_rural_classification,how='left',on='Fips_5')

a = pd.merge(a, q, how = 'left', on = ['Fips_5','simplified_created_at','state'])
a = pd.merge(a, r, how = 'left', on = ['Fips_5','simplified_created_at','state'])
a = pd.merge(a, s, how = 'left', on = ['Fips_5','simplified_created_at','state'])
a = pd.merge(a, t, how = 'left', on = ['Fips_5','simplified_created_at','state'])
a = pd.merge(a, u, how = 'left', on = ['Fips_5','simplified_created_at','state'])
a = pd.merge(a, v, how = 'left', on = ['Fips_5','simplified_created_at','state'])

#a = a.merge(n, on = ['Fips_5','simplified_created_at','state'])
a['republican'] = a['republican']*100
a['democrat'] = a['democrat']*100

a['simplified_created_at'] = pd.to_datetime(a['simplified_created_at'], errors='coerce')
a['simplified_created_at_week'] = a['simplified_created_at'].dt.week
a['month'] = a['simplified_created_at'].dt.month


a.loc[a['simplified_created_number']<=20200320, 'Cares1'] = 0
#3/20 이후
a.loc[a['simplified_created_number']>20200320, 'Cares1'] = 1

# 4/25 전 후
# df.loc[df['column name'] condition, 'new column name'] = 'value if condition is met'
#전 25일 포함
a.loc[a['simplified_created_number']<=20200425, 'Cares2'] = 0
#4/25 이후
a.loc[a['simplified_created_number']>20200425, 'Cares2'] = 1

a['dayofweek'] =  a['simplified_created_at'].dt.dayofweek


# most_partisan
def whois_more(data):
    if data['democrat'] > data['republican']:
        return 0 # democrat prevails
    elif data['democrat'] < data['republican']:
        return 1
    else: # republican prevails
        return np.nan
    
a['most_partisan'] = a.apply(whois_more,axis=1)

#a['month'] = a['month'].astype('category')
#a['simplified_created_at'] = a['simplified_created_at'].astype('category')
#a['simplified_created_at_week'] = a['simplified_created_at_week'].astype('category')
#a['Fips_5'] = a['Fips_5'].astype('category')
#a['fips'] = a['fips'].astype('category')

#a[['PovertyRate']] = a[['PovertyRate']].fillna(value=7)
#data_geofips.to_csv('almost.csv')
df_fips5 = a
df_fips5
