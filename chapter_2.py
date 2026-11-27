"""
Listing 2-1. Intro to hashlib
"""

# import hashlib
#
#
# md5hasher = hashlib.md5()
# # NOTE: Let's print a fingerprint for an empty document.
# print(md5hasher.hexdigest())
# print(len(md5hasher.hexdigest()))

"""
Listing 2-2. Hash Names
"""

# import hashlib
#
#
# md5hasher = hashlib.md5(b"alice")
# print(md5hasher.hexdigest())
# md5hasher = hashlib.md5(b"bob")
# print(md5hasher.hexdigest())


"""
Listing 2-3. Combine Operations
"""

# import hashlib
#
#
# print(hashlib.md5(b"alice").hexdigest())
# print(hashlib.md5(b"bob").hexdigest())


"""
EXERCISE 2.1. WELCOME TO MD5
"""

# import hashlib
#
# inputs = [
#     b"alice",
#     b"bob",
#     b"balice",
#     b"cob",
#     b"a",
#     b"aa",
#     b"aaaaaaaaaa",
#     b"a" * 100000,
# ]
#
# for input_ in inputs:
#     print(hashlib.md5(input_).hexdigest())

"""
Listing 2-4. Hash Update
"""

# import hashlib
#
# md5hasher = hashlib.md5()
# md5hasher.update(b"a")
# md5hasher.update(b"l")
# md5hasher.update(b"i")
# md5hasher.update(b"c")
# md5hasher.update(b"e")
#
# assert md5hasher.hexdigest() == hashlib.md5(b"alice").hexdigest()


"""
EXERCISE 2.2. GOOGLE KNOWS!
"""

# 1. 5f4dcc3b5aa765d61d8327deb882cf99
# 2. d41d8cd98f00b204e9800998ecf8427e
# 3. 6384e2b2184bcbf58eccf10ca7a6563c


"""
Listing 2-5. Avalanche
"""

# NOTE: I modified the listing a bit.
#
# import hashlib
#
#
# dad_hex = hashlib.md5(b"dad").hexdigest()
# dad_bin = bin(int(dad_hex, 16))
# print(dad_bin)
#
#
# bad_hex = hashlib.md5(b"bad").hexdigest()
# bad_bin = bin(int(bad_hex, 16))
# print(bad_bin)
#
#
# # NOTE: How many alternate bits are there in two strings?
# # Answer: 62.
# # So, 128 - 62 = 66 bits were not changed, and 62 were.
# # That's an example of an avalanche property, with roughly 50% change rate.
# print((int(dad_bin, 2) ^ int(bad_bin, 2)).bit_count())


"""
EXERCISE 2.4. MD5 OF A FILE
"""

# import io
# import hashlib
#
#
# bytes_ = io.BytesIO(b"This is an example of a file which is about to be hashed.\n")
#
#
# print(hashlib.md5(bytes_.read()).hexdigest())
#

# NOTE: md5sum utility will produce the same output:
# md5sum -b << EOF
# This is an example of a file which is about to be hashed.
# EOF
# 6e1afe993a562d1108fa8daedc35bafb *-


"""
Listing 2-6. Change to SHA-256
"""

# import hashlib
#
# print(hashlib.md5(b"alice").hexdigest())
# print(hashlib.sha1(b"alice").hexdigest())
# print(hashlib.sha256(b"alice").hexdigest())


"""
Listing 2-7. Scrypt Generate
"""

# import os
# from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
# from cryptography.hazmat.backends import default_backend
#
#
# # NOTE:
# # 1. Salt has to be generated manually in this case.
# # 2. Be sure to save compute parameters as well as salt to a database.
# # 3. The default backend is used, which might be OpenSSL or another library.
# salt = os.urandom(16)
# kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
# derived_key = kdf.derive(b"my great password")
# print(derived_key)


"""
Listing 2-9. Alphabet Permutations
"""


def generate(alphabet: str, max_len: int):
    if max_len <= 0:
        return

    for c in alphabet:
        yield c

    for c in alphabet:
        for next_ in generate(alphabet, max_len - 1):
            yield c + next_


# if __name__ == "__main__":
#     for output in generate("abc", 2):
#         print(output)


"""
EXERCISE 2.5. THE POWER OF ONE
"""


# import string
# import random
# import hashlib
# import timeit
#
#
# def compute() -> None:
#     preimage_seed = random.choice(string.ascii_lowercase)
#     preimage_seed = preimage_seed.encode()
#     test_hash = hashlib.md5(preimage_seed).hexdigest()
#
#     for char in generate(string.ascii_lowercase, 1):
#         char = char.encode()
#         candidate_hash = hashlib.md5(char).hexdigest()
#
#         if candidate_hash == test_hash:
#             print(char, candidate_hash)
#             return
#
#     raise Exception("Shouldn't be here!")
#
#
# if __name__ == "__main__":
#     print(timeit.timeit(compute, number=10))


"""
EXERCISE 2.6. THE POWER OF ONE, BUT BIGGER!
"""


# import string
# import random
# import hashlib
# import timeit
#
#
# def compute() -> None:
#     preimage_seed = random.choice(string.printable)
#     preimage_seed = preimage_seed.encode()
#     test_hash = hashlib.md5(preimage_seed).hexdigest()
#
#     for char in generate(string.printable, 1):
#         char = char.encode()
#         candidate_hash = hashlib.md5(char).hexdigest()
#
#         if candidate_hash == test_hash:
#             print(char, candidate_hash)
#             return
#
#     raise Exception("Shouldn't be here!")
#
#
# if __name__ == "__main__":
#     print(timeit.timeit(compute, number=10))


"""
EXERCISE 2.7. PASSWORD LENGTH’S EFFECTS ON ATTACK TIME
"""


import string
import random
import hashlib
import timeit


def compute() -> None:
    # NOTE: A two-letter password is now used.
    preimage_seed = random.choice(string.printable) + random.choice(string.printable)
    preimage_seed = preimage_seed.encode()
    test_hash = hashlib.md5(preimage_seed).hexdigest()

    for char in generate(string.printable, 2):
        char = char.encode()
        candidate_hash = hashlib.md5(char).hexdigest()

        if candidate_hash == test_hash:
            print(char, candidate_hash)
            return

    raise Exception("Shouldn't be here!")


if __name__ == "__main__":
    print(timeit.timeit(compute, number=10))


# NOTE: The result: 0.0001, then 0.0005, then 0.05.
