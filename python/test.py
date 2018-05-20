from Krow import *
import test_suite

chain = Chain("http://18.220.46.51:3000/")

x = test_suite.test_all(chain)
for i in x:
    print (i)
