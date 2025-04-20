import requests
import string

BASE_URL = "https://aes.cryptohack.org/ctrime/encrypt/"

# Candidate alphabet: punctuation + letters + digits
ALPHABET = string.printable
def encrypt(hex_plaintext: str) -> str:
    """Call the encrypt endpoint and return the raw hex ciphertext."""
    return requests.get(f"{BASE_URL}{hex_plaintext}/").json()["ciphertext"]

def recover_flag():
    # 1) Seed with the known flag prefix
    known = b"crypto{"
    # 2) Baseline length for compress(known‖FLAG)
    baseline_len = len(encrypt(known.hex()))

    print(f"Starting from: {known.decode()} (len={baseline_len})")
    # 3) Extend until we hit the closing '}'
    while not known.endswith(b"}"):
        for c in ALPHABET:
            trial = known + c.encode()
            ct = encrypt(trial.hex())
            L = len(ct)
            print(f"Trying {c!r}: ciphertext length = {L}")

            # 4) A match (no length increase) means c is correct
            if L == baseline_len:
                known += c.encode()
                print(f"  → Found next byte: {known.decode()}")
                break
        else:
            # If no candidate matched, something’s off
            raise RuntimeError("No matching byte found; check alphabet or endpoint.")
        # baseline stays the same while extending the match prefix
        # once you finish (flag ends with '}'), we exit
    return known

if __name__ == "__main__":
    flag = recover_flag().decode()
    print("Recovered FLAG:", flag)
