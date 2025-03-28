from Crypto.Util.number import getPrime
import random
from utils import listener

FLAG = 'crypto{???????????????????????????????????}'

class Challenge():
    def __init__(self):
        self.no_prompt = True
        self.q = getPrime(512)
        self.x = random.randint(2, self.q)

        self.g = None
        self.n = None
        self.h = None

        self.current_step = "SHARE_PRIME"

    def check_params(self, data):
        self.g = int(data['g'], 16)
        self.n = int(data['n'], 16)
        if self.g < 2:
            return False
        elif self.n < 2:
            return False
        elif pow(self.g,self.q,self.n) != 1:
            return False
        return True

    def check_secret(self, data):
        x_user = int(data['x'], 16)
        if self.x == x_user:
            return True
        return False

    def challenge(self, your_input):
        if self.current_step == "SHARE_PRIME":
            self.before_send = "Prime generated: "
            self.before_input = "Send integers (g,n) such that pow(g,q,n) = 1: "
            self.current_step = "CHECK_PARAMS"
            return hex(self.q)

        if self.current_step == "CHECK_PARAMS":
            check_msg = self.check_params(your_input)
            if check_msg:
                self.x = random.randint(0, self.q)
                self.h = pow(self.g, self.x, self.n)
            else:
                self.exit = True
                return {"error": "Please ensure pow(g,q,n) = 1"}

            self.before_send = "Generated my public key: "
            self.before_input = "What is my private key: "
            self.current_step = "CHECK_SECRET"

            return hex(self.h)

        if self.current_step == "CHECK_SECRET":
            self.exit = True
            if self.check_secret(your_input):
                return {"flag": FLAG}
            else:
                return {"error": "Protocol broke somewhere"}

        else:
            self.exit = True
            return {"error": "Protocol broke somewhere"}


import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13403)
