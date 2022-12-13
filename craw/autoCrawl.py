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
zipAll = alchemy + etherscan + normal + other


def executorReplay(function):

    while True:
        with concurrent.futures.ThreadPoolExecutor() as replayExecutor:
            executionTimeFutureResult = replayExecutor.submit(logExecutionTime,function)
            executionTime = executionTimeFutureResult.result()
            addExecutionTime(function.__name__, executionTime)
        sleepSecs = 600 - executionTime

        if sleepSecs <= 0:
            continue

        time.sleep(sleepSecs)

def specialTreatment():
    while True:
        with concurrent.futures.ThreadPoolExecutor() as replayExecutor:
            executionTimeFutureResult = replayExecutor.submit(logExecutionTime,coinPriceMinutelyHandler)
            executionTime = executionTimeFutureResult.result()
            addExecutionTime(coinPriceMinutelyHandler.__name__, executionTime)

            executionTimeFutureResult = replayExecutor.submit(logExecutionTime,coinDataHandler)
            executionTime = executionTimeFutureResult.result()
            addExecutionTime(coinDataHandler.__name__, executionTime)
        
if __name__ == '__main__':

    with concurrent.futures.ThreadPoolExecutor() as mainExecutor:
        future_to_functionName = {function.__name__ : mainExecutor.submit(executorReplay,function) for function in zipAll} 
        mainExecutor.submit(specialTreatment)
        

            
 
