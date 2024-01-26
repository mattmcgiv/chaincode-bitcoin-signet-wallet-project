# ser32(i): serialize a 32-bit unsigned integer i as a 4-byte sequence, most significant byte first.
def ser32(i):
    if i < 0 or i >= 2**32:
        raise ValueError("Integer must be in the range 0 <= p < 2**32")
    return i.to_bytes(4, byteorder="big")


# ser256(p): serializes the integer p as a 32-byte sequence, most significant byte first.
def ser256(p):
    if p < 0 or p >= 2**256:
        raise ValueError("Integer must be in the range 0 <= p < 2**256")
    return p.to_bytes(32, byteorder="big")


# serP(P): serializes the coordinate pair P = (x,y) as a byte sequence using SEC1's compressed form: (0x02 or 0x03) || ser256(x), where the header byte depends on the parity of the omitted y coordinate.
def serP(P):
    x = P.x()
    y = P.y()
    # x, y = P
    if y % 2 == 0:
        header = b"\x02"
    else:
        header = b"\x03"
    return header + ser256(x)
