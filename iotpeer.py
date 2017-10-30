
from P2PFramework import p2p
import math;
import scipy.stats as st

#Quite useful when the number of Devices are really high
def get_sample(N,confidence,error,variability=None):
    '''
    Using Central Limit theorem, calculate the sample size required for the given confidence and error

    :param N:
    :param confidence:
    :param error:
    :param variability:
    :return:
    '''

    if confidence>1 or confidence<0:
        return None;

    if not variability:
        variability=0.5;

    z=-st.norm.ppf(variability*(1-confidence));
    n=(math.pow(z,2)*variability*(1-variability))/math.pow(error,2)

    if N<n:
        n=(n*N)/(n+N-1);

    return int(n);


def hell(msg):
    print "Message ffrom hell",msg;
    return


host='10.0.0.187';
port=2429
#iot1=p2p.IOTPeer(port,'iot1',None,contype="udp")
#iot1.addhandler("HELL",hell)
#iot1.serverloop();




'''
peerid="Iot1"
idlen=len(peerid)
msg = struct.pack("!4sL%ds%ds" % (msglen,idlen), msgtype, msglen, msgdata,peerid)
print msg;
print msg.encode("hex")

msg = struct.pack("!4sL%d"% msglen,msgtype,msglen)
print msg;
print msg.encode("hex")
'''


print get_sample(10,0.95,0.05,0.5)