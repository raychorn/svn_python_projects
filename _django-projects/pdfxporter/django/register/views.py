from models import Registration
from django.http import HttpResponse
from django.template import Context, loader
from django.http import Http404

from vyperlogix.misc import _utils
from vyperlogix import oodb

from vyperlogix.products import responses as products_responses
from vyperlogix.products import keys as products_keys

import sys
import traceback
import urllib
import uuid

_username = 'raychorn@gmail.com'
_password = 'peekab00'

register_verb = 'register'
validate_verb = 'validate'
versioncheck_verb = 'versioncheck'
feedback_verb = 'feedback'
specials_verb = 'specials'

_info_Name = 'PDFexporter'
_info_Version = "1.0"
_info_name_version = "%s%s" % (_info_Version.replace('.',''),_info_Name)
_info_name__version = "%s" % (_info_name_version.replace(' ','_'))

_specials = 'The first 500 Charter Subscribers get Free upgrades for the next 2 years.'

def makeProductId(_key=None,_iv=None):
    from datetime import timedelta
    import binascii

    ts = _utils.getFromDateTimeStr(_utils.timeStamp(format=_utils.formatDate_MMDDYYYY_dashes()),format=_utils.formatDate_MMDDYYYY_dashes()) + timedelta(days=365)
    pid = str(uuid.uuid4())+'-%s' % str('%10.0f' % _utils.timeSecondsFromTimeStamp(ts)).strip()
    crc32 = binascii.crc32(pid)
    pid += '-%d' % (crc32)
    if (_key is not None) and (_iv is not None):
	data = oodb.crypt(_key,pid,_iv)
    else:
	data = pid
    pid2 = products_keys._encode(data)
    return (pid2,ts)

def makeEmailAuth(_key=None,_iv=None):
    from datetime import timedelta
    import binascii

    data = '%s,%s' % (_username,_password)
    crc32 = binascii.crc32(data)
    data += '-%d' % (crc32)
    if (_key is not None) and (_iv is not None):
	data = oodb.crypt(_key,data,_iv)
    data2 = products_keys._encode(data)
    return (data2)

def makeSpecialsResponse(_key=None,_iv=None):
    from datetime import timedelta
    import binascii

    data = '%s' % (_specials)
    crc32 = binascii.crc32(data)
    data += '-%d' % (crc32)
    if (_key is not None) and (_iv is not None):
	data = oodb.crypt(_key,data,_iv)
    data2 = products_keys._encode(data)
    return (data2)

def sendErrorEmail(msg,reason):
    from vyperlogix.mail import message
    from vyperlogix.mail import mailServer
    
    try:
	msg = message.Message('sales@vyperlogix.com', 'support@vyperlogix.com', msg, 'ERROR: %s' % (reason))
	smtp = mailServer.GMailServer(_username,_password)
	smtp.sendEmail(msg)
    except:
	exc_info = sys.exc_info()
	info_string = '\n'.join(traceback.format_exception(*exc_info))
	info_string = '1.1 Cannot send email at this time, Reason: %s' % (info_string)
	print >>sys.stderr, info_string
	print >>sys.stdout, info_string

def sendEmail(r1,isUpdate=False,verb=register_verb):
    from vyperlogix.mail import message
    from vyperlogix.mail import mailServer
    
    if (verb == register_verb):
        try:
            msg = message.Message('support@vyperlogix.com', 'sales@vyperlogix.com', 'name=%s\nemail=%s\ncname=%s\npname=%s\norder_id=%s\norder_date=%s\nactivity_date=%s\nproduct_id=%s' % (r1.name,r1.email,r1.cname,r1.pname,r1.order_id,r1.order_date,r1.activity_date,r1.product_id), '%sPDFxporter Registration%s from "%s" at %s.' % ('' if (isUpdate) else 'New ',' Update' if (isUpdate) else '',r1.name,r1.email))
            smtp = mailServer.GMailServer(_username,_password)
            smtp.sendEmail(msg)
        except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = '1. Cannot send email at this time, Reason: %s' % (info_string)
	    print >>sys.stderr, info_string
	    print >>sys.stdout, info_string
    
        try:
            msg = message.Message('sales@vyperlogix.com', r1.email, 'Thank you for submitting your Order Id of %s.\n\nPlease allow 1-2 business days for processing.' % (r1.order_id), '%sPDFxporter Registration%s from "%s" at %s.' % ('' if (isUpdate) else 'New ',' Update' if (isUpdate) else '',r1.name,r1.email))
            smtp = mailServer.GMailServer(_username,_password)
            smtp.sendEmail(msg)
        except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = '2. Cannot send email at this time, Reason: %s' % (info_string)
	    print >>sys.stderr, info_string
	    print >>sys.stdout, info_string
	    
        try:
            msg = message.Message('support@vyperlogix.com', r1.email, 'Product Key "%s" for Order Id "%s".\n\nCopy and Paste your Product Key to complete your Registration Process.' % (r1.product_id,r1.order_id), '%sPDFxporter Registration%s from "%s" at %s.' % ('' if (isUpdate) else 'New ',' Update' if (isUpdate) else '',r1.name,r1.email))
            smtp = mailServer.GMailServer(_username,_password)
            smtp.sendEmail(msg)
        except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = '2. Cannot send email at this time, Reason: %s' % (info_string)
	    print >>sys.stderr, info_string
	    print >>sys.stdout, info_string
    elif (verb == validate_verb):
        pass

