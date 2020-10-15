import ezPyCrypto

def test1():
    secretString = "Hello, this string will be encrypted"
    
    # Create a key object
    print "Generating 2048-bit keypair - could take a while..."
    k = ezPyCrypto.key(2048)
    #k = ezPyCrypto.key(512)
    
    # Encrypt a string
    print "Unencrypted string: '%s'" % secretString
    enc = k.encString(secretString)

    print "Encrypted string: '%s'" % enc
    
    # Now decrypt it
    dec = k.decString(enc)
    print "Decrypted string: '%s'" % dec

    assert dec == secretString, 'Oops, something terrible happened.'

if (__name__ == '__main__'):
    test1()
