from htmltransform import parser

fname = 'Z:/@myMagma/python-docs/sfapi2/index.html'
dlect = 'mediawiki'

if __name__=='__main__':
    import sys
    d = parser.parse(fname, dialect=dlect)
    print d
