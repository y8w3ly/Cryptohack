E = EllipticCurve(GF(9739), [497, 1768])
#To define an elliptic curve, we use the EllipticCurve function
#which takes as arguments, the fiels which must be GF(p)
#the other argument is[a,b]
#given E:Y2=X3+aX+b % p

#To define a point in the curve we use this:
P = E(2339,2213)
n = 7863
Q = P
R = None
while n>0:
	if n % 2 ==1:
		if R:
			R+=Q
		else:
			R=Q
	Q += Q
	n = n //2
print(f"crypto{{{R[0]},{R[1]}}}")	
