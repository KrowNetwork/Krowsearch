from chain import Chain
import time
# import test_suite

chain = Chain("http://18.220.46.51:3000/")

times = []
for i in range(10000):
    if ((i + 1) % 100 == 0):
        print (i + 1)
    t = time.time()
    x = chain.get_applicant("63dac59b-a670-4812-9b83-e300e30dd2c3") 
    times.append(time.time() - t)

print (sum(times)/len(times))

