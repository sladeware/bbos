
from bbos.crypto.pkcs1 import rsa_gen_key, rsaes_pkcs1_v1_5_encrypt, rsaes_pkcs1_v1_5_decrypt

if __name__=='__main__':
	public_key, private_key = rsa_gen_key(1024)
	print public_key.pem_encode()
	print private_key.pem_encode()
	msg = 'hello'
	print "Message: " + msg
	ciphertext = rsaes_pkcs1_v1_5_encrypt(public_key, msg)	
	print "Encoded message:\n" + ciphertext
	print "Decoded message: " + rsaes_pkcs1_v1_5_decrypt(private_key, ciphertext)

