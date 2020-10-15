/*!
 * VyperBlog(tm) v1.0.0
 * http://www.vyperlogix.com/
 *
 * Copyright 2010, Vyper Logix Corp.
 * Licensed under the GNU General Public License version 3 (GPLv3).
 * http://www.opensource.org/licenses/gpl-3.0.html
 *
 * Date: Thu Jun 30 16:30:00 2010 -0700
 */
var const_inline_style = 'inline';
var const_none_style = 'none';
var const_block_style = 'block';
var const_hidden_style = 'hidden';
var const_visible_style = 'visible';
var const_absolute_style = 'absolute';
var const_relative_style = 'relative';
var const_function_symbol = 'function';
var const_nativeCode_symbol = '[native code]';
var const_object_symbol = 'object';
var const_number_symbol = 'number';
var const_string_symbol = 'string';
var const_debug_symbol = 'DEBUG';
var const_error_symbol = 'ERROR';
var const_simpler_symbol = 'simpler';
var const_invalid_hrefs = [];
var const_ignore_cache = [];
var bool_ezObjectExplainer_insideObject_stack = [];
var bool_ezObjectExplainer_insideObject_cache = [];
var const_defaultReason = 'WARNING: Cannot submit your request until all the information entered is correct and valid... Please correct and try again.';
function ezObjectExplainer(obj, bool_includeFuncs, _cnt) {
	var _db = '';
	var m = -1;
	var i = -1;
	var a = [];
	var cnt = ((_cnt == null) ? '1' : _cnt.toString() + '.0');
	bool_includeFuncs = ((bool_includeFuncs == true) ? bool_includeFuncs : false);
	
	function isCntComplex(c) {
		return (c.toString().indexOf('.') > -1);
	}
	
	_db = '';
	if ( (obj.toString != null) && ((typeof obj.toString) == const_function_symbol) && (obj.toString.toString().toLowerCase().indexOf(const_nativeCode_symbol) == -1) ) {
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
					if ((typeof obj[m]) == const_object_symbol) {
						a.push(m + ' = [' + ezObjectExplainer(obj[m], bool_includeFuncs, cnt) + ']');
					} else if ( ( (bool_includeFuncs) && ((typeof obj[m]) == const_function_symbol) ) || ( (!bool_includeFuncs) && ((typeof obj[m]) != const_function_symbol) ) ) {
						a.push(m + ' = [' + obj[m] + ']');
					}
				}
			}
			_db += a.join(((isCntComplex(cnt)) ? ',' : '\n'));
		} else if ( ( (bool_includeFuncs) && ((typeof obj) == const_function_symbol) ) || ( (!bool_includeFuncs) && ((typeof obj) != const_function_symbol) ) ) {
			_db += obj + '\n';
		}
	}
	return _db;
}
function destroy(oO) { var rV = -1; try { rV = oO.destructor(); } catch(e) { rV = null; } finally { rV = null; }; return rV; }
function uuid() {
	return (new Date().getTime() + "" + Math.floor(65535 * Math.random()));
}
function randN(maxVal,floatVal){
   var randVal = Math.random()*maxVal;
   return typeof floatVal=='undefined'?Math.round(randVal):randVal.toFixed(floatVal);
}
function randRange(minVal,maxVal,floatVal){
  var randVal = minVal+(Math.random()*(maxVal-minVal));
  return typeof floatVal=='undefined'?Math.round(randVal):randVal.toFixed(floatVal);
}
String.prototype.isAlpha = function (iLoc) {
    iLoc = ((!!iLoc) ? iLoc : 0);
    iLoc = ((iLoc < 0) ? 0 : iLoc);
    iLoc = ((iLoc > (this.length - 1)) ? this.length : iLoc);
    var _ch = this.substr(iLoc, 1);
    var b = ( (_ch.toLowerCase() >= 'a') && (_ch.toLowerCase() <= 'z') );
    return b;
}
String.prototype.alpha = function () {
    var t = '';
    for (var i = 0; i < this.length; i++) {
		if (this.isAlpha(i)) {
		    t += this.substr(i, 1);
		}
    }
    return t;
}
String.prototype.alphaNumeric = function () {
    var t = '';
    for (var i = 0; i < this.length; i++) {
		if ( (this.isAlpha(i)) || (this.isNumeric(i)) ) {
			t += this.substr(i, 1);
		}
    }
    return t;
}
String.prototype.isNumeric = function (iLoc) {
    iLoc = ((!!iLoc) ? iLoc : 0);
    iLoc = ((iLoc < 0) ? 0 : iLoc);
    iLoc = ((iLoc > (this.length - 1)) ? this.length : iLoc);
    var _ch = this.substr(iLoc, 1);
    var b = ( (_ch >= '0') && (_ch <= '9') );
    return b;
}
String.prototype.endsWith = function (s) {
    var t = this.substr(this.length-s.length, s.length);
    return t == s;
}
String.prototype.numeric = function () {
    var t = '';
    for (var i = 0; i < this.length; i++) {
		if (this.isNumeric(i)) {
		    t += this.substr(i, 1);
		}
    }
    return t;
}
String.prototype.removeWhiteSpace = function () {
    return this.replace(/^\s*|\s*$/g,'');
}
if (!Array.prototype.indexOf){
	Array.prototype.indexOf = function(elt /*, from*/) {
		var len = this.length;
		
		var from = Number(arguments[1]) || 0;
		from = (from < 0) ? Math.ceil(from) : Math.floor(from);
		if (from < 0){
			from += len;
		}
		
		for (; from < len; from++){
			if (from in this && this[from] === elt){
				return from;
			}
		}
		return -1;
	};
}
Date.prototype.getWeek = function (dowOffset) {
	dowOffset = typeof(dowOffset) == 'int' ? dowOffset : 0; //default dowOffset to zero
	var newYear = new Date(this.getFullYear(),0,1);
	var day = newYear.getDay() - dowOffset; //the day of week the year begins on
	day = (day >= 0 ? day : day + 7);
	var daynum = Math.floor((this.getTime() - newYear.getTime() - 
	(this.getTimezoneOffset()-newYear.getTimezoneOffset())*60000)/86400000) + 1;
	var weeknum;
	if(day < 4) {
		weeknum = Math.floor((daynum+day-1)/7) + 1;
		if(weeknum > 52) {
			nYear = new Date(this.getFullYear() + 1,0,1);
			nday = nYear.getDay() - dowOffset;
			nday = nday >= 0 ? nday : nday + 7;
			weeknum = nday < 4 ? 1 : 53;
		}
	}
	else {
		weeknum = Math.floor((daynum+day-1)/7);
	}
	return weeknum;
}
function milliseconds() {
var d = new Date();
return d.getTime();
}
function yyyy() {
	var d = new Date();
	return d.getFullYear();
}
function populateSelect(el, items) {
	debug_write('(populateSelect).BEGIN !');
	try {
	    el.options.length = 0;
	    el.options[0] = new Option('Choose...', '');
	
	    $.each(items, function () {
			debug_write('(populateSelect).1 -> this.text='+this.text+', this.value='+this.value);
	        el.options[el.options.length] = new Option(this.text, this.value);
	    });
	} catch (e) {debug_write('(populateSelect).ERROR '+e.toString());}
	debug_write('(populateSelect).END !');
}
var __cache__;
var __jsCache__ = {};
function $css(css_file){
	var d=document.getElementsByTagName('head')[0];
	var css=document.createElement('link');
	css.setAttribute('rel','stylesheet');
	css.setAttribute('type','text/css');
	css.setAttribute('href',css_file);
	d.appendChild(css);
	css.onreadystatechange=function(){
		if(css.readyState=='complete'){}
	}
	css.onload=function(){}
	return false;
}
function $onLoaded(file){
	var callback = __jsCache__[file];
	if ( (callback) && (typeof(callback) == const_function_symbol) ) {
		__jsCache__[file] = null;
		try {callback();} catch (e) {}
	}
}
function $js(file,callback){
	var b=false;
	var d=document.getElementsByTagName('head')[0];
	var js=document.createElement('script');
	js.setAttribute('type','text/javascript');
	js.setAttribute('src',file);
	d.appendChild(js);
	__jsCache__[file] = callback;
	var cb;
	if (js.readyState){
		js.onreadystatechange=function(){
			if (/loaded|complete/.test(js.readyState)){
				if (!b){
					b=true;
					cb = __jsCache__[file];
					if ( (cb) && (typeof(cb) == const_function_symbol) ) {
						__jsCache__[file] = null;
						try {cb();} catch (e) {}
					}
				}
				js.onreadystatechange = null;
			}
		}
	} else {
		js.onload=function(){
			if (!b){
				b=true;
				cb = __jsCache__[file];
				if ( (cb) && (typeof(cb) == const_function_symbol) ) {
					__jsCache__[file] = null;
					try {cb();} catch (e) {}
				}
			}
			js.onload = null;
			return;
		}
	}
	return false;
}
function $jsP(){
	var d=document.getElementsByTagName('head')[0];
	var js=document.createElement('script');
	js.setAttribute('type','text/javascript');
	js.setAttribute('id','$xajax');
	d.appendChild(js);
	return js;
}
var __jsp__ = $jsP();
//var __$frame__ = null;
function setCookie(name, value, path) {
	return document.cookie=name+"="+escape(value)+"; path="+path;
}
function getCookie(name) {
	var dc=document.cookie;
	var prefix=name+"=";
	var begin=dc.lastIndexOf(prefix);
	if(begin==-1) return null;
	var end=dc.indexOf(";", begin);
	if(end==-1) end=dc.length;
	return unescape(dc.substring(begin+prefix.length, end));
}
function deleteCookie(name, path) {
	document.cookie=name+"="+"; path="+path+"; expires=Thu, 01-Jan-70 00:00:01 GMT";
	return getCookie(name);
}
var _current_api = {};
var __is_running_local = (window.location.href.indexOf('127.0.0.1') > -1) || (window.location.href.indexOf('localhost') > -1);
var __is_running_secure = (window.location.href.indexOf('https://') > -1);
var __is_doing_login = false;
var __facebook_api_url = '';
var __fb = null;
var __is_not_ajax_ready = false;
var _current_user = -1;
var dt = new Date();
var nStyle = dt.getWeek(0) % 4;
$css('/static/styles/style'+nStyle+'.css');
var jquery_ui_styles = ['ui-darkness','dark-hive','eggplant','dot-luv'];
$css('/js/js/jquery/jquery-ui-1.8.2.custom/css/'+jquery_ui_styles[nStyle]+'/jquery-ui-1.8.2.custom.css');
$css('/js/js/jquery/alerts/jquery.alerts.css');
$css('/js/js/jquery/menus/apycom/menu.css');
$css('/js/js/jquery/jdialog/jquery.jdialog.css');
//$css('/js/js/jquery/AeroWindow/css/AeroWindow.css');
var __is_logged_in = false;
var _timer1 = -1;
var __counter__ = 0;
var __begin__ = 0;
var __logo__ = '';
var __timeout__ = (__is_running_local) ? 30000 : 10000;
var __activity_Offset__ = 0;
var __f_width__ = (__is_running_local) ? 850 : 820;
var __f_height__ = (__is_running_local) ? 280 : 200;
var __error_message__ = 'Something went wrong with the last request you issued.  Kindly give us some time to fix the problem and then try again.';
function debug_init() {
	if (__is_running_local) {
		var c = document.getElementById('__debug');
		if (c) {
			c.value = '';
		}
	}
}
function debug_write(s) {
	if (__is_running_local) {
		var c = document.getElementById('__debug');
		if (c) {
			c.value = s+'\n' + c.value;
		}
	}
}
function signalStop() {
	clearInterval(_timer1);
	_timer1 = -1;
	debug_write('STOP !');
}
function checkForFlash() {
	var c = document.getElementById('flashContainer');
	if (c) {
	var d = new Date();
	__counter__ = d.getTime() - __begin__;
	if (__counter__ > 5000) {
		onNoFlashInstalled();
		signalStop();
	}
	debug_write(d.getTime()+' :: __counter__='+__counter__);
	}
}
function onLoadSWFObject(){
	if ( (__onLoadSWFObject__) && (typeof(__onLoadSWFObject__) == const_function_symbol) ) {
		try {__onLoadSWFObject__();} catch (e) {debug_write('_onNoFlashInstalled().ERROR -> '+e.toString());}
	}
}
function onNoFlashInstalled() {
	var c = $('#flashContainer');
	if (c) {
		c.show();
		c.html('<img src="'+__logo__+'"/>');
		__activity_Offset__ = 0;
	}
	if ( (_onNoFlashInstalled) && (typeof(_onNoFlashInstalled) == const_function_symbol) ) {
		try {_onNoFlashInstalled();} catch (e) {debug_write('_onNoFlashInstalled().ERROR -> '+e.toString());}
	}
}
function showHelp(el,content){
	var vW = window.viewport.width();
	var vH = window.viewport.height();
	var cLeft = (vW/2)-(150);
	var cTop = 100;
	var cWidth = 500;
	var settings = {
		title : "<big>Online HELP</big>",
		content : (content) ? content : '<div id="div_HELP"></div><a id="a_hidden_help_link"></a>',
		width : cWidth
	};
	el.jDialog(settings);
	var dlg = $("#paneljDialog");
	if (dlg.length > 0){
		dlg.css({
			left: cLeft+'px',
			width: cWidth+'px',
			top: cTop+'px'
		});
	}
	debug_write('(showHelp).2 -> dlg.id='+dlg.attr('id'));
}
function hide_google_balls(){
	var act = $('#google_balls');
	if (act.length > 0){
	    act.hide();
	}
}
function get_google_balls(tTok){
	return '<div id="google_balls"><img src="/static/images/activity/googleballs.gif"/><BR/><STRONG>Negotiation <U>Secure</U> <span class="errorMessage">128-bit SSL</span> Connection</STRONG></div>';
}
function _parseForID(_id,_type,prefix) {
	var recID = null;
	var k = prefix+((_type) ? _type : '')+'_';
	var toks = _id.split(k);
	if (toks.length == 2) {
		recID = toks[toks.length-1];
	}
	return recID;
}
function parseEntryID(anId,ofType) {
	return _parseForID(anId,ofType,'a_entry');
}
function parseIdInto(anId,firstName) {
	var toks = anId.split('_');
	toks[0] = firstName;
	return $('#'+toks.join('_'));
}
function $formInputById(_formName,_id){
	return $("#"+_formName+" input[id='"+_id+"']");
}
function $formTextareaById(_formName,_id){
	return $("#"+_formName+" textarea[id='"+_id+"']");
}
function setBorderColor(obj,bool){
	obj.css({
		borderColor:(bool) ? "lime" : "red",
		borderStyle:"solid",
		borderWidth:"medium"
	});
}
function setBorderColorForIn(_obj,_bool){
	setBorderColor(_obj,_bool);
}
function showDialog(el,title,content,isPositioned){
	var _id = el.attr('id')
	var pos = anchorPosition.get$(_id);
	isPositioned = (isPositioned) ? true : false;
	var vW = window.viewport.width();
	var vH = window.viewport.height();
	var cLeft = (vW/2)-(250);
	var cTop = (isPositioned) ? pos.y : 100;
	var cWidth = 500;
	var settings = {
		title : title,
		content : content,
		width : 500
	};
	el.jDialog(settings);
	var dlg = $("#paneljDialog");
	if (dlg.length > 0){
		dlg.css({
			left: cLeft+'px',
			width: cWidth+'px',
			top: cTop+'px'
		});
	}
	debug_write('(showDialog).2 -> dlg.id='+dlg.attr('id'));
}
function adjustWindowLocationHref(info) {
	var toks = window.location.href.split('?');
	toks = toks[0].split('#');
	window.location.href = toks[0]+'#'+info;
}
function parseWindowLocationHref(sep) {
	var toks = window.location.href.split(sep);
	return toks[toks.length-1];
}
function parseExtra(extra) {
	var obj = {};
	var toks = extra.split('&');
	var toks2;
	for (var i in toks) {
		toks2 = toks[i].split('=');
		if (toks2.length == 2) {
			obj[toks2[0]] = toks2[toks2.length-1];
		}
	}
	return obj;
}
function onSuccessProxy(target,data,callback){
	try {
		target.html(data);
	} catch (e) {}
	debug_write(data);
	debug_write('(onSuccessProxy).1 -> data='+data);
	adjustAnchors();
	var cb = eval(callback);
	if ( (cb) && (typeof(cb) == const_function_symbol) ) {
		try {cb(data);} catch (e) {}
	}
}
function reloadPage(){
	window.location.href = '/';
}
function reloadInSecurePage(){
	window.location.href = 'http://'+window.location.host+'/';
}
function _ajax(url,target,info,callback,dataType) {
	var mayHaveAnchors = false;
	var isShowingAjaxActivity = false;
	var isDataTypeHTML = ( (!dataType) || (dataType == 'html') );
	debug_write('_ajax(url='+url+',target='+((target) ? target.attr('id') : '')+',info='+info+',callback='+(typeof(callback))+',dataType='+dataType+')');
	debug_write('(_ajax).1 -> isDataTypeHTML='+isDataTypeHTML);
	if ( (isDataTypeHTML) && (target) ) {
		isShowingAjaxActivity = true;
		target.html('<img src="/static/images/activity/ajax-loading.gif" border="0"/>');
	}
	debug_write('(_ajax).1a -> isShowingAjaxActivity='+isShowingAjaxActivity);
	function onSuccess(data){
		if (info) {
			adjustWindowLocationHref(info);
		}
		if ( (isDataTypeHTML) && (target) ) {
			if (target.length == 1) {
				target.html(data);
			} else {
				target.get(0).html(data);
			}
		}
		debug_write(data);
		if (target) {
			try {
				mayHaveAnchors = ( (target.attr('id') == 'column_left') || (target == 'column_left') );
				debug_write('(_ajax).2 -> target.id='+target.attr('id'));
			} catch (e) {}
			debug_write('(_ajax).3 -> isDataTypeHTML='+isDataTypeHTML+', mayHaveAnchors='+mayHaveAnchors);
			if ( (isDataTypeHTML) && (mayHaveAnchors) ) {
				adjustAnchors();
			}
		}
		debug_write('(_ajax).3a -> typeof(callback)='+typeof(callback));
		if ( (callback) && (typeof(callback) == const_function_symbol) ) {
			try {callback(data);} catch (e) {}
		}
	}
	var data = null;
	try {data = ( (__cache__) && (const_ignore_cache.indexOf(url) == -1) ) ? __cache__.getItem(url) : null;} catch (e){}
	if (data){
		onSuccess(data);
	} else {
		__xxx__ = getCookie('__xxx__');
		debug_write('(_ajax).1b -> isShowingAjaxActivity='+isShowingAjaxActivity);
		if (!isShowingAjaxActivity) {
			ajaxBusyShow();
		}
		$.ajax({
			url: url+((url.endsWith('/')) ? '' : '/')+__xxx__+'/',
			dataType: (dataType) ? dataType : "html",
			cache: false,
			timeout: __timeout__,
			success: function(data){
				ajaxBusyHide();
				try {
					__cache__.setItem(url, data, {	expirationAbsolute: null,   
													expirationSliding:60*10,   
													priority:CachePriority.High,  
													callback:function(k,v){}  
												});  				
				} catch (e) {}
				onSuccess(data);
			},
		  error: function(r,s,e){
			if (!isShowingAjaxActivity) {
				ajaxBusyHide();
			}
			debug_write('_ajax(url='+url+',target='+((target) ? target.attr('id') : '')+',info='+info+',callback='+(typeof(callback))+',dataType='+dataType+')');
			debug_write('(_ajax).ERROR r='+r+', s='+s+', e='+e);
			jAlert( __error_message__, 'ERROR -> '+s);
		  }
		});
	}
}
function _post(url,target,data,info,callback,dataType) {
	var mayHaveAnchors = false;
	__xxx__ = getCookie('__xxx__');
	if (target) {
		target.html('<img src="/static/images/activity/ajax-loading.gif" border="0"/>');
	} else {
		ajaxBusyShow();
	}
	$.ajax({
		url: url+((url.endsWith('/')) ? '' : '/')+__xxx__+'/',
		type: 'POST',
		data: data,
		cache: false,
		dataType: (dataType) ? dataType : "html",
		timeout: __timeout__,
		success: function(data){
			ajaxBusyHide();
			if (info) {
				adjustWindowLocationHref(info);
			}
			if (target) {
				if (target.length == 1) {
					target.html(data);
				}
				else {
					target.get(0).html(data);
				}
			}
			debug_write(data);
			try {
				mayHaveAnchors = ( (target.attr('id') == 'column_left') || (target == 'column_left') );
				debug_write('(_post).1 -> target.id='+target.attr('id'));
			} catch (e) {}
			if (mayHaveAnchors) {
				adjustAnchors();
			}
			if ( (callback) && (typeof(callback) == const_function_symbol) ) {
				try {callback(data);} catch (e) {}
			}
		},
	  error: function(r,s,e){
		ajaxBusyHide();
		debug_write('(_post).ERROR r='+r+', s='+s+', e='+e);
		jAlert( __error_message__, 'ERROR -> '+s);
	  }
	});
}
function ajaxBusyShow(){
	$('#ajaxBusy').show(); 
}
function ajaxBusyHide(){
	$('#ajaxBusy').hide();
}
onLogoutNow = function(){
	_ajax(_current_api['blog_rest_user_logout'],$('#column_left'),null,function(data){ top.location.href = _current_api['insecure_endpoint']; });
}
function getIsAjaxReady(){
	debug_write('(getIsAjaxReady).BEGIN !');
	var bool = __is_not_ajax_ready;
	for (var _i_ in const_invalid_hrefs) {
		debug_write('(getIsAjaxReady).1 -> const_invalid_hrefs['+_i_+']='+const_invalid_hrefs[_i_]);
		if (window.location.href.indexOf(const_invalid_hrefs[_i_]) > -1) {
			bool = true;
			debug_write('(getIsAjaxReady).1 -> bool='+bool);
			break;
		}
	}
	debug_write('(getIsAjaxReady).END !');
	return bool;
}
function getCurrentUser(wasClicked,callback){
	var isCached = false;
	var hasCurrentAPI = (_current_user['__api__'] != null) ? 1 : 0;
	var brgu = '/'+['blog','rest','get','user'].join('/')+'/';
	debug_write('(getCurrentUser) -> hasCurrentAPI='+hasCurrentAPI);
	_ajax(brgu+hasCurrentAPI+'/',$('#column_left'),null,function(data){
																				//_groups = []
																				//_date_joined = "19 Jun 2010 11:33:37"
																				//_username = "your-user-name"
																				//_is_superuser = True
																				//_first_name = "First"
																				//_parent_key = null
																				//_is_staff = True
																				//_last_login = "20 Jun 2010 11:05:18"
																				//_last_name = "Name"
																				//_user_permissions = []
																				//_email = "your-email@domain.com"
																				//_app = null
																				//_is_active = True
																				// FBID = facebook app id
		_current_user = data;
		_current_api = (_current_user['__api__']) ? _current_user['__api__'] : _current_api;
		debug_write('(getCurrentUser) -> window.location.href='+window.location.href);
		debug_write('(getCurrentUser) -> _current_api='+ezObjectExplainer(_current_api));
		debug_write('(getCurrentUser) -> secure_endpoint='+_current_api['secure_endpoint']);
		__is_doing_login = (window.location.href.indexOf(_current_api['blog_rest_user_login']) > -1);
		__facebook_api_url = _current_api['facebook_api_url']; //(__is_running_local) ? _current_api['facebook_api'] : _current_api['facebook_api_url'];
		const_invalid_hrefs = [_current_api['account_activate'],'/create_admin_user/',_current_api['account_password'],_current_api['blog_sitemap'],_current_api['blog_link'],_current_api['blog_nav']];
		const_ignore_cache = [_current_api['blog_rest_get_admin'],brgu,_current_api['blog_rest_user_logout'],_current_api['blog_rest_user_login']]; // _current_api['blog_rest_user_feedback']
		__is_logged_in = (_current_user['_is_active']) && (_current_user['_first_name']) && (_current_user['_last_name']) && (_current_user['_date_joined']) && (_current_user['_email']);
		__is_logged_in = (__is_logged_in) ? __is_logged_in : false;
		debug_write('(getCurrentUser) -> __is_logged_in='+__is_logged_in);
		debug_write(ezObjectExplainer(_current_user));
		__is_not_ajax_ready = getIsAjaxReady();
		if (__is_logged_in) {
			if (!__is_not_ajax_ready) {
				//getArticles();
			}
		} else {
			if (__is_running_secure) {
				reloadInSecurePage(); // break-out of https:// when not logged-in...
			}
		}
		if ( (callback) && (typeof(callback) == const_function_symbol) ) {
			try {callback(__is_logged_in,wasClicked,_current_user);} catch (e) {}
		}
	},'json');
}
onClickSubmitFeedback = function(){
	var subject = $formInputById('formFeedback','id_subject').attr('value');
	var message = $formTextareaById('formFeedback','id_message').val();
	debug_write('(onClickSubmitFeedback) :: subject='+subject+', message='+message);
	if ( (subject) && (subject.length > 0) && (message) && (message.length > 0) ) {
		_post(_current_api['blog_rest_user_feedback'],$('#formFeedback'),{subject:subject,message:message},null,adjustFeedbackForm);
	} else {
		//jAlert(const_defaultReason);
	}
}
function adjustFeedbackForm(){
	debug_write('(adjustFeedbackForm).BEGIN !');
	try {
		var btn = $('#btn_submitFeedback');
		if (btn.length > 0) {
			btn.click(onClickSubmitFeedback);
			$formTextareaById('formFeedback','id_message').attr('rows',8);
		}
	} catch (e) {
		debug_write('(adjustFeedbackForm).ERROR '+e.toString());
	}
	debug_write('(adjustFeedbackForm).END !');
}
function getFeedbackContent(){
	debug_write('(getFeedbackContent) !');
	_ajax(_current_api['blog_rest_user_feedback'],$('#column_left'),null,adjustFeedbackForm);
}
onClickPopulateFeedback = function(){
	debug_write('(onClickPopulateFeedback) !');
	getFeedbackContent();
}
function getSponsorContent(){
	debug_write('(getSponsorContent) !');
	_ajax(_current_api['blog_rest_user_sponsor'],$('#column_left'),null,function(){});
}
onClickPopulateSponsor = function(){
	debug_write('(onClickPopulateSponsor) !');
	getSponsorContent();
}
function initTabs(){
	var tabs = $("#tabs");
	if (tabs.length > 0) {
		tabs.tabs();
	}
}
function initDialog(){
	var dialogs = $('#dialog');
	if (dialogs.length > 0) {
		dialogs.dialog({
			autoOpen: false,
			show: 'blind',
			hide: 'explode',
			modal: true,
			position: 'center',
			resizable: false,
			closeOnEscape: true,
			buttons: { "Dismiss": function() { $(this).dialog("close"); } }
		});
	}
}
//__onCrossDomain__ = function (){
//	var frm=document.body.appendChild(document.createElement('IFRAME'));
//	frm.id='xajax';
//	frm.width='0px';
//	frm.height='0px';
//	frm.marginWidth='0';
//	frm.marginHeight='0';
//	frm.scrolling='no';
//	return frm;
//}
function disableContextMenu(){
	var m$=""; 
	function cIE() { 
		if (document.all) {
			(m$); 
			return false;
		}
	}; 
	function cNS(e) { 
		if (document.layers||(document.getElementById&&!document.all)) {
			if (e.which==2||e.which==3) { 
				(m$); 
				return false;
			}
		}
	}; 
	if (document.layers) { 
		document.captureEvents(Event.MOUSEDOWN); 
		document.onmousedown=cNS; 
	} else { 
		document.onmouseup=cNS; 
		document.oncontextmenu=cIE; 
	}; 
	document.oncontextmenu = new Function("return false");
}
var __is_onDocumentReady__ = false;
__onDocumentReady__ = function () {
	disableContextMenu();
	//__onCrossDomain__();
	//__$frame__ = $('#xajax');
	if (__isOptimized__){
		$js('/js/js/flash_detect.min.js',function(){ 
			if (FlashDetect.installed) { 
				debug_write('+++ FlashDetect.revisionStr='+FlashDetect.revisionStr+', FlashDetect.raw='+FlashDetect.raw+', FlashDetect.major='+FlashDetect.major+', FlashDetect.minor='+FlashDetect.minor+', BrowserDetect.browser='+BrowserDetect.browser+', BrowserDetect.version='+BrowserDetect.version+', BrowserDetect.OS='+BrowserDetect.OS);
				$js('/js/js/swfObject.min.js',function(){ 
					$js('/js/js/rightClick.min.js',function(){
						if (!__is_running_local) {
							onLoadSWFObject();
						}
					}) 
				}); 
			} else { 
				if ( (onNoFlashInstalled) && (typeof(onNoFlashInstalled) == const_function_symbol) ) {
					try {onNoFlashInstalled();} catch (e) {}
				}
			} 
		}); 
	} else {
		if (FlashDetect.installed) { 
			debug_write('+++ FlashDetect.revisionStr='+FlashDetect.revisionStr+', FlashDetect.raw='+FlashDetect.raw+', FlashDetect.major='+FlashDetect.major+', FlashDetect.minor='+FlashDetect.minor+', BrowserDetect.browser='+BrowserDetect.browser+', BrowserDetect.version='+BrowserDetect.version+', BrowserDetect.OS='+BrowserDetect.OS);
			if (!__is_running_local) {
				onLoadSWFObject();
			}
		} else { 
			if ( (onNoFlashInstalled) && (typeof(onNoFlashInstalled) == const_function_symbol) ) {
				try {onNoFlashInstalled();} catch (e) {}
			}
		} 
	}
	window.viewport={height:function(){return $(window).height();},width:function(){return $(window).width();},scrollTop:function(){return $(window).scrollTop();},scrollLeft:function(){return $(window).scrollLeft();}};
//	$(document).ajaxStart(function(){
//		ajaxBusyShow(); 
//	}).ajaxStop(function(){ 
//		ajaxBusyHide();
//	});
	initTabs();
	initDialog();
	debug_init();
	debug_write('__isOptimized__='+__isOptimized__);
	if ( (_onDocumentReady) && (typeof(_onDocumentReady) == const_function_symbol) ) {
		try {_onDocumentReady();} catch (e) {debug_write('_onDocumentReady().ERROR -> '+e.toString());}
	}
	debug_write('__is_running_local='+__is_running_local);
	if (__is_running_local) {
		var dC = $('#__debugContainer');
		if (dC.length > 0){
			dC.show();
		} else {
			debug_write('__debugContainer.WARNING -> Missing __debugContainer !');
		}
		var dT = $('#__debug');
		if (dT.length > 0){
			dT.attr('rows',30);
		} else {
			debug_write('__debug.WARNING -> Missing __debug !');
		}
	}
};

