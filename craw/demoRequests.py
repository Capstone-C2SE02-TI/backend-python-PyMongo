# 1. Import module requests
import requests


# 2. Chuẩn bị gọi các đối số để gọi hàm
parameter = {
    'localization': False,
    'tickers': False,
    'market_data': True,
    'community_data': False,
    'developer_data': False,
    'sparkline': False
}
id = 'bitcoin'
COIN_ID_API_URL = f'https://api.coingecko.com/api/v3/coins/{id}'


# 3. Gọi module.methods rồi truyền vào các đối số chuẩn bị trước
response = requests.get(COIN_ID_API_URL, params=parameter)
# Các method ở đây có thể là : 
methods = ['GET', 'POST', 'PUT', 'PATCH']

