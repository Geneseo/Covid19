## policies_indexing
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
        
        
#df3 = pd.merge(df1,df2,how='left',on='fips')
df1 = pd.read_csv('ex.csv', index_col=False)
policy = pd.read_csv('USstatesCov19distancingpolicy.csv', index_col=False)

df3 = pd.merge(df1,policy,how='left',on='fips')
df3 = df3[['fips',
 'date',
 'StateName',
 'StatePolicy',
 'Mandate',
 'StateWide',
 'PublicMaskLevel',
 'DateEnacted',
 'DateExpiry',
 'DateEased',
 'DateEnded',
 'DateReexpanded1',
 'DateReeased1']]
df3


#Policy specify
#school_close = df3['StatePolicy'] == 'TravelRestrictIntra'
school_close = df3['StatePolicy'] == 'TravelRestrictIntra'

# return 0 --common
school_close_rule1_c1 = df3['date'] < df3['DateEnacted']
school_close_rule1_c2 = (df3['DateReexpanded1'].isnull() & df3['DateEnded'].notnull() & df3['date'] >= df3['DateEnded'])
school_close_rule1_c3 = (df3['DateReexpanded1'].isnull() & df3['DateEnded'].isnull() & df3['DateExpiry'].notnull() & df3['date'] >= df3['DateExpiry'])
school_close_rule1_c4 = (df3['DateReexpanded1'].notnull() & (df3['DateReexpanded1'] < df3['DateEnded']) & (df3['date'] >= df3['DateEnded']))
school_close_rule1_c5 = (df3['DateEased'].notnull() & df3['DateEnded'].notnull() & (df3['DateEased'] == df3['DateEnded'])) ## special case
school_close_rule1_c6 = (df3['DateEnacted'].notnull() & df3['DateEnded'].notnull() & df3['DateExpiry'].isnull() & df3['DateEased'].isnull() & df3['DateReexpanded1'].isnull() & (df3['date'] >= df3['DateEnded']))
school_close_rule1_c7 = (df3['DateEnacted'].notnull() & df3['DateEnded'].notnull() & df3['DateExpiry'].notnull() & df3['DateEased'].isnull() & df3['DateReexpanded1'].isnull() & (df3['DateExpiry'] >= df3['DateEnded']) & (df3['date'] >= df3['DateEnded']))
school_close_rule1_c8 = (df3['DateExpiry'].notnull() & df3['DateEnded'].isnull() & df3['DateEased'].isnull() & df3['DateReexpanded1'].isnull() & (df3['date']>=df3['DateExpiry']))
school_close_rule1_conditions = school_close & (school_close_rule1_c1 | school_close_rule1_c2 | school_close_rule1_c3 | school_close_rule1_c4 | school_close_rule1_c5 | school_close_rule1_c6 | school_close_rule1_c7| school_close_rule1_c8)


# return 1 -- when mandatory ==1 (df['Mandate']==1) &
school_close_rule2_c1 = ((df3['Mandate']==1) & (df3.iloc[:,12:15].isnull().sum(axis=1) == 4) & (df3['date'] >= df3['DateEnacted'])) #1.If DateExpiry&DateEnded&DateReexpanded1&DateEased is Null 
school_close_rule2_c2 = ((df3['Mandate']==1) & df3['DateEased'].isnull() & df3['DateEnded'].notnull() & df3['DateReexpanded1'].isnull() & (df3['date'] >= df3['DateEnacted']) & (df3['date'] < df3['DateEnded'])) # between DateEnacted & DateEnded
school_close_rule2_c3 = ((df3['Mandate']==1) & df3['DateEased'].isnull() & df3['DateEnded'].notnull() & df3['DateReexpanded1'].notnull() & (df3['date'] >= df3['DateEnacted']) & (df3['date'] < df3['DateEnded'])) # 1
school_close_rule2_c4 = ((df3['Mandate']==1) & df3['DateEased'].isnull() & df3['DateEnded'].notnull() & df3['DateReexpanded1'].notnull() & (df3['date'] >= df3['DateReexpanded1'])) # 1-1
school_close_rule2_c5 = ((df3['Mandate']==1) & df3['DateEased'].isnull() & df3['DateEnded'].isnull() & df3['DateExpiry'].notnull() & (df3['date'] >= df3['DateEnacted']) & (df3['date'] < df3['DateExpiry']))
school_close_rule2_c6 = ((df3['Mandate']==1) & df3['DateEased'].notnull() & df3['DateReexpanded1'].isnull() & (df3['date'] >= df3['DateEnacted']) & (df3['date'] < df3['DateEased']))
school_close_rule2_c7 = ((df3['Mandate']==1) & df3['DateEased'].notnull() & df3['DateReexpanded1'].notnull() & (df3['date'] >= df3['DateEnacted']) & (df3['date'] < df3['DateEased'])) #2
school_close_rule2_c8 = ((df3['Mandate']==1) & df3['DateEased'].notnull() & df3['DateReexpanded1'].notnull() & (df3['date'] >= df3['DateReexpanded1'])) #2-1
school_close_rule2_c9 = ((df3['Mandate']==1)& df3['DateEnacted'].notnull() & df3['DateExpiry'].isnull() & df3['DateEased'].isnull()& df3['DateEnded'].isnull()& df3['DateReexpanded1'].isnull()& (df3['date'] >= df3['DateEnacted'])) #2-1
school_close_rule2_conditions = school_close & (school_close_rule2_c1 | school_close_rule2_c2 |
                                                school_close_rule2_c3 | school_close_rule2_c4 |
                                                school_close_rule2_c5 | school_close_rule2_c6 |
                                                school_close_rule2_c7 | school_close_rule2_c8 |
                                                school_close_rule2_c9)

