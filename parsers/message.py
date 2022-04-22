from tools import *


class Message:
    def __init__(self, blockchain):
        self.magic = char(blockchain, 4)
        self.command = packet_content(blockchain)
        self.length = uint32(blockchain)
        self.position = blockchain.tell()
        self.checksum = double_hash_char(blockchain, self.length, True)
        blockchain.seek(self.position + 4)

    def __str__(self):
        return f"{'#' * 50} Message {'#' * 50}\n" \
               f"{'Magic Bytes:':15}{self.magic}\n" \
               f"{'Command:':15}{self.command}\n" \
               f"{'Block-size:':15}{self.length}\n" \
               f"{'Checksum:':15}{self.checksum}"
