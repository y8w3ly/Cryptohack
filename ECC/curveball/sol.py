from pwn import remote
import json

p = 2**256 - 2**224 + 2**192 + 2**96 - 1
n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

x_bing = 0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531
y_bing = 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A


g_x = x_bing
g_y = (p - y_bing) % p


d = n - 1

payload = {
    "host": "attacker.example",
    "curve": "secp256r1",
    "generator": [g_x, g_y],
    "private_key": d
}

io = remote('socket.cryptohack.org', 13382)
io.recvline()
payload = json.dumps(payload)
io.sendline(payload)
print(io.recvline().decode().strip())


