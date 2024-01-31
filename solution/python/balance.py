from utils import (
    parse256,
    point,
    base58_decode_and_remove_checksum,
    contains_our_pubkey,
    deserialize_key,
    derive_compressed_pubkey_from_privkey,
    ser32,
    ser256,
    serP,
    parse_derivation_path,
    hash160,
)
from ecdsa import SigningKey, SECP256k1
from decimal import Decimal
from solution_constants import (
    WALLET_DESCRIPTOR,
    WPKH,
    TPRV,
    DERIVATION_PATH,
    EXTENDED_PRIVATE_KEY,
)
from subprocess import run
from typing import List, Tuple
import hashlib
import hmac
import json


# Provided by administrator
WALLET_NAME = "wallet_000"


# Perform a BIP32 parent private key -> child private key operation
# Return a JSON object with "key" and "chaincode" properties as bytes
# https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#user-content-Private_parent_key_rarr_private_child_key
def derive_priv_child(
    key: bytes, chaincode: bytes, index: int, hardened: bool
) -> object:
    result = {
        "key": None,
        "chaincode": None,
    }
    I = None

    # hardened child
    if hardened:
        hardened_bytes = 0x80000001.to_bytes(4, byteorder="big")
        index_bytes = index.to_bytes(4, byteorder="big")
        hardened_index = hardened_bytes + index_bytes
        # let I = HMAC-SHA512(Key = cpar, Data = 0x00 || ser256(kpar) || ser32(i)).
        # (Note: The 0x00 pads the private key to make it 33 bytes long.)
        # ser256(p): serializes the integer p as a 32-byte sequence, most significant byte first.
        # ser32(i): serialize a 32-bit unsigned integer i as a 4-byte sequence, most significant byte first.
        I = hmac.new(
            chaincode,
            b"\x00" + key + hardened_index,
            hashlib.sha512,
        ).digest()

    else:
        # non-hardened child
        # let I = HMAC-SHA512(Key = cpar, Data = serP(point(kpar)) || ser32(i)).
        # ser32(i): serialize a 32-bit unsigned integer i as a 4-byte sequence, most significant byte first.
        # serP(P): serializes the coordinate pair P = (x,y) as a byte sequence using SEC1's compressed form: (0x02 or 0x03) || ser256(x), where the header byte depends on the parity of the omitted y coordinate.
        # point(p): returns the coordinate pair resulting from EC point multiplication (repeated application of the EC group operation) of the secp256k1 base point with the integer p.
        I = hmac.new(
            chaincode, (serP(point(key)) + ser32(index)), digestmod=hashlib.sha256
        ).digest()

    # Split I into two 32-byte sequences, IL and IR.
    I_L = I[:32]
    I_R = I[32:]
    # The returned child key ki is parse256(IL) + kpar (mod n).
    # parse256(p): interprets a 32-byte sequence as a 256-bit number, most significant byte first.
    # kpar_mod_n = int.from_bytes(key, byteorder="big")
    k_i = (parse256(I_L) + int.from_bytes(key, byteorder="big")) % SECP256k1.order
    # The returned chain code ci is IR.
    c_i = I_R
    result = {
        "key": k_i.to_bytes(32, byteorder="big"),
        "chaincode": c_i,
    }
    return result


# Given an extended private key and a BIP32 derivation path,
# compute the first 2000 child private keys.
# Return an array of keys encoded as bytes.
# The derivation path is formatted as an array of (index: int, hardened: bool) tuples.
def get_wallet_privs(
    key: bytes, chaincode: bytes, path: List[Tuple[int, bool]]
) -> List[bytes]:
    privs = []

    # Check if both key and chaincode are bytes
    if not isinstance(key, bytes):
        raise TypeError("key must be bytes.")

    if not isinstance(chaincode, bytes):
        raise TypeError("chaincode must be bytes.")

    current_key = key
    current_chaincode = chaincode
    for i in range(len(path)):
        if not isinstance(path[i][0], int):
            raise TypeError("index must be int.")

        if not isinstance(path[i][1], bool):
            raise TypeError("hardened must be bool.")

        priv_child = derive_priv_child(
            current_key, current_chaincode, path[i][0], path[i][1]
        )
        current_key = priv_child["key"]
        current_chaincode = priv_child["chaincode"]

    # use key_4 to derive 2000 keys and append them to privs
    for i in range(2000):
        derived_priv_child = derive_priv_child(current_key, current_key, i, False)
        privs.append(derived_priv_child["key"])

    return privs


