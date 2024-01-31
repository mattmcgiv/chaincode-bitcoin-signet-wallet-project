import unittest
from utils import base58_decode, convert_base_58_string_to_integer


class TestDecodeUtils(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_convert_base_58_string_to_integer(self):
        self.assertEqual(convert_base_58_string_to_integer("1"), 0)
        self.assertEqual(convert_base_58_string_to_integer("2"), 1)
        self.assertEqual(convert_base_58_string_to_integer("stack"), 575888597)
        self.assertEqual(convert_base_58_string_to_integer("sats"), 9869620)

    def test_base58_decode(self):
        self.assertEqual(base58_decode("StV1DL6CwTryKyV"), b"hello world")


if __name__ == "__main__":
    unittest.main()
