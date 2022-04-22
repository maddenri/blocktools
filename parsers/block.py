from tools import *
from parsers.transaction import Tx


class Block:
    def __init__(self, blockchain):
        self.transactions = ""
        self.header = BlockHeader(blockchain)

        for i in range(0, self.header.txn_count):
            self.transactions += f"{Tx(blockchain)}\n"

    def __str__(self):
        return f"{'#' * 50} Block {'#' * 52}\n" \
               f"{self.header}\n" \
               f"{self.transactions}"


class BlockHeader:
    def __init__(self, blockchain):
        self.version = int32(blockchain)
        self.prev_block = double_hash_char(blockchain, 32)
        self.merkle_root = double_hash_char(blockchain, 32)
        self.timestamp = uint32(blockchain)
        self.bits = uint32(blockchain)
        self.nonce = uint32(blockchain)
        self.txn_count = var_int(blockchain)

    def __str__(self):
        return f"{'=' * 50} Block Header {'=' * 45}\n" \
               f"{'Version:':15}{self.version}\n" \
               f"{'Previous Hash:':15}{self.prev_block}\n" \
               f"{'Merkle Root:':15}{self.merkle_root}\n" \
               f"{'Timestamp:':15}{to_utc(self.timestamp)}\n" \
               f"{'Difficulty:':15}{self.bits}\n" \
               f"{'Nonce:':15}{self.nonce}\n" \
               f"{'Txn Count:':15}{self.txn_count}"
