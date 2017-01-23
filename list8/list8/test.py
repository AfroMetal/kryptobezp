from key import get_keys
from rsa import encrypt, decrypt, sign, verify_signature

print("Getting keys...")
public_key, private_key = get_keys(1024)
print("Got keys.")
priv_file = "rsakey"
pub_file = "rsakey.pub"
print("Saving keys...")
public_key.save_pem(pub_file)
private_key.save_pem(priv_file)
print(f"Keys saved to '{priv_file}' and '{pub_file}'\n")

message = 'Hello, world!'
print(f"Message is: {message}\n")
print(f"Message: {message}\n")

print("Encrypting...")
crypto = encrypt(message, public_key)
print(f"Ciphertext: {crypto}\n")

print("Signing...")
sign = sign(message, private_key)
print(f"Signature: {sign}\n")

print("Decrypting...")
decrypted = decrypt(crypto, private_key)
print(f"Decrypted message: {decrypted}\n")

print("Checking signature...")
try:
    verify_signature(message, sign, public_key)
except ValueError as err:
    print(err)
