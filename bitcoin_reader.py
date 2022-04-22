import io
import struct
import socket
import random
import argparse
import logging
from parsers import Block, Inv, Message, Version, Tx
from tools import char, double_sha256, get_current_time


def create_message(magic, command, payload):
    """Create message structure"""
    checksum = double_sha256(payload, True)
    return struct.pack('<I12sI4s', magic, command.encode(), len(payload), checksum) + payload


def create_network_address(ip_address, port):
    """IP and Port are encoded in big endian"""
    return struct.pack('>8s16sH', b'\x01', bytearray.fromhex("00000000000000000000ffff")
                                  + socket.inet_aton(ip_address), port)


def create_version_payload(peer_ip):
    """Create version payload in order to connect with node on Bitcoin Network"""
    version = 70016
    services = 0
    timestamp = get_current_time()
    address_receive = create_network_address(peer_ip, 8333)
    address_from = create_network_address("127.0.0.1", 8333)
    nonce = random.getrandbits(64)
    user_agent = b'\x00'
    start_height = 0
    relay = True
    return struct.pack('<iQq26s26sQ1si?', version, services, timestamp, address_receive,
                       address_from, nonce, user_agent, start_height, relay)


def send_request(command, payload):
    """Send message with payload to node on Bitcoin Network"""
    magic_value = 0xd9b4bef9
    version_message = create_message(magic_value, command, payload)
    s.send(version_message)


def send_getdata_request(parser, remainder):
    """Upon receiving an 'inv' payload from node, reply with 'getdata' payload
       to get either 'tx' or 'block' payload back in response"""
    if parser == Inv:
        send_request('getdata', remainder)


def print_message_and_get_full_payload(buffer, message, remainder, response):
    """Output the parsed message structure to console. TCP connection may not send full
       payload in a single response and so s.recv(buffer_size) is continuously called while response is
       less than the length of the payload. Also io.BufferedReader has DEFAULT_BUFFER_SIZE
       of 8192 bytes which is why it is necessary to increase buffer_size with each loop iteration"""
    logging.info(message)
    while len(remainder) < message.length:
        buffer_increase = len(remainder) + buffer
        response = io.BufferedReader(io.BytesIO(remainder + s.recv(buffer)), buffer_size=buffer_increase)
        remainder = response.peek()
        response.flush()
    return remainder, response


def print_payload(message, parser, response):
    """Output the payload to console in either parsed or bytes format"""
    logging.info(f"{'Payload:':15}{response.read(message.length)}" if parser is None else parser(response))
    return response.peek()


def handle_response(buffer):
    """Handle response from node. Any payloads of type listed in 'parser_dict' will be appropriately parsed
       whereas payloads not listed here will be output to console in 'bytes' format"""
    magic_value = 'f9beb4d9'
    message_structure_length = 24
    parser_dict = {'block': Block, 'inv': Inv, 'tx': Tx, 'version': Version}
    response = io.BufferedReader(io.BytesIO(s.recv(buffer)))
    message = Message(response)
    remainder, response = print_message_and_get_full_payload(buffer, message, response.peek(), response)
    while remainder:
        parser = parser_dict[message.command] if message.command in parser_dict.keys() else None
        send_getdata_request(parser, remainder)
        remainder = print_payload(message, parser, response)
        if len(remainder) < message_structure_length:
            response = io.BufferedReader(io.BytesIO(remainder + s.recv(buffer)))
        if char(io.BytesIO(response.peek()), 4) == magic_value:
            message = Message(response)
            remainder, response = print_message_and_get_full_payload(buffer, message, response.peek(), response)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[
        logging.FileHandler("bitcoin_reader.log"),
        logging.StreamHandler()
    ])
    parser = argparse.ArgumentParser(description='Establish TCP connection to node on bitcoin '
                                                 'network and read received messages from that node')
    parser.add_argument('--peer_ip_address', type=str, default='100.16.216.41')
    parser.add_argument('--peer_tcp_port', type=int, default=8333)
    parser.add_argument('--buffer_size', type=int, default=1024)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.peer_ip_address, args.peer_tcp_port))
        send_request('version', create_version_payload(args.peer_ip_address))
        send_request('verack', bytearray.fromhex("000000005df6e0e2"))
        while True:
            handle_response(args.buffer_size)
