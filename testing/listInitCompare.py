import time
  
# initialize lists to save the times
from mongoDB_init import client
investorDocs = client['investors']

forLoopTime = []
whileLoopTime = []
listComprehensionTime = []
starOperatorTime = []
  
# repeat the process for 500 times
# and calculate average of times taken.
count = 0
runTimes = 10
for k in range(runTimes): 
    count += 1
    print(count)
    # start time
    start = time.time()
    # declare empty list
    investorAddresses = []
    latestBlocks = []
    # run a for loop for 10000 times
    for investorDoc in investorDocs.find({},{'TXs' : 0}):
        investorAddresses.append(investorDoc['_id'])
        latestBlocks.append(investorDoc['latestBlockNumber'])
    # stop time
    stop = time.time()
    forLoopTime.append(stop-start)
  
    # start time
    start = time.time()
    # declare an empty list
    latestBlockNumber = []
    investorAddresses = []
    i = 0
    # run a for loop 10000 times
  
  
    start = time.time()
    # list comprehension to initialize list
    latestBlockNumber = [investorDoc['_id'] for investorDoc in investorDocs.find({},{'TXs' : 0})] 
    investorAddresses = [investorDoc['latestBlockNumber'] for investorDoc in investorDocs.find({},{'TXs' : 0})] 

    stop = time.time()
    listComprehensionTime.append(stop-start)

  
  
  
print("Average time taken by for loop: " + str(sum(forLoopTime)/runTimes))
print("Average time taken by list comprehensions: " + str(sum(listComprehensionTime)/runTimes))