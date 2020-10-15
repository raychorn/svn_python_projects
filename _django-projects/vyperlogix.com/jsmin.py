from vyperlogix.misc import jsmin

if (__name__ == '__main__'):
    import os, sys
    if (len(sys.argv) > 1):
        if (len(sys.argv) >= 2) and (os.path.exists(sys.argv[1])):
            sys.stdin = open(sys.argv[1],'r')
        if (len(sys.argv) >= 3) and (os.path.exists(os.path.dirname(sys.argv[2]))):
            sys.stdout = open(sys.argv[2],'w')
    jsm = jsmin.JavascriptMinify()
    jsm.minify(sys.stdin, sys.stdout)
