import os
import sys
import re
from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.classes import SmartObject
from vyperlogix.classes.CooperativeClass import Cooperative

from vyperlogix.hash.lists import HashedLists,HashedFuzzyLists2

__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

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

_value_ = lambda val,_is_,default:val if (_is_(val)) else default

_bool_ = lambda val:_value_(val, lambda val:misc.isBooleanString(str(val)), False)
_bool_true_ = lambda val:_value_(val, lambda value:(value == 1) or (value == '1') or (value == 'true') or (value == 'T') or (value == 'True'), False)
_int_ = lambda val:_value_(val, misc.isInteger, -1)
_str_ = lambda val:_value_(val, misc.isString, None)
_file_ = lambda val:_value_(val, misc.isValidFile, None)
_dict_ = lambda val:_value_(val, misc.isDict, {})

def ppArgs(self):
    from vyperlogix.misc import PrettyPrint
    
    pArgs = [(k,self.args[k]) for k in self.args.keys()]
    pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
    pPretty.pprint()

class Args(Cooperative):
    def __init__(self,args,as_list=False):
        self.args = lists.HashedLists2(args) if (isinstance(args,dict)) else args
        self.dArgs = lists.HashedLists2()
        self.arguments = lists.HashedLists2()
        self.dValues = lists.HashedLists2()
        self.booleans = lists.HashedLists2()
        self.programName = sys.argv[0].split(os.sep)[-1]
        self._programName = (self.programName.split('.'))[0]
        self.__vars__ = SmartObject.SmartFuzzyObject()
	self.__as_list = as_list
        for k,v in self.args.iteritems():
            toks = k.split('=')
            if ( (len(toks) == 2) or (k.endswith('=')) ):
                self.arguments[toks[0].lower()] = ''
                self.dArgs[toks[0].lower()] = toks[-1]
		v = self.__listify_value(v)
                self.dValues[toks[0].lower()] = v
            else:
                self.arguments['is'+toks[0].replace('--','').title()] = ''
        for arg in sys.argv[1:]:
            toks = arg.split('=')
            if ( (len(toks) >= 2) or (arg.endswith('=')) ):
                # Arguments...
		normalize = lambda item,reObj:[t for t in reObj.findall(item) if (len(t) > 0) and (len(t[0]) > 0) and (len(t[-1]) > 0)]
		_is_usable = lambda items:all([(len(i) == 2) for i in items])
		is_usable = lambda items,reObj:_is_usable(normalize(items,reObj))
		if (len(toks) > 2):
		    toks[1] = '='.join(toks[1:])
		    del toks[2:]
		    _d_ = HashedLists()
		    _re = re.compile(r"(?P<token>\D*)(?P<value>\d*)")
		    from urlparse import urlparse
		    url = urlparse('http://a.b.c'+toks[-1])  # fake-up a URL to get the parms parsed
		    params = HashedFuzzyLists2(dict([t.split('=') for t in url[4].split('&')]))
		    for k,v in params.iteritems():
			matches = normalize(k,_re)
			if (_is_usable(matches)):
			    for m in matches:
				_bag_ = _d_[m[-1]]
				if (_bag_):
				    misc.unpack(_bag_)[m[0]] = v
				    continue
				else:
				    _d_[m[-1]] = m[0]
				    _bag_ = _d_[m[-1]]
				_bag_[0] = {misc.unpack(_bag_[0]):v}
				del _d_[m[-1]]
				_d_[m[-1]] = misc.unpack(_bag_)
		    for k,v in _d_.iteritems():
			del _d_[k]
			_d_[k] = HashedFuzzyLists2(misc.unpack(v))
		    toks[-1] = _d_
                argName = self.stripBeginningNonAlphaNumericsFrom(toks[0]).lower()
                self.arguments[argName] = toks[-1]
		_is_digits_ = str(self.arguments[argName]).isdigit()
		_is_floating_digits_ = _utils.is_floating_digits(str(self.arguments[argName]))
		try:
		    self.__vars__[argName] = self.__listify_value(self.arguments[argName],as_list=self.__as_list) if (not _is_digits_) and (not _is_floating_digits_) else int(str(self.arguments[argName])) if (_is_digits_) else float(str(self.arguments[argName]))
		except Exception, ex:
		    print 'ERROR: [%s] %s' % (self.arguments[argName],_utils.formattedException(details=ex))
            else:
                # Booleans...
                argName = 'is'+self.upperCaseLikeTitle(toks[0].replace('--',''))
                self.booleans[argName] = True
                self.__vars__[argName] = True

    def __listify_value(self,value,as_list=False):
	if (not misc.isString(value)):
	    return value
	import re
	_re = re.compile(r"\[(?P<value>.*)\]")
	result = _re.findall(value)
	if (len(result) == 0):
	    result = [value]
	toks = []
	if (isinstance(result, str)) and (len(result) > 0):
	    try:
		toks = [f[0].replace('[','').replace(']','') for f in result.split(',') if (len(f) > 0)]
	    except Exception, ex:
		print 'ERROR: result=%s, %s' % (result, _utils.formattedException(details=ex))
		toks = []
	if (as_list):
	    return toks
	return '[%s]' % ','.join(['"%s"' % (t) for t in toks])
    
    def upperCaseLikeTitle(self,s):
        if (len(s) < 2):
            return s[0].upper()
        return s[0].upper()+s[1:]

    def stripBeginningNonAlphaNumericsFrom(self,s):
        while ( (len(s) > 0) and (not s[0].isalpha()) and (not s[0].isdigit()) ):
            s = s[1:]
        return s

    def __repr__(self):
        return 'Args for "%s"\n\t%s\n\t%s' % (self.programName,str(self.arguments),str(self.booleans))

    def vars():
        doc = "vars - the variables for the various options being tested."
        def fget(self):
            return self.__vars__
        return locals()
    vars = property(**vars())

