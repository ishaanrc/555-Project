import random
from math import ceil
from decimal import Decimal
import random
from math import pow
import socket	
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import numpy as np
import subprocess
import subprocess as sp
import rsa
import socket	
import threading
import time
from subprocess import Popen
import os 
import binascii


# Send data to server

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




#Inputs of P1, P2, P3	
msg1 = '3'
msg2 = '2'
msg3 = '1'


print("Original M1 :", msg1)
print("Original M2 :", msg2)
print("Original M3 :", msg3)



q1 = random.randint(pow(10, 20), pow(10, 50))
key1 = gen_key(q1) #Private key
g1 = random.randint(2, q1)
h1 = power(g1, key1, q1)

#Encryption Scheme of ElGamaal
en_msg1, p1 = encrypt(msg1, q1, h1, g1)
en_msg2, p2 = encrypt(msg2, q1, h1, g1)
en_msg3, p3 = encrypt(msg3, q1, h1, g1)

#We distribute the encryptions to each player 
print("Encrypted el gamaal 1 :",en_msg1[0])
print("Encrypted el gamaal 2 :",en_msg2[0])
print("Encrypted el gamaal 3 :",en_msg3[0])









#Trusted Party will decrypt using key 1 (Private key sent in shares)
dr_msg1 = decrypt(en_msg1, p1, key1, q1)
dr_msg2 = decrypt(en_msg2, p2, key1, q1)
dr_msg3 = decrypt(en_msg3, p3, key1, q1)




dmsg1 = ''.join(dr_msg1)
dmsg2 = ''.join(dr_msg2)
dmsg3 = ''.join(dr_msg3)
print("Decrypted Message 1 :", dmsg1)
print("Decrypted Message 2 :", dmsg2)
print("Decrypted Message 3 :", dmsg3)
print("----------------------------------")
t, n = 3, 3
secret1 = en_msg1[0]
secret2 = en_msg2[0]
secret3 = en_msg3[0]
list1 = [] 
print("Private Key Secret:", key1)
# Phase I: Generation of shares
shares1 = generate_shares(n, t, key1)
print("----------------------------------")
print(f'3 Shares of Private Key: {", ".join(str(share1) for share1 in shares1)}')
print("----------------------------------")
for j, share_j in enumerate(shares1):
		list1.append(share_j[1])
# Phase II: Secret Reconstruction
# Picking t shares randomly for
# reconstruction
pool1 = random.sample(shares1, t)
print(f'Reconstructed secret by trusted party : {reconstruct_secret(pool1)}')
print("----------------------------------")


m1 = int(msg1)
m2 = int(msg2)
m3 = int(msg3)

def dec2bin(number: int):
    ans = ""
    if ( number == 0 ):
        return 0
    while ( number ):
        ans += str(number&1)
        number = number >> 1
     
    ans = ans[::-1]
 
    return ans

bm1 = dec2bin(m1)
bm2 = dec2bin(m2)
bm3 = dec2bin(m3)

print("Binary of M1", "(",m1 , ") = " , bm1)
print("Binary of M2", "(",m2 , ") = " , bm2)
print("Binary of M3", "(",m3 , ") = " , bm3)

#Split M1 into x1, x2 and M2 into y1, y2
x1 = int(str(bm1)[0])
print("x1 = " , x1)
x2 = int(str(bm1)[1])
print("x2 = " , x2)
y1 = int(str(bm2)[0])
print("y1 = ", y1)
y2 = int(str(bm2)[1])
print("y2 = " , y2)

# def binProd(binOne, binTwo):
#   i = 0
#   rem = 0
#   sum = []
#   bProd = 0
#   while binOne != 0 or binTwo != 0:
#     sum.insert(i, (((binOne % 10) + (binTwo % 10) + rem) % 2))
#     rem = int(((binOne % 10) + (binTwo % 10) + rem) / 2)
#     binOne = int(binOne/10)
#     binTwo = int(binTwo/10)
#     i = i+1
#   if rem != 0:
#     sum.insert(i, rem)
#     i = i+1
#   i = i-1
#   while i >= 0:
#     bProd = (bProd * 10) + sum[i]
#     i = i-1
#   return bProd

	
# def bn(n):
#     return list(map(int, bin(n)[:1:-1]))

# def is_zero(n):
#     return not n[1:] and not n[0]

# def add_lists(first, second):
#     n = max(len(first), len(second))
#     first += [0] * (n - len(first))
#     second += [0] * (n - len(second))
#     return [first[i] + second[i] for i in range(n)]

# def carry_over(first_num, second_num):
#     stack, overflow = [], 0
#     for i in range(len(second_num)):
#         if second_num[i] == 1:
#             stack = add_lists(stack, [0] * i + first_num)

#     for i in range(len(stack)):
#         stack[i] += overflow
#         overflow = stack[i] // 2
#         stack[i] %= 2

