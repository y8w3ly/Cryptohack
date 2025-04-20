from hashlib import sha256
import os

FLAG = b"crypto{??????????????????????????????}"

def hash256(data):
    return sha256(data).digest()

def merge_nodes(a, b):
    return hash256(a+b)

def gen_test(is_true):
    a = hash256(os.urandom(8))
    b = hash256(os.urandom(8))
    c = hash256(os.urandom(8))
    d = hash256(os.urandom(8))
    bias = b"" if is_true else os.urandom(8)
    left = merge_nodes(a, b+bias)
    right = merge_nodes(c, d)
    root = merge_nodes(left, right)
    return a.hex(), b.hex(), c.hex(), d.hex(), root.hex()

challenges = []

for bit in bin(int(FLAG.hex(),16))[2:]:
    a, b, c, d, root = gen_test(int(bit))
    challenges.append([a, b, c, d, root])

with open("output.txt", "w") as f:
    for chal in challenges:
        # Note: in your solution script, you can read each line by calling eval() on it
        f.write(str(chal))
        f.write("\n")
