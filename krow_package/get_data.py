import pandas as pd
import time
import json
import sys
import requests
# import unicode
r = requests.get("http://18.220.46.51:3000/api/queries/GetAvailableJobs")
n = {}
for i in r.json():
    x = json.dumps(i)#.encode('utf8')
    # i = json.loads(i)
    n[i['jobID']] = x

while True:
    id = input()
    # print (i)
    x = ""
    for i in id.split():
        x += (str(n[i]) + ",")

    sys.stdout.write(str(x[:-1]))#.encode( "utf-8"))
    sys.stdout.flush()
