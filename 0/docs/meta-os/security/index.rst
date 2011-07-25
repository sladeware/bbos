.. _os-api-security:

########
Security
########

:Date: |today|

Security.

******
Crypto
******

:mod:`bbos.security.crypto.asn1` --- ASN.1
==========================================

.. automodule:: bbos.security.crypto.asn1

.. autoclass:: ASN1
   :members:

.. autofunction:: bbos.security.crypto.asn1.der_decode
.. autofunction:: bbos.security.crypto.asn1.der_encode
.. autofunction:: bbos.security.crypto.asn1.pem_decode
.. autofunction:: bbos.security.crypto.asn1.pem_extract

:mod:`bbos.security.crypto.pkcs1` --- PKCS1
===========================================
 
.. automodule:: bbos.security.crypto.pkcs1

.. autofunction:: bbos.security.crypto.pkcs1.i2osp
.. autofunction:: bbos.security.crypto.pkcs1.mgf1
.. autofunction:: bbos.security.crypto.pkcs1.os2ip
.. autofunction:: bbos.security.crypto.pkcs1.rsa_gen_key

:mod:`bbos.security.crypto.prime` -- Prime numbers
==================================================

.. autofunction:: bbos.security.crypto.prime.get_fast_prime
.. autofunction:: bbos.security.crypto.prime.get_prime
.. autofunction:: bbos.security.crypto.prime.primality_test
.. autofunction:: bbos.security.crypto.prime.trial_division