# Derive the p2wpkh witness program (aka scriptPubKey) for a given compressed public key.
# Return a bytes array to be compared with the JSON output of Bitcoin Core RPC getblock
# so we can find our received transactions in blocks.
# These are segwit version 0 pay-to-public-key-hash witness programs.
# https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki#user-content-P2WPKH
def get_p2wpkh_program(pubkey: bytes, version: int = 0) -> bytes:
    return version.to_bytes(1, byteorder="big") + b"\x14" + hash160(pubkey)


# Assuming Bitcoin Core is running and connected to signet using default datadir,
# execute an RPC and return its value or error message.
# https://github.com/bitcoin/bitcoin/blob/master/doc/bitcoin-conf.md#configuration-file-path
# Examples: bcli("getblockcount")
#           bcli("getblockhash 100")
def bcli(cmd: str):
    res = run(
        ["bitcoin-cli", "-signet"] + cmd.split(" "),
        capture_output=True,
        encoding="utf-8",
    )
    if res.returncode == 0:
        return res.stdout.strip()
    else:
        raise Exception(res.stderr.strip())


# Recover the wallet state from the blockchain:
# - Parse xprv and path from descriptor and derive 2000 key pairs and witness programs
# - Request blocks 0-310 from Bitcoin Core via RPC and scan all transactions
# - Return a state object with all the derived keys and total wallet balance
def recover_wallet_state(xprv: str):
    # Generate all the keypairs and witness programs to search foraa
    deserialized_key = deserialize_key(xprv)

    decoded_key = base58_decode_and_remove_checksum(deserialized_key["key"])
    decoded_chaincode = base58_decode_and_remove_checksum(deserialized_key["chaincode"])

    # Check if both key and chaincode are bytes
    if not isinstance(decoded_key, bytes):
        raise TypeError("key must be bytes.")

    if not isinstance(decoded_chaincode, bytes):
        raise TypeError("chaincode must be bytes.")

    privs = get_wallet_privs(
        decoded_key,
        decoded_chaincode,
        parse_derivation_path(DERIVATION_PATH),
    )
    # get the public keys from the privs
    pubs = []
    for priv in privs:
        pubs.append(derive_compressed_pubkey_from_privkey(priv))

    # get the witness programs from the pubs
    programs = []
    for pub in pubs:
        programs.append(get_p2wpkh_program(pub))

    # Prepare a wallet state data structure
    state = {
        "utxo": {},
        "balance": 0,
        "privs": privs,
        "pubs": pubs,
        "programs": programs,
    }

    # pretty print state to a file
    # with open("state.json", "w") as f:
    #     json.dump(state, f, indent=4)
    #     f.close()

    # Scan blocks 0-310
    height = 310
    for h in range(height + 1):
        # Get the transactions in the block with height h
        block_hash = bcli("getblockhash " + str(h))
        block = bcli("getblock " + block_hash + " 2")
        block_json = json.loads(block)
        txs = block_json["tx"]

        # Scan every tx in every block
        for tx in txs:
            for inp in tx["vin"]:
                # Check every tx input (witness) for our own compressed public keys.
                # These are coins we have spent.

                if "coinbase" in inp:
                    continue

                # if inp doesn't have a txinwitness key, skip it
                if "txinwitness" not in inp:
                    continue

                if contains_our_pubkey(inp["txinwitness"], state["pubs"]):
                    # Remove this coin from our wallet state utxo pool
                    # so we don't double spend it later
                    state["utxo"]

            # Check every tx output for our own witness programs.
            # These are coins we have received.
            for out in tx["vout"]:
                # Add to our total balance
                print(".")
                # Keep track of this UTXO by its outpoint in case we spend it later

    return state


if __name__ == "__main__":
    print(f"{WALLET_NAME} {recover_wallet_state(EXTENDED_PRIVATE_KEY)['balance']}")
