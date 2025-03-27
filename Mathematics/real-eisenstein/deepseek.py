from sage.all import RealField, floor, ceil, round

# Given data
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]
ct = 1350995397927355657956786955603012410260017344805998076702828160316695004588429433
known_indices = [0, 1, 2, 3, 4, 5, 6, 26]  # Positions of 'crypto{ }'
known_chars = [99, 114, 117, 112, 116, 111, 123, 125]  # ASCII for 'crypto{ }'

# High precision setup
prec = 5000
R = RealField(prec)
scale = R(16)**64

# Calculate the contribution from known parts
known_sum = R(0)
for i, idx in enumerate(known_indices):
    prime = PRIMES[idx]
    char = known_chars[i]
    known_sum += R(char) * R(prime).sqrt()

known_sum_scaled = known_sum * scale
remaining = R(ct) - known_sum_scaled

# Process unknown primes in descending order of their square roots
unknown_primes = PRIMES[7:26]  # Primes for indices 7 to 25
sorted_primes = sorted(unknown_primes, key=lambda p: -R(p).sqrt())

a_values = {}
remaining_target = remaining

for p in sorted_primes:
    sqrt_p = R(p).sqrt()
    term = sqrt_p * scale
    a = remaining_target / term
    a_rounded = round(a)
    a_clamped = max(32, min(126, a_rounded))
    a_values[p] = a_clamped
    remaining_target -= a_clamped * term

# Reconstruct the flag in original order
unknown_ascii = [a_values[p] for p in unknown_primes]
full_ascii = known_chars[:7] + unknown_ascii + known_chars[7:]
flag = ''.join(chr(c) for c in full_ascii)

print(f"Flag: {flag}")