import struct

# Convert 32-bit integers to bytes
def int_to_bytes(x):
    return struct.pack('>I', x)

# Constants
W = [0x6b17d1f2, 0xe12c4247, 0xf8bce6e5, 0x63a440f2, 0x77037d81, 0x2deb33a0, 0xf4a13945, 0xd898c296]
X = [0x4fe342e2, 0xfe1a7f9b, 0x8ee7eb4a, 0x7c0f9e16, 0x2bce3357, 0x6b315ece, 0xcbb64068, 0x37bf51f5]
Y = [0xc97445f4, 0x5cdef9f0, 0xd3e05e1e, 0x585fc297, 0x235b82b5, 0xbe8ff3ef, 0xca67c598, 0x52018192]
Z = [0xb28ef557, 0xba31dfcb, 0xdd21ac46, 0xe2a91e3c, 0x304f44cb, 0x87058ada, 0x2cb81515, 0x1e610046]

W_bytes = b''.join([int_to_bytes(x) for x in W])
X_bytes = b''.join([int_to_bytes(x) for x in X])
Y_bytes = b''.join([int_to_bytes(x) for x in Y])
Z_bytes = b''.join([int_to_bytes(x) for x in Z])

# Basic operations
def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def rotate_left(data, x):
    x %= 32
    return data[x:] + data[:x]

def rotate_right(data, x):
    x %= 32
    return data[-x:] + data[:-x]

# Forward scramble_block
def scramble_block(block):
    for _ in range(40):
        block = xor(W_bytes, block)
        block = rotate_left(block, 6)
        block = xor(X_bytes, block)
        block = rotate_right(block, 17)
    return block

# Inverse of one round
def inverse_round(block):
    temp = rotate_left(block, 17)
    temp = xor(temp, X_bytes)
    temp = rotate_right(temp, 6)
    temp = xor(temp, W_bytes)
    return temp

# Inverse scramble_block
def inverse_scramble_block(block):
    for _ in range(40):
        block = inverse_round(block)
    return block

# T_1 transformation
def T_1(mix_in):
    return rotate_left(xor(rotate_right(mix_in, 12), X_bytes), 7)

# Define m1 as the empty message
m1 = b''

# Choose b1 (32 zero bytes)
b1 = bytes(32)

# Compute b0
s = scramble_block(b1)
t = T_1(s)
b0 = inverse_scramble_block(t)

# Construct m2
m2 = b0 + b1  # 64 bytes

# Hex encode for submission
hex_m1 = m1.hex()  # ''
hex_m2 = m2.hex()  # 128-character hex string
import json

payload = json.dumps({"m1": hex_m1, "m2": hex_m2})
print(payload)  # For verification
# {"m1": "", "m2": "hex string of m2"}

# To connect and send (example using socket):
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("socket.cryptohack.org", 13405))
client.recv(1024)  # Receive prompt
client.send((payload + "\n").encode())
response = client.recv(1024).decode()
print(response)  # Should contain the flag