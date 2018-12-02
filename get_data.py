import requests
import api_key
key = api_key.key

base_url = 'http://api.eia.gov/series/?api_key='

Ethanol_consumption = '&series_id=TOTAL.ENTCPUS.M'

url = base_url + key + Ethanol_consumption
consump = requests.get(url=url).json()['series']
Ethanol_production = '&series_id=TOTAL.ENPRPUS.M'
url = base_url + key + Ethanol_production
product = requests.get(url=url).json()['series']
import pandas as pd
pd.DataFrame(serial_data['category']['childseries'])
list_df = []
list_metadata = []
for i in serial_data['category']['childseries']:
    if i['series_id'][-1] == 'M':
        url = base_url + key + '&series_id=' + i['series_id']
        print(i['series_id'])
        x = requests.get(url=url).json()
        df = pd.DataFrame(x['series'][0]['data'],columns=['MonthYear','Thousand Barrels'])
        df['country'] = x['series'][0]['description']
        list_df.append(df)
        x['series'][0].pop('data')
        list_metadata.append(x['series'][0])