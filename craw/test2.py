from mongoDB_init import client

investorDocs = client['investors']

investorDocs.update_many(
    {},
    {'$set' : {'coins' : {}}}
)