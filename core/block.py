from time import time
from hashlib import sha256
from operation import calculate_hash_for_block

blockchain_file_name = 'blockchain'

class Block(object):
    def __init__(self, index=None, pre_hash=None, data=None, hash_val=None, time_stamp=str(time()).split('.')[0]):
        self.index = index
        self.pre_hash = str(pre_hash)
        self.time_stamp = time_stamp
        self.data = data
        self.hash_val = str(hash_val)

    def init_first_block(self):
        self.index = 0
        self.pre_hash = "0"
        self.data = "This is the first block"
        self.hash_val = self.calculate_hash_for_block()

    def store_block(self):
        block_str = self.stringfy_block()
        with open(blockchain_file_name, 'a') as f:
            f.write(block_str)

    def stringfy_block(self):
        content = [str(self.index), self.pre_hash, str(self.time_stamp), self.data, self.hash_val]
        return ','.join(content) + '\n'

    def calculate_hash_for_block(self):
        return calculate_hash_for_block(self)

    def validate_block(self, pre_block):
        return False if pre_block.index + 1 != self.index or pre_block.hash != self.pre_hash or \
                 self.calculate_hash_for_block() != self.hash_val else True


class BlockChain(object):
    def __init__(self, blockchain_str=None):
        self.block_chain = self.__get_existing_blockchain()
        self.is_exist = True if len(self.block_chain) != 0 else False
        self.lastest_block = self.block_chain[-1] if len(self.block_chain) != 0 else None

    def load_existing_blockchian(self):
        self.block_chain = self.__get_existing_blockchain()

    def __get_existing_blockchain(self):
        try:
            blockchain = []
            with open(blockchain_file_name, 'r') as f:
                content = f.readlines()
                for line in content:
                    blockchain += self.__load_block(line),
                return blockchain
        except OSError as e:
            print e.message
            return []
        except Exception as e:
            print e.message
            return []

    def __load_block(self, block_str):
        block_item = Block()
        block_item.index, block_item.pre_hash, block_item.data, block_item.hash_val, block_item.time_stamp = \
            block_str.split(',')
        return block_item
