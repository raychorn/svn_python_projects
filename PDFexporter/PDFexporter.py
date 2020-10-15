import os, sys, time, types, traceback

import urllib

import wx
from wx.lib.wordwrap import wordwrap
from wx.lib.embeddedimage import PyEmbeddedImage

from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix import oodb
from vyperlogix.hash import lists

from vyperlogix.misc import threadpool
from vyperlogix.pyPdf.getPDFContent import getPDFContent

from vyperlogix.wx import SplashFrame

from vyperlogix.daemon.daemon import Log

from vyperlogix.misc import decodeUnicode

import make_suggestion

from vyperlogix.win.regnow import RegNowAffiliateTracking

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import TreeNotebookPanel

from vyperlogix.products import responses as products_responses
from vyperlogix.products import keys as products_keys
from vyperlogix.products import data as products_data

_background_Q = threadpool.ThreadQueue(5,isDaemon=False)

_info_site_address = 'www.pdfxporter.com'

_info_site_url = 'http://%s' % (_info_site_address)

_isRunningLocally = lambda cname:(cname.upper() == 'UNDEFINED3') # or (cname.lower() == 'misha-lap.ad.magma-da.com')

def isRunningLocally():
    return not _isRunningLocally(_utils.getComputerName())

server_addr = '127.0.0.1:8888' if (isRunningLocally()) else _info_site_address
_registration_server = 'http://%s/register' % (server_addr)
_validation_server = 'http://%s/validate' % (server_addr)
_versioncheck_server = 'http://%s/versioncheck' % (server_addr) 
_feedback_server = 'http://%s/feedback' % (server_addr) 
_specials_server = 'http://%s/specials' % (server_addr) 

_special_offers = []

d_django_responses = products_responses.d_responses

_developers = ["Mr. Python", "Nelson"]
_writers = ["Bailey", "Prada"]
_artists = ["Sophie", "Katie", "Chanel"]
_translators = ["Simon"]

_is_product_id_valid = True
is_product_id_valid = lambda bool:'%sREGISTERED' % ('NOT ' if (not bool) else '')

_is_pdf_data_present = False

_status_bar_notification = [] # contains tuples where t[0] is the message and t[-1] is the number of seconds or -1 for longer.
last_status_bar_notification = '' # contains the last message that was on the status bar - gets displayed when no other message is available.

_data_path_prefix = products_data._data_path_prefix

dbx_name = lambda name:oodb.dbx_name(name,_data_path)

_productkey_ = 'productkey'
_namekey_ = 'namekey'
_orderidkey_ = 'orderidkey'
_emailkey_ = 'emailkey'

__copyright__ = """[**], All Rights Reserved.

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK."""

__GetRegistered__ = """Click the Shopping Cart icon, positioned to the left, to Purchase your copy of [**] to begin the process of unlocking all the powerful features you want to use.

You will be asked to validate your purchase before your registration will become active.

The validation process may take 1-2 business days to complete.

Upon validation you will be given a Product ID you must enter below in order to unlock your copy of [**].
"""

__RegisterationInfo__ = """After clicking the Submit button above your information will be reviewed and validated.

Once we have validated your Order Id we will grant you access to the current version of [*v*] including any maintenance releases for version [*v*] and any minor releases for this version.

Your Version [*v*] Registration covers you for all version through but not including Version [*vn*].

Please allow 1-2 business days for processing your Product Registration Key.
"""

__ProductKeyInfo__ = """After clicking the Submit button above your Product Key will be reviewed and validated.

Your Product Registration Key will grant you access to the current version of [**] including any maintenance releases.

Your Version [*v*] Registration covers you for all version through but not including Version [*vn*].

Please keep your Product Registration Key secure as this is your Passport to the valuable features you need to use.
"""

__ChangeLog__ = """
[*2a*]
Version [*1*] - Features.
PDF Data can be saved into a single ASCII text file.
[*2b*]
"""

_info_Name = 'PDFexporter'
_info_Version = "1.0"
_info_Copyright = "(c). Copyright 1990-%s, Vyper Logix Corp." % (_utils.timeStampLocalTime(format=_utils.formatDate_YYYY()))

_info_nextVersion = '%1.1f' % (float(_info_Version)+1.0)

_infoName_version = "%s %s" % (_info_Name,_info_Version)
_info_name_version = "%s%s" % (_info_Version.replace('.',''),_info_Name)
_info_name__version = "%s" % (_info_name_version.replace(' ','_'))

_info_root_folder = 'c:\\'

__copyright__ = __copyright__.replace('[**]',_info_Copyright)

__GetRegistered__ = __GetRegistered__.replace('[**]','%s' % (_infoName_version))

__RegisterationInfo__ = __RegisterationInfo__.replace('[**]','%s' % (_infoName_version)).replace('[*v*]',_info_Version).replace('[*vn*]',_info_nextVersion)

__ProductKeyInfo__ = __ProductKeyInfo__.replace('[*v*]',_info_Version).replace('[*vn*]',_info_nextVersion)

__ChangeLog__ = __ChangeLog__.replace('[*1*]',_info_Version).replace('[*2a*]','%s %s %s' % ('='*20,'Begin','='*20)).replace('[*2b*]','%s %s   %s' % ('='*20,'End','='*20))

wildcard_pdf = "PDF File (*.pdf)|*.pdf"
wildcard_save_as = "Text File (*.txt)|*.txt"

def fingerPrint(name=None,order_id=None,email_address=None):
    #from vyperlogix.misc import GenPasswd
    #cname = _utils.getComputerName() + GenPasswd.GenPasswd()
    cname = _utils.getComputerName()
    if (name is not None) and (len(name) > 0) and (order_id is not None) and (len(order_id) > 0) and (email_address is not None) and (len(email_address) > 0):
	name = urllib.quote_plus(name)
	order_id = urllib.quote_plus(order_id)
	email_address = urllib.quote_plus(email_address)
	data = ','.join([t.replace(',','') for t in [cname,name,order_id,email_address,_info_name__version]])
    else:
	data = ','.join([t.replace(',','') for t in [cname,_info_name__version]])
    _key = products_keys._key
    _iv = _info_name__version[0:8]
    _data = oodb.crypt(_key,data,_iv)
    return products_keys._encode(_data)

def getProductKey():
    key = ''
    fname = dbx_name(_utils.getProgramName())
    dbx = oodb.PickledLzmaHash2(fname)
    try:
	if (dbx.has_key(_productkey_)):
	    key = dbx[_productkey_]
	    key = dbx.unlistify(key)
    finally:
	dbx.close()
    return key

def getRegistrationDetails():
    details = lists.HashedLists2()
    fname = dbx_name(_utils.getProgramName())
    dbx = oodb.PickledLzmaHash2(fname)
    try:
	if (dbx.has_key(_namekey_)):
	    name = dbx[_namekey_]
	    name = dbx.unlistify(name)
	    details['name'] = name
	else:
	    details['name'] = ''
	if (dbx.has_key(_orderidkey_)):
	    orderid = dbx[_orderidkey_]
	    orderid = dbx.unlistify(orderid)
	    details['orderid'] = orderid
	else:
	    details['orderid'] = ''
	if (dbx.has_key(_emailkey_)):
	    email = dbx[_emailkey_]
	    email = dbx.unlistify(email)
	    details['email'] = email
	else:
	    details['email'] = ''
    finally:
	dbx.close()
    return details

