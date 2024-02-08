class UTXOSet:
    def __init__(self):
        self.utxo_set = {}  # Initialize the UTXO set as an empty dictionary

    def add_utxo(self, txid, balance):
        """Adds a UTXO to the utxo_set."""
        self.utxo_set[txid] = balance  # Add or update the outpoint with its balance

    def remove_utxo(self, txid):
        """Removes a UTXO from the utxo_set."""
        if txid in self.utxo_set:
            del self.utxo_set[txid]
        else:
            raise KeyError(
                f"txid {txid} not in UTXO set"
            )  # Raise a KeyError if the txid doesn't exist

    def get_utxo(self, txid):
        # if the txid isn't in utxo_set, raise a KeyError
        if txid not in self.utxo_set:
            raise KeyError(f"txid {txid} not in UTXO set")
        return self.utxo_set[txid]
