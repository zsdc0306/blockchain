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


def receive_block(block_str):
    block_obj = ojbectfy_block(block_str)
    if block_obj.validate_block(latest_block):
        block_obj.store_block()
        print "valid block received, updated to blockchain"
        global latest_block
        latest_block = block_obj
        return True
    else:
        if block_obj.index - latest_block.index != 1:
            print "missing blocks, broadcast to get the missing block"
            resolve_conflict()
        elif block_obj.pre_hash != latest_block.hash_val:
            print "invalid block, dropping"
            return False


def resolve_conflict():
    pass





