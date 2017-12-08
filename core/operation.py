import block
import Queue
from hashlib import sha256

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

    def ojbectfy_block(self, block_str):
        block_item = block_str.split(",")
        [index, pre_hash, time_stamp, data, hash_val] = block_item
        b = block.Block()
        b.set_block(index,pre_hash,data, time_stamp,hash_val)
        return b

    def read_block(self,no):
        for line in open(block.blockchain_file_name, "r"):
            blockno = line.split(",")[0]
            if no == int(blockno):
                return line
        return None

    def read_blocks(self,start_no):

        keep_adding=False
        ans=""
        for line in open(block.blockchain_file_name,'r'):
            current_block_no=line.split(",")[0]

            if int(current_block_no)==start_no:
                keep_adding=True
            if keep_adding:
                ans+=line

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
                    latest_block = self.ojbectfy_block(latest_block)
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


    def receive_block(self, block_str):
        block_obj = self.ojbectfy_block(block_str)
        if block_obj.validate_block(self.latest_block):
            block_obj.store_block()
            print "valid block received, updated to blockchain"
            latest_block = block_obj
            return True
        else:
            if block_obj.index - self.latest_block.index != 1:
                print "missing blocks, broadcast to get the missing block"
                self.resolve_conflict()
            elif block_obj.pre_hash != self.latest_block.hash_val:
                print "invalid block, dropping"
                return False

    def resolve_conflict(self):
        pass

    def response_syn_block(self, received_block_str):
        received_block = self.ojbectfy_block(received_block_str)
        last_index = self.latest_block.index
        cur_index = received_block.index
        diff = last_index - cur_index
        blockchain = self.get_block_chain()
        ret_block_list = blockchain.split('\n')[-diff:]
        # response ret_block_list
        return ret_block_list

    def calculate_hash_for_block(self,block):
        return str(sha256(str(block.index) + block.pre_hash + block.time_stamp + block.data).hexdigest())

    def validate_chain(self,chain):

        dataarr = chain.split("\n")
        dataarr=[ data for data in dataarr if len(data)>0]
        for ind,dblock in enumerate(dataarr):

            if ind==0:
                continue

            # validate dblock with previous block

            current_block= self.ojbectfy_block(dblock)
            previous_block= self.ojbectfy_block(dataarr[ind-1])
            #return False if pre_block.index + 1 != self.index or pre_block.hash_val != self.pre_hash or \
             #               self.calculate_hash_for_block() != self.hash_val else True
            if previous_block.index+1 != current_block.index or previous_block.hash_val != current_block.pre_hash or self.calculate_hash_for_block(current_block) != current_block.hash_val:
                return False

        return True