class SmartArgs(Args):
    def __init__(self,args):
	self.__named_argument_or_else = lambda name,default:self.arguments[name] if self.arguments.has_key(name) else default
	self.__normalize_option_name = lambda name:name.split('--')[-1]
	self.__normalize_boolean_name = lambda name:'is'+self.__normalize_option_name(str(name)).capitalize()
	self.__named_boolean_or_else = lambda name,default:self.booleans[self.__normalize_boolean_name(name)] if self.booleans.has_key(self.__normalize_boolean_name(name)) else default
        self.__make_key__ = lambda key:'_'+str(key)
        super(SmartArgs, self).__init__(args,as_list=True)
	self.progName = self.programName
	self.progID = os.path.splitext(self.programName)[0]
	for k,v in args.iteritems():
	    toks = k.split('=')
	    if (len(toks) > 1):
		toks[0] = toks[0].split('--')[-1]
		self[toks[0]] = ''
		try:
		    self[toks[0]] = self.__named_argument_or_else(toks[0],self[toks[0]])
		except Exception, e:
		    info_string = _utils.formattedException(details=e)
		    print >>sys.stderr, info_string
	    else:
		_k_ = self.__normalize_boolean_name(k)
		self[_k_] = False
		try:
		    self[_k_] = self.__named_boolean_or_else(k,self[_k_])
		except Exception, e:
		    info_string = _utils.formattedException(details=e)
		    print >>sys.stderr, info_string
		    self[_k_] = False
	pass

    def get_var(self, name,_type,_default,is_filter=False):
	value = self.__vars__[name]
	value = value[0] if (misc.isList(value)) and (len(value) > 0) else value
	isEmpty = lambda val:val in ['', None, [], 'none', 'None', 'null', 'nil']
	def underbar_value(_name_):
	    _name = '_%s'%(name)
	    value = None
	    if (self.__dict__.has_key(_name)):
		value = self.__dict__[_name]
	    return  value
	while (1):
	    if (not isEmpty(value)):
		try:
		    if (not is_filter):
			if (callable(_type)):
			    return _type(value)
			elif (isinstance(value,_type)):
			    return value
		    else:
			if (callable(_type)):
			    return _type(value)
			elif (isinstance(value,_type)):
			    return value
		except TypeError:
		    value = underbar_value(name)
		    return value
	    else:
		value = underbar_value(name)
		return value if (not isEmpty(value)) else _default
	return _default
    
    def __delitem__(self, key):
        _key = self.__make_key__(key)
        del self.__dict__[_key]

    def __getitem__(self, key):
        _key = self.__make_key__(key)
        return self.__dict__[_key] if (self.__dict__.has_key(_key)) else None

    def __setitem__(self, key, value):
        _key = self.__make_key__(key)
        if (self.__dict__.has_key(_key)) and (value == None):
            self.__delitem__(_key)
        elif (value != None):
            self.__dict__[_key] = value

