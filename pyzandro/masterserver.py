import socket
import time
import struct
from io import BytesIO
from enum import Enum
from .huffman import huffencode, huffdecode
from .utils import next_string
from .utils import next_long
from .utils import next_short
from .utils import next_ushort
from .utils import next_float
from .utils import next_byte
from .utils import split_hostport
from .utils import PyZandroException
from .utils import log_message
import traceback as tb

MSC_SERVERBLOCK = 8
MSC_BEGINSERVERLISTPART = 6
MSC_ENDSERVERLIST = 2
MSC_ENDSERVERLISTPART = 7
LAUNCHER_MASTER_CHALLENGE = 5660028
MASTER_SERVER_VERSION = 2

def send_query(address, timeout):
    log_message(call='masterserver.send_query()', address=address, timeout=timeout)
    host, port = split_hostport(address)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    unencoded_query = struct.pack('<lh',
        LAUNCHER_MASTER_CHALLENGE, MASTER_SERVER_VERSION)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    huffencoded_query = huffencode(unencoded_query)
    client.sendto(huffencoded_query, (host, port))
    log_message(call='[masterserver] sendto()', unencoded_query=unencoded_query, send_data=huffencoded_query, address=address)
    client.settimeout(timeout)
    return client

def get_packet(client):
    recv_data = client.recv(1500)
    try:
        huffdecoded = huffdecode(recv_data)
    except Exception as e:
        traceback = ''.join(tb.format_exception(None, e, e.__traceback__))
        log_message(call='[masterserver] recv() huffdecode failed', traceback=traceback, recv_data=recv_data)
        raise
    log_message(call='[masterserver] recv()', huffdecoded=huffdecoded, recv_data=recv_data)
    return huffdecoded

def parse_packet(huffdecoded_packet, r={}):
    streamobj = BytesIO(huffdecoded_packet)
    r['status'] = next_long(streamobj)
    if r['status'] == 6:
        r['status_meaning'] = 'MSC_BEGINSERVERLISTPART'
    elif r['status'] == 3:
        r['status_meaning'] = 'MSC_IPISBANNED'
    elif r['status'] == 4:
        r['status_meaning'] = 'MSC_REQUESTIGNORED'
    elif r['status'] == 5:
        r['status_meaning'] = 'MSC_WRONGVERSION'
    else:
        r['status_meaning'] = 'UNKNOWN'
    if r['status'] != 6:
        raise PyZandroException("Unexpected response: " + repr(r))

    assert r['status'] == MSC_BEGINSERVERLISTPART, \
        f"Invalid status code {r['status']} from master server, expected MSC_BEGINSERVERLISTPART (6). " + \
        f"huffdecoded_packet: {repr(huffdecoded_packet)}"

    packet_number = next_byte(streamobj)
    r['server_block'] = next_byte(streamobj)

    assert r['server_block'] == MSC_SERVERBLOCK, \
        f"Invalid server block {r['server_block']} from master server, expeted MSC_SERVERBLOCK (8). " + \
        f"full huffdecoded_packet: {repr(huffdecoded_packet)}"

    if 'ip_list' not in r:
        r['ip_list'] = []

    while True:
        number_of_servers_on_ip = next_byte(streamobj)
        if number_of_servers_on_ip == 0:
            break
        ip_A = next_byte(streamobj)
        ip_B = next_byte(streamobj)
        ip_C = next_byte(streamobj)
        ip_D = next_byte(streamobj)

        for i in range(number_of_servers_on_ip):
            port = next_ushort(streamobj)
            r['ip_list'].append(f'{ip_A}.{ip_B}.{ip_C}.{ip_D}:{port}')

    # either MSC_ENDSERVERLIST or MSC_ENDSERVERLISTPART
    r['closing_status'] = next_byte(streamobj)
    assert r['closing_status'] in [MSC_ENDSERVERLIST, MSC_ENDSERVERLISTPART], \
        f"Invalid closing status {r['closing_status']} from master server, " + \
        f"expeted MSC_ENDSERVERLIST (2) or MSC_ENDSERVERLISTPART (7). " + \
        f"full response: {repr(response)}"
    if r['closing_status'] ==  MSC_ENDSERVERLIST:
        r['closing_status_meaning'] = 'MSC_ENDSERVERLIST'
    if r['closing_status'] ==  MSC_ENDSERVERLISTPART:
        r['closing_status_meaning'] = 'MSC_ENDSERVERLISTPART'
    return r

def query_master(master_address, timeout=2):
    client = send_query(master_address, timeout)
    parsed = {}
    while True:
        huffdecoded_packet = get_packet(client)
        parsed = parse_packet(huffdecoded_packet, parsed)
        if parsed['closing_status'] == MSC_ENDSERVERLIST:
            break
    return parsed['ip_list']
