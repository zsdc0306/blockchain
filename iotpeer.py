
from P2PFramework import p2p

def hell(msg):
    print "Message ffrom hell",msg;
    return

host='10.0.0.187';
port=2429
iot1=p2p.IOTPeer(port,'iot1',host,contype="udp")
iot1.addhandler("HELL",hell)
iot1.serverloop();




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
