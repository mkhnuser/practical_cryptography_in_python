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

# # NEVER USE: ECB is not secure!
# import os
#
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.primitives import padding
#
#
# KEY = os.urandom(16)
#
#
# aesCipher = Cipher(algorithms.AES(KEY), modes.ECB())
# aes_encryptor = aesCipher.encryptor()
# aes_decryptor = aesCipher.decryptor()
#
# to_be_encrypted = input("Please enter a message to be encrypted:\n")
# to_be_encrypted = to_be_encrypted.encode()
#
# # NOTE: AES operates in blocks of the size of 16 bytes = 128 bits.
# # Because of this, your data has to be a multiple of 16, since blocks have to be full.
# block_size_in_bits = 16 * 8
# padder = padding.PKCS7(block_size_in_bits).padder()
# padded_data = padder.update(to_be_encrypted) + padder.finalize()
#
# # NOTE: Encrypt the stream.
# encrypted_stream = b""
#
# for L in range(0, len(padded_data), 16):
#     R = L + 16
#     chunk = padded_data[L:R]
#     encrypted_stream += aes_encryptor.update(chunk)
#
# aes_encryptor.finalize()
#
# print("Plaintext length:", len(to_be_encrypted))
# print("Padded length:", len(padded_data))
# print("Ciphertext length:", len(encrypted_stream))
#
# # NOTE: Decrypt the stream.
# decrypted_stream = b""
#
# for L in range(0, len(encrypted_stream), 16):
#     R = L + 16
#     chunk = encrypted_stream[L:R]
#     decrypted_stream += aes_decryptor.update(chunk)
#
# aes_decryptor.finalize()
#
# # NOTE: Remove PKCS7 padding.
# unpadder = padding.PKCS7(block_size_in_bits).unpadder()
# plaintext = unpadder.update(decrypted_stream) + unpadder.finalize()
# print(plaintext.decode())

"""
Listing 3-2. AES ECB KATs
"""

# # NOTE: Here we test AES implementation using just some KATs from NIST archive.
#
# # NEVER USE: ECB is not secure!
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
#
# # NIST AES ECBGFSbox128.rsp ENCRYPT Kats
# # First value of each pair is plaintext
# # Second value of each pair is ciphertext
# nist_kats = [
#     ("f34481ec3cc627bacd5dc3fb08f273e6", "0336763e966d92595a567cc9ce537f5e"),
#     ("9798c4640bad75c7c3227db910174e72", "a9a1631bf4996954ebc093957b234589"),
#     ("96ab5c2ff612d9dfaae8c31f30c42168", "ff4f8391a6a40ca5b25d23bedd44a597"),
#     ("6a118a874519e64e9963798a503f1d35 ", "dc43be40be0e53712f7e2bf5ca707209"),
# ]
#
# test_key = bytes.fromhex("00000000000000000000000000000000")
#
# aesCipher = Cipher(algorithms.AES(test_key), modes.ECB(), backend=default_backend())
# aesEncryptor = aesCipher.encryptor()
# aesDecryptor = aesCipher.decryptor()
#
# # test each input
# for index, kat in enumerate(nist_kats):
#     plaintext, want_ciphertext = kat
#     plaintext_bytes = bytes.fromhex(plaintext)
#     ciphertext_bytes = aesEncryptor.update(plaintext_bytes)
#     got_ciphertext = ciphertext_bytes.hex()
#
#     result = "[PASS]" if got_ciphertext == want_ciphertext else "[FAIL]"
#
#     print(
#         "Test {}. Expected {}, got {}. Result {}.".format(
#             index,
#             want_ciphertext,
#             got_ciphertext,
#             result,
#         )
#     )


