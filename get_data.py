import requests
import api_key
import pandas as pd
key = api_key.key # API KEY for EIA data https://www.eia.gov/opendata/register.php



base_url = 'http://api.eia.gov/category/?api_key='
url = base_url + key + '&category_id=321205'
#get list of all countries
serial_data = requests.get(url=url).json()


list_df = []
list_metadata = []
base_url = 'http://api.eia.gov/series/?api_key='
# Extract export data for each country
for i in serial_data['category']['childseries']:
    if i['series_id'][-1] == 'M' and i['units'] == 'Thousand Barrels':
        url = base_url + key + '&series_id=' + i['series_id']
        x = requests.get(url=url).json()
        df = pd.DataFrame(x['series'][0]['data'],columns=['MonthYear','Thousand Barrels'])
        df['country'] = x['series'][0]['description']
        list_df.append(df)
        x['series'][0].pop('data')
        list_metadata.append(x['series'][0])

df_data = pd.concat(list_df)
df = pd.DataFrame(list_metadata)
df_2 = df.merge(df_data,how='inner',left_on='description',right_on='country')[['MonthYear','units','Thousand Barrels','iso3166']]
df_2 = df_2[df_2['iso3166'] != 'USA']
df_meta = pd.DataFrame(requests.get(url='https://opendata.socrata.com/resource/mnkm-8ram.json').json())
df_4 = df_meta.merge(df_2,left_on='alpha_3_code',right_on = 'iso3166',how='left')[['alpha_3_code','country','latitude_average','longitude_average','MonthYear','Thousand Barrels']]
df_4.dropna(inplace=True)
df_4.sort_values(by=['MonthYear','country'],inplace=True)
df_4['text'] = df_4['country'] + ' ' + df_4['Thousand Barrels'].astype(str) + ' Thousand Barrels'
df_4.to_csv('ethanol_export.csv',index=False)