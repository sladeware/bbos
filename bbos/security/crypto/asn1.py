'''
ASN.1 DER and PEM helper routines.
'''
# XXX replace all asserts with valueerrors

from base64 import b64encode, b64decode
from binascii import a2b_hex, b2a_hex
from string import letters, digits

__all__ = [ 'sequence', 'integer' ] # XXX

# Class constants
asn1_class_universal        = 0
asn1_class_application      = 1
asn1_class_context_specific = 2
asn1_class_private          = 3
asn1_classes = [ 'universal', 'application', 'context-specific', 'private' ]

class ASN1:
  'Base class for ASN.1 objects.'

  asn1_class = asn1_class_universal # default class

  def value(self):
    '''Overridden by subclasses to give an underlying value for hash and eq
    functions.'''
    raise NotImplementedError()

  def der_encode(self):
    'Returns the DER encoding of the object.'
    raise NotImplementedError()

  @classmethod
  def der_decode(cls, tag, contents, der_strict):
    'Returns a new object decoded from the given tag and contents octets.'
    raise NotImplementedError()


  def __eq__(self, other):
    try:
      return (self.asn1_class == other.asn1_class and
              self.tag == other.tag and self.value() == other.value())
    except AttributeError:
      return False
  def __ne__( self, other ):
    return not self.__eq__( other )
  def __hash__( self ):
    return hash( self.asn1_class ) ^ hash( self.tag ) ^ hash( self.value() )




class context_specific(ASN1):
  der_constructed = True
  asn1_class = asn1_class_context_specific

  def __init__( self, tag, value ):
    self.tag, self.underlying_value = tag, value

  def value( self ): return self.underlying_value

  def __str__ ( self ):
    indented_value = str( self.value() ).replace( '\n', '\n ' )
    return 'context-specific [%i]\n %s' % ( self.tag, indented_value )
  def __repr__( self ):
    return '%s(%i, %s)' % ( self.__class__.__name__, self.tag,
                            repr( self.value() ) )

  def der_encode( self ):
    return der_tlv( self.tag, self.value().der_encode(), self.der_constructed,
                    asn1_class_context_specific )

  @classmethod
  def der_decode( cls, tag, contents, der_strict ):
    value, rest = der_decode( contents, der_strict )
    assert rest == ''
    return cls( tag, value )

class null(ASN1):
  tag = 0x05
  der_constructed = False

  def __init__( self ): pass

  def value( self ): return None

  def __str__ ( self ): return 'NULL'
  def __repr__( self ): return '%s()' % self.__class__.__name__

  def der_encode( self ):
    return der_tlv( self.tag, '' )

  @classmethod
  def der_decode( cls, tag, contents, der_strict ):
    assert contents == ''
    return cls()


class integer(ASN1):
  tag = 0x02
  der_constructed = False

  def __init__(self, i):
    self.i = i
    assert i >= 0

  def value( self ): return self.i

  def __str__ ( self ): return 'INTEGER: %i' % self.i
  def __repr__( self ):
    return '%s(%i)' % ( self.__class__.__name__, self.i )

  def __long__( self ): return long( self.i )
  def __int__ ( self ): return  int( self.i )

  def der_encode( self ):
    h = '%X' % self.i
    if len(h) % 2 == 1: h = '0' + h       # ensure multiple of 2 hex digits
    if int( h[0], 16 ) >= 8: h = '00' + h # ensure sign bit is zero
    return der_tlv( self.tag, a2b_hex( h ) )

  @classmethod
  def der_decode(cls, tag, contents, der_strict):
    assert contents[0] != '\x00' or contents == '\x00' or ord(contents[1]) >= 0x80
    assert ord(contents[0]) < 0x80 # negative numbers not supported yet
    h = b2a_hex( contents )
    return cls( long( h, 16 ) )


class bit_string(ASN1):
  tag = 0x03
  der_constructed = False

  def __init__( self, octets, unused_bits = 0 ):
    assert 0 <= unused_bits < 8
    self.octets = octets
    self.unused_bits = unused_bits

  def value( self ): return self.octets, self.unused_bits

  def __str__ ( self ): return 'BIT STRING' 
  def __repr__( self ):
    return '%s(%s, %i)' % ( self.__class__.__name__, repr( self.octets ),
                            self.unused_bits )

  def as_octets( self ):
    assert self.unused_bits == 0
    return self.octets

  def der_encode( self ):
    contents = chr( self.unused_bits ) + self.octets
    return der_tlv( self.tag, contents )

  @classmethod
  def der_decode( cls, tag, contents, der_strict ):
    assert len( contents ) > 0
    return cls( contents[1:], ord( contents[0] ) )


