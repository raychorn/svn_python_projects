def soundex(name, len=4):
    """ soundex module conforming to Knuth's algorithm
        implementation 2000-12-24 by Gregory Jorgensen
        public domain
    """

    # digits holds the soundex values for the alphabet
    digits = '01230120022455012623010202'
    sndx = ''
    fc = ''

    # translate alpha chars in name to soundex digits
    for c in name.upper():
        if c.isalpha():
            if not fc: fc = c   # remember first letter
            d = digits[ord(c)-ord('A')]
            # duplicate consecutive soundex digits are skipped
            if not sndx or (d != sndx[-1]):
                sndx += d

    # replace first digit with first alpha character
    sndx = fc + sndx[1:]

    # remove all 0s from the soundex code
    sndx = sndx.replace('0','')

    # return soundex code padded to len characters
    return (sndx + (len * '0'))[:len]

if __name__ == '__main__':
    from SequenceMatcher import *
    
    a = "qabxcd"
    b = "abycdf"
    
    n = max(len(a),len(b))
    
    _a = soundex(a,n)
    _b = soundex(b,n)
    
    print 'soundex(%s)=(%s)' % (a,_a)
    print 'soundex(%s)=(%s)' % (b,_b)
    
    s = computeRatios(a,b)
    print 'computeRatios(%s,%s)' % (a,b)
    reportRatios(s,a,b)

    print '\n\n'
    
    _s = computeRatios(_a,_b)
    reportRatios(_s,_a,_b)

    print '\n\n'

    s = computeRatios("abcd", "bcde")
    reportRatios(s, "abcd", "bcde")
    
    s = computeRatios("qabxcd", "abycdf")
    reportRatios(s, "qabxcd", "abycdf")
