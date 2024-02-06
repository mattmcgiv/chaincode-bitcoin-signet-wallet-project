from ast import parse
from itertools import chain
import unittest
from balance import derive_priv_child, get_wallet_privs, parse_derivation_path
from utils import derive_compressed_pubkey_from_privkey, deserialize_key
from utils import base58_decode_and_remove_checksum, base58_decode, hash160
from solution_constants import (
    DERIVATION_PATH,
    EXTENDED_KEY_VERSION_BYTES,
    EXTENDED_PRIVATE_KEY,
    TV_1,
)
from bip32 import BIP32, HARDENED_INDEX
from base58 import b58encode
import hashlib
import base58


class TestKeyUtils(unittest.TestCase):
    def test_deserialize_public_mainnet_key(self):
        decoded_key = base58_decode_and_remove_checksum(TV_1[0]["xpub"])
        deserialized_key = deserialize_key(decoded_key)
        expected_key_data = {
            "version": hex_to_bytes(EXTENDED_KEY_VERSION_BYTES["MAINNET_PUBLIC"]),
            "depth": b"\x00",
        }
        self.assertEqual(deserialized_key["version"], expected_key_data["version"])
        self.assertEqual(deserialized_key["depth"], expected_key_data["depth"])
        # TODO: fingerprint, child_number, chaincode, key

    def test_deserialize_private_mainnet_key(self):
        decoded_key = base58_decode_and_remove_checksum(TV_1[0]["xprv"])
        deserialized_key = deserialize_key(decoded_key)
        expected_key_data = {
            "version": hex_to_bytes(EXTENDED_KEY_VERSION_BYTES["MAINNET_PRIVATE"]),
            "depth": b"\x00",
            "fingerprint": b"\x00\x00\x00\x00",
            "child_number": b"\x00\x00\x00\x00",
            "chaincode": hex_to_bytes(
                "873DFF81C02F525623FD1FE5167EAC3A55A049DE3D314BB42EE227FFED37D508"
            ),
            "key": b"\x00"
            + hex_to_bytes(
                "E8F32E723DECF4051AEFAC8E2C93C9C5B214313817CDB01A1494B917C8436B35"
            ),
        }
        self.assertEqual(deserialized_key["version"], expected_key_data["version"])
        self.assertEqual(deserialized_key["depth"], expected_key_data["depth"])
        self.assertEqual(
            deserialized_key["fingerprint"], expected_key_data["fingerprint"]
        )
        self.assertEqual(
            deserialized_key["child_number"], expected_key_data["child_number"]
        )
        self.assertEqual(deserialized_key["chaincode"], expected_key_data["chaincode"])
        self.assertEqual(deserialized_key["key"], expected_key_data["key"])

    def test_base58_decode(self):
        test_string = b"hello world"
        encoded = base58.b58encode(test_string, base58.BITCOIN_ALPHABET)
        self.assertEqual(test_string, base58_decode(encoded.decode("utf-8")))

    def test_base58_decode_and_remove_checksum(self):
        encoded_check = b"3vQB7B6MrGQZaxCuFg4oh"
        expected = b"hello world"
        self.assertEqual(
            expected, base58_decode_and_remove_checksum(encoded_check.decode("utf-8"))
        )

    def test_derive_non_hardened_child_private_key_from_parent_private_key(self):
        parent_xpriv = "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"

        # bip32 known good reference
        bip32 = BIP32.from_xpriv(parent_xpriv)
        bip32_deriv_path = "m/0"
        bip32_privkey_hex = bip32.get_privkey_from_path(bip32_deriv_path).hex()
        bip32_pubkey_hex = bip32.get_pubkey_from_path(bip32_deriv_path).hex()
        # print("bip_32_pubkey_hex", bip32_pubkey_hex)

        # this library (my stuff)
        decoded = base58_decode_and_remove_checksum(parent_xpriv)
        deserialized = deserialize_key(decoded)

        privkey = deserialized["key"][1:]
        chaincode = deserialized["chaincode"]

        self.assertEqual(bip32.privkey, privkey)
        self.assertEqual(bip32.chaincode, chaincode)

        derived_key = derive_priv_child(privkey, chaincode, 0, False)

        self.assertEqual(bip32_privkey_hex, derived_key["key"].hex())

    def test_derive_hardened_child_private_key_from_parent_private_key(self):
        parent_xpriv = "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"

        # bip32 known good reference implementation
        bip32 = BIP32.from_xpriv(parent_xpriv)
        bip32_deriv_path = "m/0H"
        bip32_privkey_hex = bip32.get_privkey_from_path(bip32_deriv_path).hex()

        decoded = base58_decode_and_remove_checksum(parent_xpriv)
        deserialized = deserialize_key(decoded)

        privkey = deserialized["key"][1:]
        chaincode = deserialized["chaincode"]

        self.assertEqual(bip32.privkey, privkey)
        self.assertEqual(bip32.chaincode, chaincode)

        derived_key = derive_priv_child(privkey, chaincode, 0, True)

        self.assertEqual(bip32_privkey_hex, derived_key["key"].hex())

    def test_get_wallet_privs_non_hardened(self):
        parent_xpriv = "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"

        # bip32 known good reference
        bip32 = BIP32.from_xpriv(parent_xpriv)
        bip32_deriv_path = "m/0"
        descendant_xpriv = bip32.get_xpriv_from_path(bip32_deriv_path)

        print("descendant_xpriv", descendant_xpriv)

        bip32 = BIP32.from_xpriv(descendant_xpriv)
        bip32_privs = []
        bip32_pubs = []

        for i in range(2000):
            deriv_path = "m/" + str(i)
            bip32_privs.append(bip32.get_privkey_from_path(deriv_path))
            bip32_pubs.append(bip32.get_pubkey_from_path(deriv_path))

        # this library (my stuff)
        decoded = base58_decode_and_remove_checksum(parent_xpriv)
        deserialized = deserialize_key(decoded)

        privkey = deserialized["key"][1:]
        chaincode = deserialized["chaincode"]

        privs = get_wallet_privs(
            privkey, chaincode, parse_derivation_path(bip32_deriv_path)
        )

        for i in range(2000):
            print("testing key", i, "...")
            print("bip32_pubs", bip32_pubs[i].hex())
            self.assertEqual(bip32_privs[i].hex(), privs[i].hex())

    def test_get_wallet_privs_hardened(self):
        parent_xpriv = "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"

        # bip32 known good reference
        bip32 = BIP32.from_xpriv(parent_xpriv)
        bip32_deriv_path = "m/0H"
        descendant_xpriv = bip32.get_xpriv_from_path(bip32_deriv_path)

        print("descendant_xpriv", descendant_xpriv)

        bip32 = BIP32.from_xpriv(descendant_xpriv)
        bip32_privs = []
        bip32_pubs = []

        for i in range(2000):
            deriv_path = "m/" + str(i) + "H"
            bip32_privs.append(bip32.get_privkey_from_path(deriv_path))
            bip32_pubs.append(bip32.get_pubkey_from_path(deriv_path))

        # this library (my stuff)
        decoded = base58_decode_and_remove_checksum(parent_xpriv)
        deserialized = deserialize_key(decoded)

        privkey = deserialized["key"][1:]
        chaincode = deserialized["chaincode"]

        privs = get_wallet_privs(
            privkey, chaincode, parse_derivation_path(bip32_deriv_path)
        )

        for i in range(2000):
            print("testing key", i, "...")
            print("bip32_pubs", bip32_pubs[i].hex())
            self.assertEqual(bip32_privs[i].hex(), privs[i].hex())

    def test_get_wallet_privs_for_my_xpriv(self):
        parent_xpriv = EXTENDED_PRIVATE_KEY

        # bip32 known good reference
        bip32 = BIP32.from_xpriv(parent_xpriv)
        bip32_deriv_path = DERIVATION_PATH
        descendant_xpriv = bip32.get_xpriv_from_path(bip32_deriv_path)

        print("my descendant_xpriv", descendant_xpriv)

        bip32 = BIP32.from_xpriv(descendant_xpriv)
        bip32_privs = []
        bip32_pubs = []

        for i in range(2000):
            deriv_path = "m/" + str(i)
            bip32_privs.append(bip32.get_privkey_from_path(deriv_path))
            bip32_pubs.append(bip32.get_pubkey_from_path(deriv_path))

        # this library (my stuff)
        decoded = base58_decode_and_remove_checksum(parent_xpriv)
        deserialized = deserialize_key(decoded)

        privkey = deserialized["key"][1:]
        chaincode = deserialized["chaincode"]

        privs = get_wallet_privs(
            privkey, chaincode, parse_derivation_path(bip32_deriv_path)
        )

        pubs = []

        for priv in privs:
            pubs.append(derive_compressed_pubkey_from_privkey(priv))

        for i in range(2000):
            print("testing key", i, "...")
            print("bip32_pubs", bip32_pubs[i].hex())
            self.assertEqual(bip32_privs[i].hex(), privs[i].hex())
            self.assertEqual(bip32_pubs[i].hex(), pubs[i].hex())

    def test_parse_derivation_path(self):
        expected = [(0, False)]
        actual = parse_derivation_path("m/0")
        self.assertEqual(expected, actual)

        expected = [(0, True)]
        actual = parse_derivation_path("m/0H")
        self.assertEqual(expected, actual)

        expected = [(0, False), (0, False)]
        actual = parse_derivation_path("m/0/0")
        self.assertEqual(expected, actual)

        expected = [(0, False), (0, False), (0, True)]
        actual = parse_derivation_path("m/0/0/0h")
        self.assertEqual(expected, actual)

        expected = [(99, False), (23, True), (11, False)]
        actual = parse_derivation_path("m/99/23H/11")
        self.assertEqual(expected, actual)

    def test_derive_compressed_pubkey_from_privkey(self):
        decoded_private_key = base58_decode_and_remove_checksum(TV_1[1]["xprv"])
        deserialized_private_key = deserialize_key(decoded_private_key)

        modified_deserialized_private_key = deserialized_private_key["key"][1:]

        compressed_pubkey_calculated = derive_compressed_pubkey_from_privkey(
            modified_deserialized_private_key
        )
        # print("compressed_pubkey_actual (hex)", compressed_pubkey_calculated.hex())

        decoded_pubkey_given = base58_decode_and_remove_checksum(TV_1[1]["xpub"])
        deserialized_public_key_given = deserialize_key(decoded_pubkey_given)
        # print("deserialized_public_key_given", deserialized_public_key_given)
        compressed_pubkey_given = deserialized_public_key_given["key"]

        self.assertEqual(compressed_pubkey_calculated, compressed_pubkey_given)

def hex_to_bytes(hex_string):
    """
    Convert a hexadecimal string to bytes.

    Args:
    hex_string (str): The hexadecimal string to convert.

    Returns:
    bytes: The bytes representation of the hexadecimal string.
    """
    try:
        # Convert the hexadecimal string to bytes
        byte_representation = bytes.fromhex(hex_string)
        return byte_representation
    except ValueError as e:
        # Handle potential errors in the conversion process
        print(f"Error converting hex to bytes: {e}")
        return None


def hex_to_wif(hex_priv_key):
    # Add the 0x80 prefix for mainnet private keys
    prefixed_key = "80" + hex_priv_key

    # Calculate the checksum
    first_sha256 = hashlib.sha256(bytes.fromhex(prefixed_key)).digest()
    second_sha256 = hashlib.sha256(first_sha256).digest()
    checksum = second_sha256[:4]

    # Create the final byte string and Base58 encode
    final_key = bytes.fromhex(prefixed_key) + checksum
    wif_key = base58.b58encode(final_key).decode("utf-8")

    return wif_key


if __name__ == "__main__":
    unittest.main()
