from mongoDB_init import main2Client

userDocs = main2Client['users']


for userDoc in userDocs.find({},limit = 1):
    print(userDoc)