def setRegistrationDetails(details):
    try:
	name,orderid,email = details
    except:
	name,orderid,email = ('','','')
	exc_info = sys.exc_info()
	info_string = '\n'.join(traceback.format_exception(*exc_info))
	info_string = '%s :: Cannot perform this function at this time, Reason: %s' % (misc.funcName(),info_string)
	print >>sys.stderr, info_string
	print info_string
    finally:
	if (len(name) > 0) and (len(orderid) > 0) and (len(email) > 0):
	    fname = dbx_name(_utils.getProgramName())
	    dbx = oodb.PickledLzmaHash2(fname)
	    try:
		dbx[_namekey_] = name
		dbx[_orderidkey_] = orderid
		dbx[_emailkey_] = email
	    finally:
		dbx.close()

def __isProductKeyValid(self=None):
    import binascii
    
    key = ''
    now = _utils.getFromDateTimeStr(_utils.timeStampLocalTime().split('T')[0],format='%Y-%m-%d')
    now_ymd = str(now).split()[0]

    fname = dbx_name(_utils.getProgramName())
    dbx = oodb.PickledLzmaHash2(fname)
    reason = ''
    try:
	if (dbx.has_key(_productkey_)):
	    key = dbx[_productkey_]
	    key = dbx.unlistify(key)
	elif (len(dbx.keys()) > 0):
	    keys = [_utils.getFromDateTimeStr(oodb.unlistify(k),format=_utils.formatDate_YYYYMMDD_dashes()) for k in dbx.keys()]
	    keys.sort()
	    _key = _utils.getAsDateTimeStr(keys[-1],fmt=_utils.formatDate_YYYYMMDD_dashes())
	    result = str(dbx[_key])
	    parts = result.split(',')
	    result = int(parts[0])
	    if (len(parts) > 1):
		reason = parts[-1].capitalize()
	    s_result = d_django_responses[result] if (len(reason) == 0) else reason
	    print '%s :: s_result is "%s"' % (misc.funcName(),s_result)
	    _status_bar_notification.append((s_result,15))
    finally:
	dbx.close()
    if (len(key) == 0):
	return False
    else:
	_isNeedToPhoneHome = False
	dbx = oodb.PickledLzmaHash2(fname)
	try:
	    if (not dbx.has_key(now_ymd)):
		dbx[now_ymd] = products_responses.code_error
		_isNeedToPhoneHome = True
	    else:
		value = dbx[now_ymd]
		value = dbx.unlistify(value)
		_isNeedToPhoneHome = (value in [products_responses.code_error,products_responses.code_invalid])
	finally:
	    dbx.close()
	if (not _isNeedToPhoneHome):
	    _isNeedToPhoneHome = (isRunningLocally())
	print '%s :: _isNeedToPhoneHome is "%s"' % (misc.funcName(),_isNeedToPhoneHome)
	if (_isNeedToPhoneHome):
	    h_data = fingerPrint()
	    url = '%s/%s/%s' % (_validation_server,key,h_data)
	    print '%s :: url is "%s"' % (misc.funcName(),url)
	    data = fetchFromURL(url)
	    toks = data.split('=')
	    try:
		try:
		    verb,result = toks
		except ValueError:
		    verb,result,reason = toks
		parts = result.split(',')
		if (str(parts[0]).isdigit()):
		    result = int(parts[0])
		    s_result = d_django_responses[result] if (len(reason) == 0) else reason
		    print '%s :: s_result is "%s"' % (misc.funcName(),s_result)
		    print '%s :: reason is "%s"' % (misc.funcName(),reason)
		    reason = (' because ' if (len(reason) > 0) else '') + reason + ('.' if (len(reason) > 0) else '')
		    if (len(reason) > 0):
			_status_bar_notification.append(('Your product key is invalid %s' % (reason),15))
		    else:
			_status_bar_notification.append(('%s' % (s_result),15))
		else:
		    _status_bar_notification.append(('Unable to contact the Registration Server at this time.',15))
		    return False
	    except:
		result = products_responses.code_error
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		info_string = '%s :: Cannot process the response from your Product Key at this time, Reason: %s' % (misc.funcName(),info_string)
		print >>sys.stderr, info_string
		print info_string
	    # if the response comes back negative then remove the Product Key from the local cache in the dbx.
	    dbx = oodb.PickledLzmaHash2(fname)
	    try:
		if (result == products_responses.code_revoked):
		    _status_bar_notification.append(('Your Product Key has been revoked...',15))
		    if (dbx.has_key(_productkey_)):
			del dbx[_productkey_]
			pass
		    if (len(reason) > 0):
			_status_bar_notification.append((reason,15))
		if (dbx.has_key(now_ymd)):
		    del dbx[now_ymd]
		dbx[now_ymd] = result
	    finally:
		dbx.close()
	    if (self is not None):
		self.response.SetValue(str(s_result))
	    return (result == products_responses.code_valid)
    return False

def isProductKeyValid(self=None):
    return True

class PDFparser:
    def __init__(self, parent, gauge, pdfFile='', statusbar=None, callback=None):
        self.parent = parent
        self.result = ''
        self.gauge = gauge
        self.callback = callback
        self.pdfFile = pdfFile
        self.statusbar = statusbar
        self.content = []

        if (os.path.exists(self.pdfFile)):
            self.doProcess()
        else:
            _msg = 'ERROR #1 in %s()...Cannot open "%s".' % (ObjectTypeName.objectSignature(self),self.pdfFile)
            if (self.statusbar):
                self.statusbar.SetStatusText(_msg, 0)
            print _msg

    @threadpool.threadify(_background_Q)
    def doProcess(self):
        _msg = ''
	_isError = False
        print "starting %s()..." % (ObjectTypeName.objectSignature(self))
        for i in xrange(0,self.gauge.max+10,self.gauge.max/10):
            try:
                self.gauge.SetGaugeValue(i)
            except Exception, details:
                _msg = "ERROR #2 in %s()...%s" % (ObjectTypeName.objectSignature(self),str(details))
                if (self.statusbar):
                    self.statusbar.SetStatusText(_msg, 0)
                print _msg
            if (i == 0):
		try:
		    temp_stderr = sys.stderr
		    fOut = StringIO()
		    sys.stderr = fOut
		    self.content = getPDFContent(self.pdfFile)
		    if (len(self.content) > 0):
			_msg = 'Successfully read %d pages from "%s".' % (len(self.content),os.path.basename(self.pdfFile))
			i = self.gauge.max
			break
		except Exception, details:
		    _msg = 'Cannot read pages from "%s" because "%s".' % (os.path.basename(self.pdfFile),str(details))
		finally:
		    sys.stderr = temp_stderr
		    if (fOut.getvalue().find('Traceback ') > -1):
			_msg = 'Cannot read data from "%s" because it does not contain data.' % (os.path.basename(self.pdfFile))
			_status_bar_notification[0] = (_msg,30)
			_isError = True
            wx.MilliSleep(100)
	if (not _isError):
	    try:
		self.gauge.SetGaugeValue(i)
	    except Exception, details:
		_msg = "ERROR #3 in %s()...%s" % (ObjectTypeName.objectSignature(self),str(details))
		if (self.statusbar):
		    self.statusbar.SetStatusText(_msg, 0)
		print _msg
	    if (self.statusbar):
		self.statusbar.SetStatusText(_msg, 0)
	    self.result = i
	else:
	    self.result = -1
        if (callable(self.callback)):
            wx.CallAfter(self.callback, self.result)

    def save_as(self,fname):
	keys = misc.sortCopy(self.content.keys())
	io_buffer = StringIO()
	for k in keys:
	    print >>io_buffer, decodeUnicode.decodeUnicode('\n'.join(self.content[k]))
	_utils.writeFileFrom(fname,io_buffer.getvalue())
    
