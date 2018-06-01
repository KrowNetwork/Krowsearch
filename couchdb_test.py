import couchdb

db = couchdb.Server("http://18.220.46.51:5984")
for dbname in db:
    print(dbname)
