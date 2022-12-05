from mongoDB_init import client
import requests
import json
import time


categoryDocs = client['categories']
coinDocs = client['coins']

def initCategoryMetadata():

    filter = {
        'num_tokens': {'$exists': 0}
    }

    print(categoryDocs.update_many(
        filter,
        {'$set': {
            'num_tokens': 0
        }}
    ).modified_count)


def getCategories():

    statusCode = -1
    while statusCode != 200:

        response = requests.get(
            'https://api.coingecko.com/api/v3/coins/categories/list')

        statusCode = response.status_code
        if statusCode == 404:
            print(f'Dont have price for {id}')
            return []

        if statusCode != 200:
            print('Now sleep for 70 Secs')
            print(f'Status error code: {statusCode}')
            time.sleep(65)
            continue

    return response.json()


def pushCategoriesToMongo(categories):

    for category in categories:
        category['_id'] = category['category_id']
        del category['category_id']

    categoryDocs.insert_many(
        categories
    )

def updateCategoriesNumToken():

    categories = {}

    for coin in coinDocs.find({},{'categories' : 1}):

        for category in coin['categories']:
            
            if category not in categories:
                categories[category] = 1
            else:
                categories[category] += 1

    for category, num_tokens in categories.items():
        categoryDocs.update_one(
            {'name' : category},
            {'$set' : {'num_tokens' : num_tokens}}
        )
        
        



# updateCategoriesNumToken()