var __isOptimized__ = ((BrowserDetect.browser == 'Firefox') && (BrowserDetect.version >= 3.5)) || ((BrowserDetect.browser == 'Chrome') && (BrowserDetect.version >= 5.0));
if (__isOptimized__){
	$js('/js/js/csshttprequest.min.js', function(){});
	$js('/js/js/anchorPosition.min.js', function(){});
	$js('/js/js/cache.min.js', function(){__cache__ = new Cache();});
	$js('http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js', function(){
		$js('http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js', function(){});
		$js('/js/js/jquery/feedreader/feedreader.min.js', function(){});
		$js('/js/js/jquery/alerts/jquery.alerts.min.js', function(){});
		$js('/js/js/jquery/jdialog/jquery.jdialog.min.js', function(){});
		$js('/js/js/jquery/menus/apycom/menu.min.js', function(){});
		$(document).ready(function(){
			__onDocumentReady__();
			__is_onDocumentReady__ = true;
		}); 
	});
}
window.onload = function (){
	if ( (__onWindowLoad) && (typeof(__onWindowLoad) == const_function_symbol) ) {
		try {__onWindowLoad();} catch (e) {debug_write('(__onWindowLoad).ERROR '+e.toString());}
	}
	if (!__is_onDocumentReady__){
		__onDocumentReady__();
		__is_onDocumentReady__ = true;
	}
}
