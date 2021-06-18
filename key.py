# from Crypto.PublicKey import RSA

# key = RSA.generate(2048)
# private_key = key.export_key()
# file_out = open("private.pem", "wb")
# file_out.write(private_key)
# file_out.close()

# public_key = key.publickey().export_key()
# file_out = open("receiver.pem", "wb")
# file_out.write(public_key)
# file_out.close()
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

data = "bb7e16f40dab48e0985388e731d810dc".encode()
file_out = open("encrypted_data.bin", "wb")

recipient_key = RSA.import_key(open("receiver.pem").read())
session_key = get_random_bytes(16)

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(data)
[file_out.write(x)
 for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
file_out.close()
