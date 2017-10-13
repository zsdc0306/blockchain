from hashlib import sha256
import block


def generate_block(data):
    b = get_latest_block()
    new_block = block.Block(int(b.index)+1, b.hash_val, data)
    new_block.store_block()
    return


def calculate_hash_for_block(block):
    return str(sha256(str(block.index) + block.pre_hash + block.time_stamp + block.data).hexdigest())


def get_latest_block():
    blockchain = block.BlockChain().load_existing_blockchian()  # get the bloch chain. It is a list of block object
    return blockchain.block_chain[-1] if blockchain.is_exist else None


def get_block_chain():
    blockchain = block.BlockChain()
    blockchain.load_existing_blockchian()
    return blockchain.block_chain


def receive_block_chain(blockchain_str):
    block_chain = block.BlockChain()
    block_chain.load_existing_blockchian()
    block_obj = ojbectfy_blockchain(blockchain_str)
    lastest_block = block_chain.lastest_block
    if block_obj.validate_block(lastest_block):
        block_obj.store_block()
        return True
    else:
        return False


def ojbectfy_blockchain(str):
    block_item = str.split(",")
    [index, pre_hash, time_stamp, data, hash_val] = block_item
    b = block.Block(index,pre_hash,data, hash_val, time_stamp)
    return b



