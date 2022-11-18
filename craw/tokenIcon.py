from firebase_init import db
import requests
import re
import time
from bs4 import BeautifulSoup

tokenDocs = db.collection(u'tokens')

baseTokenURL = 'https://coinmarketcap.com/currencies/'

def updateTokenIcon(contractAddress):

    # Using slug to get the url
    tokenDoc = tokenDocs.document(contractAddress)
    tokenSlug = tokenDoc.get().to_dict()['slug']

    tokenCMCURL = baseTokenURL + tokenSlug

    html = requests.get(tokenCMCURL)
    soup = BeautifulSoup(html.text,'html.parser')

    divTag = soup.select_one('div.nameHeader')

    imgTag = divTag.select('img')

    tokenDoc.update({'iconURL' : imgTag[0]['src']}) 
    





def crawAllTokenIcon(runTimes):
    tokenDocsStream = tokenDocs.stream()

    for tokenDoc in tokenDocsStream:
        tokenSlug = tokenDoc.to_dict()['slug']
        print(f'Update icon url for {tokenSlug}')
        updateTokenIcon(tokenDoc.id)

        time.sleep(0.5)



crawAllTokenIcon(0,0)


