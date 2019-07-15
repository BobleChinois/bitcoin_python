import hashlib

def hash256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def string_to_byte(s):
    return s.encode()

def generate_secret(s):
    raw_secret = string_to_byte(s)
    return int.from_bytes(hash256(raw_secret), 'big')

