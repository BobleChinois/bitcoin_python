import hashlib
from re import match

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
SIGHASH_ALL = 1

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

def decode_base58(s):
    # takes a str in base58 and returns a bytes object
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    return verify_checksum(num)

def verify_checksum(num):
    # returns a byte object without the checksum if successful
    to_check = bytes.fromhex(format(num, 'x'))
    checksum = to_check[-4:]
    if hash256(to_check[:-4])[:4] != checksum:
        raise ValueError('bad address {} {}'.format(checksum,
            hash256(to_check[:-4])[:4]))
    return to_check[:-4]

"""def decode_wif(wif):
    res = decode_base58(wif)
    if res[-1:] == b'\x01':
        res = res[1:-1]
    else:
        res = res[1:]
    return big_endian_to_int(res)
"""
def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])

def little_endian_to_int(b):
    return int.from_bytes(b, 'little')

def int_to_little_endian(a, length):
    return a.to_bytes(length, 'little')

def big_endian_to_int(b):
    return int.from_bytes(b, 'big')

def read_varint(s):
    i = s.read(1)[0]
    if i == 0xfd:
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        return little_endian_to_int(s.read(8))
    else:
        return i

def encode_varint(i):
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise ValueError('integer too large: {}'.format(i))

def find_duplicate(key, filename):
    with open(filename, "r") as file:
        for line in file:
            if line.rstrip('\n') == str(key):
                return True
        return False

def isop(s):
    return match("OP_", s)

def h160_to_p2sh_address(h160, testnet=False):
    if testnet:
        prefix = b'\xc4'
    else:
        prefix = b'\x05'
    return encode_base58_checksum(prefix + h160)
