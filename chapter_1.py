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


"""
A follow-up:

Now suppose the string FANQADZAFFANQFTMFUEFTQCGQEFUAZ is given.
How do you brute force it?
"""


def brute_force(ciphertext: str) -> None:
    for shift in range(0, alphabet_length):
        print(decode_with_caesar(ciphertext, shift))


"""
EXERCISE 1.2. AUTOMATED DECODING
In our example, Eve tried decoding various messages until she saw something that looked like English.
Try automating this.
* Get a data structure containing a few thousand english words.
* Create a program that takes in an encoded string, then try decoding it with all 25 shift values.
* Use the dictionary to try to automatically determine which shift is most likely.
"""


# NOTE: The exercise is trivial.


"""
EXERCISE 1.3. A STRONG SUBSTITUTION CIPHER
What if instead of shifting the alphabet, you randomly jumbled the letters?
Create a program that encodes and decodes messages using this kind of substitution.
Some newspapers publish puzzles like this called cryptograms.
"""


import random


def shuffle(plaintext: str) -> str:
    plaintext_length = len(plaintext)
    output_list = ["" for _ in range(plaintext_length)]
    used_pos = set()

    for char in plaintext:
        pos = random.randint(0, plaintext_length - 1)
        while pos in used_pos:
            pos = random.randint(0, plaintext_length - 1)
        output_list[pos] = char
        used_pos.add(pos)

    return "".join(output_list)


"""
EXERCISE 1.4. COUNT THE DICTIONARIES
How many substitution dictionaries are possible
for the cryptogram-style substitution in the previous exercise?
"""


# NOTE: By the product rule with no replacements allowed, n! (n factorial).
# n is the length of the string.


"""
EXERCISE 1.5. IDENTIFYING THE DICTIONARY
Modify your cryptogram program so that
you can identify and pick the jumbled character substitution map with a number.

That is, each mapping has a unique number that identifies it:
picking substitution n should create the same substitution mapping every time.

This exercise is a little tougher than the others. Do your best!
"""


# NOTE: I used ChatGPT to solve this exercise.


# NOTE: We order permutations.
# 0 ABC
# 1 ACB
# 2 BAC
# 3 BCA
# 4 CAB
# 5 CBA


from math import factorial


def permutation_from_number(alphabet: str, n: int) -> str:
    alphabet_length = len(alphabet)

    if len(set(alphabet)) != alphabet_length:
        raise ValueError("Alphabet must contain distinct characters")

    if not 0 <= n < factorial(alphabet_length):
        raise ValueError("Number is out of range")

    available_chars = list(alphabet)
    res = []

    for remaining_chars in range(alphabet_length, 0, -1):
        block_size = factorial(remaining_chars - 1)
        index, n = divmod(n, block_size)
        res.append(available_chars.pop(index))

    return "".join(res)


if __name__ == "__main__":
    for n in range(0, 6):
        print(permutation_from_number("ABC", n))
