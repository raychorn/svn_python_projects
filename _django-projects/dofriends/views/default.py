from django import http
from django.template.loader import get_template, render_to_string
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.template import loader
from django.template import Context

import os, sys

import mimetypes

from vyperlogix.django import django_utils

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.js import minify

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import django_utils
from vyperlogix.django import captcha

from vyperlogix.products import keys

from vyperlogix.django.rss import content as rss_content

from models import User, UserActivity, Country

from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.django import forms
from vyperlogix.django.forms import form_as_html

from vyperlogix.crypto import md5
from vyperlogix.misc import GenPasswd

import login

import urllib

__content__ = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"><title>VyperCMS v2.0 ERROR</title></head><body>{{ content }}</body></html>'''

__development__ = ['127.0.0.1:8888']

_template_21 = '21'
_template_new = 'new'

_title = 'DoFriends&trade;&nbsp;&copy;DoFriends.Com&nbsp;All&nbsp;Rights&nbsp;Reserved.'

_root_ = os.path.dirname(__file__)

def render_static_html(request,_title,template_name,template_folder='',context={}):
    return pages._render_the_template(request,_title,template_name,context=context,template_folder=template_folder)

def get_freehost_by_name(domain_name):
    import sqlalchemy_models
    return sqlalchemy_models.get_freehost_by_name(domain_name)
    
def _form_for_model(form, context={}):
    from vyperlogix.classes.SmartObject import SmartObject
    f = form
    if (f.form_name == 'register'):
	f.fields['firstname'].min_length = 2
	f.fields['firstname'].required = True
	f.fields['lastname'].min_length = 2
	f.fields['lastname'].required = True
	f.fields['email_address'].required = True
	f.fields['email_address'].max_length = 128
	f.fields['phone_number'].max_length = 20
	f.fields['phone_number'].min_length = 12
	for k,v in f.fields.iteritems():
	    if (k not in ['firstname', 'lastname', 'email_address']):
		v.required = False
	f.fields['state'].required = True
	f.fields['country'].required = True

	f.set_choice_model_for_field_by_name('state',SmartObject({'value_id':'abbrev','text_id':'name'}))
	f.set_choice_model_for_field_by_name('country',SmartObject({'value_id':'iso3','text_id':'printable_name'}))
	
	f.set_choice_model_default_for_field_by_name('state',context['VALUE_STATE'] if (context.has_key('VALUE_STATE')) else '')
	f.set_choice_model_default_for_field_by_name('country',context['VALUE_COUNTRY'] if (context.has_key('VALUE_COUNTRY')) else '')

	validation_condition = lambda self:((len(self.fields['state'].value) == 0) and (self.fields['country'].value == 'USA')) or ((len(self.fields['state'].value) > 0) and (self.fields['country'].value != 'USA'))
	validation_message = 'Either the State or Country is invalid.'
	validation_tuple = tuple([validation_condition,{'STATE':validation_message,'COUNTRY':validation_message}])
	f.field_validation = validation_tuple

def send_registration_email(email_address, product_name, product_link, site_link):
    t_EULA = get_template('pyEggs_EULA.txt')
    EULA_context = {'PRODUCT_NAME':product_name, 'COMPANY_NAME':'Vyper Logix Corp.'}
    EULA_content = t_EULA.render(Context(EULA_context))

    t_content = get_template('pyEggs_Registration_Email.txt')
    msg_context = {'PRODUCT_NAME':product_name, 'PRODUCT_LINK':product_link, 'SITE_LINK':site_link, 'EULA':EULA_content}
    msg_content = t_content.render(Context(msg_context))

    try:
	from vyperlogix.mail.mailServer import GMailServer
	from vyperlogix.mail.message import Message
	msg = Message('support@vyperlogix.com', email_address if (not _utils.isBeingDebugged) else keys._decode('72617963686F726E40686F746D61696C2E636F6D'), msg_content, subject="We have received your %s Registration Request." % (product_name))
	smtp = GMailServer('investors@vyperlogix.com', keys._decode('7065656B61623030'), server='smtpout.secureserver.net', port=3535)
	smtp.sendEmail(msg)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	pass

    return msg_context

