import unittest
from serialization_utils import ser32, ser256


class TestSerializationUtils(unittest.TestCase):
    def test_ser32(self):
        self.assertEqual(ser32(0), b"\x00\x00\x00\x00")
        self.assertEqual(ser32(1), b"\x00\x00\x00\x01")
        self.assertEqual(ser32(2**32 - 1), b"\xff\xff\xff\xff")

class TestSer256(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(ser256(0), b'\x00' * 32)

    def test_small_number(self):
        self.assertEqual(ser256(1), b'\x00' * 31 + b'\x01')

    def test_max_256bit(self):
        self.assertEqual(ser256(2**256 - 1), b'\xFF' * 32)

    def test_negative_number(self):
        with self.assertRaises(ValueError):
            ser256(-1)

    def test_large_number(self):
        with self.assertRaises(ValueError):
            ser256(2**256)
