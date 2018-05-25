import requests
import json

class Tester(object):

    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def test_get(self):
        r = self.session.get("%ssearch" % self.url, json={"data": "hr"})
        print (r.text)


tester = Tester("http://localhost:3000/")
tester.test_get()
# exit()
