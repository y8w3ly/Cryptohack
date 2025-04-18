#Just got those values from ecdsa.curve_256 from 
from Crypto.Util.number import bytes_to_long
from hashlib import sha1
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = -3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
E = EllipticCurve(GF(p),[a,b])
hidden_flag = E(16807196250009982482930925323199249441776811719221084165690521045921016398804, 72892323560996016030675756815328265928288098939353836408589138718802282948311)
G = E.gens()[0]
q = G.order()
P = E(48780765048182146279105449292746800142985733726316629478905429239240156048277, 74172919609718191102228451394074168154654001177799772446328904575002795731796)
msgs = [
  "I have hidden the secret flag as a point of an elliptic curve using my private key.",
  "The discrete logarithm problem is very hard to solve, so it will remain a secret forever.",
  "Good luck!"
]
rs = [0x91f66ac7557233b41b3044ab9daf0ad891a8ffcaf99820c3cd8a44fc709ed3ae,
      0xe8875e56b79956d446d24f06604b7705905edac466d5469f815547dea7a3171c,
      0x566ce1db407edae4f32a20defc381f7efb63f712493c3106cf8e85f464351ca6]
ss = [0x1dd0a378454692eb4ad68c86732404af3e73c6bf23a8ecc5449500fcab05208d,
      0x582ecf967e0e3acf5e3853dbe65a84ba59c3ec8a43951bcff08c64cb614023f8,
      0x9e4304a36d2c83ef94e19a60fb98f659fa874bfb999712ceb58382e2ccda26ba]
hs = [ Integer(bytes_to_long(sha1(m.encode()).digest())) for m in msgs ]
mat = Matrix(ZZ, 2 + 3, 2 + 3)
bias = 2^160
mat[0,0] = bias
mat[1,1] = bias // q
for i in range(3):
    inv_s = Integer(ss[i]).inverse_mod(q)
    mat[0, 2+i] = (bias * (inv_s * hs[i] % q))  // q
    mat[1, 2+i] = (bias * (inv_s * rs[i] % q))  // q

for i in range(3):
    mat[2+i, 2+i] = q

L = mat.LLL()
for v in L.rows():
    ks = v[2:5]
    for cand in [ks, [-k for k in ks]]:
        d = ((ss[0]*cand[0] - hs[0]) * Integer(rs[0]).inverse_mod(q)) % q
        if d*G == P:
            print(d)
            n = d
            break
