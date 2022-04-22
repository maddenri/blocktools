from tools import *


class Inv:
    def __init__(self, blockchain):
        self.inv_count = var_int(blockchain)
        self.inv_vectors = ""
        for i in range(0, self.inv_count):
            self.inv_vectors += f"{InvVec(blockchain)}\n"

    def __str__(self):
        return f"{'=' * 50} Inventory {'=' * 48}\n" \
               f"{'Inv Entries:':15}{self.inv_count}\n" \
               f"{self.inv_vectors}"


class InvVec:
    def __init__(self, blockchain):
        self.type = uint32(blockchain)
        self.hash = double_hash_char(blockchain, 32)

    def __str__(self):
        return f"{'=' * 50} Inventory Vector {'=' * 41}\n" \
               f"{'Inv Type:':15}{self.type}\n" \
               f"{'Hash:':15}{self.hash}"





