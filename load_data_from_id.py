from Krow import *
import sys
import numpy as np
chain = Chain("http://18.220.46.51:3000/")
job = chain.get_job(np.array(sys.stdin.readlines())[0]).data
print ("TITLE: %s<br />" % job['title'])
print ("DESC: %s..." % job['description'][:100])
sys.stdout.flush()
