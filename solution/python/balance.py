from decimal import Decimal
from decode_utils import base58_decode_and_remove_checksum
from ecdsa import SigningKey, SECP256k1
from key_utils import deserialize_key
from solution_constants import WALLET_DESCRIPTOR, WPKH, TPRV, DERIVATION_PATH
from subprocess import run
from typing import List, Tuple
from wallet_utils import parse_derivation_path
import hashlib
import hmac
import json

# Provided by administrator
WALLET_NAME = "wallet_000"

# Derive the secp256k1 compressed public key from a given private key
# BONUS POINTS: Implement ECDSA yourself and multiply you key by the generator point!
def get_pub_from_priv(priv: bytes) -> bytes:


# Perform a BIP32 parent private key -> child private key operation
# Return a JSON object with "key" and "chaincode" properties as bytes
# https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#user-content-Private_parent_key_rarr_private_child_key
def derive_priv_child(key: bytes, chaincode: bytes, index: int, hardened: bool) -> object:
#TODO: once deserialize_key is done, implement this method to use in get_wallet_privs()



# Given an extended private key and a BIP32 derivation path,
# compute the first 2000 child private keys.
# Return an array of keys encoded as bytes.
# The derivation path is formatted as an array of (index: int, hardened: bool) tuples.
def get_wallet_privs(key: bytes, chaincode: bytes, path: List[Tuple[int, bool]]) -> List[bytes]:
    privs = []
    # get the 85th hardened child private key from the key param
    key_1 = derive_priv_child(key, chaincode, path[0][0], path[0][1])

    # use key_1 to get the second hardened child private key
    key_2 = derive_priv_child(key_1["key"], key_1["chaincode"], path[1][0], path[1][1])

    # use key_2 to get the first hardened child private key
    key_3 = derive_priv_child(key_2["key"], key_2["chaincode"], path[2][0], path[2][1])

    # use key_3 to get the first child private key
    key_4 = derive_priv_child(key_3["key"], key_3["chaincode"], path[3][0], path[3][1])

    # use key_4 to derive 2000 keys and append them to privs
    for i in range(2000):
        privs.append(derive_priv_child(key_4["key"], key_4["chaincode"], i, False)["key"])

    return privs

# Derive the p2wpkh witness program (aka scriptPubKey) for a given compressed public key.
# Return a bytes array to be compared with the JSON output of Bitcoin Core RPC getblock
# so we can find our received transactions in blocks.
# These are segwit version 0 pay-to-public-key-hash witness programs.
# https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki#user-content-P2WPKH
def get_p2wpkh_program(pubkey: bytes, version: int=0) -> bytes:


# Assuming Bitcoin Core is running and connected to signet using default datadir,
# execute an RPC and return its value or error message.
# https://github.com/bitcoin/bitcoin/blob/master/doc/bitcoin-conf.md#configuration-file-path
# Examples: bcli("getblockcount")
#           bcli("getblockhash 100")
def bcli(cmd: str):
    res = run(
            ["bitcoin-cli", "-signet"] + cmd.split(" "),
            capture_output=True,
            encoding="utf-8")
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
    privs = get_wallet_privs(
        deserialized_key["key"],
        deserialized_key["chaincode"],
        parse_derivation_path(DERIVATION_PATH)
    )
    pubs = 
    programs = 

    # Prepare a wallet state data structure
    state = {
        "utxo": {},
        "balance": 0,
        "privs": privs,
        "pubs": pubs,
        "programs": programs
    }

    # Scan blocks 0-310
    height = 310
    for h in range(height + 1):

        # Scan every tx in every block
        for tx in txs:
            # Check every tx input (witness) for our own compressed public keys.
            # These are coins we have spent.
            for inp in tx["vin"]:

                    # Remove this coin from our wallet state utxo pool
                    # so we don't double spend it later

            # Check every tx output for our own witness programs.
            # These are coins we have received.
            for out in tx["vout"]:
                    # Add to our total balance

                    # Keep track of this UTXO by its outpoint in case we spend it later

    return state


if __name__ == "__main__":
    print(f"{WALLET_NAME} {recover_wallet_state(EXTENDED_PRIVATE_KEY)['balance']}")
