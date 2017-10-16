import block

def init_block():
    b = block.Block()
    b.init_first_block()
    b.store_block()


def init_app():
    global latest_block
    latest_block = get_latest_block()
    if latest_block is None:
        print "init the first block"
        init_block()
        print "init app again"
        init_app()
    return True


def ojbectfy_block(str):
    block_item = str.split(",")
    [index, pre_hash, time_stamp, data, hash_val] = block_item
    b = block.Block()
    b.set_block(index,pre_hash,data, time_stamp,hash_val)
    return b


def generate_block(data):
    new_block = block.Block()
    new_block.set_block(int(latest_block.index)+1, latest_block.hash_val, data)
    new_block.store_block()
    global latest_block
    latest_block = new_block
    return new_block


def get_latest_block():
    try:
        with open(block.blockchain_file_name,"r") as f:
            content = f.readlines()
            if len(content) >= 1:
                latest_block = content[-1]
                latest_block = ojbectfy_block(latest_block)
            else:
                print "getting blockchain error"
                return None
        return latest_block
    except Exception as e:
        print e.message
        return None


def get_block_chain():
    with open(block.blockchain_file_name, 'r+') as f:
        return f.readlines()


def receive_block_chain(blockchain_str):
    block_chain = block.BlockChain()
    block_chain.load_existing_blockchain()
    block_obj = ojbectfy_block(blockchain_str)
    latest_block = block_chain.get_latest_block()
    if block_obj.validate_block(latest_block):
        block_obj.store_block()
        return True
    else:
        return False





