import os, sys

_slice_num = 5
_fname = 'sampleEpyDocSource.txt'

def main(fname):
    if (os.path.exists(fname)):
        fIn = open(fname,'r')
        lines = [l[_slice_num:] for l in fIn.readlines()]
        fIn.close()
        
        toks = fname.split('.')
        fOut = open('.'.join([toks[0],'py']),'w')
        fOut.writelines(''.join(lines))
        fOut.flush()
        fOut.close()
    else:
        print 'ERROR:: Missing file named "%s".' % fname

if (__name__ == '__main__'):
    main(_fname)
    pass
