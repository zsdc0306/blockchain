from P2PFramework import p2p
import math;
import scipy.stats as st
import Consensus.Utilities  as ut
import threading
import time

class handlers():

    def __init__(self, operations):

        self.operations=operations
        pass

# Admin update module
    def admin_update(self,iot,addr,msg):

        print addr,msg

        return

    def update_producers(self,iot,addr,msg):

        producers=msg.split(",")
        print "aa"
        if iot.update_producers(producers):
            print "Successfully updated witnesses/producers"

        return

    def update_sharedkey(self,iot,addr,msg):

        sharedkey=msg
        if iot.update_sharedkey(sharedkey):
            print "Successfully updated shared key"

        return

    # new block method

    def new_block(self,iot1,addr,msg):
        """
        If you get the NBLC command call this handler so that is can check if it is it's turn and if it is add it to the blockchain
        :param iot1:
        :param addr:
        :param msg:
        :return: True or False indicating whether success
        """

        #check turn
        print "entered handler"
        if iot1.producers==None:
            print "Error no witness found"
            return False

        mymac=ut.get_mymac()
        if mymac.lower() in iot1.producers:
            ind=ut.whoseturn(len(iot1.producers))
            print "Turn:",iot1.producers[ind]
            if iot1.producers[ind]==mymac.lower():
                print "my turn";
                # add block
                self.operations.generate_block(msg)


        return True;

    def update_block(self,iot1,addr,msg):

        #call update block function
        pass

    def hell(self,iot,addr,msg):
        print "Message ffrom hell",msg;
        return


class p2pInstance(object):

    def __init__(self,handlers):

        #host='10.0.0.187';
        self.handlers=handlers;
        self.port = 2433
        self.iot1 = p2p.IOTPeer(self.port,'iot1',None,contype="udp")
        self.iot1.addhandler("HELL",self.handlers.hell)
        self.iot1.addhandler("ADMI",self.handlers.admin_update)
        self.iot1.addhandler("PROD",self.handlers.update_producers)
        self.iot1.addhandler("NBLC",self.handlers.new_block)
        self.iot1.addhandler("UBLC",self.handlers.update_block)

    def run_server(self):
        self.iot1.serverloop()


class p2pThread(threading.Thread):

    def __init__(self,handlers):
        self.threadname="p2p"
        threading.Thread.__init__(self)
        self.handlers=handlers
        self.iot=p2pInstance(self.handlers)

    def run(self):
        print "Starting p2p";
        self.iot.run_server()





# Quite useful when the number of Devices are really high
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


#print get_sample(10,0.95,0.05,0.5)