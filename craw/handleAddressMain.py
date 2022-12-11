from mongoDB_init import mainClient
import json
investorDocs = mainClient['investors']

def writeToJson(id, score):

    f = open('./IdHandleManual.json')
    data = json.load(f)

    data[str(id)] = score
    
    f.close()

    json_object = json.dumps(data, indent=4)

    with open("./IdHandleManual.json", "w") as outfile:
        outfile.write(json_object)

def handleAddressFromMain():
    for investorDoc in investorDocs.find({},{'transactionsHistory' : 1}, batch_size = 5):

        investorId = investorDoc['_id']
        print(f'Process address of {investorId}')
        maxScoreAddress = ''
        maxScore = -1

        addressScore = {}
        for transaction in investorDoc['transactionsHistory'][:100]:
            addressFrom = transaction['from']
            addressTo = transaction['to']

            if addressFrom not in addressScore:
                addressScore[addressFrom] = 0
            else:
                addressScore[addressFrom] += 1

            if addressTo not in addressScore:
                addressScore[addressTo] = 0
            else:
                addressScore[addressTo] += 1
        
        for address,score in addressScore.items():

            if maxScore == score:
                print(f'Conflict in investor id : {investorId}')
                # writeToJson(investorId,maxScore)

            if maxScore < score:
                maxScore = score
                maxScoreAddress = address

        print(f'Address of investor id {investorId} is {maxScoreAddress} with score = {maxScore}')

        investorDocs.update_one(
            {'_id' : investorId},
            {'$set' : {'walletAddress' : maxScoreAddress}}
        )

handleAddressFromMain()

        
        

            




    
    
    