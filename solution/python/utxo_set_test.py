import unittest
from utxo_set import UTXOSet


class TestUTXOSet(unittest.TestCase):
    def test_add_utxo(self):
        """Test adding UTXOs to the set."""
        utxo_set = UTXOSet()
        utxo_set.add_utxo("txid1", 0, 100)
        self.assertIn("txid1", utxo_set.utxo_set)
        self.assertIn((0, 100), utxo_set.utxo_set["txid1"])

    def test_remove_utxo(self):
        """Test removing UTXOs from the set."""
        utxo_set = UTXOSet()
        # Add and then remove a UTXO
        utxo_set.add_utxo("txid1", 1, 100)
        utxo_set.add_utxo("txid1", 0, 100)
        utxo_set.remove_utxo("txid1", 1)
        self.assertNotIn((1, 100), utxo_set.utxo_set["txid1"])

    def test_get_utxo(self):
        """Test getting UTXOs from the set."""
        utxo_set = UTXOSet()
        utxo_set.add_utxo("txid1", 0, 100)
        utxo = utxo_set.get_utxo("txid1", 0)
        self.assertEqual(utxo, (0, 100))


if __name__ == "__main__":
    unittest.main()
