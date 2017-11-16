import block
import iotpeer

class Operation(object):
    def __init__(self):
        self.latest_block = self.get_latest_block()
        self.handlers = iotpeer.handlers(self)
        self.p2p_server = iotpeer.p2pThread(self.handlers)

    def start_p2p(self):
        self.p2p_server.start()

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
                if len(content) >= 1:
                    latest_block = content[-2]
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


    def stopp2p(self):
        self.p2p_server._stop()
        pass





