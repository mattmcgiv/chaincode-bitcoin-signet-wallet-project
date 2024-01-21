# TODO: wallet descriptor should be parsed, not hard-coded
WALLET_DESCRIPTOR = "wpkh(tprv8ZgxMBicQKsPdL9HoopTVCQ6VjpzpEPZmGoJeBtw3BUjfQATEJvTNACXjy6x9uZLjgsVvHXWkTPiRQMqmEb5BFciXVDwzt79nbBi9dXVxwA/84h/1h/0h/0/*)#6kh6r3d8"
WPKH = "wpkh"
TPRV = "tprv8ZgxMBicQKsPdL9HoopTVCQ6VjpzpEPZmGoJeBtw3BUjfQATEJvTNACXjy6x9uZLjgsVvHXWkTPiRQMqmEb5BFciXVDwzt79nbBi9dXVxwA"
DERIVATION_PATH = "84h/1h/0h/0/*"

EXTENDED_PRIVATE_KEY = "tprv8ZgxMBicQKsPfCxvMSGLjZegGFnZn9VZfVdsnEbuzTGdS9aZjvaYpyh7NsxsrAc8LsRQZ2EYaCfkvwNpas8cKUBbptDzadY7c3hUi8i33XJ"

EXTENDED_KEY_VERSION_BYTES = {
    "MAINNET_PUBLIC": "0488B21E",
    "MAINNET_PRIVATE": "0488ADE4",
    "TESTNET_PUBLIC": "043587CF",
    "TESTNET_PRIVATE": "04358394",
}

# test vector 1
TV_1 = {
    "chain": "m",
    "xpub": "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8",
    "xprv": "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi",
}
