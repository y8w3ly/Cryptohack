import requests
import string

BASE_URL = "https://aes.cryptohack.org/ctrime/encrypt/"
ALPHABET = string.printable

def get_ciphertext_length(plaintext: bytes) -> int:
    response = requests.get(f"{BASE_URL}{plaintext.hex()}/")
    ciphertext = response.json()["ciphertext"]
    return len(ciphertext) // 2

def recover_flag():
    known = b""
    while not known.endswith(b"}"):
        print(known)
        lengths = {}
        for c in ALPHABET:
            guess = known + c.encode()
            length = get_ciphertext_length(guess)
            lengths[c] = length
        next_char = min(lengths, key=lengths.get)
        known += next_char.encode()
        print(f"Recovered so far: {known.decode()}")
    return known.decode()

if __name__ == "__main__":
    flag = recover_flag()
    print(f"Recovered FLAG: {flag}")