class octet_string(ASN1):
  tag = 0x04
  der_constructed = False

  def __init__( self, octets ):
    self.octets = octets

  def value( self ): return self.octets

  def __str__ ( self ): return 'OCTET STRING'
  def __repr__( self ):
    return '%s(%s)' % ( self.__class__.__name__, repr( self.octets ) )

  def as_octets( self ): return self.octets

  def der_encode( self ):
    return der_tlv( self.tag, self.octets )

  @classmethod
  def der_decode( cls, tag, contents, der_strict ):
    return cls( contents )


class printable_string(ASN1):
  tag = 0x13
  der_constructed = False

  spec_valid_characters = letters + digits + " '()+,-./:=?"
  permitted_characters = spec_valid_characters + '@'

  def __init__( self, s ):
    self.s = s
    for c in s: assert c in self.permitted_characters

  def value( self ): return self.s

  def __str__ ( self ): return 'PRINTABLE STRING: %s' % self.s
  def __repr__( self ):
    return '%s(%s)' % ( self.__class__.__name__, repr( self.s ) )

  def as_octets( self ): return self.s

  def der_encode( self ):
    return der_tlv( self.tag, self.s )

  @classmethod
  def der_decode( cls, tag, contents, der_strict ):
    return cls( contents )


class ia5_string(ASN1):
  tag = 0x16
  der_constructed = False

  def __init__( self, s ):
    self.s = s

  def value( self ): return self.s

  def __str__ ( self ): return 'IA5 STRING: %s' % self.s
  def __repr__( self ):
    return '%s(%s)' % ( self.__class__.__name__, repr( self.s ) )

  def as_octets( self ): return self.s

  def der_encode( self ):
    return der_tlv( self.tag, self.s )

  @classmethod
  def der_decode( cls, tag, contents, der_strict ):
    return cls( contents )


class utc_time(ASN1):
  tag = 0x17
  der_constructed = False

  def __init__( self, s ):
    self.s = s

  def value( self ): return self.s

  def __str__ ( self ): return 'UTC TIME: %s' % self.s
  def __repr__( self ):
    return '%s(%s)' % ( self.__class__.__name__, repr( self.s ) )

  def as_octets( self ): return self.s

  def der_encode( self ):
    return der_tlv( self.tag, self.s )

  @classmethod
  def der_decode( cls, tag, contents, der_strict ):
    return cls( contents )


class object_identifier(ASN1):
  tag = 0x06
  der_constructed = False

  def __init__( self, ints ):
    self.ints = tuple( ints )
    assert 0 <= ints[0] <= 2
    if ints[0] < 2:
      assert 0 <= ints[1] <= 39
    else:
      assert 0 <= ints[1] < 256 - 80

  def child( self, *ints ):
    return self.__class__( self.ints + tuple( ints ) )

  def value( self ): return self.ints

  def __str__( self ):
    return 'OBJECT IDENTIFIER: %s' % ' '.join(( str(i) for i in self.ints ))
  def __repr__( self ):
    return '%s(%s)' % ( self.__class__.__name__, repr( self.ints ) )

  def __iter__( self ):
    return iter( self.ints )

  def der_encode( self ):
    contents = chr( self.ints[0] * 40 + self.ints[1] )
    for i in self.ints[ 2: ]:
      contents += b128_encode( i )
    return der_tlv( self.tag, contents )

  @classmethod
  def der_decode( cls, tag, contents, der_strict ):
    assert len( contents ) >= 1
    first = ord( contents[0] )
    if 0 <= first < 40:
      ints = [ 0, first ]
    elif 40 <= first < 80:
      ints = [ 1, first - 40 ]
    else:
      ints = [ 2, first - 80 ]

    rest = contents[ 1: ]
    while len( rest ) > 0:
      i, rest = b128_decode( rest )
      ints.append( i )
    return cls( ints )


