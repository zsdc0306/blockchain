from P2PFramework import p2p
import math
import scipy.stats as st
import Consensus.Utilities as ut
import threading
import time
import operator
import json

blockchain_file_name = 'blockchain'

class shared_thread(threading.Thread):


    msglist=[]
    winlock=threading.Lock()

    def __init__(self,msg):
        threading.Thread.__init__(self)
        self.msg=msg
        pass;

    def run(self):
        with shared_thread.winlock:
            shared_thread.msglist.append(self.msg)
            #print shared_thread.msglist
        pass;


class Handles(object):

    window = False

    def __init__(self, operations):
        self.operations = operations
        self.window=False

    # Admin update module
    def admin_update(self,iot,addr,msg):

        print "Incomplete module"

        return

    # UPDATE PRODUCERS
    def update_producers(self,iot,addr,msg):

        producers=msg.split(",")

        if iot.update_producers(producers):
            print "Successfully updated witnesses/producers"

        return

    # UPDATE SHARED KEY
    def update_sharedkey(self,iot,addr,msg):

        sharedkey=msg
        if iot.update_sharedkey(sharedkey):
            print "Successfully updated shared key"

        return


    # send missing block
    # Command - RQMB
    def send_missing_block(self,iot1,addr,msg):

        # I

        required_block=int(msg)
        print "Requested block is ",required_block

        block_data=self.operations.read_blocks(required_block)
        blocs_arr_json=json.dumps(block_data)
        #print block_data
        if block_data:

            for jblock in block_data:
                iot1.send_data("RCMB",json.dumps(jblock))
        else:
            print "I do not have the %d block myself"%required_block
            return
        return

    # RECEIVE MISSING BLOCK
    # Command - RCMB
    def missing_block_update(self,iot1,addr,msg):


        # add data and address to queue if the window is still open

        if Handles.window:
            shared_thread((addr,json.loads(msg))).start()
        else:
            print "Window closed"

        pass

    # temp functionality - opening window for sometime
    # Command - WIND
    def window_open(self,iot1,addr,msg):


        if Handles.window:
            Handles.window=False
        Handles.window=True
        time.sleep(10)
        Handles.window=False
        self.compare()
        return

    # compare received blocs
    def compare(self):

        '''
        get msgs from unique address
        filter by size
        choose the first biggest one
        '''

        temp = {}
        print "Evaluating all broadcast responses"

        # mapping it to a dictionary in the format addr:msg where addr is the IP address
        for ind,msg in enumerate(shared_thread.msglist):

            addr,data=msg

            if addr[0] not in temp:
                # validate data blocks individually and also if the block fits my blockchain
                temp[addr[0]]=[]
                print data
                # dirty fix as sometimes data appears as list and other times as single dicts
                if type(data)==list:
                    data=data[0]
                if data not in temp[addr[0]]:
                    temp[addr[0]].append(data)
            else:
                if data not in temp[addr[0]]:
                    temp[addr[0]].append(data)

        # chain is received in random order, need to sort before validating and remove duplicates

        # Validate chain
        for addr in temp:
            print addr,temp[addr];
            newlist=sorted(temp[addr], key=lambda k: k['index'])
            temp[addr]=newlist
            if self.operations.validate_chain(newlist):
                print "chain is valid"
            else:
                del temp[addr]

        # sort all chains
        biggest_chain=None
        sorted_chains = sorted(temp.items(), key=operator.itemgetter(1),reverse=True)
        searching_chain=True
        print sorted_chains

        # get the biggest chain
        print "searching for biggest chain"
        # while searching_chain:
        #
        #     if len(sorted_chains)<1:
        #         biggest_chain=None
        #         break
        #
        #     biggest_chain=sorted_chains[0][1]
        #     if self.operations.fit(biggest_chain):
        #         print " found a biggest chain that fits"
        #         searching_chain=False
        #     else:
        #         sorted_chains=sorted_chains[1:]
        # print "biggest chain is ",biggest_chain

        if len(sorted_chains)>0:
            biggest_chain=sorted_chains[0][1]

        if biggest_chain==None:
            return

        start_index=int(biggest_chain[0]["index"])

        # Store the latest block
        newcontent = ''
        try:
            with open('db.json', 'r') as f:
                content = f.readlines()

                if len(content) >= 1:

                    for ind,line in enumerate(content):
                        if int(json.loads(line)["index"])==start_index:
                            newcontent=content[:ind]+biggest_chain
                            break

                #print newcontent

        except Exception as e:
            print e.message

        # clear the message window
        shared_thread.msglist=[]

        #write new blockchain
        try:
            with open(blockchain_file_name,'w') as f:
                for content in newcontent:

                    f.write(json.dumps(content))
                    f.write("/n")
        except Exception as e:
            print e.message

        return

    # update blockchain
    # command - UBLC

    def update_bc(self, iot1, addr, msg):

        bc = self.operations.jsontoblock(json.loads(msg))#self.operations.ojbectfy_block(msg)
        print bc.data
        if bc.validate_block(self.operations.latest_block):
            print "valid block"
            bc.store_block()
            self.operations.latest_block = bc
            return True
        else:
            if ((int(bc.index) - int(self.operations.latest_block.index)) != 1):
                print "I am missing blocks, so broadcasting the missing block"
                # start timer
                Handles.window=True
                iot1.send_data("RQMB",str(self.operations.latest_block.index))
                time.sleep(10)
                Handles.window=False
                # stop timer

                # compare all collected data and choose the block after validation
                self.compare()
                # DATA FROM QUEUE

            elif bc.pre_hash != self.operations.latest_block.hash_val:
                print "invalid block, dropping"
                return False

        return False



    # new block method
    # command - NBLC

    def new_block(self,iot1,addr,msg):
        """
        If you get the NBLC command call this handler so that is can check if it is it's turn and if it is add it to the blockchain
        :param iot1:
        :param addr:
        :param msg:
        :return: True or False indicating whether success
        """

        #check turn
        #print "entered new block handler"

        if iot1.producers==None:
            print "Error no witness found"
            return False

        mymac=ut.get_mymac()
        if mymac.lower() in iot1.producers:
            ind=ut.whoseturn(len(iot1.producers))
            print "It is the Turn of",iot1.producers[ind]
            if iot1.producers[ind]==mymac.lower():
                print "Producing";
                # add block
                newblock=self.operations.generate_block(msg)
                data=json.dumps(newblock.__dict__)
                #content = [str(newblock.index), newblock.pre_hash, str(newblock.time_stamp), newblock.data, newblock.hash_val]
                #data = ','.join(content)
                # broadcast latest block
                iot1.send_data("UBLC",data)


        return True;



class p2pInstance(object):

    def __init__(self,handlers):


        self.handlers=handlers;
        self.port = 2433
        self.iot1 = p2p.IOTPeer(self.port,'iot1',None,contype="udp")
        self.iot1.addhandler("ADMI",self.handlers.admin_update)
        self.iot1.addhandler("PROD",self.handlers.update_producers)
        self.iot1.addhandler("NBLC",self.handlers.new_block)
        self.iot1.addhandler("UBLC",self.handlers.update_bc)
        self.iot1.addhandler("RQMB", self.handlers.send_missing_block)
        self.iot1.addhandler("RCMB",self.handlers.missing_block_update)
        self.iot1.addhandler("WIND",self.handlers.window_open)

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


