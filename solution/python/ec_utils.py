from ecdsa import SigningKey, SECP256k1


# point(p): returns the coordinate pair resulting from EC point multiplication (repeated application of the EC group operation) of the secp256k1 base point with the integer p.
def point(p):
    return SECP256k1.generator * int.from_bytes(p, "big")