"""
EXERCISE 3.5. ALL NIST KATS
"""
#
# # NOTE: I only test ECB KATS.
#
# import zipfile
# import pathlib
# from typing import Literal
#
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
#
#
# ENCRYPT_HEADER = "[ENCRYPT]"
# DECREPT_HEADER = "[DECRYPT]"
# KEY_ATTRIBUTE = "KEY"
# PLAINTEXT_ATTRIBUTE = "PLAINTEXT"
# CIPHERTEXT_ATTRIBUTE = "CIPHERTEXT"
# COUNT_ATTRIBUTE = "COUNT"
#
#
# artifacts_dir_path = pathlib.Path("./artifacts/")
# kats_zip_archive_path = artifacts_dir_path / "KAT_AES.zip"
#
# with zipfile.ZipFile(kats_zip_archive_path) as z:
#     z.extractall(artifacts_dir_path / "KAT_AES_responses")
#
#
# def verify_test_case(
#     key: bytes, plaintext: str, ciphertext: str, transformation_direction: str
# ) -> None:
#     aes_cipher = Cipher(
#         algorithm=algorithms.AES(key),
#         mode=modes.ECB(),
#         backend=default_backend(),
#     )
#     aes_encryptor = aes_cipher.encryptor()
#     aes_decryptor = aes_cipher.decryptor()
#
#     if transformation_direction == "encryption":
#         encrypted_data = (
#             aes_encryptor.update(bytes.fromhex(plaintext)) + aes_encryptor.finalize()
#         )
#         encrypted_data = encrypted_data.hex()
#         assert encrypted_data == ciphertext
#     elif transformation_direction == "decryption":
#         decrypted_data = (
#             aes_decryptor.update(bytes.fromhex(ciphertext)) + aes_decryptor.finalize()
#         )
#         decrypted_data = decrypted_data.hex()
#         assert decrypted_data == plaintext
#     else:
#         raise RuntimeError("Invalid Transformation Direction.")
#
#
# def try_running_a_previous_test(
#     has_a_test_been_assembled: bool,
#     key: bytes | None,
#     plaintext: str | None,
#     ciphertext: str | None,
#     transformation_direction: str | None,
#     passed_tests_counter: int,
# ) -> None | tuple:
#     if not has_a_test_been_assembled:
#         return
#
#     assert key is not None
#     assert plaintext is not None
#     assert ciphertext is not None
#     assert transformation_direction is not None
#
#     verify_test_case(key, plaintext, ciphertext, transformation_direction)
#
#     has_a_test_been_assembled = False
#     key = None
#     plaintext = None
#     ciphertext = None
#
#     passed_tests_counter += 1
#
#     return (
#         has_a_test_been_assembled,
#         key,
#         plaintext,
#         ciphertext,
#         transformation_direction,
#         passed_tests_counter,
#     )
#
#
# def verify_ecb_files() -> tuple:
#     response_file_paths = (artifacts_dir_path / "KAT_AES_responses").glob("ECB*.rsp")
#     global_tests_counter = 0
#     global_count_attributes_counter = 0
#
#     for response_file_path in response_file_paths:
#         transformation_direction: Literal["encryption", "decryption", None] = None
#         key: bytes | None = None
#         plaintext: str | None = None
#         ciphertext: str | None = None
#         passed_tests_counter_per_file = 0
#         has_a_test_been_assembled: bool = False
#
#         with response_file_path.open() as response_file:
#             for line in response_file:
#                 line = line.strip()
#
#                 if not line or line.startswith("#"):
#                     continue
#
#                 # WARNING: Just before we change a transformation direction,
#                 # run a test, if one is assembled.
#                 if ENCRYPT_HEADER in line:
#                     previous_test_run_result = try_running_a_previous_test(
#                         has_a_test_been_assembled,
#                         key,
#                         plaintext,
#                         ciphertext,
#                         transformation_direction,
#                         passed_tests_counter_per_file,
#                     )
#                     if previous_test_run_result is not None:
#                         (
#                             has_a_test_been_assembled,
#                             key,
#                             plaintext,
#                             ciphertext,
#                             transformation_direction,
#                             passed_tests_counter_per_file,
#                         ) = previous_test_run_result
#                     transformation_direction = "encryption"
#                     continue
#                 elif DECREPT_HEADER in line:
#                     previous_test_run_result = try_running_a_previous_test(
#                         has_a_test_been_assembled,
#                         key,
#                         plaintext,
#                         ciphertext,
#                         transformation_direction,
#                         passed_tests_counter_per_file,
#                     )
#                     if previous_test_run_result is not None:
#                         (
#                             has_a_test_been_assembled,
#                             key,
#                             plaintext,
#                             ciphertext,
#                             transformation_direction,
#                             passed_tests_counter_per_file,
#                         ) = previous_test_run_result
#                     transformation_direction = "decryption"
#                     continue
#
#                 # NOTE: When a new counter is encountered,
#                 # run a test, if one is assembled.
#                 if COUNT_ATTRIBUTE in line:
#                     global_count_attributes_counter += 1
#                     previous_test_run_result = try_running_a_previous_test(
#                         has_a_test_been_assembled,
#                         key,
#                         plaintext,
#                         ciphertext,
#                         transformation_direction,
#                         passed_tests_counter_per_file,
#                     )
#
#                     if previous_test_run_result is not None:
#                         (
#                             has_a_test_been_assembled,
#                             key,
#                             plaintext,
#                             ciphertext,
#                             transformation_direction,
#                             passed_tests_counter_per_file,
#                         ) = previous_test_run_result
#
#                     has_a_test_been_assembled = False
#                     key = None
#                     plaintext = None
#                     ciphertext = None
#
#                 elif KEY_ATTRIBUTE in line:
#                     key_str = line.split("=")[-1].strip()
#                     key = bytes.fromhex(key_str)
#                 elif PLAINTEXT_ATTRIBUTE in line:
#                     plaintext = line.split("=")[-1].strip()
#                 elif CIPHERTEXT_ATTRIBUTE in line:
#                     ciphertext = line.split("=")[-1].strip()
#
#                 if key is not None and plaintext is not None and ciphertext is not None:
#                     has_a_test_been_assembled = True
#
#             # WARNING: Don't forget to validate the last file line.
#             previous_test_run_result = try_running_a_previous_test(
#                 has_a_test_been_assembled,
#                 key,
#                 plaintext,
#                 ciphertext,
#                 transformation_direction,
#                 passed_tests_counter_per_file,
#             )
#             if previous_test_run_result is not None:
#                 *_, passed_tests_counter_per_file = previous_test_run_result
#
#             global_tests_counter += passed_tests_counter_per_file
#
#     return global_tests_counter, global_count_attributes_counter
#
#
# if __name__ == "__main__":
#     all_passed_tests, all_counts = verify_ecb_files()
#     print(all_passed_tests, all_counts)
#     assert all_passed_tests == all_counts

