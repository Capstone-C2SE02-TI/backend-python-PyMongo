from mongoDB_init import client
from investorCoinBalance import test


investorDocs = client['coins']
test()