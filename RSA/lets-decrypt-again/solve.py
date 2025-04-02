from sage.all import *
from pwn import remote,xor
from pkcs1 import emsa_pkcs1_v15
import json

#USED A LOT OF AI



r = remote('socket.cryptohack.org', 13394)

r.recvuntil(b"Just do it multiple times to make sure...\n")

r.sendline(b'{"option": "get_signature"}')
aux = json.loads(r.recvline().strip())
N = int(aux['N'], 16)
E = int(aux['E'], 16)
SIGNATURE = int(aux['signature'], 16)

print(f"{N = }")
print(f"{E = }")
print(f"{SIGNATURE = }")

BIT_LENGTH = 768

msg1 = b"This is a test message for a fake signature."
msg2 = b"My name is mcsky and I own CryptoHack.org"
msg3 = b"Please send all my money to 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"
msgs = [msg1, msg2, msg3]

def set_pubkey(n):
    r.sendline(json.dumps({"option": "set_pubkey", "pubkey": hex(n)[2:]}).encode())
    aux = json.loads(r.recvline().strip())
    return aux['suffix']

def claim(msg, e, index):
    dat = {"option": "claim", "msg": msg.decode(), "e": hex(e), "index": index}
    dat = str(dat).replace("'", '"').encode()
    print(dat)
    r.sendline(dat)
    aux = json.loads(r.recvline().strip())
    return aux

def generate_smooth_prime(min_bound=2**32, signature=SIGNATURE):
    """
    generates a number p that is prime and p-1 is smooth
    we also need to make sure that the signature is a primitive root
    """
    r = 2
    p = 1
    while True:
        p *= r
        r = next_prime(r)
        if is_prime(p + 1) and p + 1 > min_bound:
            if not Zmod(p + 1)(signature).is_primitive_root():
                continue
            return p + 1
        
        
p = generate_smooth_prime(min_bound=N, signature=SIGNATURE)
print("Generated smooth prime:", p)
n = p**2

suffix = set_pubkey(n)

msgs = [msg + suffix.encode() for msg in msgs]
msgs_digest = [emsa_pkcs1_v15.encode(msg, BIT_LENGTH // 8) for msg in msgs]
msgs_digest = [int.from_bytes(msg_digest, 'big') for msg_digest in msgs_digest]

K = Zmod(n)
print("signature is generator for Zmod(n):", K(SIGNATURE).is_primitive_root())

shares = []

for (i, msg_digest) in enumerate(msgs_digest):
    dlog = K(msg_digest).log(K(SIGNATURE))
    print(f"dlog for {msg_digest = } is {dlog = }")
    claim_res = claim(msgs[i], dlog, i)
    print(f"{claim_res = }")
    shares.append(bytes.fromhex(claim_res['secret']))
    print(f"Claimed {i = }")

# xor the shares to get the flag
flag = shares[0]
for share in shares[1:]:
    flag = xor(flag, share)

print("Flag:", flag)
r.close()
