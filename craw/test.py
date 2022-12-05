from mongoDB_init import client

coinDocs = client['coins']

coinDocs.update_many(
    {},
    [{'$unset' : 'id'}]
)