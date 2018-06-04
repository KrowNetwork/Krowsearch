import pandas as pd
import time
import json
import sys
import requests
r = requests.get("http://18.220.46.51:3000/api/queries/GetAvailableJobs")
n = {}
for i in r.json():
    n[i['jobID']] = i
while True:
    id = input()
    # print (i)
    print (n[id]])
