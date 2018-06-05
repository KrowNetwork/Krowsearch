from Krow import *
import requests
import time


now = time.time()
# r = requests.get("http://18.220.46.51:4200/search?key=42fc1e42-5eb8-4a8f-8904-7c58529f0f58&term=developer")#, json={"term": "software developer"})
r = requests.get("http://localhost:4200/search?key=42fc1e42-5eb8-4a8f-8904-7c58529f0f58&term=developer")#, json={"term": "software developer"})
print (r)
print (r.text)
print (time.time() - now)
