#!/usr/bin/env python3

from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
from os import urandom

from utils import listener

FLAG = 'crypto{?????????????????????????????????????????????????????}'

class Challenge:
    def __init__(self):
        self.before_input = "Let's practice padding oracle attacks! Recover my message and I'll send you a flag.\n"
        self.message = urandom(16).hex()
        self.key = urandom(16)

    def get_ct(self):
        iv = urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        ct = cipher.encrypt(self.message.encode("ascii"))
        return {"ct": (iv+ct).hex()}

    def check_padding(self, ct):
        ct = bytes.fromhex(ct)
        iv, ct = ct[:16], ct[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = cipher.decrypt(ct)  # does not remove padding
        try:
            unpad(pt, 16)
        except ValueError:
            good = False
        else:
            good = True
        return {"result": good}

    def check_message(self, message):
        if message != self.message:
            self.exit = True
            return {"error": "incorrect message"}
        return {"flag": FLAG}

    #
    # This challenge function is called on your input, which must be JSON
    # encoded
    #
    def challenge(self, msg):
        if "option" not in msg or msg["option"] not in ("encrypt", "unpad", "check"):
            return {"error": "Option must be one of: encrypt, unpad, check"}

        if msg["option"] == "encrypt": return self.get_ct()
        elif msg["option"] == "unpad": return self.check_padding(msg["ct"])
        elif msg["option"] == "check": return self.check_message(msg["message"])

import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13421)
