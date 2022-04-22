import hashlib


def double_sha256(data, checksum=False):
    if checksum:
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()[0:4]
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def double_hash_char(data, length, checksum=False):
    binary_hex = double_sha256(data.read(length))
    if checksum:
        return ''.join('{:02x}'.format(i) for i in binary_hex[0:4])
    return ''.join('{:02x}'.format(i) for i in binary_hex)


