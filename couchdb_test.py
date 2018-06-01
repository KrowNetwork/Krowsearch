import couchdb

db = couchdb.Server("http://localhost:4369")
for dbname in db:
    print(dbname)
