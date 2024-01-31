import unittest
from utils import derive_compressed_pubkey_from_privkey, deserialize_key
from utils import base58_decode_and_remove_checksum, base58_decode
from solution_constants import EXTENDED_KEY_VERSION_BYTES, TV_1


class TestKeyUtils(unittest.TestCase):
    def test_deserialize_public_mainnet_key(self):
        decoded_key = base58_decode_and_remove_checksum(TV_1[0]["xpub"])
        deserialized_key = deserialize_key(decoded_key)
        expected_key_data = {
            "version": hex_to_bytes(EXTENDED_KEY_VERSION_BYTES["MAINNET_PUBLIC"])
        }
        self.assertEqual(deserialized_key["version"], expected_key_data["version"])

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

    def test_derive_compressed_pubkey_from_privkey(self):
        decoded_private_key = base58_decode_and_remove_checksum(TV_1[1]["xprv"])
        deserialized_private_key = deserialize_key(decoded_private_key)

        modified_deserialized_private_key = deserialized_private_key["key"][1:]

        compressed_pubkey = derive_compressed_pubkey_from_privkey(
            modified_deserialized_private_key
        )
        print("compressed_pubkey", compressed_pubkey)
        print("hex", compressed_pubkey.hex())


# TODO tests for my extended private key (see TESTNET_PRIVATE in solution_constants)


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


if __name__ == "__main__":
    unittest.main()
