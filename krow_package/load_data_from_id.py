from Krow import *
import sys
import numpy as np
import pandas as pd
# chain = Chain("http://18.220.46.51:3000/")
ids = input()
ids = ids.split()
df = pd.read_csv("datasets/data2.csv")
for i in ids:
    x = df.loc[df['ID'] == i]
    print ("<p>TITLE: %s<br />" % x['title'])
    print ("DESC: %s...</p>" % x['description'][:100])
sys.stdout.flush()