"""
A padding follow-up.
"""

# # NEVER USE: ECB is not secure!
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
#
# # Alice and Bob's Shared Key
# test_key = bytes.fromhex("00112233445566778899AABBCCDDEEFF")
#
# aesCipher = Cipher(algorithms.AES(test_key), modes.ECB(), backend=default_backend())
# aesEncryptor = aesCipher.encryptor()
# aesDecryptor = aesCipher.decryptor()
#
# message = b"""
# FROM: FIELD AGENT ALICE
# TO: FIELD AGENT BOB
# RE: Meeting
# DATE: 2001-1-1
#
# Meet me today at the docks at 2300."""
#
# message += b"E" * (-len(message) % 16)
# ciphertext = aesEncryptor.update(message)
# print(ciphertext)

"""
EXERCISE 3.6. SENDING BOB A MESSAGE
"""

# NOTE: The exercise is straightforward.

"""
EXERCISE 3.7. SENDING BOB A FAKE MESSAGE
"""

# NEVER USE: ECB is not secure!
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


test_key = bytes.fromhex("00112233445566778899AABBCCDDEEFF")
aes_cipher = Cipher(algorithms.AES(test_key), modes.ECB())


message_1 = """
FROM: FIELD AGENT ALICE
TO: FIELD AGENT BOB
RE: Meeting
DATE: 2001-1-1

Meet me today at the docks at 2300."""

message_2 = """
FROM: FIELD AGENT ALICE
TO: FIELD AGENT BOB
RE: Meeting
DATE: 2001-2-2

Meet me today at the theater at 1200."""

