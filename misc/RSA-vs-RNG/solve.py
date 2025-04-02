#not as intended
from factordb import factordb
from Crypto.Util.number import long_to_bytes as l2b

N = 95397281288258216755316271056659083720936495881607543513157781967036077217126208404659771258947379945753682123292571745366296203141706097270264349094699269750027004474368460080047355551701945683982169993697848309121093922048644700959026693232147815437610773496512273648666620162998099244184694543039944346061
e = 0x10001
c = 0x04fee34327a820a5fb72e71b8b1b789d22085630b1b5747f38f791c55573571d22e454bfebe0180631cbab9075efa80796edb11540404c58f481f03d12bb5f3655616df95fb7a005904785b86451d870722cc6a0ff8d622d5cb1bce15d28fee0a72ba67ba95567dc5062dfc2ac40fe76bc56c311b1c3335115e9b6ecf6282cca

n = factordb.FactorDB(N)
n.connect()
p, q = n.get_factor_list()

phi = (p-1)*(q-1)

d = pow(e,-1,phi)

m = pow(c,d,N)

flag = l2b(m).decode()
print(flag)