from Crypto.Util.number import *
from pwn import *
from tqdm import tqdm
import json, time

#non mathematical way, deepseek's ideas

r = remote('socket.cryptohack.org', 13398)
r.recvline()

def test(bit):
    st = time.time()
    for i in range(5):
        r.send(json.dumps({'option': 'get_bit', 'i': bit}).encode())
        r.recvline()
    ed = time.time()
    return ed - st

start = time.time()
for i in range(5):
    payload = {'option': 'get_bit', 'i':0}
    r.sendline(json.dumps(payload).encode())
    print(r.recvline())
end = time.time()

diff0 = end - start

start = time.time()
for i in range(5):
    payload = {'option': 'get_bit', 'i':7}
    r.sendline(json.dumps(payload).encode())
    print(r.recvline())
end = time.time()

diff7 = end - start

print(diff0)
print(diff7)
print(diff0>diff7)

diff = diff0 - (diff0 - diff7) * 0.618
print(diff)

flag = ''
x = ''
for index in tqdm(range(8 * 43)):
    x += '01'[test(index) > diff]
    if index % 8 == 7:
        flag += chr(int(x[::-1], 2))
        x = ''
print(flag)

#didn't understand the solution lol
