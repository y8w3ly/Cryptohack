from pwn import * 
import json
import codecs
from binascii import unhexlify
from Crypto.Util.number import long_to_bytes

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    print(request)
    r.sendline(request)

for i in range(100):

    print(i)
    received = json_recv()


    type = received["type"]

    encoded = received["encoded"]
    print(encoded)
    if type == "base64":
        decoded = base64.b64decode(encoded).decode() 
    elif type == "hex":
        decoded = unhexlify(encoded).decode()
    elif type == "rot13":
        decoded = codecs.decode(encoded, 'rot_13')
    elif type == "bigint":
        decoded = long_to_bytes(int(encoded, 16)).decode()
    elif type == "utf-8":
        decoded = ''.join([chr(c) for c in encoded])


    to_send = {
        "decoded": decoded
    }

    print(json_send(to_send))

r.interactive()