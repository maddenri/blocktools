from tools import *


class Version:
    def __init__(self, blockchain):
        self.version = int32(blockchain)
        self.services = uint64(blockchain)
        self.timestamp = int64(blockchain)
        self.address_receive = NetAddress(blockchain)
        self.address_from = NetAddress(blockchain)
        self.nonce = uint64(blockchain)
        self.user_agent = var_str(blockchain)
        self.start_height = int32(blockchain)
        self.relay = c_bool(blockchain)

    def __str__(self):
        return f"{'=' * 50} Version {'=' * 50}\n" \
               f"{'Protocol Vers:':15}{self.version}\n" \
               f"{'Services:':15}{self.services}\n" \
               f"{'Timestamp:':15}{to_utc(self.timestamp)}\n" \
               f"{'Nonce:':15}{self.nonce}\n" \
               f"{'User Agent:':15}{self.user_agent}\n" \
               f"{'Start Height:':15}{self.start_height}\n" \
               f"{'Relay:':15}{self.relay}\n" \
               f"{'=' * 50} Network Address Received {'=' * 33}\n" \
               f"{self.address_receive}\n"\
               f"{'=' * 50} Network Address From {'=' * 37}\n" \
               f"{self.address_from}"


class NetAddress:
    def __init__(self, blockchain):
        self.services = uint64(blockchain)
        self.ipv_6_4 = char(blockchain, 16)
        self.port = uint16(blockchain)

    def __str__(self):
        return f"{'Services:':15}{self.services}\n" \
               f"{'IPv6/4:':15}{self.ipv_6_4}\n" \
               f"{'Port:':15}{self.port}"
