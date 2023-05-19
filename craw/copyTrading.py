from mongoDB_init import main2Client
import requests
import time
userDocs = main2Client['users']

findFilter = {'autoTrading.0': {'$exists': True}}
projection = {'autoTrading': 1, 'walletAddress': 1}


for userDoc in userDocs.find(findFilter, projection):

    _id = str(userDoc['_id'])

    autoTradings = userDoc['autoTrading']
    toAddr = userDoc['walletAddress']

    for autoTrading in autoTradings:

        sharkAddr = autoTrading['sharkAddress']
        fromTokenAddr = autoTrading['fromToken']
        toTokenAddr = autoTrading['toToken']
        ethAmount = autoTrading['ethAmount']

        hashBody = {
            "toTokenAddr": toTokenAddr,
            "receiver": toAddr
        }

        # print(hashBody)
        hashResponse = requests.post(
            "http://127.0.0.1:8000/copyTrading/hash", data=hashBody)

        if hashResponse.json()["message"] != "Success":
            print("Copy Trading fail")
            continue

        input = hashResponse.json()["input"]

        print(input)
        autoTradingBody = {
            "dex_address": "0x",
            "input_data": input,
            "eth_amount": ethAmount,
            "receiver": toAddr
        }

        print(autoTradingBody)
        autoTradingResponse = requests.post(
            "http://127.0.0.1:8000/copyTrading/auto", data=autoTradingBody)
        print(autoTradingResponse.text)

        time.sleep(1)
        # TODO danh dau transaction da duoc copy


# 1 user l cac cap
# 1 transaction moi, thi cac user co dang ky cap nay se giao dich
# thi sau khi giao dich thi phai danh dau la da~ co giao dich
