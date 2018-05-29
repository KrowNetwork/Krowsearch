from Krow import *
import sys
import numpy as np
import pandas as pd
# chain = Chain("http://18.220.46.51:3000/")
ids = input()
ids = ids.split()
df = pd.read_csv("datasets/data2.csv")
for i in ids:
    try:
        x = df.loc[df['ID'] == i]
        # print (list(x["description"]))
        print ("<p>TITLE: %s<br />" % list(x['title'])[0])
        print ("DESC: %s...</p>" % list(x['description'])[0][:100])
    except:
        pass
sys.stdout.flush()
