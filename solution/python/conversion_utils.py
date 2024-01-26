# parse256(p): interprets a 32-byte sequence as a 256-bit number, most significant byte first.
def parse256(byte_sequence):
    if len(byte_sequence) != 32:
        raise ValueError("Byte sequence must be exactly 32 bytes long")
    return int.from_bytes(byte_sequence, byteorder="big")
