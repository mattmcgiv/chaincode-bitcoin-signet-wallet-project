# Deserialize the extended key bytes and return a JSON object
# https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#serialization-format
# 4 byte: version bytes (mainnet: 0x0488B21E public, 0x0488ADE4 private; testnet: 0x043587CF public, 0x04358394 private)
# 1 byte: depth: 0x00 for master nodes, 0x01 for level-1 derived keys, ....
# 4 bytes: the fingerprint of the parent's key (0x00000000 if master key)
# 4 bytes: child number. This is ser32(i) for i in xi = xpar/i, with xi the key being serialized. (0x00000000 if master key)
# 32 bytes: the chain code
# 33 bytes: the public key or private key data (serP(K) for public keys, 0x00 || ser256(k) for private keys)
def deserialize_key(b: bytes) -> object:
    deserialized_key = {
        "version": b[0:4],
        "depth": b[4],
        "fingerprint": b[5:9],
        "child_number": b[9:13],
        "chaincode": b[13:45],
        "key": b[45:78],  # TODO: verify this
    }
    print(deserialized_key)
    return deserialized_key


# TODO: implement this to use in derive_priv_child()
