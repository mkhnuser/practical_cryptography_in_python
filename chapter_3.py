"""
Listing 3-1. AES ECB Code
"""

# # NEVER USE: ECB is not secure!
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# import os
#
#
# key = os.urandom(16)
# aesCipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
# aesEncryptor = aesCipher.encryptor()
# aesDecryptor = aesCipher.decryptor()

"""
EXERCISE 3.1. A SECRET MESSAGE

AND

EXERCISE 3.2. UPDATED TECHNOLOGY
"""

# NEVER USE: ECB is not secure!
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


KEY = os.urandom(16)


aesCipher = Cipher(algorithms.AES(KEY), modes.ECB())
aes_encryptor = aesCipher.encryptor()
aes_decryptor = aesCipher.decryptor()

to_be_encrypted = input("Please enter a message to be encrypted:\n")
to_be_encrypted = to_be_encrypted.encode()

# NOTE: AES operates in blocks of the size of 16 bytes = 128 bits.
# Because of this, your data has to be a multiple of 16, since blocks have to be full.
block_size_in_bits = 16 * 8
padder = padding.PKCS7(block_size_in_bits).padder()
padded_data = padder.update(to_be_encrypted) + padder.finalize()

# NOTE: Encrypt the stream.
encrypted_stream = b""

for L in range(0, len(padded_data), 16):
    R = L + 16
    chunk = padded_data[L:R]
    encrypted_stream += aes_encryptor.update(chunk)

aes_encryptor.finalize()

print("Plaintext length:", len(to_be_encrypted))
print("Padded length:", len(padded_data))
print("Ciphertext length:", len(encrypted_stream))

# NOTE: Decrypt the stream.
decrypted_stream = b""

for L in range(0, len(encrypted_stream), 16):
    R = L + 16
    chunk = encrypted_stream[L:R]
    decrypted_stream += aes_decryptor.update(chunk)

aes_decryptor.finalize()

# NOTE: Remove PKCS7 padding.
unpadder = padding.PKCS7(block_size_in_bits).unpadder()
plaintext = unpadder.update(decrypted_stream) + unpadder.finalize()
print(plaintext.decode())
