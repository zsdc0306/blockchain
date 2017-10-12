class Block(object):
    def __init__(self, index, pre_hash, time_stamp, data, hash_val):
        self.index = index
        self.pre_hash = str(pre_hash)
        self.time_stamp = time_stamp
        self.data = data
        self.hash_val = str(hash_val)