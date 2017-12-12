from time import time
from hashlib import sha256
import csv
import json

blockchain_file_name = 'db.json'


class Block(object):

    def __init__(self, index=None, pre_hash=None, time_stamp=None, data=None, hash_val=None):
        self.index = index
        self.pre_hash = pre_hash
        self.time_stamp = time_stamp
        self.data = data
        self.hash_val = data

    def set_block(self, index, pre_hash, data, time_stamp=None, hash_val=None):
        self.index = int(index)
        self.pre_hash = str(pre_hash)
        self.data = data
        self.time_stamp = str(time()).split('.')[0] if time_stamp is None else time_stamp
        self.hash_val = self.calculate_hash_for_block() if hash_val is None else str(hash_val)

    def init_first_block(self):
        self.index = 0
        self.pre_hash = "0"
        self.data = "This is the first block"
        self.time_stamp = "1510816805"#str(time()).split('.')[0]
        self.hash_val = self.calculate_hash_for_block()

    def store_block(self, mode='a'):
        block_str = json.dumps(self.__dict__)#self.stringify_block()
        #print block_str
        try:
            with open(blockchain_file_name, mode) as f:
                f.write(block_str)
                f.write('\n')
        except Exception as e:
            print e.message

    def stringify_block(self):
        content = [str(self.index), self.pre_hash, str(self.time_stamp), self.data, self.hash_val]
        #print self.pre_hash
        return ','.join(content)

    def calculate_hash_for_block(self):
        return str(sha256(str(self.index) + self.pre_hash + self.time_stamp + self.data).hexdigest())

    def validate_block(self, pre_block):
        return False if pre_block.index + 1 != self.index or pre_block.hash_val != self.pre_hash or \
                 self.calculate_hash_for_block() != self.hash_val else True