message_1 = message_1.encode()
message_2 = message_2.encode()

for m in (message_1, message_2):
    aes_encryptor = aes_cipher.encryptor()
    aes_decryptor = aes_cipher.decryptor()

    # NOTE: AES operates in blocks of the size of 16 bytes = 128 bits.
    # Because of this, your data has to be a multiple of 16, since blocks have to be full.
    block_size_in_bits = 16 * 8
    padder = padding.PKCS7(block_size_in_bits).padder()
    padded_data = padder.update(m) + padder.finalize()

    # NOTE: Encrypt the stream.
    encrypted_stream = b""

    for L in range(0, len(padded_data), 16):
        R = L + 16
        chunk = padded_data[L:R]
        encrypted_stream += aes_encryptor.update(chunk)

    aes_encryptor.finalize()

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


# NOTE: An example of a cut-and-paste attack follows.


# NOTE:
# The code above can be used to obtain:
# message_1 ciphertext:
# 0aee9b602c574044778d4f6de3481cb90f3b683d1af60ed69396949eaf293eb244760fa0bb791339d557b43b250ac27c8430e159229e4bf5c7b39fe1fb72cfaba5c7412fda6ac67fe63093168f474913dbd386db053613be242c6059539f93dae5e98a5471100f3fe8febcdcb1ff119c
# message_2 ciphertext:
# 0aee9b602c574044778d4f6de3481cb90f3b683d1af60ed69396949eaf293eb244760fa0bb791339d557b43b250ac27c8430e159229e4bf5c7b39fe1fb72cfabebe95d01d0207a8e9a1580563515c660738188d94d418847fd6e357a1ef861d5f2b80b2bffd06358d6f02c126a9fb642
# messages' common part:
# 0aee9b602c574044778d4f6de3481cb90f3b683d1af60ed69396949eaf293eb244760fa0bb791339d557b43b250ac27c8430e159229e4bf5c7b39fe1fb72cfab
# message_1 unique part:
# a5c7412fda6ac67fe63093168f474913dbd386db053613be242c6059539f93dae5e98a5471100f3fe8febcdcb1ff119c
# message_2 unique part:
# ebe95d01d0207a8e9a1580563515c660738188d94d418847fd6e357a1ef861d5f2b80b2bffd06358d6f02c126a9fb642

# NOTE: Let's create a new message.
# Let's use common part, some part of message 1, and some part of message 2.
message_common_part = "0aee9b602c574044778d4f6de3481cb90f3b683d1af60ed69396949eaf293eb244760fa0bb791339d557b43b250ac27c8430e159229e4bf5c7b39fe1fb72cfab"
message_1_unique_part = "a5c7412fda6ac67fe63093168f474913dbd386db053613be242c6059539f93dae5e98a5471100f3fe8febcdcb1ff119c"
message_2_unique_part = "ebe95d01d0207a8e9a1580563515c660738188d94d418847fd6e357a1ef861d5f2b80b2bffd06358d6f02c126a9fb642"

for break_point_index in range(1, len(message_1_unique_part)):
    message_1_part = message_1_unique_part[:break_point_index]
    message_2_part = message_2_unique_part[break_point_index:]
    malformed_ciphertext = message_common_part + message_1_part + message_2_part
    malformed_ciphertext = bytes.fromhex(malformed_ciphertext)

    aes_decryptor = aes_cipher.decryptor()

    # NOTE: Decrypt the stream.
    decrypted_stream = b""

    for L in range(0, len(malformed_ciphertext), 16):
        R = L + 16
        chunk = malformed_ciphertext[L:R]
        decrypted_stream += aes_decryptor.update(chunk)

    aes_decryptor.finalize()

    try:
        # NOTE: Remove PKCS7 padding.
        block_size_in_bits = 16 * 8
        unpadder = padding.PKCS7(block_size_in_bits).unpadder()
        plaintext = unpadder.update(decrypted_stream) + unpadder.finalize()
        print(plaintext.decode())
    except Exception:
        continue
