"""
Important: this code is probably super messy, because I don't know how to perform the proper checks of input and whatnot in python. I will hopefully come clean it up in the future. But, realistically, probably not. Who knows.



Implementation of pollard's (and subsequently lenstra's) algorithm for factorisation. Functions to convert a number from base 10 to binary, to perform modular exponentiation, and to apply the euclidean algorithm need to be defined first before a fourth function to implement pollard is made.

All code assumes curve is in short Weierstrass form, i.e. a = 0

Some practice numbers to test include:
    246082373
    540143
    491389 - might be the one that doesn't really work for Pollard
    6994241
    5917
    779167
    4331 - throws error when A=5, investigate
    10001
    18923
    115147
    455839
    45471277 / 3319403221
    152148213 - ?
    1331544304861 - probably best leave this to lenstra's..
    1689542430967
    8414786257
    30436307070163 - ermagehrd, need to get this one somehow -- Got it!
    15871587578715223124213557 - hmm, tried with (2,1), (3,1), (3,2), (5,2)
"""

import math

# return the binary representation of an integer, in reverse order as an array
def binary(integer):
    # compare input with increasing powers of two to generate list
    compare = 2
    powers = [1]
    while(compare <= integer):
        powers = powers + [compare]
        compare = compare * 2
    #print(powers)

    # decide which powers are in representation
    l = len(powers)
    representation = [0]*l

    for p in range(1,l+1):
        if powers[l-p]<=integer:
            integer = integer - powers[l-p]
            representation[l-p] = 1

    return representation

# oh god why must I do this in python

# perform modular exponentiation and return a^k mod n. Depends on function binary
def modex(a=1,k=1,n=1):
    bin = binary(k)

    # generate the Ai's

    A = [a]
    for i in range(0,len(bin)-1):
        x = A[i] * A[i]
        A = A + [x%n]
    # print A

    # perform calculation

    ans = 1
    #print range(0,len(bin))
    for i in range(0,len(bin)):
        if bin[i]==1:
            #print A[i]
            ans = ans * A[i]
            ans = ans%n
    ans = ans%n
    return ans

# run quick compositeness test using fermat's little theorem
def primetest(N,diag=True):
    fermat = modex(2,N-1,N)
    if fermat == 1:
        if diag:
            print "Warning: input is either prime or pseudoprime."
        return 0
    else:
        if diag:
            print "Input is composite"
        return 1

# perform the euclidean algorithm on two inputs a and b
def euclidean(a,b,prin=True,inv=False):
    if a<b:# switch a and b if necessary, to ensure that a is larger
        z = a
        a = b
        b = z
    # save initial inputs
    A = a
    B = b

    # initialise quotient and remainder and then perform algorithm

    r = a%b
    Q = [a/b]

    while r!=0:
        a = b
        b = r
        r = a%b
        Q = Q + [a/b]
    # print Q

    # work out X and Y, the coefficients of the inputs when writing gcd
    length = len(Q)
    if length == 1:
        X = 1
        Y = Q[0]-1
    elif length == 2:
        X = 1
        Y = Q[0]
    else:
        X = 1
        Y = Q[length-2]
        # print "X = %i" % (X)
        # print "Y = %i" % (Y)
        update = 0 # records whether to alter X or Y
        for iter in range(1,length-1):
            if update == 0:
                X = X + Q[length-2-iter] * Y
                update = 1
                # print "X = %i" % (X)
                # print "Y = %i" % (Y)
            else:
                Y = Y + Q[length-2-iter] * X
                update = 0
                # print "X = %i" % (X)
                # print "Y = %i" % (Y)

    if prin:# print GCD as linear combination of inputs if prin=True
        if length <= 2:
            print "GCD = %i = %i * %i - %i * %i" % (b, X, A, Y, B)

        elif length%2 == 0:
            print "GCD = %i = %i * %i - %i * %i" % (b, X, A, Y, B)

        else:
            print "GCD = %i = %i * %i - %i * %i" % (b, X, B, Y, A)

    if inv:# return inverse of smaller input in Z_(larger input). Not necessarily valid!
        if length <= 2:
            return (b,(-1*Y)%A)

        elif length%2 ==0:
            return (b,(-1*Y)%A)

        else:
            return (b,X)

    else:
        return b

