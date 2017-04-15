import random
from hashlib import sha256


def generate_random_hash():
    return sha256(random.getrandbits(256).to_bytes(256, 'big')).hexdigest()