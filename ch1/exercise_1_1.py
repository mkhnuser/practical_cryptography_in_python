"""
EXERCISE 1.1. SHIFT CIPHER ENCODER
Create a python program that encodes and decodes messages using the shift cipher described in this section.
The amount of shift must be configurable.
"""

import string


A_ORD = ord("A")
alphabet_length = len(string.ascii_uppercase)


def encode_with_caesar(plaintext: str, step: int) -> str:
    output_list = []

    for char in plaintext:
        if char in string.ascii_uppercase:
            shifted_ord = (((ord(char) - A_ORD) + step) % alphabet_length) + A_ORD
            output_list.append(chr(shifted_ord))
        else:
            output_list.append(char)

    return "".join(output_list)


def decode_with_caesar(ciphertext: str, step: int) -> str:
    output_list = []

    for char in ciphertext:
        if char in string.ascii_uppercase:
            unshifted_ord = (((ord(char) - A_ORD) - step) % alphabet_length) + A_ORD
            output_list.append(chr(unshifted_ord))
        else:
            output_list.append(char)

    return "".join(output_list)


def test() -> None:
    assert encode_with_caesar("HELLO WORLD", 1) == "IFMMP XPSME"
    assert encode_with_caesar("HELLO WORLD", 2) == "JGNNQ YQTNF"
    assert encode_with_caesar("ZA", 1) == "AB"

    assert decode_with_caesar(encode_with_caesar("HELLO WORLD", 1), 1) == "HELLO WORLD"
    assert decode_with_caesar(encode_with_caesar("HELLO WORLD", 2), 2) == "HELLO WORLD"
    assert decode_with_caesar(encode_with_caesar("ZA", 1), 1) == "ZA"


if __name__ == "__main__":
    test()
