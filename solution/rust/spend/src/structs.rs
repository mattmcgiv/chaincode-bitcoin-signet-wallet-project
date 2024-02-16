use serde_derive::{Serialize, Deserialize};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Utxo {
    pub amount: f32,
    pub txid: String,
    pub output_num: i32,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct WalletState {
    pub utxo: Vec<Utxo>,
    pub balance: f64,
    pub privs: Vec<String>,
    pub pubs: Vec<String>,
    pub programs: Vec<String>,
}