#!/usr/bin/env python3

from utils import listener

FLAG = 'crypto{????????????????????????????????????}'


def generate_basis(n):
    basis = [True] * n
    for i in range(3, int(n**0.5)+1, 2):
        if basis[i]:
            basis[i*i::2*i] = [False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3, n, 2) if basis[i]]


def miller_rabin(n, b):
    """
    Miller Rabin test testing over all
    prime basis < b
    """
    basis = generate_basis(b)
    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for b in basis:
        x = pow(b, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def lizzies_little_window(a, p):
    if p < 1 or a < 1:
        return "[*] Error: Please, I will only accept positive integers."
    if p.bit_length() <= 600:
        return "[*] Error: Of all the primes, you choose to send me one so small?"
    if p.bit_length() > 900:
        return "[*] Error: I do wonder what're you trying to prove with a prime so big?"
    if not miller_rabin(p, 64):
        return "[*] Error: Sir, do you know what a prime number is?"
    if p < a:
        return "[*] Error: I'm sorry, but your base must be coprime to p"
    x = pow(a, p-1, p)
    return f"[*] Success: You passed all my tests! Here's the first byte of my flag: {FLAG[:x]}"


class Challenge():
    def __init__(self):
        self.before_input = "Oh Mr. Darcy, send me your primes!\n"

    def challenge(self, your_input):
        if not 'prime' in your_input or not 'base' in your_input:
            return {"error": "Please send a prime and a base to the server."}

        p = your_input['prime']
        a = your_input['base']
        return {"Response": lizzies_little_window(a, p)}


import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13385)
