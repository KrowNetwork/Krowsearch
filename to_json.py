import pandas as pd
import json
import random
import numpy as np

df = pd.read_csv("data.csv")

np.random.shuffle(df.values)

descs = df['jobdescription'].values
titles = df['jobtitle'].values



count = 1000
for i in range(count):
    data = {
            "$class": "network.krow.assets.IntermediateJob",
            "title": titles[i],
            "description": descs[i],
            "tags": ["test", "test2"],
            "payment": 0,
            "paymentType": "DAILY",
            }
    with open("krow_jobs/%s.json" % i, 'w') as f:
        json.dump(data, f)
