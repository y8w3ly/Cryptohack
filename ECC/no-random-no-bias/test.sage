from Crypto.Util.number import long_to_bytes

# Given values from output.txt
e_pub = 58271
d_pub = 16314065939355844497428646964774413938010062495984944007868244761330321449198604198404787327825341236658059256072790190934480082681534717838850610633320375625893501985237981407305284860652632590435055933317638416556532857376955427517397962124909869006289022084571993305966362498048396739334756594170449299859
N = 119082667712915497270407702277886743652985638444637188059938681008077058895935345765407160513555112013190751711213523389194925328565164667817570328474785391992857634832562389502866385475392702847788337877472422435555825872297998602400341624700149407637506713864175123267515579305109471947679940924817268027249
c = 107089582154092285354514758987465112016144455480126366962910414293721965682740674205100222823439150990299989680593179350933020427732386716386685052221680274283469481350106415150660410528574034324184318354089504379956162660478769613136499331243363223860893663583161020156316072996007464894397755058410931262938
e_priv = 0x10001  # 65537

# Step 1: Compute s = e_pub * d_pub - 1
s = e_pub * d_pub - 1

# Step 2: Try small l to find phi
# Since phi is close to N, we can try dividing s by numbers around N
# Alternatively, use the fact that phi = (p-1)(q-1) = N - p - q + 1

# Step 3: Try to find phi by testing if s/l is an integer close to N
for l in range(1, 100000000):  # Try small l values
    if s % l == 0:
        phi = s // l
        # Check if phi is reasonable (close to N)
        if abs(N - phi) < N // 1000:  # Rough heuristic
            # Step 4: Use phi to factor N
            # phi = N - (p + q) + 1
            # p + q = N - phi + 1
            p_plus_q = N - phi + 1
            # Solve quadratic: x^2 - (p+q)x + N = 0
            # Discriminant: delta = (p+q)^2 - 4N
            delta = p_plus_q**2 - 4 * N
            if delta > 0:
                # Check if delta is a perfect square
                sqrt_delta = int(delta ** 0.5)
                if sqrt_delta ** 2 == delta:
                    # p and q are roots
                    p = (p_plus_q + sqrt_delta) // 2
                    q = (p_plus_q - sqrt_delta) // 2
                    # Verify p and q
                    if p * q == N:
                        print(f"Found p: {p}")
                        print(f"Found q: {q}")
                        # Step 5: Compute d_priv = inverse(e_priv, phi)
                        from Crypto.Util.number import inverse
                        d_priv = inverse(e_priv, phi)
                        # Step 6: Decrypt c to get m
                        m = pow(c, d_priv, N)
                        # Step 7: Convert m to flag
                        flag = long_to_bytes(m)
                        print(f"Flag: {flag}")
                        break