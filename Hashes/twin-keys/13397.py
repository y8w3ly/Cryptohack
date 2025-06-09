import os
import random
from Crypto.Hash import MD5
from utils import listener

KEY_START = b"CryptoHack Secure Safe"
FLAG = b"crypto{????????????????????????????}"


def xor(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))


class SecureSafe:
    def __init__(self):
        self.magic1 = os.urandom(16)
        self.magic2 = os.urandom(16)
        self.keys = {}

    def insert_key(self, key):
        if len(self.keys) >= 2:
            return {"error": "All keyholes are already occupied"}
        if key in self.keys:
            return {"error": "This key is already inserted"}

        self.keys[key] = 0
        if key.startswith(KEY_START):
            self.keys[key] = 1

        return {"msg": f"Key inserted"}

    def unlock(self):
        if len(self.keys) < 2:
            return {"error": "Missing keys"}

        if sum(self.keys.values()) != 1:
            return {"error": "Invalid keys"}

        hashes = []
        for k in self.keys.keys():
            hashes.append(MD5.new(k).digest())

        # Encrypting the hashes with secure quad-grade XOR encryption
        # Using different randomized magic numbers to prevent the hashes
        # from ever being equal
        h1 = hashes[0]
        h2 = hashes[1]
        for i in range(2, 2**(random.randint(2, 10))):
            h1 = xor(self.magic1, xor(h2, xor(xor(h2, xor(h1, h2)), h2)))
            h2 = xor(xor(xor(h1, xor(xor(h2, h1), h1)), h1), self.magic2)

        assert h1 != bytes(bytearray(16))

        if h1 == h2:
            return {"msg": f"The safe clicks and the door opens. Amongst its secrets you find a flag: {FLAG}"}
        return {"error": "The keys does not match"}


class Challenge():
    def __init__(self):
        self.securesafe = SecureSafe()
        self.before_input = "Can you help find our lost keys to unlock the safe?\n"

    def challenge(self, your_input):
        if not 'option' in your_input:
            return {"error": "You must send an option to this server"}
        elif your_input['option'] == 'insert_key':
            key = bytes.fromhex(your_input["key"])
            return self.securesafe.insert_key(key)
        elif your_input['option'] == 'unlock':
            return self.securesafe.unlock()
        else:
            return {"error": "Invalid option"}


import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13397)
