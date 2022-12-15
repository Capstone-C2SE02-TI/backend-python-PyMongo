# # export requirements.txt 
# exportCmd = 'pipreqs --force'

# #  handle list in .env
# #  1. Seperate by ,
# cmc_keys = 'a, b, c'

# # // 2.1. use split and strip to access every 
# for key in cmc_keys.split(','):
#     print(key.strip())

# # // 2.2 to list 
# cmc_keys = [i.strip() for i in cmc_keys.split(',')]


# # // Get doc have a specific field
# # havePricesDoc = metadataDocs.find({'prices' : { '$exists' : True}})

# # => Change exists to False for query non exists field


# # append token TXs 
# tokenDocs.update_one(
#         {'_id' : '0xcffad3200574698b78f32232aa9d63eabd290703'},
#         { 
#             '$push':{ 
#                 'TXs': { 
#                         '$each': [ {"blockNumber":"4730207","timeStamp":"1513240363",},{"blockNumber":"4764973","timeStamp":"1513764636",}] 
#                     } 
#                 } 
#         }
#     )

# symbolTest = metadataDocs.find_one({'contract_address.contract_address' : { '$eq' : contractAddressReq}})


# # CMC to CGC FlOW
# # CMC TOKEN SORT BY MARKETCAP IN ETH : 
# CMC_ListingLatest_API = 'v1/cryptocurrency/listings/latest'
# TOKENADDRESSES = []
# CGC_API = f'coins/ethereum/contract/{TOKENADDRESS}' # FOR TOKENADDRESS IN TOKENADDRESSES
# # CALL CGC_API with TOKENADDRESSES => TOKENID[]
# # TOKENID[] CAN BE USE IN CGC API
# TOKENID = CGC API : coins/{TOKENID} => DATA => ADDDATA TO MONGODB


# # CGC PRICE FOLLOW
# CGC API = f'coins/{TokenId}/market_chart/range?vs_currency=usd&from={from}&to={to}'

# # get Doc dont have TXs[0]
# for investorDoc in investorDocs.find({'TXs.0' : {'$exists' : False}}):
