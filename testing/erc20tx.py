import requests

x = requests.get('https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0xdac17f958d2ee523a2206206994597c13d831ec7&address=0x82a4cf34187e9196e57b7517b961a06416c3263d&page=1&offset=100&startblock=15000000&endblock=16000000&sort=asc&apikey=EMECEE42NEIYCBGX1WXCUQKXI7B1Y9K3E5')

txs = x.json()['result']

for tx in txs:
    print(tx)