def reverseFingerPrint(h_data,_key=None,_iv=None):
    _data = products_keys._decode(h_data)

    if (_key is not None) and (_iv is not None):
	data = oodb.crypt(_key,_data,_iv)
    else:
	data = ','
    
    return data.split(',')
    
def index(request):
    '''
    /register/name/order_id/email/computer_name +++ Add computer_name to the registration process
    /validate/product_id
    '''
    toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]
    tplate = loader.get_template('register_result.html')
    _key = products_keys._key
    _iv = _info_name__version[0:8]
    if (len(toks) == 1):
        html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_error)}))
    elif (toks[0] == register_verb):
        try:
	    verb,prod_key,h_data = tuple(toks)
	    _h_data = products_keys._decode(h_data)
	    _data_ = oodb.crypt(_key,_h_data,_iv)
	    cname,name,order_id,email,pname = [urllib.unquote_plus(t) for t in _data_.split(',')]
            try:
                r1 = Registration.objects.get(order_id=order_id)
            except:
                r1 = None
	    data = ','.join([t.replace(',','') for t in [cname,name,order_id,email,pname]])
            if (r1 is not None):
		# Allow License Transfers from one computer to another but revoke the previous license.
		# If computer name changes then revoke the old license and reissue a new license.
		if (r1.product_id == prod_key):
		    product_id = r1.product_id
		    is_revoked = r1.is_revoked
		    is_active = r1.is_active
		    cname = r1.cname
		    pname = r1.pname
		    order_id = r1.order_id
		    order_date = r1.order_date
		    valid_until = r1.valid_until
		    r1.delete()
		    r1.cname = cname
		    r1.pname = pname
		    r1.name = name
		    r1.email = email
		    r1.order_id = order_id
		    r1.order_date = order_date
		    r1.activity_date = _utils.timeStampLocalTime()
		    r1.product_id = product_id
		    r1.valid_until = valid_until
		    r1.is_revoked = is_revoked
		    r1.is_active = is_active
		    r1.save()
		    sendEmail(r1,isUpdate=True)
		    html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_updated)}))
		else:
		    html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_error)}))
            else:
                try:
		    pid = makeProductId(_key=_key,_iv=_iv)
                    r1 = Registration(name=name,email=email,order_id=order_id,order_date=_utils.timeStampLocalTime(),activity_date=_utils.timeStampLocalTime(),product_id=pid[0],valid_until=pid[-1],cname=cname,pname=pname,is_active=True,is_revoked=False,reason_revoked='')
                    r1.save()
		except Exception, details:
		    exc_info = sys.exc_info()
		    info_string = '\n'.join(traceback.format_exception(*exc_info))
		    sendErrorEmail(info_string,str(details))
                finally:
                    html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_accepted)}))
                    sendEmail(r1)
        except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = '3. Cannot process %s at this time, Reason: %s' % (toks[0],info_string)
	    print >>sys.stderr, info_string
	    print >>sys.stdout, info_string
            html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_error)}))
        pass
    elif (toks[0] == feedback_verb):
        try:
            verb,h_data = tuple(toks)
	    cname,info_name__version = reverseFingerPrint(h_data,_key=_key,_iv=_iv)
	    data = makeEmailAuth(_key=_key,_iv=_iv)
	    html = tplate.render(Context({'result_data': 'result=%s' % (data)}))
        except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = '4. Cannot process %s at this time, Reason: %s' % (toks[0],info_string)
	    print >>sys.stderr, info_string
	    print >>sys.stdout, info_string
            html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_error)}))
    elif (toks[0] == specials_verb):
        try:
            verb,h_data = tuple(toks)
	    cname,info_name__version = reverseFingerPrint(h_data,_key=_key,_iv=_iv)
	    data = makeSpecialsResponse(_key=_key,_iv=_iv)
	    html = tplate.render(Context({'result_data': 'result=%s' % (data)}))
        except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = '4. Cannot process %s at this time, Reason: %s' % (toks[0],info_string)
	    print >>sys.stderr, info_string
	    print >>sys.stdout, info_string
            html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_error)}))
    elif (toks[0] == validate_verb):
        try:
            verb,product_id,h_data = tuple(toks)
	    cname,info_name__version = reverseFingerPrint(h_data,_key=_key,_iv=_iv)
            try:
                r1 = Registration.objects.get(product_id=product_id)
            except:
                r1 = None
            if (r1 is not None) and (r1.cname.lower() == cname.lower()) and (_info_name__version == info_name__version):
		print 'r1.is_revoked=%s' % (r1.is_revoked)
		print 'r1.is_active=%s' % (r1.is_active)
		if (r1.is_revoked):
		    html = tplate.render(Context({'result_data': 'result=%d,reason=%s' % (products_responses.code_revoked,r1.reason_revoked)}))
		elif (not r1.is_active):
		    html = tplate.render(Context({'result_data': 'result=%d,reason=%s' % (products_responses.code_invalid,r1.reason_revoked)}))
		else:
		    html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_valid)}))
            else:
                html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_invalid)}))
        except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = '4. Cannot process %s at this time, Reason: %s' % (toks[0],info_string)
	    print >>sys.stderr, info_string
	    print >>sys.stdout, info_string
            html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_error)}))
    elif (toks[0] == versioncheck_verb):
	print 'Version is "%s".' % (toks[-1])
	html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_noUpdate)}))
	#html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_isUpdate)}))
    else:
        html = tplate.render(Context({'result_data': 'result=%d' % (products_responses.code_error)}))
    return HttpResponse(html)

#if (__name__ == '__main__'):
    #print makeTemporaryProductId()
    