#     while overflow > 0:
#         stack.append(overflow % 2)
#         overflow //= 2

#     return stack

# def multiply2(first_num, second_num):    
#     if is_zero(first_num) or is_zero(second_num):
#         return [0]  
#     else:
#         return carry_over(first_num, second_num)
           


# def multiply(x, y):
    
#     product = 0
    
  
#     while(y > 0):
    
       
#         if (y & 1):
      
#             product = product + x
        
#         x = x << 1
#         y = y >> 1
        
#     print(product)
    
# multiply(m1, m2)

def zeroPad(numberString, zeros, left = True):
   
    for i in range(zeros):
        if left:
            numberString = '0' + numberString
        else:
            numberString = numberString + '0'
    return numberString

def OneFourOT(x ,y):
    #convert to strings for easy access to digits
    x = str(x)
    y = str(y)
    #base case for recursion
    if len(x) == 1 and len(y) == 1:
        return int(x) * int(y)
    if len(x) < len(y):
        x = zeroPad(x, len(y) - len(x))
    elif len(y) < len(x):
        y = zeroPad(y, len(x) - len(y))
    n = len(x)
    j = n//2
    #for odd digit integers
    if (n % 2) != 0:
        j += 1    
    BZeroPadding = n - j
    AZeroPadding = BZeroPadding * 2
    a = int(x[:j])
    b = int(x[j:])
    c = int(y[:j])
    d = int(y[j:])
    #recursively calculate
    ac = OneFourOT(a, c)
    bd = OneFourOT(b, d)
    k = OneFourOT(a + b, c + d)
    A = int(zeroPad(str(ac), AZeroPadding, False))
    B = int(zeroPad(str(k - ac - bd), BZeroPadding, False))
    return A + B + bd
final = OneFourOT(m1,m2)+m3
print("Final answer after computung m1 times m2 + m3 = ", final )

# output = sp.getoutput('whoami --version')
# print (output)


publicKey = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALoJfUHJ4wA5DgajmX85KnZy4JEwarUxQomiv5cHkqgtrhQbooJujTA8PSA7B5SkwiVSsWX9fs7LBi2ESwOSGdECAwEAAQ=="

# def encrypt(message, key):
#     print (rsa.encrypt(message, publicKey))


# # Receive data from server
# import random
# from math import ceil
# from decimal import Decimal
# import random
# from math import pow
# import socket	
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.backends import default_backend

# # generate private/public key pair
# key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
#     key_size=2048)

# # get public key in OpenSSH format
# public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
#     serialization.PublicFormat.OpenSSH)

# # get private key in PEM container format
# pem = key.private_bytes(encoding=serialization.Encoding.PEM,
#     format=serialization.PrivateFormat.TraditionalOpenSSL,
#     encryption_algorithm=serialization.NoEncryption())

# # decode to printable strings
# private_key_str = pem.decode('utf-8')
# public_key_str = public_key.decode('utf-8')


# # clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
# # # # Connect to the server
# # clientSocket.connect(("127.0.0.1",12346))
# # Send data to server

# FIELD_SIZE = 10**5

# def reconstruct_secret(shares):
# 	"""
# 	Combines individual shares (points on graph)
# 	using Lagranges interpolation.

# 	`shares` is a list of points (x, y) belonging to a
# 	polynomial with a constant of our key.
# 	"""
# 	sums = 0
# 	prod_arr = []

# 	for j, share_j in enumerate(shares):
# 		xj, yj = share_j
# 		prod = float(1)

# 		for i, share_i in enumerate(shares):
# 			xi, _ = share_i
# 			if i != j:
# 				prod *= float(float(xi)/(xi-xj))

# 		prod *= yj
# 		sums += float(prod)

# 	return (float(sums))


# def polynom(x, coefficients):
# 	"""
# 	This generates a single point on the graph of given polynomial
# 	in `x`. The polynomial is given by the list of `coefficients`.
# 	"""
# 	point = 0
# 	# Loop through reversed list, so that indices from enumerate match the
# 	# actual coefficient indices
# 	for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
# 		point += x ** coefficient_index * coefficient_value
# 	return point


# def coeff(t, secret):
# 	"""
# 	Randomly generate a list of coefficients for a polynomial with
# 	degree of `t` - 1, whose constant is `secret`.

# 	For example with a 3rd degree coefficient like this:
# 		3x^3 + 4x^2 + 18x + 554

# 		554 is the secret, and the polynomial degree + 1 is
# 		how many points are needed to recover this secret.
# 		(in this case it's 4 points).
# 	"""
# 	coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
# 	coeff.append(secret)
# 	return coeff


# def generate_shares(n, m, secret):
# 	"""
# 	Split given `secret` into `n` shares with minimum threshold
# 	of `m` shares to recover this `secret`, using SSS algorithm.
# 	"""
# 	coefficients = coeff(m, secret)
# 	shares = []

