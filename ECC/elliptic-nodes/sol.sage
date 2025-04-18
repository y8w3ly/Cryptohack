from Crypto.Util.number import long_to_bytes
p = 4368590184733545720227961182704359358435747188309319510520316493183539079703

# Given points G and Q
gx = 8742397231329873984594235438374590234800923467289367269837473862487362482
gy = 225987949353410341392975247044711665782695329311463646299187580326445253608
qx = 2582928974243465355371953056699793745022552378548418288211138499777818633265
qy = 2421683573446497972507172385881793260176370025964652384676141384239699096612

# Calculate a and b for the elliptic curve equation y² = x³ + a*x + b
gy_sq = pow(gy, 2, p)
qy_sq = pow(qy, 2, p)
gx_cu = pow(gx, 3, p)
qx_cu = pow(qx, 3, p)

numerator = (gy_sq - qy_sq - gx_cu + qx_cu) % p
denominator = (gx - qx) % p
denominator_inv = pow(denominator, -1, p)
a = (numerator * denominator_inv) % p
b = (gy_sq - gx_cu - a * gx) % p

# Verify the curve is singular (discriminant is 0)
discriminant = (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p
assert discriminant == 0, "Curve is not singular"

# Find roots of x³ + a*x + b to identify the singular point
F = GF(p)
x = polygen(F)
f = x**3 + a * x + b
roots = f.roots()

# Determine double root (where the derivative 3x² + a = 0)
double_root = None
single_root = None
for root, multiplicity in roots:
    if (3 * root**2 + a) % p == 0:
        double_root = root
    else:
        single_root = root

assert double_root is not None and single_root is not None, "Roots not properly identified"

# Compute parameters for mapping to multiplicative group
t = (double_root - single_root) % p
t_sqrt = sqrt(F(t))  # Compute square root in the field

# Shift coordinates by the double root
gx_shifted = (gx - double_root) % p
qx_shifted = (qx - double_root) % p

# Transform points using the singular curve's mapping
def transform(x_shifted, y):
    numerator = y + t_sqrt * x_shifted
    denominator = y - t_sqrt * x_shifted
    return numerator / denominator

g = transform(gx_shifted, gy)
q = transform(qx_shifted, qy)

# Solve the discrete logarithm in the multiplicative group
d = discrete_log(q, g)
flag = long_to_bytes(d)
print(flag)