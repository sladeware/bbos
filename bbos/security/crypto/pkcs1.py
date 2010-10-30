"""
pkcs1.py

An implementation of the PKCS#1 standard for RSA cryptography.
PKCS#1 is the first of a family of standards called Public-Key Cryptography
Standards (PKCS), It provides the basic definitions of and recommendations
for implementing the RSA algorithm for public-key cryptography. It defines
the mathematical properties of public and private keys, primitive operations
for encryption and signatures, secure cryptographic schemes, and related ASN.1
syntax representations.
"""

__version__ = '0.0.2'
__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

import math
import asn1
import sha
import copy
import struct
from binascii import a2b_hex, b2a_hex
from random import randint

from bbos.security.crypto.prime import get_fast_prime

#______________________________________________________________________________

class rsa_key:
    """
    Base class for RSA public class and RSA private class
    """
    def __init__(self, n, e):
        self.n = n
        self.e = e
        self.len = octlen(n)

#______________________________________________________________________________

class rsa_public_key(rsa_key):
    """
    n -- the RSA modulus, a positive integer
    e -- the RSA public exponent, a positive integer
    """

    def __init__(self, n, e):
        rsa_key.__init__(self, n, e)

    def encrypt_primitive(self, encoded_msg):
        # convert the encoded message em to an integer
        # representative m
        m = os2ip(encoded_msg)
        # apply the RSAEP encryption primitive to produce
        # an integer ciphertext representative c 
        c = pow(m, self.e, self.n)
        # convert the ciphertext representative c to a
        # ciphertext C of k octets
        return i2osp(c, self.len)
    
    def der_encode(self):
        seq = asn1.sequence((asn1.integer(self.n), asn1.integer(self.e)))
        return seq.der_encode()

    def der_decode(self, encoded_key):
        seq, rest = asn1.der_decode(encoded_key)
        assert rest == '', 'DER decode fail'
        self.n, self.e = seq
    
    def pem_encode(self):
        seq = asn1.sequence((asn1.integer(self.n), asn1.integer(self.e)))
        return asn1.pem_encode(seq, 'RSA PUBLIC KEY')

    def pem_decode(self, encoded_key):
        asn1_object, = asn1.pem_decode(encoded_key, 'RSA PUBLIC KEY', der_strict=False)
        self.n, self.e = map(long, asn1_object)

#______________________________________________________________________________

class rsa_private_key(rsa_key):
    """
    n -- the RSA modulus, a positive integer
    d -- the RSA private exponent, a positive integer
    p -- the first factor, a positive integer
    q -- the second factor, a positive integer
    d_p -- the first factor's CRT exponent, a positive integer
    d_q -- the second factor's CRT exponent, a positive integer
    q_inv -- the (first) CRT coefficient, a positive integer
    """

    def __init__(self, n, e, p, q, d, d_p, d_q, q_inv):
        self.version = 0
        self.p, self.q, self.d, self.d_p, self.d_q, self.q_inv =\
            p, q, d, d_p, d_q, q_inv
        #self.len = octlen(self.n)
        rsa_key.__init__(self, n, e)
        
    def decrypt_primitive(self, ciphertext):
        # convert the ciphertext C to an integer ciphertext
        # representative c
        c = os2ip(ciphertext)
        # apply the RSADP decryption primitive to produce an integer
        # message representative m
        m = pow(c, self.d, self.n)
        # convert the message to an encoded message
        return i2osp(m, self.len)

    def pem_encode(self):
        seq = asn1.sequence(( \
                asn1.integer(self.version), \
                    asn1.integer(self.n),       \
                    asn1.integer(self.e),       \
                    asn1.integer(self.d),       \
                    asn1.integer(self.p),       \
                asn1.integer(self.q),       \
                asn1.integer(self.d_p),     \
                asn1.integer(self.d_q),     \
                asn1.integer(self.q_inv)    \
                ))
        return asn1.pem_encode(seq, 'RSA PRIVATE KEY')
    
    def pem_decode(self, encoded_key):
        asn1_object, = asn1.pem_decode(encoded_key, 'RSA PRIVATE KEY', der_strict=False)
        version = int(asn1_object[0])
        assert version == 0, 'Incorrect version value'
        self.version, self.n, self.e, self.d, self.p, self.q, self.d_p, self.d_q, self.q_inv = map(long, asn1_object)

#______________________________________________________________________________

class rsa_encryption_scheme:
    """
    Base class for encryption schemes
    """

    def encode(self, key, msg):
        pass

    def decode(self, key, msg):
        pass

    def encrypt(self, key, msg):
        encoded_msg = self.encode(key, msg)
        return key.encrypt_primitive(encoded_msg)

    def decrypt(self, key, ciphertext):
        encoded_msg = key.decrypt_primitive(ciphertext)
        return self.decode(key, encoded_msg)

