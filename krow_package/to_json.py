import pandas as pd
import json
import random
import numpy as np

df = pd.read_csv("datasets/data.csv")

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
            "location": random.choice(["New York City", "Sacramento", "Denver", "Austin, Texas", "Newark", "Charlotte", "Roanoke, VA"]),
            "jobType": "ENTRY_LEVEL",
            "contract": "You do work, you get paid!"
            }
    with open("krow_jobs/%s.json" % i, 'w') as f:
        json.dump(data, f)
