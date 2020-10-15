import os
import sys
import tidy
import StringIO

fname = 'Z:/@myMagma/python-docs/sfapi2/index.html'

if __name__=='__main__':
    options = dict(output_xhtml=1, add_xml_decl=1, indent=1, tidy_mark=0)
    fIn = open(fname,'r')
    data = ''.join(fIn.readlines())
    fIn.close()
    _tidyXML = tidy.parseString(data, **options)
    if (len(_tidyXML.errors) > 0):
        print 'ERRORS: \n%s' % _tidyXML.errors
    else:
        s = '%s' % _tidyXML
        lines = [l.strip() for l in s.split('\n')]
        _fname = os.path.basename(fname).replace('.','_')+'.xml'
        fOut = open(_fname,'w')
        fOut.writelines(lines)
        fOut.flush()
        fOut.close()
    pass

