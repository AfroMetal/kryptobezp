# Kryptografia i bezpieczeństwo - List 3
File coding/decoding with cryptographic keys loaded from Java KeyStore in JCEKS keystore format `.jkc`. Program supports AES 
standard with CBC, CTR and GCM modes. Nonce/iv/counter is generated randomly and saved in front of cryptogram.  
Program uses [PyCryptodome](http://pycryptodome.readthedocs.io/en/latest/src/introduction.html) library for all encrypting and decrypting operations with AES.  
For Java KeyStore parsing and decryption [PyJKS](http://pyjks.readthedocs.io/en/latest/) is used.

# Run
### Encode mode
python filecoder.py \<file-path> \<keystore-path> \<key-alias> \<mode (cbc|ctr|gcm)> [\<output-path>]
>*\<output-path> will be appended with* `.aes`.
>*If none \<output-path> is provided it will default to <file-path>*

### Decode mode
python filecoder.py \<file-path> \<keystore-path> \<key-alias>
> *\<file-path> should end with* `.aes`

## Execution
You will be asked for passphrase to Java KeyStore and key in keystore defined by `keystore_path`.

#Usage examples
```terminal
C:\home\filecoder>python filecoder.py encode "C:\home\text.txt" "C:\home\keystore.jck" key1 cbc
Enter passphrase for keystore:
Enter passphrase for key:

File was successfully encoded into C:\home\text.txt.aes

C:\home\filecoder>python filecoder.py decode "C:\home\text.txt.aes" "C:\home\keystore.jck" key1 cbc
Enter passphrase for keystore:
Enter passphrase for key:

File was successfully decoded into C:\home\text.txt
```
