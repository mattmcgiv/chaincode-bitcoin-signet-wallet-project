use balance;
use serde::{Serialize, Deserialize};
use serde_json;
use std::fs;
use std::io::{self, Read};

#[derive(Serialize, Deseralize, Debug)]
struct Utxo {
    amount: f32,
    txid: String,
    output_num: i32,
}

#[derive(Serialize, Deserialize, Debug)]
struct WalletState {
    utxo: Vec<Utxo>,
    balance: f64,
    privs: Vec<String>,
    pubs: Vec<String>,
    programs: Vec<String>,
}

fn read_file_to_string(file_path: &str) -> io::Result<String> {
    fs::read_to_string(file_path)
}

fn load_json_data(file_path: &str) -> Result<MyData, serde_json::Error> {
    let json_str = read_file_to_string(file_path)?;
    serde_json::from_str(&json_str)
}

fn main() {
    let file_path = "../../../output.json";
    match load_json_data(file_path) {
        Ok(data) => println!("Data loaded successfully: {:?}", data),
        Err(e) => println!("Error loading data: {}", e),
    }
}


#[test]
fn test_main() {
    assert_eq!(1, 1);
}