def send_activation_email(email_address, password):
    t = get_template('pyEggs_Activation_Email.txt')
    c = {'PRODUCT_PASSWORD':password}
    content = t.render(Context(c))

    try:
	from vyperlogix.mail.mailServer import GMailServer
	from vyperlogix.mail.message import Message
	msg = Message('support@vyperlogix.com', email_address if (not _utils.isBeingDebugged) else keys._decode('72617963686F726E40686F746D61696C2E636F6D'), content, subject="This is your pyEggs Account Password.")
	smtp = GMailServer('investors@vyperlogix.com', keys._decode('7065656B61623030'), server='smtpout.secureserver.net', port=3535)
	smtp.sendEmail(msg)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	pass

def on_successful_registration(form,request):
    emailField = form.email_fields[0]
    email_address = emailField.value
    html_context = send_registration_email(email_address, 'pyEggs Online (www.pyeggs.com)', 'http://%spyeggs/registration/activate/%s' % (django_utils.get_fully_qualified_http_host(request),keys._encode('%s' % (email_address))), 'http://%s' % (django_utils.get_fully_qualified_http_host(request)))
    t_content = get_template('_pyeggs_registered.html')
    if (html_context.has_key('EULA')):
	html_context['EULA'] = oohtml.render_BR().join(html_context['EULA'].split('\n'))
    return html_context

def on_unsuccessful_registration(form,context):
    return form_as_html.form_as_html(form,callback=_form_for_model,context=context)

def on_before_form_save(form,request,obj):
    # This could be used to pre-assign a password however the password should be assigned when the Account is activated.
    pass

def on_registration_form_error(form,request):
    try:
	from vyperlogix.mail.mailServer import GMailServer
	from vyperlogix.mail.message import Message
	msg = Message('support@vyperlogix.com', keys._decode('72617963686F726E40686F746D61696C2E636F6D'), form.last_error, subject="ERROR: Registration Request (%s)" % (django_utils.get_fully_qualified_http_host(request)))
	smtp = GMailServer('investors@vyperlogix.com', keys._decode('7065656B61623030'), server='smtpout.secureserver.net', port=3535)
	smtp.sendEmail(msg)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	pass

