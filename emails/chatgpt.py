from sympy import symbols, solve
from sympy.polys.specialpolys import interpolating_poly

# Define variables
x = symbols('x')
# Define known parameters
N = 37853  # The RSA modulus
e = 3  # Public exponent
c = 24137  # Ciphertext

# Construct the polynomial
P = interpolating_poly(e*x, [(0, c), (1, c**e - N)])

# Find small roots
roots = solve(P, x)

# Extract the plaintext from roots
for root in roots:
    if root.is_integer:
        plaintext = root
        break

print("Recovered plaintext:", long_to_bytes(plaintext))
