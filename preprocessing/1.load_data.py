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
        
data = TwitterData_Initialize()
data.initialize("almost_feb_june.csv")

data.processed_data =  data.processed_data[data.processed_data['lang'] == 'en'] # remove non-english tweets
data.processed_data =  data.processed_data[data.processed_data['tweet_type'] != 'retweet'] # remove retweets
data.processed_data = data.processed_data[data.processed_data["country_code"]=='US'] # remove tweets from outside of US

data.processed_data['simplified_created_at'] = data.processed_data['parsed_created_at'].str[:10] # Parsing date info to date
data.processed_data['simplified_created_at_date'] = pd.to_datetime(data.processed_data['simplified_created_at'], errors='coerce') # date
data.processed_data['simplified_created_at_week'] = data.processed_data['simplified_created_at_date'].dt.week # Week
data.processed_data['month'] = data.processed_data['simplified_created_at_date'].dt.month # Month
