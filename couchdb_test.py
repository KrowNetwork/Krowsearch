import couchdb

db = couchdb.Server("http://18.220.46.51:4369")
for dbname in db:
    print(dbname)
