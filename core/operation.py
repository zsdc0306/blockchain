import block
import Queue
from hashlib import sha256
import json

class Operation(object):
    def __init__(self):
        self.latest_block = self.get_latest_block()
        self.task_queue = Queue.Queue()


    def init_block(self):
        b = block.Block()
        b.init_first_block()
        b.store_block('w')
        self.latest_block=b

    def init_app(self):
        if self.latest_block is None:
            print "init the first block"
            self.init_block()
            print "init app again"
            self.init_app()
        return True

    def objectify_block(self, block_str):
        block_item = block_str.split(",")
        [index, pre_hash, time_stamp, data, hash_val] = block_item
        b = block.Block()
        b.set_block(index,pre_hash,data, time_stamp,hash_val)
        return b

    def jsontoblock(self,jsonstr):
        block_dict=json.loads(jsonstr)
        newblk=block.Block()
        newblk.set_block(block_dict["index"],block_dict["pre_hash"],block_dict["data"],block_dict["time_stamp"],block_dict["hash_val"])
        return newblk


    def read_block(self,no):
        for line in open(block.blockchain_file_name, "r"):
            line=json.loads(line)
            blockno = line["index"]#line.split(",")[0]
            if no == int(blockno):
                return line
        return None

    def read_blocks(self,start_no):

        keep_adding=False
        ans=[]

        for line in open(block.blockchain_file_name,'r'):
            line = json.loads(line)
            current_block_no=line["index"]#line.split(",")[0]

            if int(current_block_no)==start_no:
                keep_adding=True
            if keep_adding:
                ans.append(line)

        #print ans
        if ans=="":
            return None

        return ans


    def generate_block(self, data):
        new_block = block.Block()
        new_block.set_block(int(self.latest_block.index)+1, self.latest_block.hash_val, data)
        new_block.store_block()
        self.latest_block = new_block
        return new_block

    def get_latest_block(self):
        try:
            with open(block.blockchain_file_name,"r") as f:
                content = f.readlines()
                print content
                if len(content) >= 1:
                    latest_block = content[-1]
                    latest_block = self.jsontoblock(latest_block)#self.objectify_block(latest_block)
                else:
                    print "getting blockchain error"
                    return None
            return latest_block
        except Exception as e:
            print e.message
            return None

    def get_block_chain(self):
        with open(block.blockchain_file_name, 'r+') as f:
            return ''.join(f.readlines())

    def calculate_hash_for_block(self,block):
        return str(sha256(str(block.index) + block.pre_hash + block.time_stamp + block.data).hexdigest())

    def validate_chain(self,chain):

        dataarr = chain #.split("\n")
        dataarr=[ data for data in dataarr if len(data)>0]
        for ind,dblock in enumerate(dataarr):

            if ind==0:
                continue

            # validate dblock with previous block

            current_block= self.jsontoblock(dblock)#self.objectify_block(dblock)
            previous_block= self.jsontoblock(dataarr[ind-1])#self.objectify_block(dataarr[ind-1])

            if previous_block.index+1 != current_block.index or previous_block.hash_val != current_block.pre_hash or self.calculate_hash_for_block(current_block) != current_block.hash_val:
                return False

        return True

    def fit(self,chain):

        with open(block.blockchain_file_name,'r') as f:
            lines=f.readlines()
            last_block_no=int(json.loads(lines[-1])["index"])
            if chain[0]==last_block_no+1:
                return True
        return False




