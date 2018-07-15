import pandas as pd
import time
import json
import sys
import requests
from json.decoder import JSONDecodeError
# import unicode
r = requests.get("http://18.220.46.51:3000/api/queries/GetAvailableJobs")
n = {}
data = ["title", "description", "employerID", "created", "tags", "jobType"]

# def special_print(p):
#     # data = ["title", "description", "employerID", "postDate", "tags", "jobType"]
#     for i in 

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
        z = {}
        for a in data:
            # print (n[i])
            # print (type(n[i]))
            b = json.loads(n[i])
            if a == "description":
                d = b[a][:100]
            elif a == "jobType":
                if a not in b:
                    b[a] = "NONE"
                    break
            else:
                d = b[a]

            b[a] = d
        bb = "{"
        for i in b:
            b[i].replace('"', "++")
            bb += '"%s": "%s",' % (i, b[i])
        bb = bb[:-1] + "}"

        x += bb + "~+/="
        # x += str(b["created"]) + " "
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
    # print (" ")
    print (x)
    sys.stdout.flush()