class sequence(ASN1):
  tag = 0x10
  der_constructed = True

  def __init__( self, objs ):
    self.objs = tuple( objs )

  def value( self ): return self.objs

  def __str__ ( self ):
    return 'SEQUENCE' + ''.join(( '\n '+str(x).replace('\n','\n ') for x in self ))
  def __repr__( self ):
    return '%s(%s)' % ( self.__class__.__name__, repr( self.objs ) )

  def __iter__( self ):       return iter( self.objs )
  def __len__( self ):        return len( self.objs )
  def __getitem__( self, i ): return self.objs[i]

  def der_encode( self ):
    contents = ''
    for obj in self:
      contents += obj.der_encode()
    return der_tlv( self.tag, contents, self.der_constructed )

  @classmethod
  def der_decode( cls, tag, contents, der_strict ):
    objs = []
    while len( contents ) > 0:
      obj, contents = der_decode( contents, der_strict )
      objs.append( obj )
    return cls( objs )


class set_of(ASN1):
  tag = 0x11
  der_constructed = True

  def __init__( self, objs ):
    self.objs = tuple( objs )

  def value( self ): return self.objs

  def __str__ ( self ):
    return 'SET' + ''.join(( '\n '+str(x).replace('\n','\n ') for x in self ))
  def __repr__( self ):
    return '%s(%s)' % ( self.__class__.__name__, repr( self.objs ) )
  def __iter__( self ):
    return iter( self.objs )

  def der_encode( self ):
    encodings = [ x.der_encode() for x in self ]
    encodings.sort()
    return der_tlv( self.tag, ''.join( encodings ), self.der_constructed )

  @classmethod
  def der_decode( cls, tag, contents, der_strict ):
    objs = []
    while len( contents ) > 0:
      obj, contents = der_decode( contents, der_strict )
      objs.append( obj )
    return cls( objs )

def b128_encode( i ):
  octets = [ i % 0x80 ]
  i /= 0x80
  while i > 0:
    octets.append( ( i % 0x80 ) | 0x80 )
    i /= 0x80
  octets.reverse()
  return ''.join(( chr(x) for x in octets ))

def b128_decode( s ):
  i = 0
  for pos, c in enumerate( s ):
    octet = ord( c )
    i *= 0x80
    i |= octet & 0x7F
    if octet & 0x80 == 0: break
  else:
    raise ValueError( 'unexpected end of input while reading base128 integer' )

  return i, s[ pos+1: ]

def der_encode_tag( tag, constructed, asn_class ):
  if constructed: first = 1 << 5
  else:           first = 0
  first |= asn_class << 6

  if tag <= 30:
    return chr( first | tag )
  else:
    return chr( first | 31 ) + b128_encode( tag )

def der_encode_length( length ):
  if length < 0x80:
    len_octets = [ length ]
  else:
    len_octets = []
    while length > 0:
      len_octets.append( length % 0x100 )
      length /= 0x100
    assert len(len_octets) < 0x80
    len_octets.append( len(len_octets) | 0x80 )
    len_octets.reverse()
  return ''.join(( chr(x) for x in len_octets ))

def der_tlv(tag, contents, constructed=False,
            asn_class = asn1_class_universal):
  '''Helper routine to construct a DER encoding from the tag number and
  contents octets.'''
  return (der_encode_tag( tag, constructed, asn_class ) +
          der_encode_length( len( contents ) ) +
          contents)

def der_decode_tag( octets ):
  assert len(octets) >= 2
  first, rest = ord( octets[0] ), octets[1:]
  constructed = first & ( 1 << 5 ) != 0
  asn1_class = first >> 6
  first &= 31

  if first < 31:
    tag = first
  else:
    tag, rest = b128_decode( rest )
  return tag, constructed, asn1_class, rest

def der_decode_length( octets ):
  assert len(octets) >= 1
  first, rest = ord( octets[0] ), octets[1:]
  if first & 0x80 == 0:
    length = first
  else:
    len_len = first & 0x7F
    length = 0
    for i in xrange(len_len):
      length *= 0x100
      length |= ord( rest[i] )
    rest = rest[ len_len: ]
  return length, rest

universal_decode_handlers = dict(( ( x.tag, x ) for x in (
  null,
  integer,
  bit_string,
  octet_string,
  printable_string,
  ia5_string,
  utc_time,
  object_identifier,
  sequence,
  set_of,
)))

