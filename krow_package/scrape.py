from Krow import *
import json
import pandas as pd
import os

os.remove("datasets/data2.csv")

chain = Chain("http://18.220.46.51:3000/")
x = chain.get_all_avaliable_jobs()
data = json.loads(x.text)
titles, descriptions, IDs = [], [], []
c = 0
for i in data:
    # print (i['title'])
    titles.append(i['title'])

    # print (i['description'])
    descriptions.append(i['description'])

    # print (i['jobID'])
    IDs.append(i['jobID'])
    c += 1
    if c % 100 == 0:
        print ("Processed up to job %s" % c)



df = pd.DataFrame({
    "title": titles,
    "description": descriptions,
    "ID": IDs
})

df.to_csv("datasets/data2.csv")

print ("Saved %s jobs" % len(data))
