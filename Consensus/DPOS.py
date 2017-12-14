from time import time
import Utilities as ut
import json

#Hardcoded in all Iots

producers=[1,2,3]

#print ut.gettime_ntp();

total_blocks=3

data=None
with open("../AdminInfo.json") as file:
    data=json.load(file)
    print data
    file.close()


#for i in range(1,100):
 #   ut.whoseturn(3)

print ut.validate_timestamp(0,1509866656)
print ut.validate_timestamp(1, 1509866669)
print "done"


'''
take ip from address, get its corresponding mac address
check producer array for it
if in producer array:
    get its index
send the timestamp and index to validate_timestamp function
if result is true:
    its true
else:
    its false
'''