def der_decode( octets, der_strict = True ):
  '''Public routine to convert a DER encoding to an ASN1 object.  Returns the
  object and the remaining bytes.'''
  tag, constructed, asn1_class, rest = der_decode_tag( octets )
  length, rest = der_decode_length( rest )
  assert len( rest ) >= length
  contents, rest = rest[ :length ], rest[ length: ]

  if asn1_class == asn1_class_universal:
    assert tag in universal_decode_handlers
    handler = universal_decode_handlers[ tag ]
    assert constructed == handler.der_constructed
    obj = handler.der_decode( tag, contents, der_strict )

  elif asn1_class == asn1_class_context_specific:
    assert constructed == context_specific.der_constructed
    obj = context_specific.der_decode( tag, contents, der_strict )

  else:
    raise ValueError( 'cannot handle %s class tag %i' % ( asn1_classes[asn1_class], tag ) )

  return obj, rest







# PEM routines.

def pem_encode( asn1_object, type_string ):
  '''Encode an asn1_object as PEM.  The PEM format is base64-encoded DER
  wrapped in BEGIN/END lines.'''
  der = asn1_object.der_encode()

  b64 = b64encode( der )
  b64_lines = ( b64[ i*64 : (i+1)*64 ] for i in xrange( (len(b64)+63)/64 ) )

  fmt = '-----BEGIN %s-----\n%s\n-----END %s-----\n'
  return fmt % ( type_string, '\n'.join( b64_lines ), type_string )

def pem_extract( pem_text, type_string = None ):
  '''Find all PEM objects of the appropriate type in the text, base64-decode
  them into octet blobs, and return them as a list of strings.'''
  begin, end, dashes = '-----BEGIN ', '-----END ', '-----'
  bodies = []
  line_iterator = iter( pem_text.splitlines() )
  for line in line_iterator:
    if line.startswith( begin ) and line.endswith( dashes ):
      if type_string is not None and line != begin+type_string+dashes: continue

      # Accumulate base64 lines.
      b64 = ''
      for line in line_iterator:
        if line.startswith( end ) and line.endswith( dashes ): break
        b64 += line

      bodies.append( b64decode( b64 ) )

  return bodies

def pem_decode( pem_text, type_string = None, der_strict = True ):
  '''Find all PEM objects of the appropriate type in the text, DER-decode them
  into ASN.1 objects, and return them as a list.'''
  objs = []
  for body in pem_extract( pem_text, type_string ):
    obj, rest = der_decode( body, der_strict = der_strict )
    assert rest == ''
    objs.append( obj )
  return objs


if __name__ == '__main__':
  from sys import stdin
  for obj in pem_decode( stdin.read(), der_strict = False ):
    print str( obj )

