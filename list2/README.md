# Kryptografia i bezpieczeństwo - List 2
AES-256-CBC bruteforce on key prefix

# Usage

## Run
python "aesbrute.py" "cryptogram in base64" "iv in hex" "key suffix in hex" "key prefix space"

## Input
- iv have to be 32 characters long hex string
- key suffix have to be 63 or less characters long hex string
- key prefix space is hex string of characters allowed as 1st key char, for example '89ab' will only check keys starting with '8', '9', 'a' or 'b'

## Output
On success will give key, decrypted message and run time in seconds. Also file containing cryptogram, iv, key and message will be created with name from first 16 chars of key.

On fail will give 'Decryption failed.' information and run time in seconds.
