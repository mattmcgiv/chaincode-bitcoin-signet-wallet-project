use serde_json;
use std::fs;
use std::io::{self};

use crate::structs;

pub fn convert_to_little_endian_hex(input: &[u8]) -> String {
    // Reverse the slice to get little-endian byte order
    let little_endian_bytes = input.iter().rev();
    // Convert each byte to its hex representation and collect into a String
    little_endian_bytes.map(|byte| format!("{:02x}", byte)).collect()
}

pub fn get_utxo_from_state(state: structs::WalletState) -> structs::Utxo {
    state.utxo[0].clone()
}

pub fn read_file_to_string(file_path: &str) -> io::Result<String> {
    fs::read_to_string(file_path)
}

pub fn load_json_data(file_path: &str) -> Result<structs::WalletState, Box<dyn std::error::Error>> {
    let json_str = read_file_to_string(file_path)?;
    Ok(serde_json::from_str(&json_str)?)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_convert_to_little_endian_hex() {
        // Prepare a byte array for testing
        let bytes = [0x12, 0x34, 0x56, 0x78];
        // Call the function with the test data
        let hex_str = convert_to_little_endian_hex(&bytes);
        // Assert that the output is as expected
        assert_eq!(hex_str, "78563412");
    }

    #[test]
    fn test_get_utxo_from_state() {
        // load state from file
        let state = load_json_data("output.json").unwrap();

        // set expected values
        let expected = structs::Utxo {
            amount: 0.00908893,
            txid: "059e96ffa442b08af92d7fbecbe61877f47bf5c071d5f321e7852e3a07116fd3".to_string(),
            output_num: 177,
        };

        // get utxo
        let utxo = get_utxo_from_state(state);

        // assert
        assert_eq!(utxo.amount, expected.amount);
        assert_eq!(utxo.txid, expected.txid);
        assert_eq!(utxo.output_num, expected.output_num);
    }
}