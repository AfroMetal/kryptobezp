# Kryptografia i bezpieczeństwo - List 3
File coding/decoding with own keystore implementation. Program supports AES 
standard with CBC, CTR and GCM modes. Keys, nonce/iv/counter are generated randomly and saved together with key in keystore as `.key` file encrypted using passphrase provided during execution according to [PKCS#8](https://www.wikiwand.com/en/PKCS_8) standard.  
Program uses [PyCryptodome](http://pycryptodome.readthedocs.io/en/latest/src/introduction.html) library for all encrypting and decrypting operations with AES and to store keys securely in keystore with PKCS#8.
# Usage

## Run
### Encode mode
python filecoder.py <file-path> <keystore-path> <key-id> <mode (cbc|ctr|gcm)> [<output-path>]
>*<output-path> will be appended with* `.<key-id>.aes`.
>*If none <output-path> is provided it will default to <file-path>*

### Decode mode
python filecoder.py <file-path> <keystore-path> <key-id>
> *<file-path> should end with* `.<key-id>.aes`

## Execution
You will be asked for passphrase to key with provided `key-id` in keystore defined by `keystore_path`, during encoding to wrap key with it and during decoding to unwrap key with that passphrase.``