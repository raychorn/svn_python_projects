__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import logging

import urllib2

import simplejson

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.classes import MagicObject

arg0 = lambda args:args[0] if (misc.isIterable(args)) and (len(args) > 0) and (misc.isString(args[0])) else None
list0 = lambda args:args[0] if (misc.isIterable(args)) and (len(args) > 0) and ( (misc.isList(args[0])) or (misc.isDict(args[0])) ) else []
int0 = lambda args:args[0] if (misc.isIterable(args)) and (len(args) > 0) and (misc.isInteger(args[0])) else None
bool0 = lambda args:args[0] if (misc.isIterable(args)) and (len(args) > 0) and (misc.isBooleanString(args[0])) else None

__only__ = lambda value,target:value if (str(value).lower().capitalize() == str(target).lower().capitalize()) else None

class SleepyMongoose(MagicObject.MagicObject2):
    def __init__(self,sleepy_mongoose):
        '''
        See also: https://github.com/kchodorow/sleepy.mongoose/wiki/
        '''
        toks = sleepy_mongoose.split(':')
        try:
            self.__sleepy_mongoose__ = sleepy_mongoose if (misc.isString(toks[0]) and misc.isInteger(int(toks[-1]))) else None
        except:
            self.__sleepy_mongoose__ = None
        self.__database__ = None
        self.__collection__ = None
        self.__server__ = None
        self.__server_name__ = None
        self.__last_exception__ = None
        self.__n__ = None
        self.__docs__ = None
        self.__criteria__ = None
        self.__newobj__ = None
        self.__fields__ = None
        self.__sort__ = None
        self.__skip__ = None
        self.__limit__ = None
        self.__explain__ = None
        self.__batch_size__ = None
        self.__id__ = None
        
    def __http_gets__(self,url,parms=[]):
        data = None
        try:
            q = ''
            if (misc.isList(parms)) and (len(parms) > 0):
                q = '?'+'&'.join(['%s=%s' % (p[0],urllib2.quote(p[-1])) for p in parms]) if (len(parms) > 0) else ''
            response = urllib2.urlopen(url+q)
            data = response.read()
        except Exception, ex:
            self.__last_exception__ = _utils.formattedException(details=ex)
            data = None
        return data

    def __http_get__(self,url,parms=[]):
        data = None
        try:
            json = self.__http_gets__(url,parms=parms)
            data = simplejson.loads(json)
        except Exception, ex:
            self.__last_exception__ = _utils.formattedException(details=ex)
            data = None
        return data

    def __http_post__(self,url,parms=()):
        from vyperlogix.url._urllib2 import http_post
        data = None
        try:
            json = http_post(url,parms)
            data = simplejson.loads(json if (json) else '')
        except Exception, ex:
            self.__last_exception__ = _utils.formattedException(details=ex)
            data = None
        return data

    def __handle_exceptions__(self):
        if (not self.__sleepy_mongoose__):
            logging.error('ERROR: Cannot understand "SleepyMongoose(%s)"' % (self.__sleepy_mongoose__))
        elif (not self.__database__):
            logging.error('ERROR: Cannot understand "db(%s)"' % (self.__database__))
        elif (not self.__collection__):
            logging.error('ERROR: Cannot understand "collection(%s)"' % (self.__collection__))
    
    def __getattr__(self,name):
        self.__n__ = name
        return super(SleepyMongoose, self).__getattr__(name)

    def __call__(self,*args,**kwargs):
        if (self.__n__ == 'db'):
            self.__database__ = arg0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'collection'):
            self.__collection__ = arg0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'server'):
            self.__server__ = arg0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'name'):
            self.__server_name__ = arg0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'docs'):
            self.__docs__ = list0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'criteria'):
            self.__criteria__ = list0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'fields'):
            self.__fields__ = list0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'sort'):
            self.__sort__ = list0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'skip'):
            self.__skip__ = int0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'limit'):
            self.__limit__ = int0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'batch_size'):
            self.__batch_size__ = int0(args)
            self.__reset_magic__()
        elif (self.__id__ == 'id'):
            self.__id__ = int0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'explain'):
            self.__explain__ = __only__(bool0(args),'True')
            self.__reset_magic__()
        elif (self.__n__ == 'newobj'):
            self.__newobj__ = list0(args)
            self.__reset_magic__()
        elif (self.__n__ == 'find'):
            if (self.__sleepy_mongoose__) and (self.__database__) and (self.__collection__):
                p = []
                if (self.__criteria__):
                    p.append(tuple(["criteria",simplejson.dumps(self.__criteria__)]))
                    self.__criteria__ = None
                elif (len(args) > 0):
                    p.append(tuple(["criteria",simplejson.dumps(list0(args))]))
                if (self.__fields__):
                    p.append(tuple(["fields",simplejson.dumps(self.__fields__)]))
                    self.__fields__ = None
                if (self.__sort__):
                    p.append(tuple(["sort",simplejson.dumps(self.__sort__)]))
                    self.__sort__ = None
                if (self.__skip__):
                    p.append(tuple(["skip",'%d'%(self.__skip__)]))
                    self.__skip__ = None
                if (self.__limit__):
                    p.append(tuple(["limit",'%d'%(self.__limit__)]))
                    self.__limit__ = None
                if (self.__explain__):
                    p.append(tuple(["explain",'%s'%(self.__explain__)]))
                    self.__explain__ = None
                if (self.__batch_size__):
                    p.append(tuple(["batch_size",'%d'%(self.__batch_size__)]))
                    self.__batch_size__ = None
                if (self.__server_name__):
                    p.append(tuple(["name",self.__server_name__]))
                url = 'http://%s/%s/%s/_%s' % (self.__sleepy_mongoose__,self.__database__,self.__collection__,self.__n__)
                return self.__http_get__(url,parms=p)
            else:
                self.__handle_exceptions__()
            self.__reset_magic__()
        elif (self.__n__ == 'insert'):
            if (self.__sleepy_mongoose__) and (self.__database__) and (self.__collection__):
                p = []
                if (self.__docs__):
                    p.append(tuple(["docs",simplejson.dumps(self.__docs__)]))
                    self.__docs__ = None
                else:
                    p.append(tuple(["docs",simplejson.dumps(list0(args))]))
                    self.__docs__ = None
                if (self.__server_name__):
                    p.append(tuple(["name",self.__server_name__]))
                url = 'http://%s/%s/%s/_%s' % (self.__sleepy_mongoose__,self.__database__,self.__collection__,self.__n__)
                return self.__http_post__(url,tuple(p))
            else:
                self.__handle_exceptions__()
            self.__reset_magic__()
        elif (self.__n__ == 'update'):
            if (self.__sleepy_mongoose__) and (self.__database__) and (self.__collection__):
                p = []
                if (self.__criteria__):
                    p.append(tuple(["criteria",simplejson.dumps(self.__criteria__)]))
                    self.__criteria__ = None
                if (self.__newobj__):
                    p.append(tuple(["newobj",simplejson.dumps(self.__newobj__)]))
                    self.__newobj__ = None
                if (self.__server_name__):
                    p.append(tuple(["name",self.__server_name__]))
                url = 'http://%s/%s/%s/_%s' % (self.__sleepy_mongoose__,self.__database__,self.__collection__,self.__n__)
                return self.__http_post__(url,tuple(p))
            else:
                self.__handle_exceptions__()
            self.__reset_magic__()
        elif (self.__n__ == 'more'):
            if (self.__sleepy_mongoose__) and (self.__database__) and (self.__collection__):
                p = []
                if (self.__id__):
                    p.append(tuple(["id",'%d'%(self.__id__)]))
                    self.__id__ = None
                if (self.__batch_size__):
                    p.append(tuple(["batch_size",'%d'%(self.__batch_size__)]))
                    self.__batch_size__ = None
                if (self.__server_name__):
                    p.append(tuple(["name",self.__server_name__]))
                url = 'http://%s/%s/%s/_%s' % (self.__sleepy_mongoose__,self.__database__,self.__collection__,self.__n__)
                return self.__http_get__(url,parms=p)
            else:
                self.__handle_exceptions__()
            self.__reset_magic__()
        elif (self.__n__ == 'cmd'):
            if (self.__sleepy_mongoose__) and (self.__database__):
                p = []
                _c_ = list0(args)
                if (_c_):
                    p.append(tuple(["cmd",simplejson.dumps(_c_)]))
                url = 'http://%s/%s/_%s' % (self.__sleepy_mongoose__,self.__database__,self.__n__)
                return self.__http_post__(url,tuple(p))
            else:
                self.__handle_exceptions__()
            self.__reset_magic__()
        elif (self.__n__ == 'remove'):
            if (self.__sleepy_mongoose__) and (self.__database__) and (self.__collection__):
                p = []
                if (self.__criteria____):
                    p.append(tuple(["criteria",simplejson.dumps(self.__criteria____)]))
                    self.__criteria____ = None
                else:
                    p.append(tuple(["criteria",simplejson.dumps(list0(args))]))
                    self.__criteria____ = None
                if (self.__server_name__):
                    p.append(tuple(["name",self.__server_name__]))
                url = 'http://%s/%s/%s/_%s' % (self.__sleepy_mongoose__,self.__database__,self.__collection__,self.__n__)
                return self.__http_post__(url,tuple(p))
            else:
                self.__handle_exceptions__()
            self.__reset_magic__()
        elif (self.__n__ == 'connect'):
            _token = self.__n__
            if (self.__sleepy_mongoose__):
                p = []
                if (self.__server__):
                    p.append(tuple(["server",self.__server__]))
                if (self.__server_name__):
                    p.append(tuple(["name",self.__server_name__]))
                url = 'http://%s/_%s' % (self.__sleepy_mongoose__,_token)
                return self.__http_post__(url,tuple(p))
            else:
                self.__handle_exceptions__()
            self.__reset_magic__()
        else:
            logging.debug('DEBUG: Cannot understand "%s(%s,%s)"' % (self.n,args,kwargs))
        return self
