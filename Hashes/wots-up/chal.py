import hashlib
import json
from os import urandom
from Crypto.Cipher import AES

BYTE_MAX = 255
KEY_LEN = 32


class Winternitz:
    def __init__(self, priv_seed=urandom(KEY_LEN)):
        self.priv_key = []
        for _ in range(KEY_LEN):
            priv_seed = self.hash(priv_seed)
            self.priv_key.append(priv_seed)
        self.gen_pubkey()

    def gen_pubkey(self):
        self.pub_key = []
        for i in range(KEY_LEN):
            pub_item = self.hash(self.priv_key[i])
            for _ in range(BYTE_MAX):
                pub_item = self.hash(pub_item)
            self.pub_key.append(pub_item)

    def hash(self, data):
        return hashlib.sha256(data).digest()

    def sign(self, data):
        data_hash = self.hash(data)
        data_hash_bytes = bytearray(data_hash)
        sig = []
        for i in range(KEY_LEN):
            sig_item = self.priv_key[i]
            int_val = data_hash_bytes[i]
            hash_iters = BYTE_MAX - int_val
            for _ in range(hash_iters):
                sig_item = self.hash(sig_item)
            sig.append(sig_item)
        return sig

    def verify(self, signature, data):
        data_hash = self.hash(data)
        data_hash_bytes = bytearray(data_hash)
        verify = []
        for i in range(KEY_LEN):
            verify_item = signature[i]
            hash_iters = data_hash_bytes[i] + 1
            for _ in range(hash_iters):
                verify_item = self.hash(verify_item)
            verify.append(verify_item)
        return self.pub_key == verify


if __name__ == "__main__":
    w = Winternitz()

    message1 = b"WOTS Up???"
    signature1 = w.sign(message1)
    assert w.verify(signature1, message1)

    message2 = b"Sign for flag"
    signature2 = w.sign(message2)
    assert w.verify(signature2, message2)

    with open("flag.txt") as f:
        flag = f.read().strip().encode()

    aes_key = bytes([s[0] for s in signature2])
    aes_iv = urandom(16)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted = cipher.encrypt(flag)

    with open("data.json", "w") as f:
        f.write(json.dumps({
            "public_key": [s.hex() for s in w.pub_key],
            "message": message1.decode(),
            "signature": [s.hex() for s in signature1],
            "iv": aes_iv.hex(),
            "enc": encrypted.hex(),
        }))