class ProgressDialogPanel(wx.Panel):
    def __init__(self, parent, title='Progress Dialog Title', message='A message.', max=100, log=None, style=wx.PD_CAN_ABORT | wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME | wx.PD_REMAINING_TIME):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        dlg = wx.ProgressDialog(title, message, maximum=max, parent=self, style=style)

    def run(self):
        keepGoing = True
        count = 0

        while keepGoing and count < max:
            count += 1
            wx.MilliSleep(250)

            if count >= max / 2:
                (keepGoing, skip) = dlg.Update(count, 'count=%d, max=%d' % (count,max))
            else:
                (keepGoing, skip) = dlg.Update(count, 'count=%d, max=%d' % (count,max))

class ProgressPanel(wx.Panel):
    def __init__(self, parent, log=None):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        self.max = -1
        self.timer = None
	self.restart()

    def restart(self):
        self.count = 0
    
    def run(self, msg='', max=100, isSimulated=False):
        self.max = max
        self.text = wx.StaticText(self, -1, msg, (45, 15))

        self.gauge = wx.Gauge(self, -1, max, (110, 50), (250, 25))
        
        if (isSimulated):
            self.Bind(wx.EVT_TIMER, self.TimerHandler)
            self.timer = wx.Timer(self)
            self.timer.Start(250)

    def __del__(self):
        if (self.timer):
            self.timer.Stop()

    def SetGaugeValue(self,value):
        self.count = value
        self.gauge.SetValue(self.count)
    
    def TimerHandler(self, event):
        self.count = self.count + 1

        if self.count >= self.max:
            self.text.SetLabel('Done %s' % (self.text.GetLabel()))
            self.timer.Stop()

        self.SetGaugeValue(self.count)
    
    def signalDone(self):
        self.text.SetLabel('Done %s' % (self.text.GetLabel()))
    
class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent, log):
        wx.StatusBar.__init__(self, parent, -1)

        self.SetFieldsCount(3)

        self.SetStatusWidths([-4, -1, -2])
        self.log = log
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.SetStatusText("Online", 0)

        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000)
        self.Notify()

    def Notify(self):
	global _status_bar_notification, last_status_bar_notification
        
        t = time.localtime(time.time())
        st = time.strftime("%A %d-%b-%Y   %I:%M:%S %p", t)
        self.SetStatusText(st, self.GetFieldsCount()-1)
        self.SetStatusText(is_product_id_valid(_is_product_id_valid), self.GetFieldsCount()-2)
	st = (last_status_bar_notification,15)
	if (len(_status_bar_notification) > 0):
	    st = _status_bar_notification[0]
	    _status_bar_notification = _status_bar_notification[1:]
	    if (st[-1] == -1):
		st[-1] = 15
	    if (st[-1] > -1):
		i = st[-1]
		i -= 1
		if (i > 0):
		    st = (st[0],i)
		    _status_bar_notification.insert(0,st)
		    if (len(st[0]) > 0):
			last_status_bar_notification = st[0]
		    if (self.log):
			self.log.WriteText("tick...\n")
	print 'st=%s' % (str(st))
	self.SetStatusText(st[0], 0)

    def OnSize(self, evt):
        self.sizeChanged = True

    def OnIdle(self, evt):
        if self.sizeChanged:
            pass

