from vyperlogix.xml import xml_utils

if (__name__ == '__main__'):
    
    l = ['Now is the time for all & good men.',
         'Now is the time for all <> good men.',
         'Now is the time for all good men.']

    for s in l:
        f = '(**)' if (xml_utils.is_cdata(s)) else ''
        print '%s%s' % (f,s)
        print '-'*20
    