# return 0.75 (eased)  (df['Mandate']==1)
school_close_rule3_c1 = ((df3['Mandate']==1) & df3['DateEased'].notnull() & df3['DateReexpanded1'].isnull() & df3['DateEnded'].notnull() & (df3['DateEased']!=df3['DateEnded']) & (df3['date']>=df3['DateEased']) & (df3['date']<df3['DateEnded']))
school_close_rule3_c2 = ((df3['Mandate']==1) & df3['DateEased'].notnull() & df3['DateReexpanded1'].isnull() & df3['DateEnded'].isnull() & df3['DateExpiry'].notnull() & (df3['date']>=df3['DateEased']) & (df3['date']<df3['DateExpiry']))
school_close_rule3_c3 = ((df3['Mandate']==1) & df3['DateEased'].notnull() & df3['DateExpiry'].isnull() & df3['DateReexpanded1'].isnull() & df3['DateEnded'].isnull() & (df3['date']>=df3['DateEased']))
school_close_rule3_c4 = ((df3['Mandate']==1) & df3['DateEased'].notnull() & df3['DateReexpanded1'].notnull() & (df3['DateEased']==df3['DateEnacted']) & (df3['DateEased']<df3['DateReexpanded1']))
school_close_rule3_c5 = ((df3['Mandate']==1) & df3['DateReeased1'].notnull() & (df3['DateEased']>=df3['DateReeased1']))
school_close_rule3_conditions = school_close & (school_close_rule3_c1 | school_close_rule3_c2 | school_close_rule3_c3 | school_close_rule3_c4 |school_close_rule3_c5)


# return 0.5 -- when mandatory==0 (df['Mandate']==0)
school_close_rule4_c1 = ((df3['Mandate']==0) & (df3.iloc[:,12:15].isnull().sum(axis=1) == 4) & (df3['date'] >= df3['DateEnacted'])) #1.If DateExpiry&DateEnded&DateReexpanded1&DateEased is Null 
school_close_rule4_c2 = ((df3['Mandate']==0) & df3['DateEased'].isnull() & df3['DateEnded'].notnull() & df3['DateReexpanded1'].isnull() & (df3['date'] >= df3['DateEnacted']) & (df3['date'] < df3['DateEnded'])) # between DateEnacted & DateEnded
school_close_rule4_c3 = ((df3['Mandate']==0) & df3['DateEased'].isnull() & df3['DateEnded'].notnull() & df3['DateReexpanded1'].notnull() & (df3['date'] >= df3['DateEnacted']) & (df3['date'] < df3['DateEnded'])) # 1
school_close_rule4_c4 = ((df3['Mandate']==0) & df3['DateEased'].isnull() & df3['DateEnded'].notnull() & df3['DateReexpanded1'].notnull() & (df3['date'] >= df3['DateReexpanded1'])) # 1-1
school_close_rule4_c5 = ((df3['Mandate']==0) & df3['DateEased'].isnull() & df3['DateEnded'].isnull() & df3['DateExpiry'].notnull() & (df3['date'] >= df3['DateEnacted']) & (df3['date'] < df3['DateExpiry']))

