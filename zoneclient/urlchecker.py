import mechanize

if (__name__ == '__main__'):
    br = mechanize.Browser()
    br.set_handle_redirect(False)
    try:
        br.open_novisit('http://www.cargochief.com')
        print 'OK'
    except:
        print '~OK'
