import os
import struct
import time
from base64 import b64encode
import json
import traceback as tb

log_config = {'log_target': None}

def set_log_target(target):
    log_config['log_target'] = target

def base64ify(val):
    """
    bytes -> b64encode(val)
    anythine else -> passthru
    """
    if isinstance(val, bytearray) or isinstance(val, bytes):
        return str(b64encode(val), 'utf-8')
    return val

def log_message(**kwargs):
    if log_config['log_target'] is None:
        return
    d = {'unix_time': time.time()}
    for k,v in kwargs.items():
        d[k] = base64ify(v)
    try:
        d['stack'] = ''.join(tb.format_stack())
    except:
        pass
    with open(log_config['log_target'], 'a', encoding='utf-8') as f:
        f.write(json.dumps(d))
        f.write('\n')


def split_hostport(hostport):
    host, port = hostport.split(':')
    return (host, int(port))

def next_string(streamobj):
    ba = bytearray()
    while True:
        b = (streamobj.read(1))[0]
        if b == 0:
            return bytes(ba)
        ba.append(b)
    return bytes(ba)

def next_long(streamobj):
    return struct.unpack('I', streamobj.read(4))[0]

def next_short(streamobj):
    return struct.unpack('h', streamobj.read(2))[0]

def next_ushort(streamobj):
    return struct.unpack('H', streamobj.read(2))[0]

def next_float(streamobj):
    return struct.unpack('f', streamobj.read(4))[0]

def next_byte(streamobj):
    return streamobj.read(1)[0]

class PyZandroException(Exception):
    pass
