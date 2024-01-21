import unittest
from key_utils import deserialize_key
from decode_utils import base58_decode_and_remove_checksum, base58_decode
from solution_constants import EXTENDED_KEY_VERSION_BYTES, TV_1


class TestKeyUtils(unittest.TestCase):
    def test_deserialize_public_mainnet_key(self):
        decoded_key = base58_decode_and_remove_checksum(TV_1["xpub"])
        deserialized_key = deserialize_key(decoded_key)
        expected_key_data = {
            "version": hex_to_bytes(EXTENDED_KEY_VERSION_BYTES["MAINNET_PUBLIC"])
        }
        self.assertEqual(deserialized_key["version"], expected_key_data["version"])

    def test_deserialize_private_mainnet_key(self):
        decoded_key = base58_decode_and_remove_checksum(TV_1["xprv"])
        deserialized_key = deserialize_key(decoded_key)
        expected_key_data = {
            "version": hex_to_bytes(EXTENDED_KEY_VERSION_BYTES["MAINNET_PRIVATE"])
        }
        self.assertEqual(deserialized_key["version"], expected_key_data["version"])


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
