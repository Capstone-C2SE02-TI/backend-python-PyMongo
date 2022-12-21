import requests
from bs4 import BeautifulSoup
import random
import concurrent.futures
import json
# get the list of free proxies


def getProxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        proxyAttributes = row.find_all('td')
        proxyType = proxyAttributes[4].text
        isSupportHttps = proxyAttributes[6].text

        if proxyType == 'elite proxy' and isSupportHttps == 'yes':
            proxy = ':'.join([row.find_all('td')[0].text,
                             row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies

unActiveProxy = '0:0'
def extract(proxy):
    # this was for when we took a list into the function, without conc futures.
    #proxy = random.choice(proxylist)

    with open('./utils/userAgents.json') as userAgentsFile:
        userAgents = json.load(userAgentsFile)

    headers = {'User-Agent': random.choice(userAgents)}
    try:
        # change the url to https://httpbin.org/ip that doesnt block anything
        r = requests.get('https://httpbin.org/ip', headers=headers,
                         proxies={'http': proxy, 'https': proxy}, timeout=2)
        print(r.json(), r.status_code)
    except:
        return unActiveProxy

    return proxy
    
def getBlockProxiesJson():
    with open('./utils/blockProxies.json', 'r') as blockProxyFile:
        blockProxies = json.load(blockProxyFile)

    return blockProxies

def isFailureProxy(proxy):

    blockProxies = getBlockProxiesJson()

    return (proxy ==  unActiveProxy) or (proxy in blockProxies)

def getActivateProxiesFromWeb():

    proxies = getProxies()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futureResults = executor.map(extract, proxies)

    activateProxies = []
    for futureResult in futureResults:
        proxy = str(futureResult)

        if isFailureProxy(proxy):
            continue

        activateProxies.append(proxy)
    return activateProxies

def activeProxiesRemove(proxy):
    with open('./utils/activeProxies.json', 'r') as activeProxiesFile:
        activateProxies = json.load(activeProxiesFile)
    
    if proxy in activateProxies.keys():
        del activateProxies[proxy]

    json_object = json.dumps(activateProxies, indent=4)

    with open('./utils/activeProxies.json', 'w') as outfile:
        outfile.write(json_object)


def BlockProxy(proxy):
    with open('./utils/blockProxies.json', 'r') as blockProxiesFile:
        blockProxies = json.load(blockProxiesFile)

    if proxy not in blockProxies:
        blockProxies.append(proxy)
        activeProxiesRemove(proxy)
        
    json_object = json.dumps(blockProxies, indent=4)

    with open('./utils/blockProxies.json', 'w') as outfile:
        outfile.write(json_object)

def LowProxy(proxy):
    with open('./utils/lowProxies.json', 'r') as lowProxiesFile:
        lowProxies = json.load(lowProxiesFile)

    if proxy not in lowProxies:
        lowProxies.append(proxy)
        activeProxiesRemove(proxy)
        
    json_object = json.dumps(lowProxies, indent=4)

    with open('./utils/lowProxies.json', 'w') as outfile:
        outfile.write(json_object)

def getActivateProxiesJson():
    with open('./utils/activeProxies.json', 'r') as activeProxiesFile:
        activateProxies = json.load(activeProxiesFile)

    return activateProxies

def activeProxiesToJson(newActivateProxies):

    with open('./utils/activeProxies.json', 'r') as activeProxiesFile:
        activateProxies = json.load(activeProxiesFile)

    with open('./utils/blockProxies.json', 'r') as blockProxiesFile:
        blockProxies = json.load(blockProxiesFile)
        
    print(newActivateProxies)
    for proxy in newActivateProxies:
        if (proxy not in activateProxies) and (blockProxies not in blockProxies):
            activateProxies[proxy] = 5
            print(f'New proxy : {proxy}')

    json_object = json.dumps(activateProxies, indent=4)

    with open('./utils/activeProxies.json', 'w') as outfile:
        outfile.write(json_object)

def addTimeoutProxy(proxy):
    with open('./utils/activeProxies.json', 'r') as activeProxiesFile:
        activateProxies = json.load(activeProxiesFile)

    proxyTimeout = activateProxies[proxy]
    newProxyTimeout = proxyTimeout + 5

    if newProxyTimeout >= 20:
        LowProxy(proxy)
        return

    activateProxies[proxy] = newProxyTimeout
    json_object = json.dumps(activateProxies, indent=4)

    with open('./utils/activeProxies.json', 'w') as outfile:
        outfile.write(json_object)

def subTimeoutProxy(proxy):
    with open('./utils/activeProxies.json', 'r') as activeProxiesFile:
        activateProxies = json.load(activeProxiesFile)

    proxyTimeout = activateProxies[proxy]
    newProxyTimeout = proxyTimeout - 10

    if newProxyTimeout < 5:
        return

    activateProxies[proxy] = newProxyTimeout
    json_object = json.dumps(activateProxies, indent=4)

    with open('./utils/activeProxies.json', 'w') as outfile:
        outfile.write(json_object)


def fullCycle():
    newProxies = []

    newProxies += getProxies()

    activeProxiesToJson(newProxies)

if __name__ == '__main__':
    # print(getActivateProxiesFromWeb())
    LowProxy("102.130.192.231:8080")
    # BlockProxy('3.90.130.193:80')

    
    
