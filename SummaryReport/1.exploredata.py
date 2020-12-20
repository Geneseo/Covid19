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
        
data_geofips = TwitterData_Initialize()
data_geofips.initialize("/Users/macbook/1Tweet_Sentiment/almost_feb_june.csv")
data_geofips = data_geofips.processed_data


# Tweet_Count by state : data_geofips
# data_geofips vs data_stateonly

col = 'most_partisan'
grouped = data_geofips[col].value_counts().reset_index()
grouped = grouped.rename(columns = {col:'count', 'index' : 'Partisan Identity'})
grouped = grouped.sort_values('count', ascending=False)
grouped

# Tweet_Count by state : data_geofips
# data_geofips vs data_stateonly

col = 'afinn_category'
grouped = data_geofips[col].value_counts().reset_index()
grouped = grouped.rename(columns = {col:'count', 'index' : 'Partisan Identity'})
grouped = grouped.sort_values('count', ascending=False)
grouped


#data_geofips vs data_stateonly

col = 'simplified_created_at_date'
v1 = data_geofips[col].value_counts().reset_index()
v1 = v1.rename(columns = {col: 'count', 'index':col})
v1['percent'] = v1['count'].apply(lambda data_geofips : 100*data_geofips/sum(v1['count']))
v1 = v1.sort_values(col)
trace1 = go.Scatter(x = v1[col], y =v1['count'],name = '0', marker = dict(color = 'rgb(63,72,204)'))
y = [trace1]
layout = {'title': 'tweet_counts','xaxis':{'title':'date'}}
fig1 = go.Figure(data=y, layout=layout)
fig1.update_layout(
    autosize=False,
    width=1000,
    height=350,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",
)
fig1.layout.template = 'presentation'
fig1.layout.template = 'plotly_dark'
iplot(fig1)


#describe
data_geofips['afinn_score'].describe()
data_geofips['decentralized_afinn'].describe()
