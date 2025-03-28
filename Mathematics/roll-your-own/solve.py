from Crypto.Util.number import *
from pwn import remote
import json


r = remote('socket.cryptohack.org', 13403)


r.recvuntil(b'Prime generated: "')
p = r.recvline().decode()[:-2]
p = int(p,16)
print(p)

g = p+1
n = pow(p,2)
payload = {'g':hex(g),'n':hex(n)}
r.recvuntil(b"pow(g,q,n) = 1: ")
r.sendline(json.dumps(payload).encode())

r.recvuntil(b'Generated my public key: "')
pubkey = r.recvline().decode()[:-2]
pubkey = int(pubkey,16)
print(pubkey)

r.recvuntil(b"What is my private key: ")
privkey = (pubkey - 1)// p
payload = {'x': hex(privkey)}
r.sendline(json.dumps(payload).encode())
r.interactive()
