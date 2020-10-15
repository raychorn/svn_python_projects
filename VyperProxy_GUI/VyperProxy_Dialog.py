
# Created with FarPy GUIE v0.5.5

import wx
import wx.calendar
import  wx.lib.mixins.listctrl  as  listmix

import sys
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.hash import lists

from vyperlogix.wx.mixins import EnableMixin
from vyperlogix.wx.mixins import DisableMixin

import unicodedata

from wx.lib.wordwrap import wordwrap

import  wx.lib.rcsizer  as rcs

from VyperProxy_version import ProductVersion

from VyperProxy_version import explain_version
from VyperProxy_version import explain_ports_limits
from VyperProxy_version import explain_address_limits

info_web_app_url = '''
Enter your HTTP 1.1 Web App URL in the etnry field above.

The URL you enter can be for any HTTP 1.1 Web App whether that URL is for your local computer or not.

For instance, if you want to make your Django App serve content faster your URL might be http://{{ IP_SAMPLE }}:8000 assuming your Django App runs on your local computer. 

You may enter "http://{{ IP_SAMPLE }}:8000,8001,8002" or "http://{{ IP_SAMPLE }}:8000-8002" to enter a series of ports for the same web app URL.

{{ IP_NOTES }}
'''

notes_ip_localhost_limited = '''The Community and Professional Versions are limited to performing Proxy functions for 127.0.0.1 and only 3 ports.'''

notes_ip_localhost_unlimited = '''The Enterprise Version can perform proxy functions for any IP address including those IP addresses not associated with your local computer and no limit on the ports.'''

class URLValidator(wx.PyValidator):
    def __init__(self, pyVar=None, error_color='pink', notifyStatusBar=None, version=ProductVersion.community_version):
        wx.PyValidator.__init__(self)
	self.error_color = error_color
	self.notifyStatusBar = notifyStatusBar
	self.version = version
        self.Bind(wx.EVT_KEY_UP, self.OnChar)

    def Clone(self):
        return URLValidator(notifyStatusBar=self.notifyStatusBar, error_color=self.error_color, version=self.version)

    def Validate(self, window):
	gather_digits_only = lambda chars:''.join([ch for ch in chars if (str(ch).isdigit())])
	gather_ports = lambda parts:[int(p) for p in parts if (str(p).isdigit())]
	gather_valid_port = lambda p:(p > -1) and (p <= 65535)
	gather_valid_ports = lambda _parts:[p for p in _parts if gather_valid_port(p)]
        window = self.GetWindow()
        text = window.GetValue().strip()
	ports = []
	isIP_Valid = False
	toks = text.split(':')
	if (toks[0] in ['http','https']):
	    _conjunction = '//'
	    parts = toks[1].split(_conjunction)
	    parts2 = parts[-1].split('.')
	    if (len(parts) == 2) and (len(parts2) == 4) and (all([str(p).isdigit() for p in parts2])):
		isIP_Valid = True if (ProductVersion.test_address_limits(version,toke[1])) else False
	    toks[0] = ':'.join(toks[0:len(toks)-1])
	    del toks[1]
	isValid = isIP_Valid and (len(toks) == 2) and ( (toks[0].find('http://') > -1) or (toks[0].find('https://') > -1) )
	print '1.0 isValid=%s' % (isValid)
	ports_conjunction = ''
	if (isValid):
	    ports_conjunction = '-'
	    parts = toks[-1].split(ports_conjunction)
	    if (len(parts) == 2):
		parts = [gather_digits_only(p) for p in parts]
		_parts = gather_ports(parts)
		_parts = gather_valid_ports(_parts)
		isValid = isValid and (len(_parts) == len(parts))
		if (isValid):
		    ports = [p for p in _parts]
	    else:
		ports_conjunction = ','
		parts = toks[-1].split(ports_conjunction)
		if (len(parts) > 0):
		    _parts = gather_ports(parts)
		    _parts = gather_valid_ports(_parts)
		    isValid = isValid and (len(_parts) == len(parts))
		    if (isValid):
			ports = [p for p in _parts]
		elif (toks[-1].isdigit()):
		    p = int(toks[-1])
		    if gather_valid_port(p):
			ports.append(p)
		else:
		    isValid = False
	toks[-1] = ports_conjunction.join([str(p) for p in ports])
	_text = ':'.join(toks)
	isValid = isValid and (text == _text)

	print '2.0 isValid=%s, _text=%s' % (isValid,_text)
	print '2.1 ports=%s' % (ports)
	if (isValid):
            window.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            window.Refresh()
	    if (callable(self.notifyStatusBar)):
		try:
		    self.notifyStatusBar('Your Web App URL is acceptable.',1)
		except:
		    pass
	else:
	    info_string = 'Your Web App URL is not acceptable.'
            window.SetBackgroundColour(self.error_color)
            window.SetFocus()
            window.Refresh()
	    if (callable(self.notifyStatusBar)):
		try:
		    self.notifyStatusBar(info_string,1)
		except:
		    pass
            return False
	return True

    def OnChar(self, event):
        key = event.GetKeyCode()
	try:
	    self.Validate(None)
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    print info_string
	finally:
	    event.Skip()
        return

