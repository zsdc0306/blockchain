from time import time
from operation import calculate_hash_for_block


class Block(object):
    def __init__(self, index=None, pre_hash=None, time_stamp=None, data=None, hash_val=None):
        self.index = index
        self.pre_hash = str(pre_hash)
        self.time_stamp = time_stamp
        self.data = data
        self.hash_val = str(hash_val)

    def init_first_block(self):
        self.index = 0
        self.pre_hash = "0"
        self.time_stamp = str(time()).split('.')[0]
        self.data = "This is the first block"
        self.hash_val = calculate_hash_for_block(self)


class BlockChain(object):
    def __init__(self):
        self.block_chain = self.get_existing_blockchain()
        self.blochchain_file_name = 'blockchain'
        self.is_exist = True if len(self.block_chain) != 0 else False

    def get_existing_blockchain(self):
        try:
            blockchain = []
            with open(self.blochchain_file_name, 'r') as f:
                for line in f:
                    blockchain += line,
                return blockchain
        except OSError as e:
            print e.message
            return []
        except Exception as e:
            print e.message
            return []