#______________________________________________________________________________

class pkcs1_v1_5_encryption(rsa_encryption_scheme):
    """
    Encryption scheme specified as PKCS1-v1_5 in PKCS#1 v2.1
    """
    def encode(self, key, msg):
        """
        encoded_msg = [0x00||0x02||padding||0x00||msg]
        """
        encoded_msg = ''
        padding_len = 0
        msg_len = len(msg)
        assert msg_len < (key.len-11), "Message too long!"
        encoded_msg += '\x00'
        encoded_msg += '\x02'
        padding_len = key.len - msg_len - 3
        for i in range(padding_len):
            encoded_msg += chr(randint(1, 255))
        encoded_msg += '\x00'
        encoded_msg += msg
        return encoded_msg

    def decode(self, key, encoded_msg):
        assert key.len>=11 and len(encoded_msg)==key.len, "Decryption error"
        assert encoded_msg[0:1]=='\x00', 'Decryption error'
        assert encoded_msg[1:2]=='\x01' or encoded_msg[1:2]=='\x02', 'Decryption error'
        padding, msg = encoded_msg[2:].split('\x00', 1)
        assert len(padding)>=8, "Decryption error"
        return msg

#______________________________________________________________________________

def rsaes_pkcs1_v1_5_encrypt(key, msg):
    return pkcs1_v1_5_encryption().encrypt(key, msg)

def rsaes_pkcs1_v1_5_decrypt(key, ciphertext):
    return pkcs1_v1_5_encryption().decrypt(key, ciphertext)

def rsa_gen_key(k):
    """
    Generate a key pair with a key of size k
    """
    if (k & 1): # Make sure that we generate p, q of equal size
        k += 1
    p, q, n = 0, 0, 0
    while 1: # The modulus n should have k-bits length
        p = get_fast_prime((k+1)>>1)
        q = get_fast_prime((k+1)>>1)
        if p==q: # can be so for small k
            continue
        if p > q: # p should be smaller then q
            (p,q) = reversed([p,q])
        n = p * q
        if nbits(n) == k:
            break
    phi = (p-1)*(q-1)
    e = 65537
    d = modinv(e, phi)
    d_p = d % (p-1)
    d_q = d % (q-1)
    q_inv = modinv(p, q)
    return \
        rsa_public_key(n, e), \
        rsa_private_key(n, e, p, q, d, d_p, d_q, q_inv)

#______________________________________________________________________________

def mgf1(seed, l):
    """
    Mask Generation Function
    """
    sd = sha.new(seed)
    t = ''
    c = 0
    while len(t)<l:
        try:
            c = struct.pack('>I',c)
        except OverflowError:
            raise ValueError('Required mask length too long')
        cd = sd.copy()
        cd.update(c)
        t += cd.digest()
    if len(t)==l: return t
    else: return t[:l]
    

def i2osp(long_integer, block_size):
    """
    Convert a long integer into an octet string.
    """
    hex_string = '%X' % long_integer
    if len(hex_string) > 2*block_size:
        raise ValueError('integer %i too large to encode in %i octets' % (long_integer, block_size))
    return a2b_hex(hex_string.zfill(2*block_size))

def os2ip(str):
    """
    Converts an octet string to a nonnegative integer
    (converts message to RSA number)
    """
    return long(b2a_hex(str), 16)

def octlen(a):
    size = nbits(a)
    octlen = size / 8
    if (size & 7)!=0: octlen += 1
    return octlen

def modinv(a,b):
    """
    If gcd(a,b)=1, then inverse(a,b)*a mod b = 1,
    otherwise, if gcd(a,b)!=1, return 0
    """
    inv,n,gcd = ext_gcd(a,b)
    return (gcd==1) * inv


def ext_gcd(a,b):
    """
    Extended version of Euclid's Algorithm
    Returns (m,n,gcd) such that  m*a + n*b = gcd(a,b)
    """
    g,u,v = [b,a],[1,0],[0,1]
    while g[1]<>0:
        y = g[0]/g[1]
        g[0],g[1] = g[1],g[0]%g[1]
        u[0],u[1] = u[1],u[0] - y*u[1]
        v[0],v[1] = v[1],v[0] - y*v[1]
    m = v[0]%b
    gcd = (m*a)%b
    n = (gcd - m*a)/b
    return (m,n,gcd)

def nbits(n):
    return int(math.log(n,2))+1

