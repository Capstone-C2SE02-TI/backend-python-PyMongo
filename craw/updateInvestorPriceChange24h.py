from mongoDB_init import client,mainClient

investorDocs = client['investors']
main_investorDocs = mainClient['investors']

def updateInvestorPriceChange24h():
    totalModifiedCount = 0
    for investorDoc in investorDocs.find({}, {'snapshots' : 1}):
        investorAddress = investorDoc['_id']
        
        snapshots = investorDoc.get('snapshots',{})

        if snapshots == {}:
            continue

        sortedSnapshots = sorted(snapshots, reverse=True)

        try:
            latestUnix = sortedSnapshots[0]
            secondLatestUnix = sortedSnapshots[1]
        except:
            print(f'Dont have snapshots in {investorAddress} bruh')
            continue

        currentValue = snapshots[latestUnix]
        last24HourValue = snapshots[secondLatestUnix]

        if int(last24HourValue) == 0:
            continue

        ratioAssetAfter24h = float(currentValue)/last24HourValue

        updateResult = main_investorDocs.update_one(
            {'walletAddress' : investorAddress},
            {'$set' : {'percent24h': (ratioAssetAfter24h - 1)*100}}
        )

        totalModifiedCount += updateResult.modified_count
        print(investorAddress,totalModifiedCount)
        # percent24h

    print(totalModifiedCount, 'investor have been update 24h price')