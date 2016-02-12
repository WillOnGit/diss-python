"""
This is some code to implement basic RSA functionality, mainly for the purposes of an example breaking of encryption with Lenstra's algorithm.

This code will use some functions which are defined in what is currently "pollard.py", which is currently in ~/Documents/Uni/Python/ , but I'm debating rearranging the DISS491 directory so that the .git repository includes all of the 'meta' files. This isn't really the place to be documenting this but oh well. Since I'll presumably be working on this file a bunch in the near-future, it may inspire me to actually do something.

The prime 1512094127 might be a good one for modulus. Make sure it is actually prime before you go-go though. -- It is. But actually, the new website makes it redundant. This is the website: http://compoasso.free.fr/primelistweb/page/prime/liste_online_en.php

1250812582321 I also found, go me.

Lazy examples:
p = 791648724667
q = 3992747141

For this, with initial point (3,1), the algorithm succeeds when b = 39850, when trying to add the two points
(2191801374392476491053L, 2332211434379395076998L)
and
(406058948051076877967L, 3156968592727602662096L)
"""

execfile("pollard.py")

# public key of form (exponent, modulus)
def encrypt(plaintext,public_key):
	if plaintext<0 or plaintext>public_key[1]:
		return "Invalid plaintext: must be between one and modulus"
	return modex(plaintext,public_key[0],public_key[1])

# decryption key of form (exponent, modulus)
def decrypt(ciphertext, decryption_key):
	if ciphertext<0 or ciphertext>decryption_key[1]:
		return "Invalid ciphertext: must be between one and modulus"
	return modex(ciphertext,decryption_key[0],decryption_key[1])

# generate keys from two primes p and q
def keygen(p,q):
	#include primality test?
	if p <10 or q <10:
		return "Choose primes greater than 10"

	N = p * q
	totient = (p-1) * (q-1)
        # is this necessary?
        if N > 65537:
            exponent = 65537
        else:
            exponent = int((N**0.5))
	while euclidean(exponent, totient, prin=False) != 1:
		exponent = exponent + 1

	inverse = euclidean(exponent,totient,prin=False,inv=True)[1]

	public = (exponent,N)
	private = (inverse,N)

	return (public,private)

# END OF RSA STUFF

def strxor(input,key):
    return [input,key]
