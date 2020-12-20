## Get Census_tract Fips_code
import requests
import urllib
from tqdm import tqdm_notebook as tqdm
from tqdm import trange

def get_fips_code(x):
    try:
    #Sample latitude and longitudes
        latitude = x['latitude']
        longtitude = x['longitude']

        #Encode parameters
        params = urllib.parse.urlencode({'latitude':latitude, 'longitude':longtitude, 'format':'json'})
        #Contruct request URL
        url = 'https://geo.fcc.gov/api/census/block/find?' + params

        #Get response from API
        response = requests.get(url)
        response.status_code

        #Parse json in response
        data = response.json()

        #Print FIPS code
        return data['Block']['FIPS'][0:11]
    except:
        return np.nan

data_geofips['CensusTract_Fips'] = data_geofips.apply(get_fips_code, axis=1)


#converting fips code to State name
#pip install git+https://github.com/jsh9/python-plot-utilities@v0.6.6
def fips2state(location):
    if '01' ==location:
        state = 'Alabama'
    elif '02' ==location:
        state = 'Alaska'
    elif '04' ==location:
        state = 'Arizona'
    elif '05' ==location:
        state = 'Arkansas'
    elif '06' ==location:
        state = 'California'
    elif '08' ==location:
        state = 'Colorado'
    elif '09' ==location:
        state = 'Connecticut'
    elif '10' ==location:
        state = 'Delaware'
    elif '12' ==location:
        state = 'Florida'
    elif '13' ==location:
        state = 'Georgia'
    elif '15' ==location:
        state = 'Hawaii'
    elif '16' ==location:
        state = 'Idaho'
    elif '17' ==location:
        state = 'Illinois'
    elif '18' ==location:
        state = 'Indiana'
    elif '19' ==location:
        state = 'Iowa'
    elif '20' ==location:
        state = 'Kansas'
    elif '21' ==location:
        state = 'Kentucky'
    elif '22' ==location:
        state = 'Louisiana'
    elif '23' ==location:
        state = 'Maine'
    elif '24' ==location:
        state = 'Maryland'
    elif '25' ==location:
        state = 'Massachusetts'
    elif '26' ==location:
        state = 'Michigan'
    elif '27' ==location:
        state = 'Minnesota'
    elif '28' ==location:
        state = 'Mississippi'
    elif '29' ==location:
        state = 'Missouri'
    elif '30' ==location:
        state = 'Montana'
    elif '31' ==location:
        state = 'Nebraska'
    elif '32' ==location:
        state = 'Nevada'
    elif '33' ==location:
        state = 'New Hampshire'
    elif '34' ==location:
        state = 'New Jersey'
    elif '35' ==location:
        state = 'New Mexico'
    elif '36' ==location:
        state = 'New York'
    elif '37' ==location:
        state = 'North Carolina'
    elif '38' ==location:
        state = 'North Dakota'
    elif '39' ==location:
        state = 'Ohio'
    elif '40' ==location:
        state = 'Oklahoma'
    elif '41' ==location:
        state = 'Oregon'
    elif '42' ==location:
        state = 'Pennsylvania'
    elif '44' ==location:
        state = 'Rhode Island'
    elif '45' ==location:
        state = 'South Carolina'
    elif '46' ==location:
        state = 'South Dakota'
    elif '47' ==location:
        state = 'Tennessee'
    elif '48' ==location:
        state = 'Texas'
    elif '49' ==location:
        state = 'Utah'
    elif '50' ==location:
        state = 'Vermont'
    elif '51' ==location:
        state = 'Virginia'
    elif '53' ==location:
        state = 'Washington'
    elif '54' ==location:
        state = 'West Virginia'
    elif '55' ==location:
        state = 'Wisconsin'
    elif '56' ==location:
        state = 'Wyoming'
    elif '60' ==location:
        state = 'American Samoa'
    elif '66' ==location:
        state = 'Guam'
    elif '69' ==location:
        state = 'Northern Mariana Islands'
    elif '72' ==location:
        state = 'Puerto Rico'
    elif '78' ==location:
        state = 'Virgin Islands'
    else : 
        return None
    
    return state

data.processed_data['state'] = data.processed_data['fips'].apply(fips2state)
data.processed_data = data.processed_data.dropna(subset=['state'])