class Dialog(wx.Frame, EnableMixin, DisableMixin):	
    def __init__(self, parent, title='Dialog', version=ProductVersion.community_version, notifyStatusBar=None):
	global info_web_app_url

	_is_not_enterprise_version = (version != ProductVersion.enterprise_version)
	
	row = 1
	self.notifyStatusBar = notifyStatusBar
	
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, (700, 500), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER | 0 | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        self.panel = wx.Panel(self, -1)
        
	gbs = self.gbs = wx.GridBagSizer(6, 5)
	
	self.label1 = wx.StaticText(self.panel, -1, 'HTTP 1.1 Web App URL:')
	self.label1.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.label1.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
	
	gbs.Add( self.label1, (row,0) )

	self.txtWebAppURL = wx.TextCtrl(self.panel, -1, 'http://127.0.0.1:8000-8002', validator=URLValidator(notifyStatusBar=self.notifyStatusBar))
	self.txtWebAppURL.SetBackgroundColour(wx.Colour(255, 255, 255))
	self.txtWebAppURL.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.txtWebAppURL.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	gbs.Add( self.txtWebAppURL, (row,1), (1,4), flag=wx.EXPAND)

	self.lbl_url_helper = wx.StaticText(self.panel, -1, 'Web App URL Hints:')
	self.lbl_url_helper.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.lbl_url_helper.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	row += 1
	gbs.Add( self.lbl_url_helper, (row,0))
	
	self.cb_url_helper_list = ['Choose your Web App URL pattern from this list, edit it as desired...', 'http://127.0.0.1:8000-8002', 'http://127.0.0.1:8000,8001,8002']
	self.cb_url_helper = wx.ComboBox(self.panel, -1, 'Choose your Web App URL from this list...', (21,13), (121, 21), self.cb_url_helper_list)
	self.cb_url_helper.SetBackgroundColour(wx.Colour(255, 255, 255))
	self.cb_url_helper.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.cb_url_helper.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	gbs.Add( self.cb_url_helper, (row,1), (1,3), flag=wx.EXPAND)
	
	info_web_app_url = info_web_app_url.replace('{{ IP_SAMPLE }}', '127.0.0.1' if (_is_not_enterprise_version) else '0.0.0.0')
	info_web_app_url = info_web_app_url.replace('{{ IP_NOTES }}', notes_ip_localhost_limited if (_is_not_enterprise_version) else notes_ip_localhost_unlimited)
	self.infoLbl = wx.StaticText(self.panel, -1, wordwrap(info_web_app_url, self.Size[0], wx.ClientDC(self.panel)))
	self.infoLbl.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.infoLbl.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	row += 1
	gbs.Add( self.infoLbl, (row,0), (1,4), flag=wx.EXPAND)
	
	self.label3 = wx.StaticText(self.panel, -1, 'HTTP 1.1 Proxy:')
	self.label3.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.label3.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	row += 1
	gbs.Add( self.label3, (row,0) )
	
	address_limits = explain_address_limits(version)
	
	self.label3a = wx.StaticText(self.panel, -1, '(%s requires %s)' % (explain_version(version),address_limits))
	self.label3a.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.label3a.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	gbs.Add( self.label3a, (row,2), (1,2), flag=wx.EXPAND )
	
	self.txtProxyAddress = wx.TextCtrl(self.panel, -1, '127.0.0.1')
	self.txtProxyAddress.SetBackgroundColour(wx.Colour(255, 255, 255))
	self.txtProxyAddress.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.txtProxyAddress.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	gbs.Add( self.txtProxyAddress, (row,1))
	
	ports_limits = explain_ports_limits(version)
	
	self.label4 = wx.StaticText(self.panel, -1, 'Ports: (%s)' % ('%d ports allowed' % (ports_limits) if (ports_limits > 0) else 'UNLIMITED'))
	self.label4.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.label4.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	row += 1
	gbs.Add( self.label4, (row,0) )
	
	# Code a validator for the port number based on the existing validator.
	
	self.txtProxyPort1 = wx.TextCtrl(self.panel, -1, '8888', size=(40,22))
	self.txtProxyPort1.SetBackgroundColour(wx.Colour(255, 255, 255))
	self.txtProxyPort1.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.txtProxyPort1.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	self.txtProxyPort2 = wx.TextCtrl(self.panel, -1, '8889', size=(40,22))
	self.txtProxyPort2.SetBackgroundColour(wx.Colour(255, 255, 255))
	self.txtProxyPort2.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.txtProxyPort2.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	self.txtProxyPort3 = wx.TextCtrl(self.panel, -1, '8890', size=(40,22))
	self.txtProxyPort3.SetBackgroundColour(wx.Colour(255, 255, 255))
	self.txtProxyPort3.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.txtProxyPort3.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	hbox1 = wx.BoxSizer(wx.HORIZONTAL)
	hbox1.Add(self.txtProxyPort1)
	hbox1.Add(self.txtProxyPort2)
	hbox1.Add(self.txtProxyPort3)

	gbs.Add( hbox1, (row,1), (1,2))
	
	if (version == ProductVersion.professional_version):
	    pass
	elif (version == ProductVersion.enterprise_version):
	    pass
	
	self.btnStartProxy = wx.Button(self.panel, -1, 'Start Proxy')
	self.btnStartProxy.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.btnStartProxy.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	row += 1
	gbs.Add( self.btnStartProxy, (row,0) )
	
	self.btnStopProxy = wx.Button(self.panel, -1, 'Stop Proxy')
	self.btnStopProxy.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
	self.btnStopProxy.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
	
	self.btnStopProxy.Disable()

	gbs.Add( self.btnStopProxy, (row,1) )
	
        x = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        y = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        self.SetSizeHints(700,500,x,y)

        box = wx.BoxSizer()
        box.Add(gbs, 0, wx.ALL, 10)
        self.panel.SetSizerAndFit(box)
	
	if (_is_not_enterprise_version):
	    self.txtProxyAddress.Disable()
	else:
	    self.txtProxyAddress.Enable()
	
	self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.cb_url_helper)
	
    def EvtComboBox(self, evt):
        cb = evt.GetEventObject()
        text = cb.GetLabelText()
	self.txtWebAppURL.SetValue(text)
	cb.SetSelection(0)
        
