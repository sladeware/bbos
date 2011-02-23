
__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

import sys
import os.path
import unittest

# Setup the path properly for bbos builder imports
path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../.."
sys.path.append(path)

from bbos.security.crypto.pkcs1 import *

HEX_STRING = "8b4157d26da9eb9cf7671190d4c71d24f1dd4f7ca312c1ba757e14f7a977c332"

class SanityCheck(unittest.TestCase):
    def test(self):
	public_key, private_key = rsa_gen_key(256)
	#print public_key.pem_encode()
	#print private_key.pem_encode()
	msg = 'hello'
	#print "Message: " + msg + "\n"
	ciphertext = rsaes_pkcs1_v1_5_encrypt(public_key, msg)
	#print "Encoded message (hex):\n" + ciphertext.encode("hex") + "\n"
	#print "Decoded message: " + rsaes_pkcs1_v1_5_decrypt(private_key, ciphertext)
        self.assertEquals(HEX_STRING, ciphertext.encode("hex"))
