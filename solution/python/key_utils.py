from decode_utils import base58_decode
from ecdsa import SigningKey, SECP256k1


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
    return deserialized_key


def compress_public_key(public_key):
    x = public_key.pubkey.point.x()
    y = public_key.pubkey.point.y()
    prefix = 0x02 if y % 2 == 0 else 0x03
    return bytes([prefix]) + x.to_bytes(32, "big")


def derive_compressed_pubkey_from_privkey(private_key_bytes):
    signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    public_key = signing_key.verifying_key
    compressed_pubkey = compress_public_key(public_key)
    return compressed_pubkey
