from pwn import remote
import json, hashlib
from Crypto.Util.number import inverse, bytes_to_long
from ecdsa.ecdsa import generator_192
N = generator_192.order()
def sha1_long(m: bytes) -> int:
    return bytes_to_long(hashlib.sha1(m).digest())
def recover_privkey(r: int, s: int, h: int, max_k: int) -> int:
    for k in range(1, max_k):
        if (generator_192 * k).x() % N == r:
            return (s * k - h) * inverse(r, N) % N
    raise ValueError("Could not recover k!")
def sign_msg(msg: str, d: int, k: int) -> (int, int):
    h = sha1_long(msg.encode())
    R = generator_192 * k
    r = R.x() % N
    s = (inverse(k, N) * (h + d * r)) % N
    return r, s
io = remote('socket.cryptohack.org', 13381)
print(io.recvline().decode(), end='')
io.sendline(json.dumps({"option": "sign_time"}).encode())
resp = json.loads(io.recvline().decode())
msg, r_hex, s_hex = resp['msg'], resp['r'], resp['s']
r, s = int(r_hex, 16), int(s_hex, 16)
_, time_str = msg.split(" is ")
secs = int(time_str.split(":")[1])
h = sha1_long(msg.encode())
d = recover_privkey(r, s, h, secs)
print(f"[+] Recovered d = {hex(d)}")
k_forge = 2  
r_new, s_new = sign_msg("unlock", d, k_forge)
payload = {
    "option": "verify",
    "msg": "unlock",
    "r": hex(r_new),
    "s": hex(s_new)
}
io.sendline(json.dumps(payload).encode())
print(io.recvline().decode())
#ai is so powerful