from ecc.util import *

class Block:

    def __init__(self, version, prev_block, merkle_root, timestamp, bits, nonce):
        self.version = version
        self.prev_block = prev_block
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += self.prev_block[::-1]
        result += self.merkle_root[::-1]
        result += int_to_little_endian(self.timestamp, 4)
        result += self.bits
        result += self.nonce
        return result

    def hash(self):
        return hash256(self.serialize())[::-1]

    def bip9(self):
        return self.version >> 29 == 0b001

    def bip91(self):
        return self.version >> 4 & 1 == 1

    def bip141(self):
        return self.version >> 1 & 1 == 1

    def difficulty(self):
        return 0xffff * 256**(0x1d-3) / self.target()

    def target(self):
        return bits_to_target(self.bits)

    def check_pow(self):
        proof = little_endian_to_int(hash256(self.serialize()))
        return proof < self.target()

    def calculate_new_bits(first_block, self):
        time_differential = self.timestamp - first_block.timestamp
        if time_differential > PERIOD * 4:
            time_differential = PERIOD * 4
        if time_differential < PERIOD // 4:
            time_differential = PERIOD // 4
        return self.target() * time_differential // PERIOD

    @classmethod
    def parse(cls, s):
        version = little_endian_to_int(s.read(4))
        prev_block = s.read(32)[::-1]
        merkle_root = s.read(32)[::-1]
        timestamp = little_endian_to_int(s.read(4))
        bits = s.read(4)
        nonce = s.read(4)
        return cls(version, prev_block, merkle_root, timestamp, bits, nonce)

