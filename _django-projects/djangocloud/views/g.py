from vyperlogix.win.hosts import WindowsHosts

if (__name__ == '__main__'):
    import re
    from vyperlogix.enum.Enum import Enum

    class Modes(Enum):
        Unknown = 0
        Adding = 2**1
        Removing = 2**2
        Querying = 2**3

    hosts = WindowsHosts()
    #mode = Modes.Adding
    mode = Modes.Removing
    #mode = Modes.Querying
    if (mode == Modes.Adding):
        for n in xrange(0,100):
            hosts['127.0.0.1'] = 'mysite%s.djangocloud.vyperlogix.com' % (n)
        hosts.save()
    elif (mode == Modes.Querying):
        __re__ = re.compile(r"mysite1\d*\.djangocloud\.vyperlogix\.com")
        print hosts.has_domains(regex=__re__)
    elif (mode == Modes.Removing):
        __re__ = re.compile(r"mysite1\d*\.djangocloud\.vyperlogix\.com")
        hosts.remove_domains(regex=__re__)
        __re__ = re.compile(r"mysite1\d*\.djangocloud\.vyperlogix\.com")
        l = len(hosts.has_domains(regex=__re__))
        assert l == 0, '(#1) Oops !  Something went wrong somewhere !!!  %s was not expected !!!' % (l)
        __re__ = re.compile(r"mysite2\d*\.djangocloud\.vyperlogix\.com")
        l = len(hosts.has_domains(regex=__re__))
        assert l == 11, '(#2) Oops !  Something went wrong somewhere !!!  %s was not expected !!!' % (l)
        __re__ = re.compile(r"mysite3\d*\.djangocloud\.vyperlogix\.com")
        l = len(hosts.has_domains(regex=__re__))
        assert l == 11, '(#3) Oops !  Something went wrong somewhere !!!  %s was not expected !!!' % (l)
        __re__ = re.compile(r"mysite4\d*\.djangocloud\.vyperlogix\.com")
        l = len(hosts.has_domains(regex=__re__))
        assert l == 11, '(#4) Oops !  Something went wrong somewhere !!!  %s was not expected !!!' % (l)
        __re__ = re.compile(r"mysite5\d*\.djangocloud\.vyperlogix\.com")
        l = len(hosts.has_domains(regex=__re__))
        assert l == 11, '(#5) Oops !  Something went wrong somewhere !!!  %s was not expected !!!' % (l)
        __re__ = re.compile(r"mysite6\d*\.djangocloud\.vyperlogix\.com")
        l = len(hosts.has_domains(regex=__re__))
        assert l == 11, '(#6) Oops !  Something went wrong somewhere !!!  %s was not expected !!!' % (l)
        __re__ = re.compile(r"mysite7\d*\.djangocloud\.vyperlogix\.com")
        l = len(hosts.has_domains(regex=__re__))
        assert l == 11, '(#7) Oops !  Something went wrong somewhere !!!  %s was not expected !!!' % (l)
        __re__ = re.compile(r"mysite8\d*\.djangocloud\.vyperlogix\.com")
        l = len(hosts.has_domains(regex=__re__))
        assert l == 11, '(#8) Oops !  Something went wrong somewhere !!!  %s was not expected !!!' % (l)
        __re__ = re.compile(r"mysite9\d*\.djangocloud\.vyperlogix\.com")
        l = len(hosts.has_domains(regex=__re__))
        assert l == 11, '(#9) Oops !  Something went wrong somewhere !!!  %s was not expected !!!' % (l)
        hosts.save()
    #print hosts.settings
    #print hosts.prettyPrint()
    