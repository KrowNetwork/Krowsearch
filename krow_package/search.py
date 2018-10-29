import requests
import json
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

headers = {'x-api-key': 'qLBrEwIv690nAbMfVHB965WC3KfoC1VpvkBjDUiBfVOG5mTzlUlwkckKLerAUxxv'}
r = requests.get("http://18.220.46.51:3000/api/queries/GetUsers", headers=headers)
data = {}
for i in r.json():
    data[ i['applicantID']] = i["firstName"] + " " + i["lastName"]
    # print (i['firstName'] + " " + i["lastName"])
    # print (i['applicantID'])

def search(name):
    name = name.split()
    res = []
    stop = False
    for i in data:
        a = data[i]
        # print (i)
        for n in name:
            if n in a.lower():
                res.append([a, i, similar(a.lower(), " ".join(name).lower())])
                
            
    # for i in res:
        # print (i)

    res.sort(key=lambda x: x[2])
    res = res[::-1]
    s = ""
    for i in res:
        i = str(i).replace("[", "").replace("]", "|").replace("'", "")
        s += i
    print (s[:-1])
while True:
    text = input()
    search(text)