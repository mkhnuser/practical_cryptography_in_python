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

# NOTE: I only test ECB KATS.

import zipfile
import pathlib
from typing import Literal

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


ENCRYPT_HEADER = "[ENCRYPT]"
DECREPT_HEADER = "[DECRYPT]"
KEY_ATTRIBUTE = "KEY"
PLAINTEXT_ATTRIBUTE = "PLAINTEXT"
CIPHERTEXT_ATTRIBUTE = "CIPHERTEXT"
COUNT_ATTRIBUTE = "COUNT"


artifacts_dir_path = pathlib.Path("./artifacts/")
kats_zip_archive_path = artifacts_dir_path / "KAT_AES.zip"

with zipfile.ZipFile(kats_zip_archive_path) as z:
    z.extractall(artifacts_dir_path / "KAT_AES_responses")


def verify_test_case(
    key: bytes, plaintext: str, ciphertext: str, transformation_direction: str
) -> None:
    aes_cipher = Cipher(
        algorithm=algorithms.AES(key),
        mode=modes.ECB(),
        backend=default_backend(),
    )
    aes_encryptor = aes_cipher.encryptor()
    aes_decryptor = aes_cipher.decryptor()

    if transformation_direction == "encryption":
        encrypted_data = (
            aes_encryptor.update(bytes.fromhex(plaintext)) + aes_encryptor.finalize()
        )
        encrypted_data = encrypted_data.hex()
        assert encrypted_data == ciphertext
    elif transformation_direction == "decryption":
        decrypted_data = (
            aes_decryptor.update(bytes.fromhex(ciphertext)) + aes_decryptor.finalize()
        )
        decrypted_data = decrypted_data.hex()
        assert decrypted_data == plaintext
    else:
        raise RuntimeError("Invalid Transformation Direction.")


def try_running_a_previous_test(
    has_a_test_been_assembled: bool,
    key: bytes | None,
    plaintext: str | None,
    ciphertext: str | None,
    transformation_direction: str | None,
    passed_tests_counter: int,
) -> None | tuple:
    if not has_a_test_been_assembled:
        return

    assert key is not None
    assert plaintext is not None
    assert ciphertext is not None
    assert transformation_direction is not None

    verify_test_case(key, plaintext, ciphertext, transformation_direction)

    has_a_test_been_assembled = False
    key = None
    plaintext = None
    ciphertext = None

    passed_tests_counter += 1

    return (
        has_a_test_been_assembled,
        key,
        plaintext,
        ciphertext,
        transformation_direction,
        passed_tests_counter,
    )


def verify_ecb_files() -> tuple:
    response_file_paths = (artifacts_dir_path / "KAT_AES_responses").glob("ECB*.rsp")
    global_tests_counter = 0
    global_count_attributes_counter = 0

    for response_file_path in response_file_paths:
        transformation_direction: Literal["encryption", "decryption", None] = None
        key: bytes | None = None
        plaintext: str | None = None
        ciphertext: str | None = None
        passed_tests_counter_per_file = 0
        has_a_test_been_assembled: bool = False

        with response_file_path.open() as response_file:
            for line in response_file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                # WARNING: Just before we change a transformation direction,
                # run a test, if one is assembled.
                if ENCRYPT_HEADER in line:
                    previous_test_run_result = try_running_a_previous_test(
                        has_a_test_been_assembled,
                        key,
                        plaintext,
                        ciphertext,
                        transformation_direction,
                        passed_tests_counter_per_file,
                    )
                    if previous_test_run_result is not None:
                        (
                            has_a_test_been_assembled,
                            key,
                            plaintext,
                            ciphertext,
                            transformation_direction,
                            passed_tests_counter_per_file,
                        ) = previous_test_run_result
                    transformation_direction = "encryption"
                    continue
                elif DECREPT_HEADER in line:
                    previous_test_run_result = try_running_a_previous_test(
                        has_a_test_been_assembled,
                        key,
                        plaintext,
                        ciphertext,
                        transformation_direction,
                        passed_tests_counter_per_file,
                    )
                    if previous_test_run_result is not None:
                        (
                            has_a_test_been_assembled,
                            key,
                            plaintext,
                            ciphertext,
                            transformation_direction,
                            passed_tests_counter_per_file,
                        ) = previous_test_run_result
                    transformation_direction = "decryption"
                    continue

                # NOTE: When a new counter is encountered,
                # run a test, if one is assembled.
                if COUNT_ATTRIBUTE in line:
                    global_count_attributes_counter += 1
                    previous_test_run_result = try_running_a_previous_test(
                        has_a_test_been_assembled,
                        key,
                        plaintext,
                        ciphertext,
                        transformation_direction,
                        passed_tests_counter_per_file,
                    )

                    if previous_test_run_result is not None:
                        (
                            has_a_test_been_assembled,
                            key,
                            plaintext,
                            ciphertext,
                            transformation_direction,
                            passed_tests_counter_per_file,
                        ) = previous_test_run_result

                    has_a_test_been_assembled = False
                    key = None
                    plaintext = None
                    ciphertext = None

                elif KEY_ATTRIBUTE in line:
                    key_str = line.split("=")[-1].strip()
                    key = bytes.fromhex(key_str)
                elif PLAINTEXT_ATTRIBUTE in line:
                    plaintext = line.split("=")[-1].strip()
                elif CIPHERTEXT_ATTRIBUTE in line:
                    ciphertext = line.split("=")[-1].strip()

                if key is not None and plaintext is not None and ciphertext is not None:
                    has_a_test_been_assembled = True

            # WARNING: Don't forget to validate the last file line.
            previous_test_run_result = try_running_a_previous_test(
                has_a_test_been_assembled,
                key,
                plaintext,
                ciphertext,
                transformation_direction,
                passed_tests_counter_per_file,
            )
            if previous_test_run_result is not None:
                *_, passed_tests_counter_per_file = previous_test_run_result

            global_tests_counter += passed_tests_counter_per_file

    return global_tests_counter, global_count_attributes_counter


if __name__ == "__main__":
    all_passed_tests, all_counts = verify_ecb_files()
    print(all_passed_tests, all_counts)
    assert all_passed_tests == all_counts