_scripts_loginHead = '''
var const_inline_style = 'inline';
var const_none_style = 'none';
var const_block_style = 'block';
var const_hidden_style = 'hidden';
var const_visible_style = 'visible';

var const_absolute_style = 'absolute';
var const_relative_style = 'relative';

var $cache = [];

var const_function_symbol = 'function';

var const_object_symbol = 'object';
var const_number_symbol = 'number';
var const_string_symbol = 'string';

var const_debug_symbol = 'DEBUG';
var const_error_symbol = 'ERROR';

var const_simpler_symbol = 'simpler';

function $(id, fromObj) {
	var obj = null;
	
	function usingGetElementById(id, fromObj) {
		return ((typeof fromObj.getElementById == const_function_symbol) ? fromObj.getElementById(id) : null);
	};
	
	function usingAll(id, fromObj) {
		return ((fromObj.all) ? fromObj.all[id] : null);
	};
	
	function usingLayers(id, fromObj) {
		return ((fromObj.layers) ? fromObj.layers[id] : null);
	};
	
	if (typeof id == const_string_symbol) {
		try { obj = usingGetElementById(id, fromObj); } catch(e) { obj = null; };
		if (obj == null) {
			try { obj = usingAll(id, fromObj); } catch(e) { obj = null; };
			if (obj == null) {
				try { obj = usingLayers(id, fromObj); } catch(e) { obj = null; };
			}
		}
	}
	return obj;
}

var bool_ezObjectExplainer_insideObject_stack = [];
var bool_ezObjectExplainer_insideObject_cache = [];

function ezObjectExplainer(obj, bool_includeFuncs) {
	var _db = '';
	var m = -1;
	var i = -1;
	var a = [];
	bool_includeFuncs = ((bool_includeFuncs == true) ? bool_includeFuncs : false);
	
	_db = '';
	if (obj) {
       	s_obj = obj.toString;
       	t_obj = typeof obj;
		if ( (s_obj != null) && ((t_obj.toString) == const_function_symbol) && (s_obj.toString().toLowerCase().indexOf('[native code]') == -1) ) {
			_db += obj.toString();
		} else {
			if ( (obj != null) && ((typeof obj) == const_object_symbol) ) {
				if (obj.length != null) {
				    for (i = 0; i < obj.length; i++) {
						if ( ( (bool_includeFuncs) && ((typeof obj[i]) == const_function_symbol) ) || ( (!bool_includeFuncs) && ((typeof obj[i]) != const_function_symbol) ) ) {
							a.push('[' + obj[i] + ']');
						}
				    }
				} else {
					for (m in obj) {
						if (obj[m]) {
							if ((typeof obj[m]) == const_object_symbol) {
								a.push(m + ' = [' + ((obj[m]) ? obj[m].toString() : 'null') + ']');
							} else if ( ( (bool_includeFuncs) && ((typeof obj[m]) == const_function_symbol) ) || ( (!bool_includeFuncs) && ((typeof obj[m]) != const_function_symbol) ) ) {
								a.push(m + ' = [' + obj[m] + ']');
							}
						}
					}
				}
				_db += a.join(', ');
			} else if ( ( (bool_includeFuncs) && ((typeof obj) == const_function_symbol) ) || ( (!bool_includeFuncs) && ((typeof obj) != const_function_symbol) ) ) {
				_db += obj + '\\n';
			}
		}
	}
	return _db;
}

/*
 * A JavaScript implementation of the RSA Data Security, Inc. MD5 Message
 * Digest Algorithm, as defined in RFC 1321.
 * Version 2.1 Copyright (C) Paul Johnston 1999 - 2002.
 * Other contributors: Greg Holt, Andrew Kepert, Ydnar, Lostinet
 * Distributed under the BSD License
 * See http://pajhome.org.uk/crypt/md5 for more info.
 */

/*
 * Configurable variables. You may need to tweak these to be compatible with
 * the server-side, but the defaults work in most cases.
 */
var hexcase = 0;  /* hex output format. 0 - lowercase; 1 - uppercase        */
var b64pad  = ""; /* base-64 pad character. "=" for strict RFC compliance   */
var chrsz   = 8;  /* bits per input character. 8 - ASCII; 16 - Unicode      */

/*
 * These are the functions you'll usually want to call
 * They take string arguments and return either hex or base-64 encoded strings
 */
function hex_md5(s){ return binl2hex(core_md5(str2binl(s), s.length * chrsz));}
function b64_md5(s){ return binl2b64(core_md5(str2binl(s), s.length * chrsz));}
function str_md5(s){ return binl2str(core_md5(str2binl(s), s.length * chrsz));}
function hex_hmac_md5(key, data) { return binl2hex(core_hmac_md5(key, data)); }
function b64_hmac_md5(key, data) { return binl2b64(core_hmac_md5(key, data)); }
function str_hmac_md5(key, data) { return binl2str(core_hmac_md5(key, data)); }

/*
 * Perform a simple self-test to see if the VM is working
 */
function md5_vm_test()
{
  return hex_md5("abc") == "900150983cd24fb0d6963f7d28e17f72";
}

/*
 * Calculate the MD5 of an array of little-endian words, and a bit length
 */
function core_md5(x, len)
{
  /* append padding */
  x[len >> 5] |= 0x80 << ((len) % 32);
  x[(((len + 64) >>> 9) << 4) + 14] = len;

  var a =  1732584193;
  var b = -271733879;
  var c = -1732584194;
  var d =  271733878;

  for(var i = 0; i < x.length; i += 16)
  {
    var olda = a;
    var oldb = b;
    var oldc = c;
    var oldd = d;

    a = md5_ff(a, b, c, d, x[i+ 0], 7 , -680876936);
    d = md5_ff(d, a, b, c, x[i+ 1], 12, -389564586);
    c = md5_ff(c, d, a, b, x[i+ 2], 17,  606105819);
    b = md5_ff(b, c, d, a, x[i+ 3], 22, -1044525330);
    a = md5_ff(a, b, c, d, x[i+ 4], 7 , -176418897);
    d = md5_ff(d, a, b, c, x[i+ 5], 12,  1200080426);
    c = md5_ff(c, d, a, b, x[i+ 6], 17, -1473231341);
    b = md5_ff(b, c, d, a, x[i+ 7], 22, -45705983);
    a = md5_ff(a, b, c, d, x[i+ 8], 7 ,  1770035416);
    d = md5_ff(d, a, b, c, x[i+ 9], 12, -1958414417);
    c = md5_ff(c, d, a, b, x[i+10], 17, -42063);
    b = md5_ff(b, c, d, a, x[i+11], 22, -1990404162);
    a = md5_ff(a, b, c, d, x[i+12], 7 ,  1804603682);
    d = md5_ff(d, a, b, c, x[i+13], 12, -40341101);
    c = md5_ff(c, d, a, b, x[i+14], 17, -1502002290);
    b = md5_ff(b, c, d, a, x[i+15], 22,  1236535329);

    a = md5_gg(a, b, c, d, x[i+ 1], 5 , -165796510);
    d = md5_gg(d, a, b, c, x[i+ 6], 9 , -1069501632);
    c = md5_gg(c, d, a, b, x[i+11], 14,  643717713);
    b = md5_gg(b, c, d, a, x[i+ 0], 20, -373897302);
    a = md5_gg(a, b, c, d, x[i+ 5], 5 , -701558691);
    d = md5_gg(d, a, b, c, x[i+10], 9 ,  38016083);
    c = md5_gg(c, d, a, b, x[i+15], 14, -660478335);
    b = md5_gg(b, c, d, a, x[i+ 4], 20, -405537848);
    a = md5_gg(a, b, c, d, x[i+ 9], 5 ,  568446438);
    d = md5_gg(d, a, b, c, x[i+14], 9 , -1019803690);
    c = md5_gg(c, d, a, b, x[i+ 3], 14, -187363961);
    b = md5_gg(b, c, d, a, x[i+ 8], 20,  1163531501);
    a = md5_gg(a, b, c, d, x[i+13], 5 , -1444681467);
    d = md5_gg(d, a, b, c, x[i+ 2], 9 , -51403784);
    c = md5_gg(c, d, a, b, x[i+ 7], 14,  1735328473);
    b = md5_gg(b, c, d, a, x[i+12], 20, -1926607734);

    a = md5_hh(a, b, c, d, x[i+ 5], 4 , -378558);
    d = md5_hh(d, a, b, c, x[i+ 8], 11, -2022574463);
    c = md5_hh(c, d, a, b, x[i+11], 16,  1839030562);
    b = md5_hh(b, c, d, a, x[i+14], 23, -35309556);
    a = md5_hh(a, b, c, d, x[i+ 1], 4 , -1530992060);
    d = md5_hh(d, a, b, c, x[i+ 4], 11,  1272893353);
    c = md5_hh(c, d, a, b, x[i+ 7], 16, -155497632);
    b = md5_hh(b, c, d, a, x[i+10], 23, -1094730640);
    a = md5_hh(a, b, c, d, x[i+13], 4 ,  681279174);
    d = md5_hh(d, a, b, c, x[i+ 0], 11, -358537222);
    c = md5_hh(c, d, a, b, x[i+ 3], 16, -722521979);
    b = md5_hh(b, c, d, a, x[i+ 6], 23,  76029189);
    a = md5_hh(a, b, c, d, x[i+ 9], 4 , -640364487);
    d = md5_hh(d, a, b, c, x[i+12], 11, -421815835);
    c = md5_hh(c, d, a, b, x[i+15], 16,  530742520);
    b = md5_hh(b, c, d, a, x[i+ 2], 23, -995338651);

    a = md5_ii(a, b, c, d, x[i+ 0], 6 , -198630844);
    d = md5_ii(d, a, b, c, x[i+ 7], 10,  1126891415);
    c = md5_ii(c, d, a, b, x[i+14], 15, -1416354905);
    b = md5_ii(b, c, d, a, x[i+ 5], 21, -57434055);
    a = md5_ii(a, b, c, d, x[i+12], 6 ,  1700485571);
    d = md5_ii(d, a, b, c, x[i+ 3], 10, -1894986606);
    c = md5_ii(c, d, a, b, x[i+10], 15, -1051523);
    b = md5_ii(b, c, d, a, x[i+ 1], 21, -2054922799);
    a = md5_ii(a, b, c, d, x[i+ 8], 6 ,  1873313359);
    d = md5_ii(d, a, b, c, x[i+15], 10, -30611744);
    c = md5_ii(c, d, a, b, x[i+ 6], 15, -1560198380);
    b = md5_ii(b, c, d, a, x[i+13], 21,  1309151649);
    a = md5_ii(a, b, c, d, x[i+ 4], 6 , -145523070);
    d = md5_ii(d, a, b, c, x[i+11], 10, -1120210379);
    c = md5_ii(c, d, a, b, x[i+ 2], 15,  718787259);
    b = md5_ii(b, c, d, a, x[i+ 9], 21, -343485551);

    a = safe_add(a, olda);
    b = safe_add(b, oldb);
    c = safe_add(c, oldc);
    d = safe_add(d, oldd);
  }
  return Array(a, b, c, d);

}

/*
 * These functions implement the four basic operations the algorithm uses.
 */
function md5_cmn(q, a, b, x, s, t)
{
  return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s),b);
}
function md5_ff(a, b, c, d, x, s, t)
{
  return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t);
}
function md5_gg(a, b, c, d, x, s, t)
{
  return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t);
}
function md5_hh(a, b, c, d, x, s, t)
{
  return md5_cmn(b ^ c ^ d, a, b, x, s, t);
}
function md5_ii(a, b, c, d, x, s, t)
{
  return md5_cmn(c ^ (b | (~d)), a, b, x, s, t);
}

/*
 * Calculate the HMAC-MD5, of a key and some data
 */
function core_hmac_md5(key, data)
{
  var bkey = str2binl(key);
  if(bkey.length > 16) bkey = core_md5(bkey, key.length * chrsz);

  var ipad = Array(16), opad = Array(16);
  for(var i = 0; i < 16; i++)
  {
    ipad[i] = bkey[i] ^ 0x36363636;
    opad[i] = bkey[i] ^ 0x5C5C5C5C;
  }

  var hash = core_md5(ipad.concat(str2binl(data)), 512 + data.length * chrsz);
  return core_md5(opad.concat(hash), 512 + 128);
}

/*
 * Add integers, wrapping at 2^32. This uses 16-bit operations internally
 * to work around bugs in some JS interpreters.
 */
function safe_add(x, y)
{
  var lsw = (x & 0xFFFF) + (y & 0xFFFF);
  var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
  return (msw << 16) | (lsw & 0xFFFF);
}

/*
 * Bitwise rotate a 32-bit number to the left.
 */
function bit_rol(num, cnt)
{
  return (num << cnt) | (num >>> (32 - cnt));
}

/*
 * Convert a string to an array of little-endian words
 * If chrsz is ASCII, characters >255 have their hi-byte silently ignored.
 */
function str2binl(str)
{
  var bin = Array();
  var mask = (1 << chrsz) - 1;
  for(var i = 0; i < str.length * chrsz; i += chrsz)
    bin[i>>5] |= (str.charCodeAt(i / chrsz) & mask) << (i%32);
  return bin;
}

/*
 * Convert an array of little-endian words to a string
 */
function binl2str(bin)
{
  var str = "";
  var mask = (1 << chrsz) - 1;
  for(var i = 0; i < bin.length * 32; i += chrsz)
    str += String.fromCharCode((bin[i>>5] >>> (i % 32)) & mask);
  return str;
}

/*
 * Convert an array of little-endian words to a hex string.
 */
function binl2hex(binarray)
{
  var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
  var str = "";
  for(var i = 0; i < binarray.length * 4; i++)
  {
    str += hex_tab.charAt((binarray[i>>2] >> ((i%4)*8+4)) & 0xF) +
           hex_tab.charAt((binarray[i>>2] >> ((i%4)*8  )) & 0xF);
  }
  return str;
}

/*
 * Convert an array of little-endian words to a base-64 string
 */
function binl2b64(binarray)
{
  var tab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  var str = "";
  for(var i = 0; i < binarray.length * 4; i += 3)
  {
    var triplet = (((binarray[i   >> 2] >> 8 * ( i   %4)) & 0xFF) << 16)
                | (((binarray[i+1 >> 2] >> 8 * ((i+1)%4)) & 0xFF) << 8 )
                |  ((binarray[i+2 >> 2] >> 8 * ((i+2)%4)) & 0xFF);
    for(var j = 0; j < 4; j++)
    {
      if(i * 8 + j * 6 > binarray.length * 32) str += b64pad;
      else str += tab.charAt((triplet >> 6*(3-j)) & 0x3F);
    }
  }
  return str;
}

function _onclick_login() {
    btn = $('id_btn_login', document);
    if (btn) {
        btn.disabled = true;
    }
    username = '';
    uid = $('id_username', document);
    if (uid) {
        username = uid.value;
    }
    pid = $('id_password', document);
    if (pid) {
        pid.value = hex_md5(pid.value);
	//toks = window.location.href.split('//');
	//toks2 = toks[toks.length-1].split('/');
	//toks2[toks2.length-1] = 'accepted';
	//toks[toks.length-1] = toks2.join('/');
	//url = toks.join('//') + '/' + username + '/' + msg;
        //alert(url);
	//window.location.href = url;
    }
}

function onkeydown_login_password(event) {
    if (event.keyCode == 13) { 
        _onclick_login();
    };
}

function onclick_login(event) {
    _onclick_login();
}

'''