def MakeRegistrationPane(collapsible_pane,callback=None,data={}):
    '''Just make a few controls to put on the collapsible pane'''
    data = lists.HashedLists2(lists.asDict(data))
    nameLbl = wx.StaticText(collapsible_pane, -1, "Name:")
    name = wx.TextCtrl(collapsible_pane, -1, data['name']);

    #addrLbl = wx.StaticText(collapsible_pane, -1, "Address:")
    #addr1 = wx.TextCtrl(collapsible_pane, -1, "");
    #addr2 = wx.TextCtrl(collapsible_pane, -1, "");

    #cstLbl = wx.StaticText(collapsible_pane, -1, "City, State, Zip:")
    #city  = wx.TextCtrl(collapsible_pane, -1, "", size=(150,-1));
    #state = wx.TextCtrl(collapsible_pane, -1, "", size=(50,-1));
    #zipcode   = wx.TextCtrl(collapsible_pane, -1, "", size=(70,-1));

    orderLbl = wx.StaticText(collapsible_pane, -1, "RegNow Order ID:")
    order_id = wx.TextCtrl(collapsible_pane, -1, data['orderid'], size=(300,-1));

    emailLbl = wx.StaticText(collapsible_pane, -1, "EMail Address:")
    email_address = wx.TextCtrl(collapsible_pane, -1, data['email'], size=(300,-1));

    btn_submit = wx.Button(collapsible_pane, 0, "Submit")
    btn_submit.SetToolTip(wx.ToolTip('Click this button to submit your Registration details.'))
    
    infoLbl = wx.StaticText(collapsible_pane, -1, wordwrap(__RegisterationInfo__, 500, wx.ClientDC(collapsible_pane)))

    addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
    addrSizer.AddGrowableCol(1)
    addrSizer.Add(nameLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    addrSizer.Add(name, 0, wx.EXPAND)
    #addrSizer.Add(addrLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    #addrSizer.Add(addr1, 0, wx.EXPAND)
    #addrSizer.Add((5,5)) 
    #addrSizer.Add(addr2, 0, wx.EXPAND)

    #addrSizer.Add(cstLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

    #cstSizer = wx.BoxSizer(wx.HORIZONTAL)
    #cstSizer.Add(city, 1)
    #cstSizer.Add(state, 0, wx.LEFT|wx.RIGHT, 5)
    #cstSizer.Add(zipcode)
    #addrSizer.Add(cstSizer, 0, wx.EXPAND)

    addrSizer.Add(orderLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    addrSizer.Add(order_id, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
    
    addrSizer.Add(emailLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    addrSizer.Add(email_address, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
    
    addrSizer.Add((5,5)) 
    addrSizer.Add(btn_submit, 0, wx.ALL)
    
    addrSizer.Add((5,5)) 
    addrSizer.Add(infoLbl, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)

    border = wx.BoxSizer()
    border.Add(addrSizer, 1, wx.EXPAND|wx.ALL, 5)
    collapsible_pane.SetSizer(border)

    if (callable(callback)):
	try:
	    d = lists.HashedLists2({'name':name, 'email_address':email_address, 'order_id':order_id, 'btn_submit':btn_submit})
	    callback(d)
	except:
	    pass
	
def MakeProductKeyPane(collapsible_pane,callback=None):
    '''Just make a few controls to put on the collapsible pane'''
    keyLbl = wx.StaticText(collapsible_pane, -1, "Product Key:")
    key = wx.TextCtrl(collapsible_pane, -1, "");
    
    btn_submit = wx.Button(collapsible_pane, 0, "Submit")
    btn_submit.SetToolTip(wx.ToolTip('Click this button to submit your Product Key.'))
    
    infoLbl = wx.StaticText(collapsible_pane, -1, wordwrap(__ProductKeyInfo__, 500, wx.ClientDC(collapsible_pane)))

    addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
    addrSizer.AddGrowableCol(1)
    addrSizer.Add(keyLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    addrSizer.Add(key, 0, wx.EXPAND)
    addrSizer.Add((5,5)) 
    addrSizer.Add(btn_submit, 0, wx.ALL)
    
    addrSizer.Add((5,5)) 
    addrSizer.Add(infoLbl, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)

    border = wx.BoxSizer()
    border.Add(addrSizer, 1, wx.EXPAND|wx.ALL, 5)
    collapsible_pane.SetSizer(border)

    if (callable(callback)):
	try:
	    d = lists.HashedLists2({'key':key, 'btn_submit':btn_submit})
	    callback(d)
	except:
	    pass
	
class RegistrationPanel(wx.Panel):
    def __init__(self, parent, log=None, callback=None, pane_callback=None, submit_callback=None, label1="Click here to show pane", label2="Click here to hide pane",data={}):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

	self.label1 = label1
	self.label2 = label2
	
	self.__callback__ = callback
	self.__pane_callback__ = pane_callback
	self.__submit_callback__ = submit_callback
	
	self.__data__ = data
	
        self.cp = cp = wx.CollapsiblePane(self, label=self.label1, style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, cp)
        self.MakePaneContent(cp.GetPane())

	sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        sizer.Add(cp, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 25)

    def IsExpanded():
        doc = "IsExpanded"
        def fget(self):
            return self.cp.IsExpanded()
        return locals()
    IsExpanded = property(**IsExpanded())

    def togglePane(self):
        self.cp.Collapse(self.IsExpanded)
        self.OnPaneChanged()

    def OnPaneChanged(self, evt=None):
        if (evt) and (self.log is not None):
            self.log.write('wx.EVT_COLLAPSIBLEPANE_CHANGED: %s' % evt.Collapsed)

        # redo the layout
        self.Layout()

        if self.IsExpanded:
            self.cp.SetLabel(self.label2)
        else:
            self.cp.SetLabel(self.label1)
	    
	if (callable(self.__callback__)):
	    try:
		self.__callback__(self.IsExpanded)
	    except:
		pass
        
    def MakePaneContent(self, pane):
	if (callable(self.__pane_callback__)):
	    try:
		self.__pane_callback__(pane,callback=self.bindPaneEvents,data=self.__data__)
	    except:
		pass
	    
    def bound_objects():
        doc = "bound_objects returns the objects that are bound to the submit function."
        def fget(self):
            return self.__bound_objects__
        return locals()
    bound_objects = property(**bound_objects())

    def bindPaneEvents(self, d_objs):
	self.__bound_objects__ = lists.HashedLists2(d_objs)
	btn = self.__bound_objects__['btn_submit']
	self.Bind(wx.EVT_BUTTON, self.onSubmit, btn)
	    
    def onSubmit(self, evt):
	print '%s :: onSubmit' % (ObjectTypeName.objectSignature(self))
	self.togglePane()
	for k,v in self.bound_objects.iteritems():
	    if (k != 'btn_submit'):
		print '%s --> %s' % (k,v.GetValue())
	if (callable(self.__submit_callback__)):
	    try:
		self.__submit_callback__(self)
	    except:
		pass
	pass

def fetchFromURL(url):
    from vyperlogix.url import fetch
    import urllib2
    while (1):
	txt = '='
	try:
	    txt = fetch.fetchFromURL(url)
	    print '%s :: [%s]' % (misc.funcName(),txt)
	    break
	except urllib2.URLError:
	    time.sleep(5)
	except:
	    if (isRunningLocally()):
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		info_string = 'Cannot process your Registration at this time, Reason: %s' % (info_string)
		print >>sys.stderr, info_string
		print info_string
    return txt

class GetRegisteredDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GetRegisteredDialog.__init__
	import wx.lib.hyperlink as hlink
	from vyperlogix.wx import AnimatedGIFPanel
	
	self.__widgets__ = []
	
	self.dialog_width = 700
	self.dialog_height = 500
	
	self.url = 'http://%s' % (_info_site_address) if (not kwds.has_key('url')) else kwds['url']
	if (kwds.has_key('url')):
	    del kwds['url']
	kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP|wx.CENTRE
        wx.Dialog.__init__(self, *args, **kwds)
	import Shoppingcart_32x32
        self.btn_regnow = wx.BitmapButton(self, -1, Shoppingcart_32x32.getShoppingcart_32x32Bitmap())
	self.btn_regnow.SetToolTip(wx.ToolTip('Click this icon to purchase a license for your copy of this product and unlock all the available features.\nYou must do this before you attempt to Register for a Product Key below.'))
        self.btn_close = wx.Button(self, wx.ID_CLOSE, "")
	self.btn_close.SetToolTip(wx.ToolTip('Click this button to close this dialog.'))

	self.activity_indicator = AnimatedGIFPanel.AnimatedGIFPanel(self, -1, filename=os.sep.join([os.path.abspath('.'),'animated_indicator.gif']))
	self.activity_indicator.Show(False)
	
        self._hyper1 = hlink.HyperLinkCtrl(self, wx.ID_ANY, "",URL=self.url)
	s__GetRegistered__ = __GetRegistered__
	s_special_offers_header = 'Special Offer%s: ' % ('s' if (len(_special_offers) > 1) else '')
	for s in _special_offers:
	    s__GetRegistered__ += '\n' + s_special_offers_header + s
	    s_special_offers_header = ''
        self.text_1 = wx.StaticText(self, -1, wordwrap(s__GetRegistered__, self.dialog_width - 30, wx.ClientDC(self)))
	
	data = getRegistrationDetails()
	self.reg_panel = RegistrationPanel(self,callback=self.__resize_panel,submit_callback=self.onSubmit,pane_callback=MakeRegistrationPane,label1='Register for Product Key',label2='Hide Registration Panel',data=data)
	wx.EVT_KEY_DOWN(self.reg_panel.bound_objects['order_id'], self.OnKeyDown_OrderId)
	
	self.reg_panel2 = RegistrationPanel(self,callback=self.__resize_panel2,submit_callback=self.onSubmit2,pane_callback=MakeProductKeyPane,label1='Enter Product Key',label2='Hide Product Key Panel')
	
	self.response = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY, size=(self.dialog_width - 150,-1));

	self.__widgets__.append(self.btn_regnow)
	self.__widgets__.append(self.btn_close)
	self.__widgets__.append(self.reg_panel)
	self.__widgets__.append(self.reg_panel2)

	self.__callback_registration_complete__ = None
	
	self.__set_properties()
        self.__do_layout()

        #self._hyper1.Bind(hlink.EVT_HYPERLINK_RIGHT, self.OnLink)
        self.Bind(wx.EVT_BUTTON, self.onRegister, self.btn_regnow)
        self.Bind(wx.EVT_BUTTON, self.onClose, self.btn_close)
        # end wxGlade

    def callback_registration_complete():
        doc = "callback_registration_complete fires whenever the registration process is complete."
        def fget(self):
            return self.__callback_registration_complete__
        def fset(self, callback):
            self.__callback_registration_complete__ = callback
        return locals()
    callback_registration_complete = property(**callback_registration_complete())

    def __set_properties(self):
        self.SetTitle("Get Registered")
        self.SetSize((self.dialog_width, self.dialog_height))
	import Shoppingcart
	self.SetIcon(wx.IconFromBitmap(Shoppingcart.getShoppingcartBitmap()))

    def __do_layout(self):
        # begin wxGlade: GetRegisteredDialog.__do_layout
        sizer_1 = wx.FlexGridSizer(rows=4, cols=2, hgap=5, vgap=5)
        sizer_1.Add(self.btn_regnow, 0, wx.ALIGN_CENTER, 0)
        sizer_1.Add(self.text_1, 0, wx.ALL, 0)

        sizer_1a = wx.BoxSizer(wx.VERTICAL)
        sizer_1a.Add(self.activity_indicator, 0, wx.ALIGN_CENTER, 0)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(self.btn_close, 0, wx.ALIGN_CENTER, 0)
	sizer_1.Add((5,5)) 
        sizer_1.Add(sizer_1a, 0, wx.ALL, 0)
        sizer_1.Add(sizer_3, 0, wx.EXPAND, 0)

	sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.reg_panel, 0, wx.ALL, 0)
        sizer_1.Add(sizer_2, 0, wx.ALL, 0)

	sizer_1.Add((5,5)) 

	sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(self.reg_panel2, 0, wx.ALL, 0)
        sizer_1.Add(sizer_3, 0, wx.ALL, 0)

	sizer_1.Add((5,5)) 

	sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.response, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_4, 0, wx.ALL, 0)

	self.SetSizer(sizer_1)
        sizer_1.Fit(self)
	
	self.sizer_1 = sizer_1

	self.Layout()
        # end wxGlade

    def __resize_panel(self,isExpanded):
	val = 0 if (isExpanded) else -200
        self.SetSize((self.dialog_width, self.dialog_height + val))
	if (self.reg_panel2.IsExpanded):
	    self.reg_panel2.togglePane()
	self.reg_panel2.cp.Enable(not isExpanded)
	self.reg_panel.cp.SetSize((self.dialog_width if (not isExpanded) else (self.dialog_width - 150), 50 if (not isExpanded) else (self.dialog_height + val)))
	self.Layout()
	self.Centre(wx.BOTH)
	self.sizer_1.RecalcSizes()
    
    def __resize_panel2(self,isExpanded):
	val = 0 if (isExpanded) else -200
        self.SetSize((self.dialog_width, self.dialog_height + val))
	self.sizer_1.RecalcSizes()
	if (self.reg_panel.IsExpanded):
	    self.reg_panel.togglePane()
	self.reg_panel.cp.Enable(not isExpanded)
	self.Layout()
	self.Centre(wx.BOTH)
	self.sizer_1.RecalcSizes()
	
    def OnKeyDown_OrderId(self, event):
	valid_keys = ['0','1','2','3','4','5','6','7','8','9','-']
	key = event.KeyCode
	ch = chr(key)
	if (not ch in valid_keys):
	    Level = event.StopPropagation()
	else:
	    event.Skip(True)
	pass
    
    def onSubmit(self,pane):
	for w in self.__widgets__:
	    w.Disable()
	self.activity_indicator.Show(True)
	try:
	    self.response.SetValue('Processing your submission... Please stand-by... This may take a few moments...')
	    print '%s' % (ObjectTypeName.objectSignature(self))
	    for k,v in pane.bound_objects.iteritems():
		if (k != 'btn_submit'):
		    print '%s --> %s' % (k,v.GetValue())
	    _name = pane.bound_objects['name'].GetValue()
	    _order_id = pane.bound_objects['order_id'].GetValue()
	    _email_address = pane.bound_objects['email_address'].GetValue()
	    if (_name is not None) and (len(_name) > 0) and (_order_id is not None) and (len(_order_id) > 0) and (_email_address is not None) and (len(_email_address) > 0):
		setRegistrationDetails((_name,_order_id,_email_address))
		h_data = fingerPrint(name=pane.bound_objects['name'].GetValue(),order_id=pane.bound_objects['order_id'].GetValue(),email_address=pane.bound_objects['email_address'].GetValue())
		url = '%s/%s/%s' % (_registration_server,getProductKey(),h_data)
		print 'url is "%s"' % (url)
		data = fetchFromURL(url)
		toks = data.split('=')
		try:
		    verb,result = toks
		    try:
			result = int(result)
		    except ValueError:
			result = products_responses.code_error
		    s_result = d_django_responses[result]
		    print 's_result is "%s"' % (s_result)
		    self.response.SetValue(str(s_result))
		except:
		    exc_info = sys.exc_info()
		    info_string = '\n'.join(traceback.format_exception(*exc_info))
		    info_string = 'Cannot process the response from your Registration at this time, Reason: %s' % (info_string)
		    print >>sys.stderr, info_string
		    print info_string
	    else:
		self.response.SetValue('Unable to process your Registration unless all fields are entered with valid information.')
	finally:
	    self.activity_indicator.Show(False)
	    for w in self.__widgets__:
		w.Enable()
    
    def onSubmit2(self,pane):
	global _is_product_id_valid
	# Increase the amount of time this part of the GUI waits before proceeding based on the number of requests since the program started.
	for w in self.__widgets__:
	    w.Disable()
	self.activity_indicator.Show(True)
	try:
	    self.response.SetValue('Please stand-by...')
	    print '%s :: _data_path=%s' % (ObjectTypeName.objectSignature(self),_data_path)
	    for k,v in pane.bound_objects.iteritems():
		if (k != 'btn_submit'):
		    print '%s --> %s' % (k,v.GetValue())
	    key = urllib.quote_plus(pane.bound_objects['key'].GetValue())
	    dbx = oodb.PickledLzmaHash2(dbx_name(_utils.getProgramName()))
	    try:
		if (dbx.has_key(_productkey_)):
		    del dbx[_productkey_]
		dbx[_productkey_] = key
	    finally:
		dbx.sync()
		dbx.close()
		self.response.SetValue('Your Product Key has been saved.')
		_is_product_id_valid = isProductKeyValid(self)
		if (_is_product_id_valid):
		    if (_is_pdf_data_present):
			_status_bar_notification.append(('"Export As" function is now enabled...',30))
		    if (callable(self.callback_registration_complete)):
			try:
			    self.callback_registration_complete(_is_product_id_valid)
			except:
			    pass
	finally:
	    self.activity_indicator.Show(False)
	    for w in self.__widgets__:
		w.Enable()
    
    def onClose(self, event): # wxGlade: GetRegisteredDialog.<event_handler>
        self.btn_close.Enable(False)
        self.btn_regnow.Enable(False)
        self.Destroy()

    def onRegister(self, event): # wxGlade: GetRegisteredDialog.<event_handler>
        self.btn_regnow.Enable(False)
        self.btn_close.Enable(False)
	self._hyper1.GotoURL(self.url, True, True)
        self.Destroy()

# end of class GetRegisteredDialog

def sendEmail(username,password,email,subj,body):
    from vyperlogix.mail import message
    from vyperlogix.mail import mailServer
    
    try:
	email = 'do-not-reply@vyperlogix.com' if (email is None) or (len(email) == 0) else email
	msg = message.Message(email, 'support@vyperlogix.com', body, subj)
	smtp = mailServer.GMailServer(username,password)
	smtp.sendEmail(msg)
    except:
	exc_info = sys.exc_info()
	info_string = '\n'.join(traceback.format_exception(*exc_info))
	info_string = '1. Cannot send email at this time, Reason: %s' % (info_string)
	print >>sys.stderr, info_string
	print >>sys.stdout, info_string

def decodeData(h_data,_key=None,_iv=None):
    _data = products_keys._decode(h_data)
    if (_key is not None) and (_iv is not None):
	data = oodb.crypt(_key,_data,_iv)
	toks = data.split('-')
	data = toks[0]
    else:
	data = ','
    return data.split(',')

@threadpool.threadify(_background_Q)
def procify_checkForSpecials():
    global _special_offers
    h_data = fingerPrint()
    url = '%s/%s' % (_specials_server,h_data)
    print '%s :: url is "%s"' % (misc.funcName(),url)
    data = fetchFromURL(url)
    print '%s :: data is "%s"' % (misc.funcName(),data)
    toks = data.split('=')
    try:
	try:
	    verb,result = toks
	    _key = products_keys._key
	    _iv = _info_name__version[0:8]
	    data = decodeData(result,_key=_key,_iv=_iv)
	    if (not _is_product_id_valid):
		_special_offers += data
		for s in _special_offers:
		    _status_bar_notification.append((s,30))
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = '1. Cannot process the submission of your feedback at this time, Reason: %s' % (info_string)
	    print >>sys.stderr, info_string
	    print info_string
    finally:
	pass

@threadpool.threadify(_background_Q)
def process_feedback(textSummary,textDetails,textEmailAddress,callback=None):
    h_data = fingerPrint()
    url = '%s/%s' % (_feedback_server,h_data)
    print '%s :: url is "%s"' % (misc.funcName(),url)
    data = fetchFromURL(url)
    print '%s :: data is "%s"' % (misc.funcName(),data)
    toks = data.split('=')
    try:
	try:
	    verb,result = toks
	    _key = products_keys._key
	    _iv = _info_name__version[0:8]
	    data = decodeData(result,_key=_key,_iv=_iv)
	    details = getRegistrationDetails()
	    sendEmail(data[0],data[-1],textEmailAddress,'From: %s on behalf of %s (%s,%s), %s' % (textEmailAddress,details['email'],details['name'],details['orderid'],textSummary),textDetails)
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = '1. Cannot process the submission of your feedback at this time, Reason: %s' % (info_string)
	    print >>sys.stderr, info_string
	    print info_string
    finally:
	if (callable(callback)):
	    try:
		_status_bar_notification.append(('Thank you for the feedback.',15))
		_status_bar_notification.append(('We value your opinions and feature requests.',15))
		callback()
	    except:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		info_string = '2. Cannot process the submission of your feedback at this time, Reason: %s' % (info_string)
		print >>sys.stderr, info_string
		print info_string

def checkForUpdates(parent):
    isError = False
    url = '%s/%s' % (_versioncheck_server,_info_Version)
    print 'url is "%s"' % (url)
    data = fetchFromURL(url)
    toks = data.split('=')
    try:
	verb,result = toks
	result = int(result)
	s_result = d_django_responses[result]
	s_result = s_result.replace(products_responses._info_site_address,_info_site_url)
	print 's_result is "%s"' % (s_result)
	_status_bar_notification.append((str(s_result),30))
    except:
	isError = True
	exc_info = sys.exc_info()
	info_string = '\n'.join(traceback.format_exception(*exc_info))
	info_string = 'Cannot process the response from your Version Check at this time, Reason: %s' % (info_string)
	print >>sys.stderr, info_string
	print info_string
    if (not isError) and (result == products_responses.code_isUpdate):
	dlg = wx.MessageDialog(parent, str(s_result), 'Check for New Version', wx.CANCEL | wx.ICON_INFORMATION)
	dlg.ShowModal()
	dlg.Destroy()
    pass
    
@threadpool.threadify(_background_Q)
def procify_checkForUpdates(parent):
    checkForUpdates(parent)

class TopFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: TopFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.top_frame_menubar = wx.MenuBar()
        self.file_menu_item = wx.Menu()
        self.open_menu_item = wx.MenuItem(self.file_menu_item, wx.NewId(), "Open PDF...", "") # , wx.ITEM_NORMAL
	#import open_pdf
	#self.open_menu_item.SetBitmap(wx.BitmapFromImage(open_pdf.getopen_pdfImage()))

        self.export_menu_item = wx.MenuItem(self.file_menu_item, wx.NewId(), "Export As...", "", wx.ITEM_NORMAL)
	
        self.exit_menu_item = wx.MenuItem(self.file_menu_item, wx.NewId(), "Exit", "", wx.ITEM_NORMAL)
	#import exit
	#self.exit_menu_item.SetBitmap(wx.BitmapFromImage(exit.getexitImage()))
	
        self.exit_menu_item.Enable(True)
        self.export_menu_item.Enable(False)
        self.file_menu_item.AppendItem(self.open_menu_item)
        self.file_menu_item.AppendItem(self.export_menu_item)
        self.file_menu_item.AppendItem(self.exit_menu_item)
        self.top_frame_menubar.Append(self.file_menu_item, "File")
	
        self.help_menu_item = wx.Menu()
        self.about_menu_item = wx.MenuItem(self.help_menu_item, wx.NewId(), "About", "", wx.ITEM_NORMAL)
        self.help_menu_item.AppendItem(self.about_menu_item)
        self.changelog_menu_item = wx.MenuItem(self.help_menu_item, wx.NewId(), "Change Log", "", wx.ITEM_NORMAL)
        self.help_menu_item.AppendItem(self.changelog_menu_item)
        self.updates_menu_item = wx.MenuItem(self.help_menu_item, wx.NewId(), "Check for Updates", "", wx.ITEM_NORMAL)
        self.help_menu_item.AppendItem(self.updates_menu_item)
        self.feedback_menu_item = wx.MenuItem(self.help_menu_item, wx.NewId(), "Submit Feedback...", "", wx.ITEM_NORMAL)
        self.help_menu_item.AppendItem(self.feedback_menu_item)
        self.top_frame_menubar.Append(self.help_menu_item, "Help")
        self.feedback_menu_item.Enable(_is_product_id_valid)

        self.register_menu_item = wx.Menu()
        self.register_now_menu_item = wx.MenuItem(self.register_menu_item, wx.NewId(), "Register Now" if (not _is_product_id_valid) else "Update Registration", "", wx.ITEM_NORMAL)
        self.register_menu_item.AppendItem(self.register_now_menu_item)
        self.top_frame_menubar.Append(self.register_menu_item, "Register")
        #self.register_now_menu_item.Enable(not _is_product_id_valid)

        self.SetMenuBar(self.top_frame_menubar)
        # Menu Bar end
        
        self.gauge_panel = ProgressPanel(self)
        #self.tree_panel = TreeNotebookPanel.TreeNotebookPanel(self,None)
        
        self.sb = CustomStatusBar(self, None)
        self.SetStatusBar(self.sb)

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_MENU, self.onFileOpen, self.open_menu_item)
        self.Bind(wx.EVT_MENU, self.onSaveAsOpen, self.export_menu_item)
        self.Bind(wx.EVT_MENU, self.onExit, self.exit_menu_item)
        self.Bind(wx.EVT_MENU, self.onAbout, self.about_menu_item)
        self.Bind(wx.EVT_MENU, self.onChangeLog, self.changelog_menu_item)
        self.Bind(wx.EVT_MENU, self.onCheckForUpdates, self.updates_menu_item)
        self.Bind(wx.EVT_MENU, self.onSubmitFeedback, self.feedback_menu_item)
        self.Bind(wx.EVT_MENU, self.onRegisterNow, self.register_now_menu_item)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
	# end wxGlade

    def __set_properties(self):
        # begin wxGlade: TopFrame.__set_properties
        self.SetTitle(_infoName_version)
        self.SetSize((800, 600))
	
	import icon4
	self.SetIcon(wx.IconFromBitmap(icon4.geticon4Bitmap()))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: TopFrame.__do_layout
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.frame_size = self.GetSize()
        self.gauge_panel.SetSize((self.frame_size.width-10,self.frame_size.height-80))
        self.sizer.Add(self.gauge_panel, 0, wx.EXPAND, 0)
        self.SetSizer(self.sizer)
        self.Layout()
        self.Centre()
        # end wxGlade
        
    def onRegisterNow(self, event): # wxGlade: TopFrame.<event_handler>
        print "Time to Get Registered !"
	regNow = RegNowAffiliateTracking('pdfxporter')
	print regNow
	url1 = regNow.buyURL(regNow.rootHKLM)
	print '1 :: url=%s' % (url1)
	url2 = regNow.buyURL(regNow.rootHKCU)
	print '2 :: url=%s' % (url2)
	url = url1 if (url1 != url2) else url2
	dialog_1 = GetRegisteredDialog(None, -1, url=url)
	dialog_1.callback_registration_complete = self.onRegistrationComplete
	dialog_1.Show()

    def onRegistrationComplete(self, bool):
        print "Registration Complete"
        self.export_menu_item.Enable(bool)
	
    def onChangeLog(self, event):
	dlg = wx.MessageDialog(self, __ChangeLog__, 'Change Log', wx.CANCEL | wx.ICON_INFORMATION)
	dlg.ShowModal()
	dlg.Destroy()
	pass
    
    def onSubmitFeedback(self, event):
	self._feedback_frame = make_suggestion.MyFrame(self, 'Please Send Feedback - We want to serve your needs.')
	self._feedback_frame.Show(True)
	self._feedback_frame.Bind(wx.EVT_BUTTON, self.onFeedbackSubmit, self._feedback_frame.btnSubmit)
	self._feedback_frame.Bind(wx.EVT_BUTTON, self.onFeedbackCancel, self._feedback_frame.btnCancel)
	self._feedback_frame.Centre(wx.BOTH)
	pass

    def closeFeedbackDialog(self):
	self._feedback_frame.Destroy()
    
    def onFeedbackSubmit(self, evt):
	# Do the submit then close...
	self._feedback_frame.btnSubmit.Enable(False)
	self._feedback_frame.btnCancel.Enable(False)
	self._feedback_frame.activity_indicator.Show(True)
	process_feedback(self._feedback_frame.textSummary.GetValue(),self._feedback_frame.textDetails.GetValue(),self._feedback_frame.textEmailAddress.GetValue(),callback=self.closeFeedbackDialog)
    
    def onFeedbackCancel(self, evt):
	self.closeFeedbackDialog()
    
    def onCheckForUpdates(self, event):
	isError = False
	url = '%s/%s' % (_versioncheck_server,_info_Version)
	print 'url is "%s"' % (url)
	data = fetchFromURL(url)
	toks = data.split('=')
	try:
	    verb,result = toks
	    result = int(result)
	    s_result = d_django_responses[result]
	    s_result = s_result.replace(products_responses._info_site_address,_info_site_url)
	    print 's_result is "%s"' % (s_result)
	    _status_bar_notification.append((str(s_result),30))
	except:
	    isError = True
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = 'Cannot process the response from your Version Check at this time, Reason: %s' % (info_string)
	    print >>sys.stderr, info_string
	    print info_string
	if (not isError):
	    dlg = wx.MessageDialog(self, str(s_result), 'Check for Updates', wx.CANCEL | wx.ICON_INFORMATION)
	    dlg.ShowModal()
	    dlg.Destroy()
	pass
    
    def onAbout(self, event): # wxGlade: TopFrame.<event_handler>
	import indian_python

        info = wx.AboutDialogInfo()
        info.Name = _info_Name
        info.Version = _info_Version
        info.Copyright = _info_Copyright
        info.Description = wordwrap(
            "\"%s\" is a software program that exports data from your PDF Bank Statements. "
            "Banks such as Wells Fargo and Citibank commonly issue Monthly Bank Statements "
	    "in the form of Adobe PDF Documents as a way to reduce their costs "
            "however it is not all that easy to get computer readable data from PDF Documents "
            "suitable for use by another program such as Microsoft Excel or some other 3rd Party "
	    "Accounting Software Product."
            
            "\n\n\"%s\" can be used to extract data you can use when preparing "
            "documentation for the IRS such as when documenting your Personal or Business Tax Deductions." % (_info_Name,_info_Name),
            350, wx.ClientDC(self))
        info.WebSite = ("http://%s" % (_info_site_address), "%s Home Page" % (_infoName_version))

        info.License = wordwrap(__copyright__, 700, wx.ClientDC(self))

	info.SetIcon(wx.IconFromBitmap(indian_python.getindian_pythonBitmap()))
	
	for n in _developers:
	    info.AddDeveloper(n)
	for n in _writers:
	    info.AddDocWriter(n)
	for n in _artists:
	    info.AddArtist(n)
	for n in _translators:
	    info.AddTranslator(n)
        
        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)

    def onFileOpen(self, event): # wxGlade: TopFrame.<event_handler>
        global _info_root_folder, _is_pdf_data_present
        
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=_info_root_folder, 
            defaultFile="",
            wildcard=wildcard_pdf,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()

            for self.path in paths:
                print '%s :: %s' % (ObjectTypeName.objectSignature(self),self.path)
                _info_root_folder = os.path.dirname(self.path)
		self.gauge_panel.restart()
		self.gauge_panel.Show()
                self.gauge_panel.run(msg='Reading %s' % (self.path))
                self.pdf = PDFparser(self, self.gauge_panel, pdfFile=self.path, statusbar=self.sb, callback=self.receive_result)
		_is_pdf_data_present = True
		if (not _is_product_id_valid):
		    _status_bar_notification.append(('"Export As" function disabled until REGISTRATION has been completed...',30))
		else:
		    _status_bar_notification.append(('Use the "Export As" File Menu Item to complete the export process.',30))

        dlg.Destroy()
        
    def onSaveAsOpen(self, event):
        global _info_root_folder
        
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=_info_root_folder, 
            defaultFile="%s" % (os.path.basename(self.path).replace('.pdf','.txt')),
            wildcard=wildcard_save_as,
            style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()

            for path in paths:
                print '%s :: %s' % (ObjectTypeName.objectSignature(self),path)
		self.pdf.save_as(path)
		_status_bar_notification.append(('PDF Data has been exported to "%s".' % (path),30))

        dlg.Destroy()

    def receive_result(self, result):
        print "Hey, I'm done with that long, slow PDF parsing process."
        print "The result was:", result
        self.gauge_panel.signalDone()
        wx.MilliSleep(1500)
        self.gauge_panel.Hide()
        self.tree_panel = TreeNotebookPanel.TreeNotebookPanel(self,titles=[os.path.basename(self.path)])
        self.sizer.Add(self.tree_panel, 1, wx.EXPAND, 0)
        self.tree_panel.SetSize((self.frame_size.width,self.frame_size.height-80))
        _items = ['Page %d' % (n+1) for n in xrange(len(self.pdf.content))]
        self.tree_panel.addItems(items=_items)
        for i in xrange(len(_items)):
            items = self.pdf.content[i+1]
            self.tree_panel.addItemsTo(indicesList=[i],items=items)
        #self.save_as_menu_item.Enable(True)
        self.export_menu_item.Enable(_is_product_id_valid and (result > -1))
        pass

    def closeWindow(self):
	try:
	    self.sb.timer.Stop()
	    del self.sb.timer
	finally:
	    self.Destroy()
        
    def OnCloseWindow(self, event):
        self.closeWindow()
        
    def onExit(self, event):
        self.closeWindow()

# end of class TopFrame

from vyperlogix.wx.PopUpDialog import wx_PopUp_Dialog

class MyStderr:
    def __init__(self, fOut=None):
	self.fOut = sys.stderr
	self.msg = ''
	self.dlg = None
	self.textctrl = None
    
    def write(self, message):
	message = message.strip()
	if (len(message) > 0):
	    self.msg += message
	    wx_PopUp_Dialog(parent=None,msg=message,title='ERROR',styles=wx.ICON_ERROR | wx.CANCEL)
	    
	    if (self.fOut is not None):
		print >>self.fOut, message
		self.fOut.flush()
    
    def OnCloseWindow(self, evt):
	self.msg = ''

class PDFexporter(wx.App):
    def OnInit(self):
        #wx.InitAllImageHandlers()
        frame_1 = TopFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class PDFexporter

_isProductKeyGetValidated = False

@threadpool.threadify(_background_Q)
def procify_isProductKeyValid():
    global _is_product_id_valid
    global _isProductKeyGetValidated
    global _data_path
    _data_path = _utils.appDataFolder(prefix=_data_path_prefix(_utils.getProgramName()))
    _utils._makeDirs(_data_path)
    _is_product_id_valid = isProductKeyValid()
    _isProductKeyGetValidated = True

def isProductKeyGetValidated():
    global _isProductKeyGetValidated
    return _isProductKeyGetValidated

def main(sys_stderr):
    from logo import getlogoImage

    procify_isProductKeyValid()
    
    s = SplashFrame.Splash(bitmapFile=getlogoImage(),delay=(1000,5000,30000),callback=isProductKeyGetValidated)
    _background_Q.join()
    
    sys.stderr = MyStderr(sys_stderr) 
    try:
	PDCexporter = PDFexporter(0)
	procify_checkForUpdates(None)
	procify_checkForSpecials()
	PDCexporter.MainLoop()
    except Exception, exception:
	# This handles exceptions before and after the MainLoop
	type, value, stack = sys.exc_info()
	formattedBacktrace = ''.join(traceback.format_exception(type, value, stack, 5))
	dlg = wx.MessageDialog(None, 'An unexpected problem occurred:\n%s' % (formattedBacktrace), 'Fatal Error',wx.CANCEL | wx.ICON_ERROR)
	dlg.ShowModal()
	dlg.Destroy()

def exception_callback(sections):
    _msg = 'EXCEPTION Causing Abend.\n%s' % '\n'.join(sections)
    print >>sys.stdout, _msg
    print >>sys.stderr, _msg
    if (_sys_stderr is not None):
	print >>_sys_stderr, _msg
	_sys_stderr.f.flush()

if __name__ == "__main__":
    _isBeingDebugged = _utils.isBeingDebugged
    
    if (not _isBeingDebugged):
	from vyperlogix.handlers.ExceptionHandler import *
	excp = ExceptionHandler()
	excp.callback = exception_callback

    from vyperlogix.misc._psyco import *
    importPsycoIfPossible(func=main,isVerbose=True)

    _stderr = sys.stderr

    if (_isBeingDebugged):
	_stdErr = open(os.sep.join([os.path.dirname(sys.argv[0]),'stderr.txt']),'w')
	_sys_stderr = Log(_stdErr)
	main(_sys_stderr)
    else:
	main(None)
    

    #if (sys.platform == 'win32'):
	#from vyperlogix.win.WinProcesses import WinProcesses
	#pid = WinProcesses.getProcessIdByName(_utils.getProgramName())
	#print >>sys.stderr, 'pid = %s' % (pid)
	#pass
    