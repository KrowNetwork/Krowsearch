import couchdb

db = couchdb.Server("http://18.220.46.51:5984")
for dbname in db:
    print(dbname)
db = db['composerchannel_krow']
for i in db.view("_all_docs"):
    if ("\x00Asset:network.krow.assets.Job\x00c5b8f44a-d818-48c7-b301-805bae81007d\x00" in i['id']):
        print (i)
        print (db.get(i['id']))
# for i in db(params={'key': 'Asset'}):
#     print (i)
# for i in db.view("_design/GetAllJobsDoc"):#["composerchannel_krow"]["Asset:network.krow.assets.Job c5b8f44a-d818-48c7-b301-805bae81007d"]:
#     print (i)
#
# for i in db["composerchannel_krow"]:#["_design/_replicator"]:#["Asset:network.krow.assets.Job c5b8f44a-d818-48c7-b301-805bae81007d"]:
#     print (i)


# Asset:network.krow.assets.Job c5b8f44a-d818-48c7-b301-805bae81007d
