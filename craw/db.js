a = {
    "tokens": {
        "name": "",
        "categories": ["categori 1", "categori 3"],
        "transactions": [
            { "id": 1, "time": "1/1/2001" },
            { "id": 2, "time": "1/1/2002" }
        ],
        "metada": as
    },
    "categories": [
        { "id": 1, "name": "categori 1", "coins": [{ "id": 1, "name": "coin 1" }] },
        { "id": 2, "name": "categori 2", "coins": [{ "id": 2, "name": "coin 2" }] }
    ],
    "users": {
        "name": "",
        "paymentStatus": true,
        "follower": ["dc1", "dc2"]
    },
    "paymentMethod": {
        "ADDRESS": 123,
        "NETWORK": 123,
        "PRICE": 123
    },
    "investors": {
        "_id": "dc1",
        "isShark": true,
        "transactions": [
            { "id": 1, "time": "1/1/2001" },
            { "id": 2, "time": "1/1/2002" }
        ],
        "crypto": [{}, {}],
        "tokenHolders": [
            { "coin": "eth","percent": 20 },
            { "coin": "btc", "percent": 10 },
            { "coin": "bnz", "percent": 70 }
        ],
    }
}


coinsInfoAPI = {
    'id': 1, 
    'name': 'Bitcoin', 
    'symbol': 'BTC', 
    'slug': 'bitcoin', 
    'num_market_pairs': 9748, 
    'date_added': '2013-04-28T00:00:00.000Z', 
    'tags': ['mineable', 'pow', 'sha-256', 'store-of-value', 'state-channel', 'coinbase-ventures-portfolio', 'three-arrows-capital-portfolio', 'polychain-capital-portfolio', 'binance-labs-portfolio', 'blockchain-capital-portfolio', 'boostvc-portfolio', 'cms-holdings-portfolio', 'dcg-portfolio', 'dragonfly-capital-portfolio', 'electric-capital-portfolio', 'fabric-ventures-portfolio', 'framework-ventures-portfolio', 'galaxy-digital-portfolio', 'huobi-capital-portfolio', 'alameda-research-portfolio', 'a16z-portfolio', '1confirmation-portfolio', 'winklevoss-capital-portfolio', 'usv-portfolio', 'placeholder-ventures-portfolio', 'pantera-capital-portfolio', 'multicoin-capital-portfolio', 'paradigm-portfolio'], 
    'max_supply': 21000000, 
    'circulating_supply': 19157643, 
    'total_supply': 19157643, 
    'is_market_cap_included_in_calc': 1, 
    'platform': None, 'cmc_rank': 1, 
    'self_reported_circulating_supply': None, 
    'self_reported_market_cap': None, 
    'tvl_ratio': None, 
    'last_updated': '2022-09-22T12:19:00.000Z', 
    'quote': {
        'USD': {
            'price': 19244.924672563982, 
            'volume_24h': 53099867940.15944, 
            'volume_24h_reported': 198378000879.4153, 
            'volume_7d': 303753515059.9908, 
            'volume_7d_reported': 1103261453408.2634, 
            'volume_30d': 1041542517618.7972, 
            'volume_30d_reported': 3639257229179.54, 
            'volume_change_24h': 55.5823, 
            'percent_change_1h': 0.78760371, 
            'percent_change_24h': 0.42112019, 
            'percent_change_7d': -4.50980926, 
            'percent_change_30d': -10.14401065, 
            'percent_change_60d': -15.39273673, 
            'percent_change_90d': -9.57176159, 
            'market_cap': 368687396438.8727, 
            'market_cap_dominance': 39.4914, 
            'fully_diluted_market_cap': 404143418123.84, 
            'tvl': None, 
            'market_cap_by_total_supply': 368687396438.8727, 
            'last_updated': '2022-09-22T12:19:00.000Z'
        }
    }
}

coinsInfoAPI2 = {
    'id': 1027, 
    'name': 'Ethereum', 
    'symbol': 'ETH', 
    'slug': 'ethereum', 
    'num_market_pairs': 6099, 
    'date_added': '2015-08-07T00:00:00.000Z', 
    'tags': [
        'pos', 
        'smart-contracts', 
        'ethereum-ecosystem', 
        'coinbase-ventures-portfolio', 
        'three-arrows-capital-portfolio', 
        'polychain-capital-portfolio', 
        'binance-labs-portfolio', 
        'blockchain-capital-portfolio', 
        'boostvc-portfolio', 
        'cms-holdings-portfolio', 
        'dcg-portfolio', 
        'dragonfly-capital-portfolio', 
        'electric-capital-portfolio', 
        'fabric-ventures-portfolio', 
        'framework-ventures-portfolio', 
        'hashkey-capital-portfolio', 
        'kenetic-capital-portfolio', 
        'huobi-capital-portfolio', 
        'alameda-research-portfolio', 
        'a16z-portfolio', 
        '1confirmation-portfolio', 
        'winklevoss-capital-portfolio', 
        'usv-portfolio', 
        'placeholder-ventures-portfolio', 
        'pantera-capital-portfolio', 
        'multicoin-capital-portfolio', 
        'paradigm-portfolio', 
        'injective-ecosystem'
    ], 
    'max_supply': None, 
    'circulating_supply': 122476663.499, 
    'total_supply': 122476663.499, 
    'is_market_cap_included_in_calc': 1, 
    'platform': None, 'cmc_rank': 2, 
    'self_reported_circulating_supply': None, 
    'self_reported_market_cap': None, 
    'tvl_ratio': None, 
    'last_updated': '2022-09-22T12:25:00.000Z', 
    'quote': {
        'USD': {
            'price': 1308.8662583652495, 
            'volume_24h': 23207621164.783592, 
            'volume_24h_reported': 105820216340.4478, 
            'volume_7d': 151269403847.5294, 
            'volume_7d_reported': 689144109957.5103, 
            'volume_30d': 631732916488.8242, 
            'volume_30d_reported': 2893684596860.3745, 
            'volume_change_24h': 67.2561, 
            'percent_change_1h': 1.20041333, 
            'percent_change_24h': -2.96279556, 
            'percent_change_7d': -17.64521677, 
            'percent_change_30d': -18.90106165, 
            'percent_change_60d': -18.90725887, 
            'percent_change_90d': 8.22615033, 
            'market_cap': 160305572290.99585, 
            'market_cap_dominance': 17.174, 
            'fully_diluted_market_cap': 160305572291, 
            'tvl': None, 
            'market_cap_by_total_supply': 160305572290.99585, 
            'last_updated': '2022-09-22T12:25:00.000Z'
        }
    }
}