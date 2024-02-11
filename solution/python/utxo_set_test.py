import unittest
from utxo_set import UTXOSet, UTXOSetEncoder
import json


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

    def test_utxo_set_encode(self):
        """Test encoding the UTXO set."""
        utxo_set = UTXOSet()
        utxo_set.add_utxo("txid1", 0, 100)
        utxo_set.add_utxo("txid1", 1, 200)
        utxo_set.add_utxo("txid2", 0, 7000)
        encoded_utxo_set = json.dumps(utxo_set, cls=UTXOSetEncoder)
        expected = [
            {"txid": "txid1", "output_num": 0, "amount": 100},
            {"txid": "txid1", "output_num": 1, "amount": 200},
            {"txid": "txid2", "output_num": 0, "amount": 7000},
        ]
        self.assertTrue(file_writer("utxo_set.json", encoded_utxo_set))

    def test_state_write_to_file(self):
        state = {
            "utxo": UTXOSet(),
            "balance": 0,
            "privs": [],
            "pubs": [],
            "programs": [],
        }

        state["utxo"].add_utxo("txid1", 0, 100)
        state["balance"] = state["utxo"].sum_total_value_of_utxo_set()
        state["privs"] = [
            # list of bytes
            b"byte1",
            b"byte2",
            b"byte3",
            # add more bytes here
        ]
        state["pubs"] = [
            # list of bytes
            b"byte1",
            b"byte2",
            b"byte3",
        ]
        state["programs"] = [
            # list of bytes
            b"byte1",
            b"byte2",
            b"byte3",
            # add more bytes here
        ]

        # prepare to write to file

        # convert utxo to json
        state["utxo"] = state["utxo"].to_json()

        # convert privs to hex
        state["privs"] = [
            hex(int.from_bytes(i, byteorder="big")) for i in state["privs"]
        ]

        # convert pubs to hex
        state["pubs"] = [hex(int.from_bytes(i, byteorder="big")) for i in state["pubs"]]

        # convert programs to hex
        state["programs"] = [
            hex(int.from_bytes(i, byteorder="big")) for i in state["programs"]
        ]

        print("STATE")
        print(state)
        self.assertTrue(file_writer("state_output.json", state))


def file_writer(name, obj):
    try:
        with open(name, "w") as file:
            json.dump(obj, file)
        return True
    except Exception as e:
        print(e)
        print("Error writing to file")
        return False


if __name__ == "__main__":
    unittest.main()
