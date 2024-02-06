import binascii
import hashlib
import struct
from Crypto.Hash import SHA256, RIPEMD160
from ecdsa import SigningKey, SECP256k1
from bip32 import BIP32, HARDENED_INDEX


def base58_decode_and_remove_checksum(base58check_string: str) -> bytes:
    decoded_bytes = base58_decode(base58check_string)
    return remove_checksum(decoded_bytes)


def base58_decode(base58_string: str) -> bytes:
    big_integer = convert_base_58_string_to_integer(base58_string)
    converted_bytes = big_integer.to_bytes(
        (big_integer.bit_length() + 7) // 8, byteorder="big"
    )
    return converted_bytes


# def compress_public_key(public_key):
#     x = public_key.pubkey.point.x()
#     y = public_key.pubkey.point.y()
#     prefix = 0x02 if y % 2 == 0 else 0x03
#     return bytes([prefix]) + x.to_bytes(32, "big")


def compress_public_key(public_key):
    """
    Compress a given ECDSA public key using the SECP256k1 curve.

    Args:
    public_key (VerifyingKey): The ECDSA public key to compress.

    Returns:
    str: The compressed public key as a hexadecimal string.
    """
    x = public_key.pubkey.point.x()
    y = public_key.pubkey.point.y()
    prefix = b"\x02" if y % 2 == 0 else b"\x03"
    # return binascii.hexlify(v).decode("utf-8")
    return prefix + x.to_bytes(32, byteorder="big")

# check txinwitness of a P2WPKH transaction against a list of our wallet's public keys
def contains_our_pubkey(txinwitness, public_keys):
    if len(txinwitness) < 2:
        return False  # Not a valid txinwitness array for P2WPKH
    public_keys_hex = [pubkey.hex() for pubkey in public_keys]

    for pubkey_hex in public_keys_hex:
        print(pubkey_hex, txinwitness[1])
        if pubkey_hex == txinwitness[1]:
            raise Exception("Found our pubkey in txinwitness")
            # return True  # Found our pubkey in txinwitness
        # else:
        # raise Exception("Pubkey not found in txinwitness")
    return False


def convert_base_58_string_to_integer(base_58_string):
    base58_alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    integer_result = 0
    power_of_base = 0
    reversed_string = base_58_string[::-1]
    for char in reversed_string:
        integer_value = base58_alphabet.find(char)
        integer_result += integer_value * (58**power_of_base)
        power_of_base += 1
    return integer_result


def deserialize_key(b: bytes) -> object:
    deserialized_key = {
        "version": b[0:4],
        "depth": b[4:5],
        "fingerprint": b[5:9],
        "child_number": b[9:13],
        "chaincode": b[13:45],
        "key": b[45:78],
    }
    # print("deserialized_key", deserialized_key)
    return deserialized_key


# def derive_compressed_pubkey_from_privkey(private_key_bytes):
#     signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
#     public_key = signing_key.verifying_key
#     compressed_pubkey = compress_public_key(public_key)
#     return compressed_pubkey


def derive_compressed_pubkey_from_privkey(private_key_bytes):
    """
    Derive a compressed public key from a private key using the SECP256k1 curve.

    Args:
    private_key_bytes (bytes): The private key as bytes.

    Returns:
    str: The compressed public key as a hexadecimal string.
    """
    signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    public_key = signing_key.verifying_key
    compressed_pubkey = compress_public_key(public_key)
    return compressed_pubkey


def hash160(data):
    sha256 = hashlib.sha256(data).digest()
    ripemd160 = RIPEMD160.new()
    ripemd160.update(sha256)
    return ripemd160.digest()


# parse256(p): interprets a 32-byte sequence as a 256-bit number, most significant byte first.
def parse256(byte_sequence):
    if len(byte_sequence) != 32:
        raise ValueError("Byte sequence must be exactly 32 bytes long")
    return int.from_bytes(byte_sequence, byteorder="big")


def parse_derivation_path(derivation_path):
    path_parts = derivation_path.split("/")
    result = []
    for part in path_parts:
        if part == "*":
            continue
        if part == "m":
            continue
        if part.endswith("h") or part.endswith("H"):
            index = int(part[:-1])
            hardened = True
        else:
            index = int(part)
            hardened = False
        result.append((index, hardened))
    return result


def point(p):
    return SECP256k1.generator * int.from_bytes(p, "big")


def remove_checksum(bytes):
    return bytes[0:-4]


def ser32(i):
    if i < 0 or i >= 2**32:
        raise ValueError("Integer must be in the range 0 <= p < 2**32")
    return i.to_bytes(4, byteorder="big")


def ser256(p):
    if p < 0 or p >= 2**256:
        raise ValueError("Integer must be in the range 0 <= p < 2**256")
    return p.to_bytes(32, byteorder="big")


def serP(P):
    x = P.x()
    y = P.y()
    if y % 2 == 0:
        header = b"\x02"
    else:
        header = b"\x03"
    return header + ser256(x)
