__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import os,sys
import re

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash.lists import HashedUniqueLists
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.misc import ObjectTypeName

__localhost__ = '127.0.0.1'

class WindowsHosts(HashedUniqueLists,SmartObject):
    def __init__(self):
        super(HashedUniqueLists, self).__init__(fromDict={},caseless=True)
        #self.settings = {'backup':True}
        self.__readHosts__(self.hosts_path)

    def hosts_path():
        doc = "hosts_path"
        def fget(self):
            return 'C:/Windows/System32/drivers/etc/hosts' if (_utils.isUsingWindows) else '/etc/hosts'
        return locals()
    hosts_path = property(**hosts_path())

    def unique(self,iterable):
        return list(sorted(set(iterable), key=unicode.lower))

    def __unique__(self,iterable):
        return list(sorted(set(iterable)))

    def __readHosts__(self,path=None):
        if not path:
            path = self.hosts_path
        hostsFile = open(path, 'rU')

        for rawLine in hostsFile:
            _line = line = rawLine.strip()
            if '#' in line:
                eol = line.index('#')
                line = line[:eol]
                if (eol > -1):
                    comment = _line[eol:]
                    self['comments'] = comment
            if line:
                destination, aliases = re.split(r'\s', line, 1)
                try:
                    hostsLine = self.unique(unicode(i).strip() for i in re.split(ur'\s*,\s*', unicode(aliases)))
                except UnicodeDecodeError:
                    continue
                if (misc.isList(hostsLine)):
                    for host in hostsLine:
                        self[destination] = host
                else:
                    self[destination] = hostsLine
        hostsFile.close()
        return

    def __writeHosts__(self,path=None):
        if not path:
            path = self.hosts_path
        try:
            if (self.settings is not None and self.settings.has_key('backup') and self.settings['backup'] == True):
                toks = list(os.path.splitext(path))
                toks[-1] += '.backup'
                path = ''.join(toks)
            hostsFile = open(path, 'w')
            for key,value in self.iteritems():
                if (key == 'comments'):
                    print >> hostsFile, value if (not misc.isList(value)) else '\n'.join(value)
            for key,value in self.iteritems():
                if (key not in ['settings','comments']):
                    for alias in self.__unique__(value):
                        print >> hostsFile, '{destination}\t{aliases}'.format(destination=key, aliases=alias)
            hostsFile.flush()
            hostsFile.close()
        except IOError, ex:
            print 'An error occured while trying to write the file:\n{path}\n\nError {message}\n\nWindows Vista/7 users:\nIf enabled, UAC prevents alterations to this file or location.\n\nConsider making a backup file in a different location.'.format(path=path, message=ex.message)
            print _utils.formattedException(details=ex)
        except Exception, ex:
            print 'Unexpected error:\n{info}'.format(info=sys.exc_info()[0])
            print _utils.formattedException(details=ex)
        return

    def invert(self):
        d = HashedUniqueLists()
        for key,value in self.iteritems():
            if (key not in ['settings','comments']):
                for alias in self.__unique__(value):
                    d[key] = alias
        return d.invert()

    def has_domains(self,regex=None):
        '''re can be None or a String that defines a regex or an actual regex object.
        '''
        if (regex is None):
            return []
        __re__ = re.compile(regex) if (misc.isString(regex)) else regex if (misc.isRePattern(regex)) else None
        if (not misc.isRePattern(__re__)):
            return []
        values = []
        d = self.invert()
        for key,value in d.iteritems():
            if (__re__.match(key)):
                values.append(key)
        values = list(set(values))
        return values

    def has_domain(self,regex=None):
        '''re can be None or a String that defines a regex or an actual regex object.
        '''
        values = self.has_domains(regex=regex)
        return len(values) > 0
    
    def add_domain(self,domain,ip=__localhost__):
        if (not self.has_domain(regex=domain)):
            self[ip] = domain

    def add_domain_and_save(self,domain,ip=__localhost__):
        self.add_domain(domain,ip=ip)
        self.save()
    
    def clone_without_domains(self):
        d = WindowsHosts()
        d['comments'] = self['comments']
        if (self.settings is not None):
            d.settings = self.settings
        return d

    def remove_domains(self,regex=None):
        '''re can be None or a String that defines a regex or an actual regex object.
        Does not auto-save...
        '''
        if (regex is None):
            return []
        __re__ = re.compile(regex) if (misc.isString(regex)) else regex if (misc.isRePattern(regex)) else None
        if (not misc.isRePattern(__re__)):
            return []
        d = self.invert()
        values = []
        for key,value in d.iteritems():
            if (__re__.match(key)):
                for v in value:
                    values.append(v)
                del d[key]
        values = list(set(values))
        for value in values:
            del self[value]
        for key,value in d.iteritems():
            for v in value:
                self[v] = key

    def save(self):
        self.__writeHosts__()
