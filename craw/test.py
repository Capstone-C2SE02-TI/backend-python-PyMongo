from mongoDB_init import mainClient

userDocs = mainClient['tokens']


for userDoc in userDocs.find():
    print(userDoc['_id'])