# 	for i in range(1, n+1):
# 		x = random.randrange(1, FIELD_SIZE)
# 		shares.append((x, polynom(x, coefficients)))

# 	return shares

# # Python program to illustrate ElGamal encryption
# a = random.randint(2, 10)

# def gcd(a, b):
# 	if a < b:
# 		return gcd(b, a)
# 	elif a % b == 0:
# 		return b
# 	else:
# 		return gcd(b, a % b)

# # Generating large random numbers
# def gen_key(q):
# 	key = random.randint(pow(10, 20), q)
# 	while gcd(q, key) != 1:
# 		key = random.randint(pow(10, 20), q)

# 	return key

# # Modular exponentiation
# def power(a, b, c):
# 	x = 1
# 	y = a

# 	while b > 0:
# 		if b % 2 != 0:
# 			x = (x * y) % c
# 		y = (y * y) % c
# 		b = int(b / 2)

# 	return x % c

# # Asymmetric encryption
# def encrypt(msg, q, h, g):

# 	en_msg = []

# 	k = gen_key(q)# Private key for sender
# 	s = power(h, k, q)
# 	p = power(g, k, q)
	
# 	for i in range(0, len(msg)):
# 		en_msg.append(msg[i])

# 	#print("g^k used : ", p)
# 	#print("g^ak used : ", s)
# 	for i in range(0, len(en_msg)):
# 		en_msg[i] = s * ord(en_msg[i])

# 	return en_msg, p

# def decrypt(en_msg, p, key, q):

# 	dr_msg = []
# 	h = power(p, key, q)
# 	for i in range(0, len(en_msg)):
# 		dr_msg.append(chr(int(en_msg[i]/h)))
		
# 	return dr_msg
# msg1 = '1'
# msg2 = '2'
# msg3 = '3'
# print("Original M1 :", msg1)
# print("Original M2 :", msg2)
# print("Original M3 :", msg3)
# q1 = random.randint(pow(10, 20), pow(10, 50))
# g1 = random.randint(2, q1)
# key1 = gen_key(q1)
# h1 = power(g1, key1, q1)
# en_msg1, p1 = encrypt(msg1, q1, h1, g1)
# en_msg2, p2 = encrypt(msg2, q1, h1, g1)
# en_msg3, p3 = encrypt(msg3, q1, h1, g1)
# print("Encrypted el gamaal 1 :",en_msg1[0])
# print("Encrypted el gamaal 2 :",en_msg2[0])
# print("Encrypted el gamaal 3 :",en_msg3[0])
# dr_msg1 = decrypt(en_msg1, p1, key1, q1)
# dr_msg2 = decrypt(en_msg2, p2, key1, q1)
# dr_msg3 = decrypt(en_msg3, p3, key1, q1)
# dmsg1 = ''.join(dr_msg1)
# dmsg2 = ''.join(dr_msg2)
# dmsg3 = ''.join(dr_msg3)
# print("Decrypted Message 1 :", dmsg1)
# print("Decrypted Message 2 :", dmsg2)
# print("Decrypted Message 3 :", dmsg3)
# print("----------------------------------")
# t, n = 3, 3
# secret1 = en_msg1[0]
# secret2 = en_msg2[0]
# secret3 = en_msg3[0]
# list1 = [] 
# print("Private Key Secret:", key1)
# # Phase I: Generation of shares
# shares1 = generate_shares(n, t, key1)
# print("----------------------------------")
# print(f'3 Shares of Private Key: {", ".join(str(share1) for share1 in shares1)}')
# print("----------------------------------")
# for j, share_j in enumerate(shares1):
# 		list1.append(share_j[1])
# # Phase II: Secret Reconstruction
# # Picking t shares randomly for
# # reconstruction
# pool1 = random.sample(shares1, t)
# print(f'Reconstructed secret: {reconstruct_secret(pool1)}')


# m1 = int(msg1)
# m2 = int(msg2)
# m3 = int(msg3)

# finalMessage = (m1*m2) + m3
# print(finalMessage)





#######

 

# Create a stream based socket(i.e, a TCP socket)

# operating on IPv4 addressing scheme

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 

# Bind and listen

serverSocket.bind(("127.0.0.1",12346))

serverSocket.listen()

 
publicKey = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALoJfUHJ4wA5DgajmX85KnZy4JEwarUxQomiv5cHkqgtrhQbooJujTA8PSA7B5SkwiVSsWX9fs7LBi2ESwOSGdECAwEAAQ=="
# Accept connections

while(True):

    (clientConnected, clientAddress) = serverSocket.accept()
    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
    # Send some data back to the client

	
    clientConnected.send("MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALoJfUHJ4wA5DgajmX85KnZy4JEwarUxQomiv5cHkqgtrhQbooJujTA8PSA7B5SkwiVSsWX9fs7LBi2ESwOSGdECAwEAAQ==".encode())
    #clientConnected.send(cipher.encode())
