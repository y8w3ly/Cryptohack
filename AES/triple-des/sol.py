import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long

def encrypt(key, plain):
    url = "http://aes.cryptohack.org/triple_des/encrypt/"
    url += key
    url += "/"
    url += plain.hex()
    url += "/"
    r = requests.get(url).json()
    return bytes.fromhex(r["ciphertext"])

def encrypt_flag(key):
    url = "http://aes.cryptohack.org/triple_des/encrypt_flag/"
    r = requests.get(url + key + '/').json()
    return bytes.fromhex(r["ciphertext"])

key = b'\x00'*8 + b'\xff'*8
flag = encrypt_flag(key.hex())
cipher = encrypt(key.hex(), flag)
print(cipher)
