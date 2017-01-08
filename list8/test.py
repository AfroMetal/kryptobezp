from list8 import key, rsa

public_key, private_key = key.get_keys(1024)

message = 'Hello, world!'

print(f"Message is: {message}")

crypto = rsa.encrypt(message, public_key)
sign = rsa.sign(message, private_key)

print(f"Ciphertext: {crypto}")
print(f"Signature: {sign}")

print(f"Decrypted message: {rsa.decrypt(crypto, private_key)}")
print("Checking signature...")
print(rsa.verify_signature(message, sign, public_key))
