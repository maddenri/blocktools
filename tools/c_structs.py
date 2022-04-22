import binascii
import struct


def c_bool(data):
    return struct.unpack('?', data.read(1))[0]


def char(data, length):
    return binascii.hexlify(data.read(length)).decode('utf-8')


def uint8(data):
    return ord(data.read(1))


def uint16(data):
    return struct.unpack('H', data.read(2))[0]


def int32(data):
    return struct.unpack('i', data.read(4))[0]


def uint32(data):
    return struct.unpack('I', data.read(4))[0]


def int64(data):
    return struct.unpack('q', data.read(8))[0]


def uint64(data):
    return struct.unpack('Q', data.read(8))[0]


def var_int(data):
    size = uint8(data)
    if size < 0xfd:
        return size
    if size == 0xfd:
        return uint16(data)
    if size == 0xfe:
        print('here32')
        return uint32(data)
    if size == 0xff:
        print('here64')
        return uint64(data)
    return -1


def var_str(data):
    return bytes.fromhex(char(data, var_int(data))).decode('utf-8')


def packet_content(data):
    """Message Type followed by nulls (0x00)"""
    return data.read(12).replace(b'\x00', b'').decode('utf-8')
