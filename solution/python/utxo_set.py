class UTXOSet:
    def __init__(self):
        self.utxo_set = {}  # Initialize the UTXO set as an empty dictionary

    def add_utxo(self, txid, output_num, balance):
        """Adds a UTXO to the utxo_set."""
        # if the txid is already in the utxo_set, append a new UTXO (output_num, balance) to the list
        if txid in self.utxo_set:
            self.utxo_set[txid].append((output_num, balance))
        else:
            self.utxo_set[txid] = [(output_num, balance)]
        # sort the utxo_set after adding the UTXO
        self.sort_utxo_set()

    def remove_utxo(self, txid, output_num):
        """Removes a UTXO from the utxo_set."""
        # if the txid is in the utxo_set, but the list of UTXOs for the txid is empty, raise a KeyError
        if self.utxo_set[txid] == []:
            raise KeyError(f"txid {txid} not in UTXO set")
        # if the txid is already in the utxo_set, remove the UTXO (output_num, balance) from the list
        if txid in self.utxo_set:
            counter = 0
            for stored_output_num, amount in self.utxo_set[txid]:
                if stored_output_num == output_num:
                    self.utxo_set[txid].remove(self.utxo_set[txid][counter])
                    # sort the utxo_set after removing the UTXO
                    self.sort_utxo_set()
                    break
                counter += 1
        # if the txid is not in the utxo_set, raise a KeyError
        else:
            raise KeyError(f"txid {txid} not in UTXO set")

    def get_utxo(self, txid, output_num):
        # if the txid isn't in utxo_set, raise a KeyError
        if txid not in self.utxo_set:
            raise KeyError(f"txid {txid} not in UTXO set")
        # if the output_num isn't in the list of UTXOs for the txid, raise a KeyError
        for utxo in self.utxo_set[txid]:
            if utxo[0] == output_num:
                return utxo
        raise KeyError(f"output_num {output_num} not in UTXO set")

    def sort_utxo_set(self):
        """Sorts the utxo_set by txid."""
        self.utxo_set = dict(sorted(self.utxo_set.items()))
        for txid in self.utxo_set:
            self.utxo_set[txid].sort(key=lambda x: x[0])
        return self.utxo_set

    def sum_total_value_of_utxo_set(self):
        """Sums the total value of the UTXO set."""
        total_value = 0
        for txid in self.utxo_set:
            for utxo in self.utxo_set[txid]:
                total_value += utxo[1]
        # return the total value but rounded to 8 decimal places
        return round(total_value, 8)
