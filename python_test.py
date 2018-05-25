import requests
import json
from Krow import *


class Tester(object):

    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def test_get(self):
        r = self.session.get("%ssearch" % self.url, json={"data": "mechanical engineer"})
        return r


tester = Tester("http://localhost:3000/")
r = tester.test_get()
# print (r.text)
print (json.loads(r.text)["0"])
chain = Chain("http://18.220.46.51:3000/")
job = chain.get_job(json.loads(r.text)["0"]).data
print ("TITLE: %s" % job['title'])
print ("DESC: %s..." % job['description'][:100])
# exit()