class Test:
  def test_cert(self):
    from base64 import b64decode
    cert_der = b64decode('''
MIIDdTCCAt6gAwIBAgIDGgTWMA0GCSqGSIb3DQEBBQUAMGwxCzAJBgNVBAYTAlVT
MRYwFAYDVQQIEw1NYXNzYWNodXNldHRzMS4wLAYDVQQKEyVNYXNzYWNodXNldHRz
IEluc3RpdHV0ZSBvZiBUZWNobm9sb2d5MRUwEwYDVQQLEwxDbGllbnQgQ0EgdjEw
HhcNMDUwMjEwMjE0NDIxWhcNMDUwNzMwMjE0NDIxWjCBoTELMAkGA1UEBhMCVVMx
FjAUBgNVBAgTDU1hc3NhY2h1c2V0dHMxLjAsBgNVBAoTJU1hc3NhY2h1c2V0dHMg
SW5zdGl0dXRlIG9mIFRlY2hub2xvZ3kxFTATBgNVBAsTDENsaWVudCBDQSB2MTEV
MBMGA1UEAxMMQ2hyaXMgVCBMYWFzMRwwGgYJKoZIhvcNAQkBEw1nb2xlbUBNSVQu
RURVMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA9RAulq4jGegpyn24
3JDiXI1Y/pYVASqxjfg1MXr59QWywnwmH11VuX1jzxRObszhWxOwCPR5Tvdqrikd
F5cLzyqIXDGSY6UdVCEFm9KTGIRHBm8QjqNUH67sySkjpvXgiLS/UfsM3N9XUgIh
9vEPZnLxRLXpYxkS54tG92FLOY3HHWKGXPaDs4u3+OeFDhI9VDBjNiy3UVWr2x3P
D3tWvX6ADY2w7bno1F1Jpd1FweIU/9eLLu4GeBSiUJKJ3xGIRv3+lowAC7n731GA
7Aw7F/9JccOdQ5OjYu2Oeu00YdBxJL7bnrhsngZ4WLREuDkjluBToAjIKH1XR65n
7aJlBQIDAQABo2swaTAJBgNVHRMEAjAAMBEGCWCGSAGG+EIBAQQEAwIFoDAdBgNV
HSUEFjAUBggrBgEFBQcDBAYIKwYBBQUHAwIwCwYDVR0PBAQDAgXgMB0GA1UdDgQW
BBQKCBNTN785F4yP/vv8oJvP4OW9ajANBgkqhkiG9w0BAQUFAAOBgQAspnWlJsap
qy14qy6il0pRVs+G62kBuOK3fPtTV0IYK74bxN6NdJqnjoy37sv2O/ewJv5BOWzA
BOHPGNYR5fdN/oiWXpuGVwgKwX5wC4U9CAjkqSOO2Rp8hYIc+GmdfEPJMkhtcd6d
A7DcwPNoj1dcSwaFIt1k3ezKFwJBJqjUOw==
    ''')
    cert, rest = der_decode( cert_der )
    print cert
    print rest
    reencoded = cert.der_encode()
    print b2a_hex( cert_der )
    print b2a_hex( reencoded )
    assert reencoded == cert_der

  def test_pem(self):
    pem = '''-----BEGIN CERTIFICATE-----
MIIDdTCCAt6gAwIBAgIDGgTWMA0GCSqGSIb3DQEBBQUAMGwxCzAJBgNVBAYTAlVT
MRYwFAYDVQQIEw1NYXNzYWNodXNldHRzMS4wLAYDVQQKEyVNYXNzYWNodXNldHRz
IEluc3RpdHV0ZSBvZiBUZWNobm9sb2d5MRUwEwYDVQQLEwxDbGllbnQgQ0EgdjEw
HhcNMDUwMjEwMjE0NDIxWhcNMDUwNzMwMjE0NDIxWjCBoTELMAkGA1UEBhMCVVMx
FjAUBgNVBAgTDU1hc3NhY2h1c2V0dHMxLjAsBgNVBAoTJU1hc3NhY2h1c2V0dHMg
SW5zdGl0dXRlIG9mIFRlY2hub2xvZ3kxFTATBgNVBAsTDENsaWVudCBDQSB2MTEV
MBMGA1UEAxMMQ2hyaXMgVCBMYWFzMRwwGgYJKoZIhvcNAQkBEw1nb2xlbUBNSVQu
RURVMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA9RAulq4jGegpyn24
3JDiXI1Y/pYVASqxjfg1MXr59QWywnwmH11VuX1jzxRObszhWxOwCPR5Tvdqrikd
F5cLzyqIXDGSY6UdVCEFm9KTGIRHBm8QjqNUH67sySkjpvXgiLS/UfsM3N9XUgIh
9vEPZnLxRLXpYxkS54tG92FLOY3HHWKGXPaDs4u3+OeFDhI9VDBjNiy3UVWr2x3P
D3tWvX6ADY2w7bno1F1Jpd1FweIU/9eLLu4GeBSiUJKJ3xGIRv3+lowAC7n731GA
7Aw7F/9JccOdQ5OjYu2Oeu00YdBxJL7bnrhsngZ4WLREuDkjluBToAjIKH1XR65n
7aJlBQIDAQABo2swaTAJBgNVHRMEAjAAMBEGCWCGSAGG+EIBAQQEAwIFoDAdBgNV
HSUEFjAUBggrBgEFBQcDBAYIKwYBBQUHAwIwCwYDVR0PBAQDAgXgMB0GA1UdDgQW
BBQKCBNTN785F4yP/vv8oJvP4OW9ajANBgkqhkiG9w0BAQUFAAOBgQAspnWlJsap
qy14qy6il0pRVs+G62kBuOK3fPtTV0IYK74bxN6NdJqnjoy37sv2O/ewJv5BOWzA
BOHPGNYR5fdN/oiWXpuGVwgKwX5wC4U9CAjkqSOO2Rp8hYIc+GmdfEPJMkhtcd6d
A7DcwPNoj1dcSwaFIt1k3ezKFwJBJqjUOw==
-----END CERTIFICATE-----
'''
    cert, = pem_decode( pem, 'CERTIFICATE' )
    reencoded = pem_encode( cert, 'CERTIFICATE' )
    print reencoded
    assert reencoded == pem
