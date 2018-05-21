from Krow import *
import json
import pandas as pd
chain = Chain("http://18.220.46.51:3000/")
x = chain.get_all_avaliable_jobs()
data = json.loads(x.text)
titles, descriptions, IDs = [], [], []
for i in data:
    print (i['title'])
    titles.append(i['title'])

    print (i['description'])
    descriptions.append(i['description'])

    print (i['jobID'])
    IDs.append(i['jobID'])

df = pd.DataFrame({
    "title": titles,
    "description": descriptions,
    "ID": IDs
})

df.to_csv("../data2.csv")
