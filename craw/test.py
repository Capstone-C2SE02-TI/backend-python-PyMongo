from mongoDB_init import client
import requests
coinTestDocs = client['tokensTest']


response = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=true')
response = response.json()
response['_id'] = response['id']
response.pop('id',None)

coinTestDocs.insert_one(response)