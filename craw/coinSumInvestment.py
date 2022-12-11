from mongoDB_init import crawlClient
from utils import logExecutionTime, isExistedCoinSymbol
coinDocs = crawlClient['coins']
investorDocs = crawlClient['investors']


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

        if updateResult.modified_count == 0:
            print(f'Cant update sum invest in {symbol}. Sum invest = {sumInvest}')

if __name__ == '__main__':
    function = UpdateCoinSumInvest
    logExecutionTime(function)