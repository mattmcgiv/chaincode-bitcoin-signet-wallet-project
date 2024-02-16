use hex_literal::hex;
use hex as hex_2;
use sha2::{Sha256, Digest};

mod structs;
mod utils;

fn create_multisig_script(threshold: i32, total_keys: i32, public_keys: Vec<String>) -> String {
    // concatenate threshold followed by each public key, the total number of keys and OP_CHECKMULTISIG
    // example: 2 public_keys[0]public_keys[1] public_keys[2] 3 OP_CHECKMULTISIG 
    let mut script = "OP_".to_string();
    script.push_str(&mut threshold.to_string());
    
    for key in public_keys {
        script.push_str(" ");
        script.push_str(key.as_str());
    }
    script.push_str(" OP_");
    script.push_str(total_keys.to_string().as_str());
    script.push_str(" OP_CHECKMULTISIG");
    script.to_string()
}

fn compute_p2wsh_program(script: String) -> String {
    let mut hasher = Sha256::new();
    hasher.update(script);
    let result = hasher.finalize();
    result.iter().map(|byte| format!("{:02x}", byte)).collect()
}

fn main() {
    // load data from file
    let file_path = "output.json";

    match utils::load_json_data(file_path) {
        Ok(_data) => println!("Data loaded successfully."),
        Err(e) => println!("Error loading data: {}", e),
    }

    let data = utils::load_json_data(file_path).expect("Failed to load data");
    
    // Create a 2-of-2 multi-sig script from public keys index 0 and 1
    let script = create_multisig_script(2, 2, data.pubs[0..2].to_vec());
}


#[test]
fn test_create_multisig_script() {
    let script = create_multisig_script(2, 2, vec!["pubkey1".to_string(), "pubkey2".to_string()]);
    assert_eq!(script, "OP_2 pubkey1 pubkey2 OP_2 OP_CHECKMULTISIG");
}

#[test]
fn test_create_p2wsh_program() {
    let script = create_multisig_script(2, 2, vec!["pubkey1".to_string(), "pubkey2".to_string()]);
    let computed = compute_p2wsh_program(script);
    let given = hex!("df1b505df21ccc1f5781e5f56cdef5202dd8b2ca6fe47a4418e48e411f4a6658");
    assert_eq!(computed, hex_2::encode(given));
}
