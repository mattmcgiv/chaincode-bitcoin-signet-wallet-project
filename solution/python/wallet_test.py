import unittest
from wallet_utils import parse_derivation_path, hash160
from solution_constants import DERIVATION_PATH


class TestWalletUtils(unittest.TestCase):
    def test_parse_derivation_path(self):
        path = "44h/60/0h/0/0"
        result = parse_derivation_path(path)
        self.assertEqual(
            result, [(44, True), (60, False), (0, True), (0, False), (0, False)]
        )

        path = DERIVATION_PATH
        result = parse_derivation_path(path)
        self.assertEqual(result, [(84, True), (1, True), (0, True), (0, False)])

    def test_hash160(self):
        data = b"Hello, Bitcoin!"
        result = hash160(data)
        self.assertEqual(result, b'\x84NZ\xed\xbf \xa1\x04\xe1\xa8\xcd\xcb\xe8?\x82\x96uy\xb4\xc3')