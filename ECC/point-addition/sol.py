"""
Algorithm for the addition of two points: P+QP+Q
(a) If P=OP=O, then P+Q=QP+Q=Q.
(b) Otherwise, if Q=OQ=O, then P+Q=PP+Q=P.
(c) Otherwise, write P=(x1,y1)P=(x1​,y1​) and Q=(x2,y2)Q=(x2​,y2​).
(d) If x1=x2x1​=x2​ and y1=−y2y1​=−y2​, then P+Q=OP+Q=O.
(e) Otherwise:
  (e1) if P≠QP=Q: λ=(y2−y1)/(x2−x1)λ=(y2​−y1​)/(x2​−x1​)
  (e2) if P=QP=Q: λ=(3x12+a)/2y1λ=(3x12​+a)/2y1​
(f) x3=λ2−x1−x2x3​=λ2−x1​−x2​
(h) y3=λ(x1−x3)−y1y3​=λ(x1​−x3​)−y1​
(i) P+Q=(x3,y3)P+Q=(x3​,y3​)
"""
#P=(493,5564),Q=(1539,4742),R=(4403,5202)
#S(x,y)=P+P+Q+R
#Our eqaution is : E:Y2=X3+497X+1768 % 9739 we working on GF(9739)
#Our points coordinates:
x1 = 493
x2 = 1539
x3 = 4403
y1 = 5564
y2 = 4742
y3 = 5202
#From the equation:
a = 497
b = 1768
p = 9739
#P+P:
#we should know that division in finite fields(GF(p)) are the multiplication with the inverse modulo p(which is 9739 in our case)
lambda1 = ((3*pow(x1,3)+a)*pow(2*y1,-1,p))%p
x4 = (pow(lambda1,2)-2*x1)%p
y4 = (lambda1*(x1-x4)-y1)%p
#P+P+Q:
lambda2 = ((y4-y2)*pow((x4-x2),-1,p))%p
x5 = (pow(lambda2,2)-x2-x4)%p
y5 = (lambda2*(x2-x5)-y2)%p
#P+P+Q+R:
lambda3 = ((y5-y3)*pow((x5-x3),-1,p))%p
x6 = (pow(lambda3,2)-x3-x5)%p
y6 = (lambda2*(x3-x6)-y3)%p

print(f"crypto{{{x6},{y6}}}")
