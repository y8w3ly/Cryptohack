    print("Curve is supersingular. Applying MOV attack...")
    ord = E.order()
    
    # Find embedding degree k
    k = 1
    while (pow(p, k, ord) - 1) % ord != 0:
        k += 1
    print(f"Embedding degree k = {k}")
    
    # Map ECDLP to DLP in GF(p^k) using Weil pairing
    F = GF(p^k, 'a')
    E_F = E.base_extend(F)
    G_F = E_F(G)
    P_F = E_F(P)
    
    # Compute Weil pairing
    w = G_F.weil_pairing(P_F, ord)
    g = F.multiplicative_generator()
    n = discrete_log(w, g, ord, operation='*')
    print(f"n = {n}")
