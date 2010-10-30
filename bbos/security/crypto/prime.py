"""
prime.py

Prime numbers library

Copyright (c) 2009 Sun Scoper Inc.
"""

__version__ = '0.0.3'

from random import random, randint

def get_fast_prime(k):
    """
    Maurer's algorithm for finding provable primes in
    relation to the Miller-Rabin algorithm (see primality_test function) 
    """
    k0 = 20
    if k <= k0: return get_prime(k)
    c = 0.1
    m = 20 # margin
    n = 0
    g = c * (k**2)
    r = 0.5 # relative size
    if k > 2*m:
	while 1:
	    r = 0.5 + (random() % 0.5)
	    if (k-r*k) > m:
                break
    q = get_fast_prime(int(r*k))
    success = False
    I = int(pow(2,k-1) / (2*q))
    while not success:
        R = randint(I+1, 2*I)
	n = 2 * R * q + 1
	a = randint(2, n-1)
	if trial_division(n, g):
            # check Maurer's lemma #1
            a = randint(2,n-2)
            b = pow(a, n-1, n)
            if b == 1 and q > n ** (1.0/3):
                success = True
    return n

def get_prime(k, r=0, s=1):
    """
    Generate k-bits prime number.
    Takes 'k' as number of bits, 'r' - number of attemps, 's' - number of
    Miller-Rabin tests. Returns k-bits prime number.
    """
    if r==0: r = 100 * k # Max number of attempts
    if s<2: s=10  # Number of Miller-Rabin tests. Should be at least 1!
    n = 0 # result k-bits prime number
    p1 = 2**(k-1) #  interval [2**(k-1), 2**k-1]
    p2 = 2**k - 1 #
    while r > 0:
        n = randint(p1, p2)
        if primality_test(n, s): # Miller-Rabin test
            break
        r -= 1
    return n

def primality_test(n, s):
    """
    Miller-Rabin primality test
    Takes tested number n and s as number of tests. Returns false if n
    is a composite number and true otherwise.
    """
    for _ in range(s):
        a = randint(1, n-1)
        # Now the witness should gives the statements.
        # Returns false only in the case when "a" says that "n" is the
        # composite number.
        u = n-1;
        t = 0
        # ] n-1 = (2 ** t) * t, t>=1, u - odd
        while u%2 == 0:
            u = u / 2
            t += 1
        x = [pow(a,u,n)]
        if t>0:
            for i in range(1, t+1):
                x.append((x[i-1] ** 2) % n)
                if x[i]==1 and x[i-1] != 1 and x[i-1] != (n-1):
                    return False # composite number
	if x[t]!=1: return False # composite number
    return True

def trial_division(n, bound=None):
    """
    Return the smallest prime divisor <= bound of the 
    positive integer n, or n if there is no such prime.  
    If the optional argument bound is omitted, then bound=n.
    """
    if n == 1: return 1
    for p in [2,3,5]:
        if n%p==0: return p
    if bound == None: bound = n
    dif = [6,4,2,4,2,4,6,2]
    m=7
    i=1
    while m <= bound and m*m <= n:
        if n%m == 0:
            return m
        m+=dif[i%8]
        i+=1
    return n

