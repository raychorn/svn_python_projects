import os, win32api

def getFileVersionInfo(fname):
    d = {}
    pairs = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')
    for lang, codepage in pairs:
        lang_codepage = '%s,%s' % (lang,codepage)
        d[lang_codepage] = {}
        for ver_string in ver_strings:
            str_info = u'\\StringFileInfo\\%04X%04X\\%s' %(lang,codepage,ver_string)
            try:
                (d[lang_codepage])[ver_string] = win32api.GetFileVersionInfo(fname, str_info)
            except:
                pass
    return d

if __name__ == '__main__':
    ver_strings=('Comments','InternalName','ProductName', 
        'CompanyName','LegalCopyright','ProductVersion', 
        'FileDescription','LegalTrademarks','PrivateBuild', 
        'FileVersion','OriginalFilename','SpecialBuild')
    fname = os.environ["comspec"]
    d=win32api.GetFileVersionInfo(fname, '\\')
    ## backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
    for n, v in d.items():
        print n, v

    if (False):
        pairs=win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')
        ## \VarFileInfo\Translation returns list of available (language, codepage) pairs that can be used to retreive string info
        ## any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle two are language/codepage pair returned from above
        for lang, codepage in pairs:
            print 'lang: ', lang, 'codepage:', codepage
            for ver_string in ver_strings:
                str_info = u'\\StringFileInfo\\%04X%04X\\%s' %(lang,codepage,ver_string)
                #print '[%s]\n' % (str(str_info))
                try:
                    print '(1) :: %s %s' % (ver_string, win32api.GetFileVersionInfo(fname, str_info))
                except Exception, details:
                    pass
                    #toks = str(details).split(':')
                    #toks2 = toks[0].split(' ')
                    #ch = ''
                    #if ( (toks2[-3] == 'in') and (toks2[-2] == 'position') and (toks2[-1].isdigit()) ):
                    #    pos = int(toks2[-1])
                    #    ch = str_info[pos]
                    #print '(ERROR) :: toks2=(%s)' % (str(toks2))
                    #print 'ERROR details (%s) [%s] [%s].' % (str(details),str(str_info),ch)

    if (True):
        print 'getFileVersionInfo()=(%s)' % (str(getFileVersionInfo(fname)))
    