_scripts_loginForm = '''
try {
    btn = $('id_btn_login', document);
    pid = $('id_password', document);
    if (pid) {
       pid.onkeydown = onkeydown_login_password;
    }
    if (btn) {
        btn.onclick = onclick_login;
    }
} catch (e) { }
'''

def get_login_attempts(request):
    try:
	return request.session.get('login_attempts', None)
    except:
	pass
    return None

def get_is_logged_in(request):
    try:
	return request.session.get('is_logged_in', False)
    except:
	pass
    return False

def get_current_user(request):
    try:
	return request.session.get('user', None)
    except:
	pass
    return None

def _default(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    
    _template_folder = _template_new # _template_21

    t_analytics = get_template('_google_analytics.html')
    _context = {'GOOGLE_ANALYTICS':t_analytics.render(Context({})),
		'TITLE':'%s - %s (%s)',
		'EXTRA_HEAD_ELEMENTS':'',
		'USER_STATUS':''
		}
    from django.conf import settings
    _settings = settings
    _default_context = {'MEDIA_URL':_settings.MEDIA_URL}
    sub_title = ''

    if (_template_folder == _template_new):
	_context['LOGIN_REGISTER_BUTTON'] = render_static_html(request,'','_log%s-button.html' % ('in' if (not get_is_logged_in(request)) else 'Out'),template_folder=_template_folder,context=_default_context)
	aUser = None
	if (get_is_logged_in(request)):
	    aUser = get_current_user(request)
	    _users_name = '%s %s' % (aUser.firstname,aUser.lastname)
	    _context['SALUTATION'] = 'Welcome back %s.<br/>Please %s if you are not %s.' % (_users_name,oohtml.renderAnchor('/logoff/','click here',target="_top"),_users_name)
	    anActivity = UserActivity(user=aUser,ip=django_utils.get_from_environ(request,'REMOTE_ADDR'),action='/'.join(url_toks))
	    anActivity.save()
	    if (len(url_toks) == 0) or (url_toks[0] != 'upgrade'):
		u_context['UPGRADE_BUTTON'] = render_static_html(request,'','_upgrade_button.html',template_folder=_template_folder,context=u_context)
	    _context['USER_STATUS'] = render_static_html(request,'','_user-status.html',template_folder=_template_folder,context=u_context)
	if (len(url_toks) == 0):
	    _context['PAGE_CONTENT'] = render_static_html(request,'','_home.html',template_folder=_template_folder,context=_default_context)
	elif (url_toks[0] == 'get-started'):
	    _context['PAGE_CONTENT'] = render_static_html(request,'','_get_%s_home.html' % ('account' if (not get_is_logged_in(request)) else 'started'),template_folder=_template_folder,context=_default_context)
	elif (url_toks[0] == 'terms-of-service'):
	    _context['PAGE_CONTENT'] = render_static_html(request,'','_terms-of-service.html',template_folder=_template_folder,context=_default_context)
	elif (url_toks[0] in ['login','forgot-password']):
	    if (len(url_toks) == 1):
		_context['LOGIN_REGISTER_BUTTON'] = render_static_html(request,'','_register-button.html' if (url_toks[0] == 'login') else '_%s-button.html' % (url_toks[0]),template_folder=_template_folder,context=_default_context) if (not get_is_logged_in(request)) else ''
		resp = login.login(request,template='%s.html' % (url_toks[0]),onAction='/%s/process/' % (url_toks[0]),onSuccess='/%s/accepted/' % (url_toks[0]))
		if (isinstance(resp,str)):
		    m_scripts_loginHead = minify.minify_js(_scripts_loginHead)
		    js_head = oohtml.render_scripts(m_scripts_loginHead)
		    _context['EXTRA_HEAD_ELEMENTS'] = js_head
		    js = oohtml.render_scripts(_scripts_loginForm)
		    _context['PAGE_CONTENT'] = resp + js
		else:
		    return resp
	    elif (len(url_toks) > 1) and (url_toks[1] == 'process'):
		form_html = ''
		users = User.objects.filter(email_address=request.POST['username'])
		if (len(users) > 0):
		    aUser = users[0]
		    _password = django_utils.get_from_post(request,'password',default='')
		    if (_password == ''):
			email_address = aUser.email_address
			password = GenPasswd.GenPasswdIntuitive()
			aUser.password = md5.md5(password)
			aUser.save()
			t_content = get_template('_pyeggs_reactivate.html')
			form_html = t_content.render(Context({}))
			send_activation_email(email_address, password)
		    else:
			if (aUser.password is None) or (aUser.password != _password):
			    t_content = get_template('_pyeggs_reject_%s.html' % (url_toks[0]))
			    num_login_attempts = get_login_attempts(request)
			    if (num_login_attempts is None):
				request.session['login_attempts'] = 2
				num_login_attempts = get_login_attempts(request)
			    form_html = t_content.render(Context({'MORE_ATTEMPTS':num_login_attempts}))
			elif (aUser.password is not None):
			    request.session['login_attempts'] = None
			    request.session['is_logged_in'] = True
			    request.session['user'] = aUser
			    anActivity = UserActivity(user=aUser,ip=django_utils.get_from_environ(request,'REMOTE_ADDR'),action='/'.join(url_toks))
			    anActivity.save()
			    return http.HttpResponseRedirect('/')
		if (len(form_html) == 0):
		    return http.HttpResponseRedirect('/')
		_context['PAGE_CONTENT'] = form_html
	    elif (len(url_toks) > 1) and (url_toks[1] == 'accepted'):
		_context['PAGE_CONTENT'] = 'Logged In'
	elif (url_toks[0] == 'logoff'):
	    request.session['login_attempts'] = None
	    request.session['is_logged_in'] = False
	    request.session['user'] = None
	    return http.HttpResponseRedirect('/')
	elif (url_toks[0] == 'register'):
	    d_context = {}
	    form_register = forms.DjangoForm(request,'register', User, '/register/submit/')
	    if (len(url_toks) == 1):
		form_register.use_captcha = True
		form_register.captcha_form_name = 'captcha_form_fields.html'
		form_register.captcha_font_name = 'BerrysHandegular.ttf'
		form_register.captcha_font_size = 32
		try:
		    form_html = form_as_html.form_as_html(form_register,callback=_form_for_model)
		    _context['LOGIN_REGISTER_BUTTON'] = render_static_html(request,'','_log%s-button.html' % ('in' if (not get_is_logged_in(request)) else 'Out'),template_folder=_template_folder,context=_default_context)
		except Exception, e:
		    form_html = _utils.formattedException(details=e)
		_context['PAGE_CONTENT'] = form_html
	    elif (len(url_toks) > 1) and (url_toks[1] == 'submit'):
		try:
		    form_register.use_captcha = True
		    form_register.captcha_form_name = 'captcha_form_fields.html'
		    form_register.captcha_font_name = 'BerrysHandegular.ttf'
		    form_register.captcha_font_size = 32
		    form_html = form_as_html.form_as_html(form_register,callback=_form_for_model)
		    if (captcha.is_captcha_form_valid(request)):
			_form_for_model(form_register, context=d_context)
			form_register.get_freehost_by_name = get_freehost_by_name
			form_html = form_register.validate_and_save(request,d_context,callback=on_successful_registration,callback_beforeSave=on_before_form_save,callback_validation_failed=on_unsuccessful_registration,callback_error=on_registration_form_error)
			if (isinstance(form_html,dict)):
			    html_context = form_html
			    t_content = get_template('_pyeggs_registered.html')
			    form_html = t_content.render(Context(html_context))
			else:
			    _context['LOGIN_REGISTER_BUTTON'] = render_static_html(request,'','_log%s-button.html' % ('in' if (not get_is_logged_in(request)) else 'Out'),template_folder=_template_folder,context=_default_context)
			    _context['PAGE_CONTENT'] = form_html
		except Exception, e:
		    form_html = _utils.formattedException(details=e)
		_context['PAGE_CONTENT'] = form_html
	    elif ('/'.join(url_toks[0:-1]).lower().find('/pyeggs/registration/activate') > -1):
		email_address = keys._decode(url_toks[-1])
		users = User.objects.filter(email_address=email_address)
		if (len(users) > 0):
		    aUser = users[0]
		    if (aUser.password is None):
			password = GenPasswd.GenPasswdIntuitive()
			aUser.password = md5.md5(password)
			aUser.save()
			t_content = get_template('_pyeggs_active.html')
			form_html = t_content.render(Context({}))
			send_activation_email(email_address, password)
		    else:
			t_content = get_template('_pyeggs_activated.html')
			form_html = t_content.render(Context({}))
		    aContract = UserContract(user=aUser,num_days=7,num_uploads=1)
		    aContract.save()
		    _context['PAGE_CONTENT'] = form_html
	elif (url_toks[0] == 'upload-zip'):
	    if (len(url_toks) == 1):
		resp = zip_upload.zip_upload(request,saveTo=_uploads_,onSuccess='/%s/accepted/' % (url_toks[0]))
		if (isinstance(resp,str)):
		    _context['PAGE_CONTENT'] = resp
		else:
		    return resp
	    elif (len(url_toks) > 1) and (url_toks[1] == 'accepted'):
		_context['PAGE_CONTENT'] = '(+++) --> %s %s' % (_uploads_,os.path.exists(_uploads_))
	elif (url_toks[0] == 'upgrade'):
	    _context['PAGE_CONTENT'] = render_static_html(request,'','_upgrade-service.html',template_folder=_template_folder,context=_default_context)
	elif (url_toks[0] == 'captcha'):
	    if (captcha.is_captcha_form_valid(request)):
		_context['PAGE_CONTENT'] = '(+++)'
	    else:
		_context['PAGE_CONTENT'] = captcha.render_captcha_form(request,form_name='captcha_form.html',font_name='BerrysHandegular.ttf',font_size=26)
	    pass
    now = _utils.timeStamp(format=pages.formatTimeStr())
    _context['TITLE'] = _context['TITLE'] % (_title,sub_title,now)
    _context['MEDIA_URL'] = _settings.MEDIA_URL
    return pages.render_the_template(request,'%s' % (_title),'index.html',context=_context,template_folder=_template_folder)

def default(request):
    try:
        s_response = ''
        __error__ = ''

        params = django_utils.parse_url_parms(request)
        url = '/%s' % (str('/'.join(params)))

        if (url == '/'):
	    return render_to_response('main.html', {}, context_instance=RequestContext(request))
        else:
	    if (len(params) == 2) and (params[0] == u'enter') and (params[-1] != u'enter.html'):
		request.session['uuid'] = params[1]
		return HttpResponseRedirect('/'+params[0]+'.html')
            try:
		d = {'uuid':request.session.get('uuid', '')}
		s = render_to_string(url.replace('/',''), dictionary=d, context_instance=RequestContext(request))
		if (len(params) == 1) and (params[0] == u'enter.html'):
		    countries = [SmartObject(record.__dict__) for record in Country.objects.order_by('printable_name').all()]
		    l_usa = [c for c in countries if (c.iso == 'US')]
		    l_others = [c for c in countries if (c.iso != 'US')]
		    countries = l_usa + l_others
		    usa = l_usa[0] if (misc.isList(l_usa) and (len(l_usa) > 0)) else l_usa
		    html_selection = oohtml.render_select_content(countries,id='country_code',name='country_code',value_id='id',text_id='printable_name',selected=usa.id)
		    s = s.replace('__country_code__',html_selection)
		return HttpResponse(s, mimetype=mimetypes.guess_type('.html')[0])
            except Exception, e:
                cname = request.META['HTTP_HOST']
                return render_to_response(request, '404.html', {'details':'<BR/>'.join(_utils.formattedException(details=e).split('\n')),'HTTP_HOST':cname} if (django_utils._is_(request,__development__)) else {})
	return render_to_response('404.html', {'details':''}, context_instance=RequestContext(request))	
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        mimetype = mimetypes.guess_type('.html')[0]
        return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n'))), mimetype=mimetype)
