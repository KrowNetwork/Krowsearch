from Krow import *
import requests
import time

for i in range(100):
    try:
        now = time.time()
        r = requests.get("http://18.220.46.51:4200/search?key=42fc1e42-5eb8-4a8f-8904-7c58529f0f58&term=designer")#, json={"term": "software developer"})
        # r = requests.get("http://localhost:4200/search?key=dgf463d4-4fg5-55la-3z0f-7c78ft9s9z64&term=dev")#, json={"term": "software developer"})
        print (r)
        z = r.text

        z = z.split("~+/=")

        print (z)
        print (time.time() - now)
        print (i + 1)
    except Exception as e:
        print (r.text)
        print (e)
        exit()