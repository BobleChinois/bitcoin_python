import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def hash256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def string_to_byte(s):
    return s.encode()

def generate_secret(s):
    raw_secret = string_to_byte(str(s))
    return int.from_bytes(hash256(raw_secret), 'big')

def to_string(*args):
    a = [args]
    b = ""
    for thing in args[:]:
        b += str(thing)
    return b

def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result

def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])

def little_endian_to_int(b):
    return int.from_bytes(b, 'little')

def int_to_little_endian(a, length):
    return a.to_bytes(length, 'little')
