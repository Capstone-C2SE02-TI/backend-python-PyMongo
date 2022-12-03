from mongoDB_init import client

coinDocs = client['coins']
investorDocs = client['investors']


def getSumInvestBySymbol():

    SumInvestBySymbol = {}

    filter = {}
    projection = {'coins' : 1}
    for investor in investorDocs.find(filter,projection):
        investorCoinBalances = investor['coins']

        for symbol,coinAsset in investorCoinBalances.items():

            if symbol not in SumInvestBySymbol:
                SumInvestBySymbol[symbol] = 0
            else:
                SumInvestBySymbol[symbol] += coinAsset

    return SumInvestBySymbol


def UpdateCoinSumInvest():

    SumInvestBySymbol = getSumInvestBySymbol()

    for symbol, sumInvest in SumInvestBySymbol.items():

        updateResult = coinDocs.update_one(
            {'symbol' : symbol},
            {'$set' : {'sumInvest' : sumInvest}}
        )

        if updateResult.modified_count == 1:
            print(f'Update sum invest of {symbol} is {sumInvest}')

UpdateCoinSumInvest()