# double input point P modulo N, on C: Y2 = X3 + bX + c (mod N)
# when called within function, returns [success,value], so either [all fine, point] or [couldn't double point, this is the offending inverse]
def dub(P,N,b=1,func=False):
    # first calculate lambda, = lamb
    e = euclidean((2*P[1])%N,N,prin=False,inv=True)

    if e[0]!=1:# no need for corresponding else
        if func:
            return [1,e[0]]
        return "Found %i as a factor" % (e[0])

    n = (3 * P[0]**2 + b)%N
    d = e[1]%N# modulus may be redundant..
    lamb = (d*n)%N

    # calculate new coords, x and y
    x = (lamb**2 - (2*P[0]))%N
    y = (-1*lamb*x - P[1] + lamb*P[0])%N
    
    if func:
        return [0,(x,y)]
    return (x,y)

# adds two distinct points modulo N, on EC : Y2 = X3 + bX + c
# when called within function, returns [success,value], so either [all fine, point] or [couldn't double point, this is the offending inverse]
def add(P1,P2,N,func=False):
    #calculate lambda, = lamb
    e = euclidean((P2[0]-P1[0])%N,N,prin=False,inv=True)

    if e[0]!=1:# no need for corresponding else
        if func:
            return [1,e[0]]
        return "Found %i as a factor" % (e[0])

    n = P2[1]-P1[1]
    d = e[1]%N# modulus may be redundant..
    lamb = (d*n)%N

    # calculate new coords, x and y
    x = (lamb**2 -P1[0]-P2[0])%N
    y = (lamb*(P1[0] - x) - P1[1])%N

    if func:
        return [0,(x,y)]
    return(x,y)

# MAIN FUNCTIONS

# use trial division on input to either return a factor or confirm a number is prime
def brute(N):
    if N < 20:
        return "What the fuck are you, stupid?"
    if N % 2 == 0:
        return "Even, so obviously composite"
    for x in range(3,int(N**0.5)+1,2):
        if N % x == 0:
            return "%i is a factor" % (x)
    return "Prime"

# perform pollard's algorithm on an input
def pollard(N,K=10):
    a = 2
    for exp in range(2,K):
        a = modex(a,exp,N)
        g = euclidean(a-1,N,prin=False)
        if g>1:
            return "Found %i as a factor." % g
    return "Unable to find a factor."

# perform lenstra's algorithm on an input
def lenstra(N,K=20,b=False,X=2,Y=1):
    # if b specified, execute only b
    if b:
        # initialise stuff
        k = 10*9*8*7*6*5*4*3*2
        bin = binary(k)
        length = len(bin)

        # print "k = %i"%(k)

        # generate list of points via doubling
        points = [(X,Y)]
        for e in range(0,length-1):
            new = dub(points[e],N,b,func=True)
            if new[0]!=0:
                print points
                return "Found %i as a factor on curve with b = %i" % (new[1],b)

            points = points + [new[1]]
        # print points

        # compute kP
        # find first point in binary representation
        for x in range(0,length+1):
            if bin[x] ==1:
                start = x
                kP = points[start]
                # print kP
                break

        # add relevant points to find kP
        for x in range(start+1,length):
            if bin[x] == 1:
                new = add(kP,points[x],N,func=True)
                if new[0]!=0:
                    print kP
                    print points[x]
                    return "Found %i as a factor on curve with b = %i" % (new[1],b)
                # print new[1]
                kP = new[1]

        return "kP = (%i,%i)" % (kP[0],kP[1])

    # end of single-case



    # pre-start checks

    # run quick compositeness test using primetest
    primetest(N)
    
    # test to make sure gcd(6,n) == 1
    six = euclidean(N,6,prin=False)
    if six != 1:
        return "Found %i as a factor" % six

    # begin algorithm proper

    # initialise variables
    k = 10*9*8*7*6*5*4*3*2

    bin = binary(k)
    
    length = len(bin)
    b = 1

    while b<=50000:
        # generate list of points via doubling
        points = [(X,Y)]
        for e in range(0,length-1):
            new = dub(points[e],N,b,func=True)
            if new[0]!=0:
                return "Found %i as a factor on curve with b = %i" % (new[1],b)

            points = points + [new[1]]

        # compute kP
        # find first point in binary representation
        for x in range(0,length+1):
            if bin[x] ==1:
                start = x
                kP = points[start]
                break

        # add relevant points to find kP
        for x in range(start+1,length):
            if bin[x] == 1:
                new = add(kP,points[x],N,func=True)
                if new[0]!=0:
                    return "Found %i as a factor on curve with b = %i" % (new[1],b)
                kP = new[1]

        b = b + 1
    
    return "Unable to find a factor :("
