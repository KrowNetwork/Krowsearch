from Krow import *
import requests

r = requests.get("http://18.220.46.51:4200/search?key=42fc1e42-5eb8-4a8f-8904-7c58529f0f58", json={"term": "test"})
print (r)
print (r.text)
