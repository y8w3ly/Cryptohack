from hashlib import sha1
from Crypto.Util.number import bytes_to_long, long_to_bytes
from sage.all import *
from ecdsa.ecdsa import curve_256, generator_256, Public_key, ellipticcurve

# Given data
hidden_flag = (16807196250009982482930925323199249441776811719221084165690521045921016398804, 72892323560996016030675756815328265928288098939353836408589138718802282948311)
pubkey_point = (48780765048182146279105449292746800142985733726316629478905429239240156048277, 74172919609718191102228451394074168154654001177799772446328904575002795731796)
sig_r = [
    0x91f66ac7557233b41b3044ab9daf0ad891a8ffcaf99820c3cd8a44fc709ed3ae,
    0xe8875e56b79956d446d24f06604b7705905edac466d5469f815547dea7a3171c,
    0x566ce1db407edae4f32a20defc381f7efb63f712493c3106cf8e85f464351ca6
]
sig_s = [
    0x1dd0a378454692eb4ad68c86732404af3e73c6bf23a8ecc5449500fcab05208d,
    0x582ecf967e0e3acf5e3853dbe65a84ba59c3ec8a43951bcff08c64cb614023f8,
    0x9e4304a36d2c83ef94e19a60fb98f659fa874bfb999712ceb58382e2ccda26ba
]

messages = [
    'I have hidden the secret flag as a point of an elliptic curve using my private key.',
    'The discrete logarithm problem is very hard to solve, so it will remain a secret forever.',
    'Good luck!'
]

# Curve parameters
curve = curve_256

G = generator_256
q = G.order()
# Compute message hashes
h = [bytes_to_long(sha1(msg.encode()).digest()) for msg in messages]

# Calculate A_i and B_i for each signature
A = []
B = []
for i in range(3):
    s_inv = inverse_mod(sig_s[i], q)
    A_i = (sig_r[i] * s_inv) % q
    B_i = (-h[i] * s_inv) % q
    A.append(A_i)
    B.append(B_i)

# Lattice parameters
K = 2**160  # Nonce upper bound (SHA1 is 160 bits)
n = 3       # Number of signatures

# Build the lattice basis matrix
m = matrix(ZZ, n + 1, n + 2)
for i in range(n):
    m[i, i]     = q
    m[i, n]     = A[i]
# <-- FIX HERE -->
m[n, 0:n]       = vector(ZZ, B)
m[n, n]         = K // q
m[n, n + 1]     = K

# Perform LLL reduction
m_lll = m.LLL()

# Extract private key d
d = None
for row in m_lll:
    if row[-1] == K:
        d_candidate = (row[-2] * q) // K
        # Verify against public key
        try:
            candidate_pub = Public_key(G, d_candidate * G)
            if (candidate_pub.point.x(), candidate_pub.point.y()) == pubkey_point:
                d = d_candidate % q
                break
        except:
            continue

if d is None:
    raise ValueError("Private key not found")

# Recover the flag
T = ellipticcurve.Point(curve, hidden_flag[0], hidden_flag[1])
Q = inverse_mod(d, q) * T
flag = long_to_bytes(int(Q.x())).decode()

print(f"Private Key d: {d}")
print(f"Flag: {flag}")