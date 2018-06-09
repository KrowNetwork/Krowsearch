import pandas as pd
import time
import json
import sys
import requests
from json.decoder import JSONDecodeError
# import unicode
r = requests.get("http://18.220.46.51:3000/api/queries/GetAvailableJobs")
n = {}
def special_print(p):
    pp = "{"
    for i in p:
        pp += "\"%s\": %s," % (i, p[i])
    # pp = pp + "}"
    pp = pp[:-1] + "}"
    return pp 

for i in json.loads(r.text):
    x = json.dumps(i)
    # print (x)
    # x = json.loads(x)
    n[i['jobID']] = x

while True:
    # x = json.loads("{}")
    x = ""
    id = input()
    # print (i)
    
    c = 0
    for i in id.split():
        # x[str(c)] = n[i]
        x += n[i] + "~+/="
        c += 1

    x = x[:-4]
    # sys.stdout.write#(json.dumps(x))#.encode( "utf-8"))
    # print(json.dumps(str(x)))#.encode( "utf-8"))
    
    # x = special_print(x)
    # try:
    #     json.loads(x)
    #     print (x)
    # except JSONDecodeError:
    #     print (x[:-1])
    print (x)
    sys.stdout.flush()
