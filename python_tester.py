from Krow import *
import requests
import time
import json

for i in range(100):
    try:
        now = time.time()
        # r = requests.get("http://18.220.46.51:4200/search?key=dgf463d4-4fg5-55la-3z0f-7c78ft9s9z64&term=designer")#, json={"term": "software developer"})
        r = requests.get("http://localhost:4200/search?key=dgf463d4-4fg5-55la-3z0f-7c78ft9s9z64&term=designer")#, json={"term": "software developer"})
        print (r)
        z = r.text

        z = z.split("~+/=")
        print (json.loads(z[-1]))

        # print (z[-1])
        # print (r.headers)
        print (time.time() - now)
        print (i + 1)
    except Exception as e:
        print (r.text)
        print (e)
        exit()