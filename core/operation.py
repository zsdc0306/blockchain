from hashlib import sha256


def validate_block(new_block, pre_block):
    """
    :param new_block: Block
    :param pre_block: Block
    :return: Boolean
    """
    return False if pre_block.index + 1 != new_block.index or pre_block.hash != new_block.pre_hash or \
                    calculate_hash_for_block(new_block) != new_block.hash else True


def calculate_hash_for_block(block):
    return str(sha256(block.index + block.pre_hash + block.timestamp + block.data))


def generate_block(data):
    pass


def get_latest_block():
    pass