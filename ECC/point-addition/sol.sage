def ecc_add(points, a, b, p):
    F = GF(p)
    E = EllipticCurve(F, [a, b])
    curve_points = [E(point) for point in points]
    result = curve_points[0]
    for pt in curve_points[1:]:
        result+= pt
    return (int(result[0]), int(result[1]))


a = 497
b = 1768
p = 9739

P = (493, 5564)
Q = (1539, 4742)
R = (4403, 5202)

S = ecc_add([P, P, Q, R], a, b, p)
print(f"crypto{{{S[0]},{S[1]}}}")
