import random
from math import ceil
from decimal import Decimal
import random
from math import pow

FIELD_SIZE = 10**5


def reconstruct_secret(shares):
	"""
	Combines individual shares (points on graph)
	using Lagranges interpolation.

	`shares` is a list of points (x, y) belonging to a
	polynomial with a constant of our key.
	"""
	sums = 0
	prod_arr = []

	for j, share_j in enumerate(shares):
		xj, yj = share_j
		prod = float(1)

		for i, share_i in enumerate(shares):
			xi, _ = share_i
			if i != j:
				prod *= float(float(xi)/(xi-xj))

		prod *= yj
		sums += float(prod)

	return (float(sums))


def polynom(x, coefficients):
	"""
	This generates a single point on the graph of given polynomial
	in `x`. The polynomial is given by the list of `coefficients`.
	"""
	point = 0
	# Loop through reversed list, so that indices from enumerate match the
	# actual coefficient indices
	for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
		point += x ** coefficient_index * coefficient_value
	return point


def coeff(t, secret):
	"""
	Randomly generate a list of coefficients for a polynomial with
	degree of `t` - 1, whose constant is `secret`.

	For example with a 3rd degree coefficient like this:
		3x^3 + 4x^2 + 18x + 554

		554 is the secret, and the polynomial degree + 1 is
		how many points are needed to recover this secret.
		(in this case it's 4 points).
	"""
	coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
	coeff.append(secret)
	return coeff


def generate_shares(n, m, secret):
	"""
	Split given `secret` into `n` shares with minimum threshold
	of `m` shares to recover this `secret`, using SSS algorithm.
	"""
	coefficients = coeff(m, secret)
	shares = []

	for i in range(1, n+1):
		x = random.randrange(1, FIELD_SIZE)
		shares.append((x, polynom(x, coefficients)))

	return shares

# Python program to illustrate ElGamal encryption
a = random.randint(2, 10)

def gcd(a, b):
	if a < b:
		return gcd(b, a)
	elif a % b == 0:
		return b
	else:
		return gcd(b, a % b)

# Generating large random numbers
def gen_key(q):

	key = random.randint(pow(10, 20), q)
	while gcd(q, key) != 1:
		key = random.randint(pow(10, 20), q)

	return key

# Modular exponentiation
def power(a, b, c):
	x = 1
	y = a

	while b > 0:
		if b % 2 != 0:
			x = (x * y) % c
		y = (y * y) % c
		b = int(b / 2)

	return x % c

# Asymmetric encryption
def encrypt(msg, q, h, g):

	en_msg = []

	k = gen_key(q)# Private key for sender
	s = power(h, k, q)
	p = power(g, k, q)
	
	for i in range(0, len(msg)):
		en_msg.append(msg[i])

	#print("g^k used : ", p)
	#print("g^ak used : ", s)
	for i in range(0, len(en_msg)):
		en_msg[i] = s * ord(en_msg[i])

	return en_msg, p

def decrypt(en_msg, p, key, q):

	dr_msg = []
	h = power(p, key, q)
	for i in range(0, len(en_msg)):
		dr_msg.append(chr(int(en_msg[i]/h)))
		
	return dr_msg




msg1 = '1'
msg2 = '2'
msg3 = '3'
print("Original M1 :", msg1)
print("Original M2 :", msg2)
print("Original M3 :", msg3)
q1 = random.randint(pow(10, 20), pow(10, 50))
g1 = random.randint(2, q1)
q2 = random.randint(pow(10, 20), pow(10, 50))
g2 = random.randint(2, q1)
q3 = random.randint(pow(10, 20), pow(10, 50))
g3 = random.randint(2, q1)
key1 = gen_key(q1)# Private key for receiver1
key2 = gen_key(q2)# Private key for receiver2
key3 = gen_key(q3)# Private key for receiver3
h1 = power(g1, key1, q1)
h2 = power(g2, key2, q2)
h3 = power(g3, key3, q3)
# print("g used 1: ", g1)
# print("g^a used 1: ", h1)
# print("g used 2: ", g2)
# print("g^a used 2: ", h2)
# print("g used 3: ", g3)
# print("g^a used 3: ", h3)
en_msg1, p1 = encrypt(msg1, q1, h1, g1)
en_msg2, p2 = encrypt(msg2, q2, h2, g2)
en_msg3, p3 = encrypt(msg3, q3, h3, g3)
# print("Encrypted el gamaal 1 :",en_msg1[0])
# print("Encrypted el gamaal 2 :",en_msg2[0])
# print("Encrypted el gamaal 3 :",en_msg3[0])
dr_msg1 = decrypt(en_msg1, p1, key1, q1)
dr_msg2 = decrypt(en_msg2, p2, key2, q2)
dr_msg3 = decrypt(en_msg3, p3, key3, q3)
dmsg1 = ''.join(dr_msg1)
dmsg2 = ''.join(dr_msg2)
dmsg3 = ''.join(dr_msg3)
# print("Decrypted Message 1 :", dmsg1)
# print("Decrypted Message 2 :", dmsg2)
# print("Decrypted Message 3 :", dmsg3)
print("----------------------------------")
t, n = 3, 3
secret1 = en_msg1[0]
secret2 = en_msg2[0]
secret3 = en_msg3[0]
list1 = [] 
list2 = [] 
list3 = [] 
print(f'Original Secret: {secret1}')
print(f'Original Secret: {secret2}')
print(f'Original Secret: {secret3}')

# Phase I: Generation of shares
shares1 = generate_shares(n, t, secret1)
shares2 = generate_shares(n, t, secret2)
shares3 = generate_shares(n, t, secret3)
print("----------------------------------")
print(f'Shares 1: {", ".join(str(share1) for share1 in shares1)}')
print("----------------------------------")
for j, share_j in enumerate(shares1):
		list1.append(share_j[1])

print(f'Shares 2: {", ".join(str(share2) for share2 in shares2)}')
print("----------------------------------")
for j, share_j in enumerate(shares2):
		list2.append(share_j[1])
print(f'Shares 3: {", ".join(str(share3) for share3 in shares3)}')
print("----------------------------------")
for j, share_j in enumerate(shares3):
		list3.append(share_j[1])
# Phase II: Secret Reconstruction
# Picking t shares randomly for
# reconstruction
sumCol1 = list1[0] + list2[0] + list3[0]
print("sum1:" , sumCol1)
sumCol2 = list1[1] + list2[1] + list3[1]
print("sum2:" , sumCol2)
sumCol3 = list1[2] + list2[2] + list3[2]
print("sum3:" , sumCol3)
finalSum = sumCol1 + sumCol2 + sumCol3
print("Final sun:", finalSum)
pool1 = random.sample(shares1, t)
pool2 = random.sample(shares2, t)
pool3 = random.sample(shares3, t)
# print(f'Combining shares: {", ".join(str(share1) for share1 in pool1)}')
# print(f'Combining shares: {", ".join(str(share2) for share2 in pool2)}')
# print(f'Combining shares: {", ".join(str(share3) for share3 in pool3)}')
print(f'Reconstructed secret: {reconstruct_secret(pool1)}')
print(f'Reconstructed secret: {reconstruct_secret(pool2)}')
print(f'Reconstructed secret: {reconstruct_secret(pool3)}')






