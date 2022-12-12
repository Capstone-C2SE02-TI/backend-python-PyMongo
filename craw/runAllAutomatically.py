import subprocess
import os
import concurrent.futures
import time

from coinInfo import coinDataHandler
from coinPrice import coinPriceMinutelyHandler
from coinSumInvestment import UpdateCoinSumInvest
from investorCoinBalance import updateInvestorERC20Balances, updateInvestorETHBalances
from investorTotalAsset import investorTotalAssetSnapshot, updateSharkStatus
from investorTXs import updateInvestorTXs2
from utils import logExecutionTime, addExecutionTime

coingecko1 = [coinPriceMinutelyHandler]
coingecko2 = [coinDataHandler]
alchemy = [updateInvestorERC20Balances]
etherscan = [updateInvestorTXs2, updateInvestorETHBalances]
normal = [investorTotalAssetSnapshot, UpdateCoinSumInvest, updateSharkStatus]
other = []
zipAll = coingecko1 + alchemy + etherscan + normal


def executorReplay(function):

    with concurrent.futures.ThreadPoolExecutor() as replayExecutor:
        executionTimeFutureResult = replayExecutor.submit(logExecutionTime,function)
        executionTime = executionTimeFutureResult.result()
        addExecutionTime(function.__name__, executionTime)


if __name__ == '__main__':

    with concurrent.futures.ThreadPoolExecutor() as mainExecutor:
        future_to_functionName = {function.__name__ : mainExecutor.submit(executorReplay,function) for function in zipAll} 

        while future_to_functionName[coinPriceMinutelyHandler.__name__].running():
            time.sleep(5)
        print(f'Executed success {coinPriceMinutelyHandler.__name__} now run {coinDataHandler.__name__}')

        mainExecutor.submit(executorReplay,coinDataHandler)

            
 
