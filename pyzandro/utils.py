import struct

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
