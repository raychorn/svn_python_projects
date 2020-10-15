'''
1) “Write a subroutine, function, or method that takes an array of characters and 
returns an array of the same characters in reversed order with every consonant 
lower cased and every vowel upper cased. Prove your implementation works."
'''

__vowels__ = [t for t in 'aeiouy']

if (__name__ == '__main__'):
    
    print 'Enter some characters, letters or words. ',
    words = raw_input()
    
    new_words = []
    for i in xrange(len(words),0,-1):
        ch = words[i-1]
        if (ch in __vowels__):
            ch = ch.upper()
        else:
            ch = ch.lower()
        new_words.append(ch)
    print ''.join(new_words)
    print '\n'
    