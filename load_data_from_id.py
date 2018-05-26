from Krow import *
import sys
import numpy as np
chain = Chain("http://18.220.46.51:3000/")
ids = input()
ids = ids.split()
for i in ids:
    job = chain.get_job(i).data
    print ("<p>TITLE: %s<br />" % job['title'])
    print ("DESC: %s...</p>" % job['description'][:100])
sys.stdout.flush()