school_close_rule4_c6 = ((df3['Mandate']==0) & df3['DateEased'].notnull() & df3['DateReexpanded1'].isnull() & (df3['date'] >= df3['DateEnacted']) & (df3['date'] < df3['DateEased']))
school_close_rule4_c7 = ((df3['Mandate']==0) & df3['DateEased'].notnull() & df3['DateReexpanded1'].notnull() & (df3['date'] >= df3['DateEnacted']) & (df3['date'] < df3['DateEased'])) #2
school_close_rule4_c8 = ((df3['Mandate']==0) & df3['DateEased'].notnull() & df3['DateReexpanded1'].notnull() & (df3['date'] >= df3['DateReexpanded1'])) #2-1
school_close_rule4_c9 = ((df3['Mandate']==0) & df3['DateEased'].isnull() & df3['DateEnacted'].notnull() & df3['DateExpiry'].isnull() & df3['DateEnded'].isnull()& df3['DateReexpanded1'].isnull()& (df3['date'] >= df3['DateEnacted'])) #2-1
school_close_rule4_conditions = school_close & (school_close_rule4_c1 | school_close_rule4_c2 |
                                                school_close_rule4_c3 | school_close_rule4_c4 |
                                                school_close_rule4_c5 | school_close_rule4_c6 |
                                                school_close_rule4_c7 | school_close_rule4_c8 |
                                                school_close_rule4_c9)

# return 0.25 (eased)  (df['Mandate']==0)
school_close_rule5_c1 = ((df3['Mandate']==0) & df3['DateEased'].notnull() & df3['DateReexpanded1'].isnull() & df3['DateEnded'].notnull() & (df3['DateEased']!=df3['DateEnded']) & (df3['date']>=df3['DateEased']) & (df3['date']<df3['DateEnded']))
school_close_rule5_c2 = ((df3['Mandate']==0) & df3['DateEased'].notnull() & df3['DateReexpanded1'].isnull() & df3['DateEnded'].isnull() & df3['DateExpiry'].notnull() & (df3['date']>=df3['DateEased']) & (df3['date']<df3['DateExpiry']))
school_close_rule5_c3 = ((df3['Mandate']==0) & df3['DateEased'].notnull() & df3['DateExpiry'].isnull() & df3['DateReexpanded1'].isnull() & df3['DateEnded'].isnull() & (df3['date']>=df3['DateEased']))
school_close_rule5_c4 = ((df3['Mandate']==0) & df3['DateEased'].notnull() & df3['DateReexpanded1'].notnull() & (df3['DateEased']==df3['DateEnacted']) & (df3['DateEased']<df3['DateReexpanded1']))
school_close_rule5_c5 = ((df3['Mandate']==0) & df3['DateReeased1'].notnull() & (df3['DateEased']>=df3['DateReeased1']))
school_close_rule5_conditions = school_close & (school_close_rule5_c1 | school_close_rule5_c2 | school_close_rule5_c3 | school_close_rule5_c4 | school_close_rule5_c5)


school_close_conditions = [school_close_rule1_conditions, school_close_rule2_conditions, school_close_rule3_conditions, school_close_rule4_conditions ,school_close_rule5_conditions]
school_close_results = [0, 1, 0.75, 0.5, 0.25]

#df3['TravelRestrictIntra'] = np.select(school_close_conditions, school_close_results, np.nan) #np.nan should be passed as the alternative result
df3['TravelRestrictIntra'] = np.select(school_close_conditions, school_close_results, np.nan) #np.nan should be passed as the alternative result

df3

test = df3[['fips', 'date', 'TravelRestrictIntra']]
test = test.dropna(subset = ['TravelRestrictIntra'])
test = test.groupby(['fips','date']).sum().reset_index()
df_TravelRestrictIntra = test
df_TravelRestrictIntra.isnull().sum()

merg = pd.merge(df1,df_mask, how='left', on=['fips','date'])
merg = pd.merge(merg,df_BarRestrict, how='left', on=['fips','date'])
merg = pd.merge(merg,df_CaseIsolation, how='left', on=['fips','date'])
merg = pd.merge(merg,df_EmergDec, how='left', on=['fips','date'])
merg = pd.merge(merg,df_GathRestrict, how='left', on=['fips','date'])
merg = pd.merge(merg,df_NEBusinessClose, how='left', on=['fips','date'])
merg = pd.merge(merg,df_OtherBusinessClose, how='left', on=['fips','date'])
merg = pd.merge(merg,df_Quarantine, how='left', on=['fips','date'])
merg = pd.merge(merg,df_RestaurantRestrict, how='left', on=['fips','date'])
merg = pd.merge(merg,df_SchoolClose, how='left', on=['fips','date'])
merg = pd.merge(merg,df_StayAtHome, how='left', on=['fips','date'])
merg = pd.merge(merg,df_TravelRestrictEntry, how='left', on=['fips','date'])
merg = pd.merge(merg,df_TravelRestrictExit, how='left', on=['fips','date'])
merg = pd.merge(merg,df_TravelRestrictIntra, how='left', on=['fips','date'])

merg.to_csv('policies.csv', index=False)
