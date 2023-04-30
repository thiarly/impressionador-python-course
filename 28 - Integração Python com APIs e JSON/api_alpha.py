from chave import chave_api

import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=BBAS3.SA={chave_api}'
r = requests.get(url)
data = r.json()
#print(data['Meta Data'])

print(data)
