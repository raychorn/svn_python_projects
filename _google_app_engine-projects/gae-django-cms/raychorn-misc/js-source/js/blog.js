/*!
 * VyperBlog(tm) v1.0.0
 * http://www.vyperlogix.com/
 *
 * Copyright 2010, Vyper Logix Corp.
 * Licensed under the GNU General Public License version 3 (GPLv3).
 * http://www.opensource.org/licenses/gpl-3.0.html
 *
 * Date: Sun Jun 13 22:00:04 2010 -0700
 */
var const_getAbout = 'get=about';
var const_getCategories = 'get=categories';
var const_getTags = 'get=tags';
var const_getLanguages = 'get=languages';
var const_getLoginRegister = 'get=loginRegister';
var const_getLogin = 'get=login';
var const_getRegister = 'get=register';
var _has_clicked_submitRegister = false;
var _timer2 = -1;
function checkForDocumentReady() {
	debug_write('(checkForDocumentReady).1 -> '+__is_onDocumentReady__);
	if (__is_onDocumentReady__) {
		debug_write('(clearInterval(_timer2)).1 !');
		clearInterval(_timer2);
		_timer2 = -1;
		try {onDocumentReady();} catch(e){debug_write('onDocumentReady().ERROR.2 -> '+e.toString());}
	}
}
function __onLoadSWFObject__(){
	var s=generate_flash_content(10,1,0,'/static/swf/SwfLoader/SwfLoader.swf?swf=2F7374617469632F7377662F7377664C6F676F2F766C634C6F676F2E737766&width='+(__f_width__-50)+'&height='+(__f_height__-0)+'&c=flashContainer',__f_width__,__f_height__,'vlcLogo','vlcLogo','white','/',__logo__,'RayCHorn.Com&copy;GPLv3'); 
	var c = $('#flashContainer');
	if (c) {
		c.html(s);
		RightClick.init('vlcLogo2','flashContainer');
		var d = new Date();
		__begin__ = d.getTime();
		_timer1 = setInterval('checkForFlash()',1000);
		__activity_Offset__ = 330;
	}
	if ( (_onLoadSWFObject) && (typeof(_onLoadSWFObject) == const_function_symbol) ) {
		try {_onLoadSWFObject();} catch (e) {debug_write('_onLoadSWFObject().ERROR -> '+e.toString());}
	}
}
function loadAIRBadge(){
	flashVars = {appname:'',appurl:airApplicationURL,airversion:airVersion,buttoncolor:'FF0000',messagecolor:'ffffff',imageurl:airApplicationImage};
	var s=generate_flash_content(10,1,0,'/static/air/badge.swf',400,300,'airBadge','airBadge','white','/',airApplicationImage,'RayCHorn.Com&copy;GPLv3',flashVars); 
	var c = $('#airBadgeContainer');
	if (c) {
		c.html(s);
	}
}
onClickMain = function () {
	var _id = $(this).attr('id');
	if (_id == 'a_Home') {
		if (__is_not_ajax_ready){
			window.location.href = '/';
		} else {
			getArticles();
		}
	} else if (_id == 'a_About') {
		if (__is_not_ajax_ready){
			window.location.href = '/#'+const_getAbout;
		} else {
			getAbout();
		}
	} else if (_id == 'a_Categories') {
		if (__is_not_ajax_ready){
			window.location.href = '/#'+const_getCategories;
		} else {
			getCategories();
		}
	} else if (_id == 'a_Tags') {
		if (__is_not_ajax_ready){
			window.location.href = '/#'+const_getTags;
		} else {
			getTags();
		}
	} else if (_id == 'a_Languages') {
		if (__is_not_ajax_ready){
			window.location.href = '/#'+const_getLanguages;
		} else {
			getLanguages();
		}
	} else if (_id == 'a_LoginRegister') {
		if (__is_not_ajax_ready){
			window.location.href = '/#'+const_getLoginRegister;
		} else {
			getUserRegisterForm();
		}
	} else if (_id == 'a_Login') {
		if (__is_not_ajax_ready){
			window.location.href = '/#'+const_getLogin;
		} else {
			getUserLoginForm();
		}
	} else if (_id == 'a_Admin') {
		getUserAdmin();
	} else if (_id == 'a_Register') {
		if (__is_not_ajax_ready){
			window.location.href = '/#'+const_getRegister;
		} else {
			getUserRegisterForm();
		}
	}
}
var _isRssFeedUrlValid = false;
var _isVerificationValid = false;
function init_rss_feeds_validations(){
	_isRssFeedUrlValid = false;
}
function init_verification_validations(){
	_isVerificationValid = false;
}
function adjustRssFeedSelect(){
	var selects = $('#dialog #tabs #s_rssfeeds');
	debug_write('(adjustRssFeedSelect).1 -> selects.length='+selects.length);
	if (selects.length > 0){
		selects.each(function(index) {
			$(this).change(onChangeRssFeedSelect);
		});
	}
}
function adjustRemoveRssFeedButton(disableOnly){
	debug_write('adjustRemoveRssFeedButton.BEGIN !');
	var btns = $('#dialog #tabs #btn_removeRssFeed');
	disableOnly = (disableOnly) ? true : false;
	debug_write('(adjustRemoveRssFeedButton).1 -> btns.length='+btns.length);
	try {
		if (btns.length > 0){
			btns.each(function(index) {
				$(this).attr("disabled", "disabled");
				if (!disableOnly){
					$(this).click(onClickRemoveRssFeed);
				}
			});
		}
	} catch (e) {debug_write('(adjustRemoveRssFeedButton) -> ERROR.2: '+e.toString());}
	debug_write('adjustRemoveRssFeedButton.END !');
}
function adjustRemoveVerificationButton(disableOnly){
	debug_write('adjustRemoveVerificationButton.BEGIN !');
	var btns = $('#dialog #tabs #btn_removeVerification');
	disableOnly = (disableOnly) ? true : false;
	debug_write('(adjustRemoveVerificationButton).1 -> btns.length='+btns.length);
	try {
		if (btns.length > 0){
			btns.each(function(index) {
				if (!disableOnly){
					$(this).click(onClickRemoveVerification);
				} else {
					$(this).attr("disabled", "disabled");
				}
			});
		}
	} catch (e) {debug_write('(adjustRemoveVerificationButton) -> ERROR.2: '+e.toString());}
	debug_write('adjustRemoveVerificationButton.END !');
}
function adjustSubmitRssFeedButton(disableOnly){
	debug_write('(adjustSubmitRssFeedButton).BEGIN !');
	var btns = $('#dialog #tabs #formAddRssFeed #btn_submitRssFeed');
	disableOnly = (disableOnly) ? true : false;
	debug_write('(adjustSubmitRssFeedButton).1 -> btns.length='+btns.length);
	try {
		if (btns.length > 0){
			btns.each(function(index) {
				$(this).attr("disabled", "disabled");
				if (!disableOnly) {
					$(this).click(onClickSubmitRssFeed);
				}
			});
		}
	} catch (e) {debug_write('(adjustSubmitRssFeedButton) -> ERROR.2: '+e.toString());}
	debug_write('(adjustSubmitRssFeedButton).END !');
}
onClickSubmitVerification = function (){
	debug_write('(onClickSubmitVerification).BEGIN !');
	adjustSubmitRssFeedButton(true);
	var divs;
	try {
		var inputs = $('#dialog #tabs #formAddVerification #id_content');
		debug_write('(onClickSubmitVerification).1 -> inputs.length='+inputs.length);
		if (inputs.length > 0) {
			inputs.each(function () {
				var content = $(this).attr('value');
 				$(this).attr('value','');
				debug_write('(onClickSubmitVerification).3 -> content='+content);
				divs = $("#dialog #tabs #div_siteVerification");
				debug_write('(onClickSubmitVerification).4 -> divs.length='+divs.length);
				_post(_current_api['blog_rest_post_verification'],divs,{content:content},null,function(data){handle_formAddVerification_display();adjustSubmitVerificationButton();});
			});
		}
	} catch (e) {debug_write('(onClickSubmitVerification).ERROR '+e.toString());}
	debug_write('(onClickSubmitVerification).END !');
}
function adjustSubmitVerificationButton(disableOnly){
	debug_write('(adjustSubmitVerificationButton).BEGIN !');
	var btns = $('#dialog #tabs #formAddVerification #btn_submitVerification');
	disableOnly = (disableOnly) ? true : false;
	debug_write('(adjustSubmitVerificationButton).1 -> btns.length='+btns.length);
	try {
		if (btns.length > 0){
			btns.each(function(index) {
				$(this).attr("disabled", "disabled");
				if (!disableOnly) {
					$(this).click(onClickSubmitVerification);
				}
			});
		}
	} catch (e) {debug_write('(adjustSubmitVerificationButton) -> ERROR.2: '+e.toString());}
	debug_write('(adjustSubmitVerificationButton).END !');
}
onClickSubmitRssFeed = function (){
	debug_write('(onClickSubmitRssFeed).BEGIN !');
	adjustSubmitRssFeedButton(true);
	var divs;
	try {
		var inputs = $('#dialog #tabs #formAddRssFeed #id_url');
		debug_write('(onClickSubmitRssFeed).1 -> inputs.length='+inputs.length);
		if (inputs.length > 0) {
			inputs.each(function () {
				var url = $(this).attr('value');
				divs = $("#dialog #tabs #div_rssfeed_test");
				debug_write('(onClickSubmitRssFeed).2 -> divs.length='+divs.length);
 				$(this).attr('value','');
				debug_write('(onClickSubmitRssFeed).3 -> url='+url);
				divs = $("#dialog #tabs #div_rssfeeds");
				debug_write('(onClickSubmitRssFeed).4 -> divs.length='+divs.length);
				_post(_current_api['blog_rest_post_rssfeed'],divs,{url:url},null,function(data){adjustRssFeedSelect();adjustRemoveRssFeedButton();});
			});
		}
	} catch (e) {debug_write('(onClickSubmitRssFeed).ERROR '+e.toString());}
	debug_write('(onClickSubmitRssFeed).END !');
}
onClickRemoveRssFeed = function(){
	debug_write('(onClickRemoveRssFeed).BEGIN !');
	adjustRemoveRssFeedButton(true);
	try {
		var t = '';
		var v = '';
		$("#dialog #tabs #div_rssfeeds #s_rssfeeds option:selected").each(function () {
		    t = $(this).text();
		    v = $(this).val();
		});
		var hasSelection = ( (v) && (t) );
		debug_write('(onClickRemoveRssFeed) -> t='+t+', v='+v);
		var divs = $("#dialog #tabs #div_rssfeeds");
		debug_write('(onClickSubmitRssFeed).4 -> divs.length='+divs.length);
		_post(_current_api['blog_rest_remove_rssfeed'],divs,{url:v},null,function(data){adjustRssFeedSelect();adjustRemoveRssFeedButton()});
	} catch (e) {debug_write('(onClickRemoveRssFeed).ERROR '+e.toString());}
	debug_write('(onClickRemoveRssFeed).END !');
}
function isVerificationsPopulated(){
	debug_write('(isVerificationsPopulated).BEGIN !');
	var isVerificationsPopulated = false;
	try {
		var iCount = 0;
		$("#dialog #tabs #div_siteVerification #s_verifications option").each(function () {
		    iCount++;
		});
		var isVerificationsPopulated = (iCount > 0);
		debug_write('(isVerificationsPopulated) -> isVerificationsPopulated='+isVerificationsPopulated);
	} catch (e) {debug_write('(isVerificationsPopulated).ERROR '+e.toString());}
	debug_write('(isVerificationsPopulated).END !');
	return isVerificationsPopulated;
}
function handle_formAddVerification_display(){
	var forms = $('#formAddVerification');
	var selects = $("#dialog #tabs #div_siteVerification #s_verifications");
	var btns = $('#dialog #tabs #btn_removeVerification');
	if (forms.length > 0) {
		if (isVerificationsPopulated()) {
			forms.hide();
			selects.each(function () {
			    $(this).show();
			});
			btns.each(function () {
			    $(this).show();
			});
			adjustRemoveVerificationButton();
		} else {
			forms.show();
			selects.each(function () {
			    $(this).hide();
			});
			btns.each(function () {
			    $(this).hide();
			});
		}
		if (!isVerificationsPopulated()) {
			$formInputById('formAddVerification','id_content').attr('autocomplete','off').keyup(function(event) {
				handle_checkVerification($(this));
				if (event.keyCode == '13') {
					 //event.preventDefault();
				}
			});
			_checkVerification();
		}
	}
}
onClickRemoveVerification = function(){
	debug_write('(onClickRemoveVerification).BEGIN !');
	adjustRemoveVerificationButton(true);
	try {
		var t = '';
		var v = '';
		$("#dialog #tabs #div_siteVerification #s_verifications option:selected").each(function () {
		    t = $(this).text();
		    v = $(this).val();
		});
		var hasSelection = ( (v) && (t) );
		debug_write('(onClickRemoveVerification) -> t='+t+', v='+v);
		var divs = $("#dialog #tabs #div_siteVerification");
		debug_write('(onClickRemoveVerification).4 -> divs.length='+divs.length);
		_post(_current_api['blog_rest_remove_verification'],divs,{id:v,content:t},null,function(data){handle_formAddVerification_display();adjustRemoveVerificationButton();});
	} catch (e) {debug_write('(onClickRemoveVerification).ERROR '+e.toString());}
	debug_write('(onClickRemoveVerification).END !');
}
onChangeRssFeedSelect = function(){
	var t = '';
	var v = '';
	$("#dialog #tabs #s_rssfeeds option:selected").each(function () {
	    t = $(this).text();
	    v = $(this).val();
	});
	var hasSelection = ( (v) && (t) );
	var _id = $(this).attr('id');
	debug_write('(onChangeRssFeedSelect) -> _id='+_id+', t='+t+', v='+v);
	var btns = $('#dialog #tabs #btn_removeRssFeed');
	btns.each(function(index) {
		$(this).attr("disabled", "disabled");
		if (hasSelection) {
			$(this).removeAttr("disabled");
		}
	});
}
function checkRssFeedUrl(value){
	var isListed = false;
	var t, v, toks, tT, vT;
	toks = value.split('/');
	vT = toks.join('');
	debug_write('(checkRssFeedUrl).1 -> value='+value+', vT='+vT);
	$("#dialog #tabs #div_rssfeeds #s_rssfeeds option").each(function () {
		t = $(this).text();
		toks = t.split('/');
		tT = toks.join('');
		debug_write('(checkRssFeedUrl).2 -> value='+value+', t='+t+', tT='+tT);
		if (vT == tT){
			isListed = true;
			debug_write('(checkRssFeedUrl).3 -> isListed='+isListed+', t='+t);
		}
	});
	if (!isListed){
		var bool = (value.match(/\b(https?):\/\/([\-A-Z0-9.]+)(\/[\-A-Z0-9+&@#\/%=~_|!:,.;]*)?(\?[A-Z0-9+&@#\/%=~_|!:,.;]*)?/gi)) && (value.indexOf(_current_api['secure_endpoint']) == -1) && (value.indexOf(_current_api['insecure_endpoint']) == -1);
		debug_write('(checkRssFeedUrl).4 -> bool='+bool);
	}
	return bool;
}
function checkVerification(value){
	return (value.match(/^[\w'_]+\s?[\w'_]+$/gi));
}
function checkSubmitRssFeedValidity() {
	debug_write('(checkSubmitRssFeedValidity).1 -> _isRssFeedUrlValid='+_isRssFeedUrlValid);
	var btns = $('#dialog #tabs #formAddRssFeed #btn_submitRssFeed');
	btns.each(function(index) {
		$(this).attr("disabled", "disabled");
		if (_isRssFeedUrlValid) {
			$(this).removeAttr("disabled");
		}
	});
}
function checkSubmitVerificationValidity() {
	debug_write('(checkSubmitVerificationValidity).1 -> _isVerificationValid='+_isVerificationValid);
	var btns = $('#dialog #tabs #formAddVerification #btn_submitVerification');
	btns.each(function(index) {
		$(this).attr("disabled", "disabled");
		if (_isVerificationValid) {
			$(this).removeAttr("disabled");
		}
	});
}
function handle_checkRssFeedUrl(_obj){
	_isRssFeedUrlValid = checkRssFeedUrl(_obj.attr('value'));
	debug_write('(handle_checkRssFeedUrl).1 -> _isRssFeedUrlValid='+_isRssFeedUrlValid);
	checkSubmitRssFeedValidity();
	setBorderColorForIn(_obj,_isRssFeedUrlValid);
	return _isRssFeedUrlValid;
}
function _checkRssFeedUrl(){
	return handle_checkRssFeedUrl($formInputById('formAddRssFeed','id_url'));
}
function handle_checkVerification(_obj){
	_isVerificationValid = checkVerification(_obj.attr('value'));
	debug_write('(handle_checkVerification).1 -> _isVerificationValid='+_isVerificationValid);
	checkSubmitVerificationValidity();
	setBorderColorForIn(_obj,_isVerificationValid);
	return _isVerificationValid;
}
function _checkVerification(){
	return handle_checkVerification($formInputById('formAddVerification','id_content'));
}
var _rssfeed_elements = ['id_url'];
function adjustRssFeedAdminForm(){
	debug_write('adjustRssFeedAdminForm.BEGIN !');
	adjustRssFeedSelect();
	adjustRemoveRssFeedButton();
	adjustSubmitRssFeedButton();
	adjustSubmitVerificationButton();
	adjustRemoveVerificationButton();
	try {
		$formInputById('formAddRssFeed','id_url').attr('autocomplete','off').keyup(function(event) {
			handle_checkRssFeedUrl($(this));
			if (event.keyCode == '13') {
				 //event.preventDefault();
			}
		});
		_checkRssFeedUrl();
		handle_formAddVerification_display();
	} catch (e) {debug_write('(adjustLoginForm) -> ERROR.1: '+e.toString());}
	debug_write('adjustRssFeedAdminForm.END !');
}
function getUserAdmin(){
	var dialogs = $('#dialog');
	if (dialogs.length > 0) {
		dialogs.dialog( "option", "height", window.viewport.height()-100 );
		dialogs.dialog( "option", "width", window.viewport.width()-100 );
		dialogs.dialog('open');
		_ajax(_current_api['blog_rest_get_admin'],dialogs,'',adjustAdminPage);
	}
}
function adjustAdminPage(){
	init_rss_feeds_validations();
	init_verification_validations();
	debug_write('(adjustAdminPage).BEGIN !');
	var tabs = $("#dialog #tabs");
	debug_write('(adjustAdminPage).1 -> tabs.length='+tabs.length);
	tabs.tabs();
	adjustRssFeedAdminForm();
	loadAIRBadge();
	debug_write('(adjustAdminPage).END !');
}
function adjustAnchors() {
	var _id, _val;
	var anchors = $("#column_left").find("a");
	debug_write('(adjustAnchors).1 anchors.length='+anchors.length);
	anchors.each(function(index) {
		_id = $(this).attr('id');
		debug_write('(adjustAnchors).2 _id='+_id);
		try {
			_val = parseEntryID(_id);
			debug_write('(adjustAnchors).3 _val='+_val);
			if (_val) {
				$(this).click(onClickArticle);
			}
			_val = parseEntryID(_id,'Tag');
			debug_write('(adjustAnchors).4 _val='+_val);
			if (_val) {
				$(this).click(onClickArticleTag);
			}
			_val = parseEntryID(_id,'Language');
			debug_write('(adjustAnchors).5 _val='+_val);
			if (_val) {
				$(this).click(onClickArticleLanguage);
			}
			_val = parseEntryID(_id,'Category');
			debug_write('(adjustAnchors).6 _val='+_val);
			if (_val) {
				$(this).click(onClickArticleCategory);
			}
			_val = parseEntryID(_id,'Details');
			debug_write('(adjustAnchors).7 _val='+_val);
			if (_val) {
				$(this).click(onClickArticleDetails);
			}
			_val = parseEntryID(_id,'Comments');
			debug_write('(adjustAnchors).8 _val='+_val);
			if (_val) {
				$(this).click(onClickArticleComments);
			}
			_val = parseEntryID(_id,'MORE');
			debug_write('(adjustAnchors).8 _val='+_val);
			if (_val) {
				$(this).click(onClickArticleMore);
			}
		} catch (e) {jAlert(e.toString() ,'ERROR ! ');}
	});
}
function onClickTab(){
	var _href = $(this).attr('href');
	debug_write('(onClickTab) -> _href='+_href);
	$('#'+_href.replace('#','')).show();
}
onClickSubmitResendRegister = function(){
	var email = $formInputById('formResendRegister','id_email').attr('value');
	debug_write('(onClickSubmitResendRegister) :: email='+email);
	if (_isEmailAddrsValid){
		_post(_current_api['blog_rest_resend_register'],$('#column_left'),{email:email},null,adjustResendRegisterForm);
	} else {
		jAlert(const_defaultReason);
	}
}
var isOnProcessContent = false;
function onProcessContent(){
	var extraObj = parseExtra(parseWindowLocationHref('#'));
	var _article = extraObj['article'];
	var _get = extraObj['get'];
	var _tag = extraObj['tag'];
	var _category = extraObj['category'];
	var _language = extraObj['language'];
	var _getAbout = const_getAbout.split('=');
	var _getCategories = const_getCategories.split('=');
	var _getTags = const_getTags.split('=');
	var _getLanguages = const_getLanguages.split('=');
	var _getLoginRegister = const_getLoginRegister.split('=');
	var _getLogin = const_getLogin.split('=');
	var _getRegister = const_getRegister.split('=');
	if (_article) {
		getOneArticle(_article);
	} else if (_get == _getAbout[_getAbout.length-1]) {
		getAbout();
	} else if (_get == _getCategories[_getCategories.length-1]) {
		getCategories();
	} else if (_get == _getTags[_getTags.length-1]) {
		getTags();
	} else if (_get == _getLanguages[_getLanguages.length-1]) {
		getLanguages();
	} else if (_get == _getLoginRegister[_getLoginRegister.length-1]) {
		getUserRegisterForm();
	} else if (_get == _getLogin[_getLogin.length-1]) {
		getUserRegisterForm();
	} else if (_get == _getRegister[_getRegister.length-1]) {
		getUserRegisterForm();
	} else if (_tag) {
		getOneTaggedArticles(_tag);
	} else if (_category) {
		getOneCategoryArticles(_category);
	} else if (_language) {
		getOneLanguageArticles(recID);
	} else {
		debug_write('__is_not_ajax_ready='+__is_not_ajax_ready);
		if (!__is_not_ajax_ready){
			getArticles();
		} else if (window.location.href.indexOf(_current_api['account_password']) > -1) {
			adjustForgotPasswordForm();
		}
	}
	isOnProcessContent = true;
}
onFaceBookAPI = function(){
	debug_write('(onFaceBookAPI) !');
	try {
		try {
		__fb = (__is_running_local) ? FB.get$() : FB;
		} catch (e) {
		__fb = FB;
		}
		debug_write('(onFaceBookAPI) -> BEGIN: FaceBook Init -> FBID='+_current_user['FBID']);
		__fb.init({appId: _current_user['FBID'], status: true, cookie: true, xfbml: true});
		debug_write('(onFaceBookAPI) -> END:   FaceBook Init -> FBID='+_current_user['FBID']);
		var aDiv = $('#user-ident #user-facebook');
		if (aDiv.length > 0){
			aDiv.html('<b><a id="a_faceBookLogin" href="#">FaceBook Login</a>');
			$('#a_faceBookLogin').click(onClickSubmitFaceBookLogin);
		}
	} catch (e) {jAlert(e.toString() ,'onFaceBookAPI.ERROR !');}
}
onGetUser = function(is_logged_in,wasClicked,current_user){
	if (!isOnProcessContent) {
		onProcessContent();
	}
	if (is_logged_in){
		var aName = current_user['_first_name']+' '+current_user['_last_name'];
		var is_superuser = current_user['_is_superuser'];
		$('#user-ident #user-welcome').html('Welcome back, <b>'+aName+'</b>&nbsp;&nbsp;(<small><b><a id="a_logoutNow" href="#">Logout</a></b></small>)'+((is_superuser) ? '&nbsp;|&nbsp;<a id="a_AdminNow" href="#"><B>Admin</B></a>' : ''));
		$('#a_logoutNow').click(onLogoutNow);
		$('#a_AdminNow').click(getUserAdmin);
		if (wasClicked){
			window.location.href = '/';
		}
	} else {
		if (wasClicked){
			window.location.href = '/';
		}
		$('#user-ident #user-login').html('<b><a id="a_loginNow" href="#">Login</a></b>');
		$('#user-ident #user-register').html('<b><a id="a_RegisterNow" href="#">Register</a></b>');
		$('#a_loginNow').click(getUserLoginForm);
		$('#a_RegisterNow').click(getUserRegisterForm);
		debug_write('(onGetUser).1 -> __isOptimized__='+__isOptimized__);
		if (__isOptimized__){
			$js(__facebook_api_url, function(){
				onFaceBookAPI();
			});
		} else {
			onFaceBookAPI();
		}
	}
	$('#user-ident #user-feedback').html('<b><a id="a_FeedBackNow" href="#">Feedback</a></b>');
	var a = $('#a_FeedBackNow');
	debug_write('(onGetUser).2 -> a.length='+a.length);
	if (a.length > 0){
		a.click(onClickPopulateFeedback);
	}
	$('#user-ident #user-sponsor').html('<b><a id="a_SponsorNow" href="#">Vyper Logix Corp.</a></b>');
	var a = $('#a_SponsorNow');
	debug_write('(onGetUser).3 -> a.length='+a.length);
	if (a.length > 0){
		a.click(onClickPopulateSponsor);
	}
	$('#user-ident #user-feed-rss').html('<b><a id="a_RssFeed" href="/feeds/rss/" target="_blank">Rss News Feed</a></b>');
	$('#user-ident #user-feed-atom').html('<b><a id="a_AtomFeed" href="/feeds/atom/" target="_blank">Atom News Feed</a></b>');
	getCurrentMenu();
}
function getUserLoginForm(){
	var aBtn = $('#btn_submitLogin');
	debug_write('(getUserLoginForm).BEGIN -> aBtn.length='+aBtn.length);
	try {
		if (aBtn.length == 0){
			var val = getCookie('__xxx__');
			if (1) {
				var obj = $('#column_left');
				if (obj.length > 0) {
					var url = _current_api['secure_endpoint'] + _current_api['blog_rest_user_login'] + val + '/' + '?fr=1&dst=' + $('#column_left').attr('id') + '&cb=adjustLoginForm&p=onSuccessProxy';
					debug_write('(getUserLoginForm).1 -> url='+url);
					obj.html('<iframe id="iframe0" bordercolor="white" width="820" height="'+((
					__is_running_local) ? 600 : 450)+'" frameborder="0" scrolling="'+((__is_running_local) ? 'auto' : 'no')+'" src="'+url+'"></iframe>'); // ((__is_running_local) ? get_google_balls() : '')+
				}
			} else if (__jsp__) {
				__jsp__.setAttribute('src', _current_api['secure_endpoint'] + _current_api['blog_rest_user_login'] + '/' + val + '/' + '?jsp=1&dst=' + $('#column_left').attr('id') + '&cb=adjustLoginForm&p=onSuccessProxy');
			}
		}
	} catch (e) {debug_write('(getUserLoginForm).ERROR -> e='+e.toString());}
	debug_write('(getUserLoginForm).END !');
}
onClickArticle = function () {
	var _id = $(this).attr('id');
	var recID = parseEntryID(_id);
	getOneArticle(recID);
}
onClickArticleTag = function () {
	var _id = $(this).attr('id');
	var recID = parseEntryID(_id,'Tag');
	getOneTaggedArticles(recID);
}
onClickArticleLanguage = function () {
	var _id = $(this).attr('id');
	var recID = parseEntryID(_id,'Language');
	getOneLanguageArticles(recID);
}
onClickArticleCategory = function () {
	var _id = $(this).attr('id');
	var recID = parseEntryID(_id,'Category');
	getOneCategoryArticles(recID);
}
function getOneArticle(recID) {
	_ajax(_current_api['blog_rest_get_article']+recID+'/',$('#column_left'),'article='+recID);
}
function getOneTaggedArticles(recID) {
	_ajax(_current_api['blog_rest_get_tagged']+recID+'/',$('#column_left'),'tag='+recID);
}
function getOneCategoryArticles(recID) {
	_ajax(_current_api['blog_rest_get_category']+recID+'/',$('#column_left'),'category='+recID);
}
function getOneLanguageArticles(recID) {
	_ajax(_current_api['blog_rest_get_language']+recID+'/',$('#column_left'),'language='+recID);
}
onClickArticleDetails = function () {
	var _id = $(this).attr('id');
	var recID = parseEntryID(_id,'Details');
	getOneArticle(recID);
}
onSubmitArticleComment = function () {
	$(this).attr("disabled", "disabled");
	var recid = $formInputById('formComment','id_recid').val();
	var comment = $formTextareaById('formComment','id_comment').val();
	var div = $('#div_entryComments_'+recid);
	debug_write('(onSubmitArticleComment).1 -> recid='+recid);
	if ( (comment) && (recid) ) {
		_post(_current_api['blog_rest_get_comments'],div,{recid:recid,comment:comment},null,adjustArticleComments);
	} else {
		jAlert('WARNING: Cannot submit your Comment unless you enter a comment... Please correct and try again.');
	}
}
function adjustArticleComments(){
	debug_write('(adjustArticleComments).BEGIN !');
	var buttons = $('#formComment #btn_submitComment');
	debug_write('(adjustArticleComments).1 -> buttons.length='+buttons.length);
	buttons.click(onSubmitArticleComment);
	debug_write('(adjustArticleComments).END !');
}
onClickArticleComments = function () {
	var _id = $(this).attr('id');
	var div_comments = parseIdInto(_id,'div');
	var recID = parseEntryID(_id,'Comments');
	debug_write('(onClickArticleComments).1 _id='+_id+', recID='+recID);
	_ajax(_current_api['blog_rest_get_comments']+recID+'/',div_comments,'',adjustArticleComments);
}
onClickArticleMore = function () {
	var _id = $(this).attr('id');
	var recID = parseEntryID(_id,'MORE');
	_ajax(_current_api['blog_rest_get_more']+recID+'/',$('#column_left'),null);
}
function checkResendRegistrationSubmitValidity() {
	debug_write('(checkResendRegistrationSubmitValidity) _isEmailAddrsValid='+_isEmailAddrsValid);
	if (_isEmailAddrsValid) {
		$('#btn_submitResendRegister').removeAttr("disabled");
	} else {
		$('#btn_submitResendRegister').attr("disabled", "disabled");
	}
}
function checkSendPasswordSubmitValidity() {
	debug_write('(checkSendPasswordSubmitValidity) _isEmailAddrsValid='+_isEmailAddrsValid);
	if (_isEmailAddrsValid) {
		$('#btn_submitSendPassword').removeAttr("disabled");
	} else {
		$('#btn_submitSendPassword').attr("disabled", "disabled");
	}
}
function getUserRegisterForm() {
	var val = getCookie('__xxx__');
	var obj = $('#column_left');
	if (obj.length > 0) {
		var url = _current_api['secure_endpoint'] + _current_api['blog_rest_user_register'] + val + '/' + '?fr=1&dst=' + $('#column_left').attr('id') + '&cb=adjustLoginForm&p=onSuccessProxy';
		obj.html('<iframe id="iframe0" bordercolor="white" width="840" height="'+((__is_running_local) ? 600 : 550)+'" frameborder="0" scrolling="'+((__is_running_local) ? 'auto' : 'no')+'" src="'+url+'"></iframe>'); // ((__is_running_local) ? get_google_balls() : '')+
	}
	//_ajax(_current_api['blog_rest_user_register'],$('#column_left'),'',adjustRegisterForm);
}
function getArticles() {
	_ajax(_current_api['blog_rest_get_articles'],$('#column_left'),'',getExternals);
}
function getExternals() {
	_ajax(_current_api['blog_rest_get_externals'],$('#column_left_aux'),'');
}
function getAbout(){
	window.location.href = '/about/';
}
function getCategories() {
	_ajax(_current_api['blog_rest_get_categories'],$('#column_left'),const_getCategories);
}
function getTags() {
	_ajax(_current_api['blog_rest_get_tags'],$('#column_left'),const_getTags);
}
function getLanguages() {
	_ajax(_current_api['blog_rest_get_languages'],$('#column_left'),const_getLanguages);
}
onClickSubmitFaceBookLogin = function () {
	__fb.login(function(response) {
		if (response.session) {
			var post_obj = {session_key:response.session['session_key'],uid:response.session['uid'],expires:response.session['expires'],secret:response.session['secret'],base_domain:response.session['base_domain'],access_token:response.session['access_token'],sig:response.session['sig']};
			if (response.perms) {
				// user is logged in and granted some permissions.
				// perms is a comma separated list of granted permissions
												//session_key = [71aacd59654a705a52ac518f-1167633888]
												//uid = [1167633888]
												//expires = [0]
												//secret = [cd3b1326d1c8685b3c1a0f6db774a328]
												//base_domain = [raychorn.com]
												//access_token = [122703234439995|71aacd59654a705a52ac518f-1167633888|dawx-NVvnhrjykTCJI9CwLBnMaM.]
												//sig = [0cdf92258cbc6f79aec3a57554057032]
				post_obj['perms'] = response.perms;
			} else {
				// user is logged in, but did not grant any permissions
			}
			_post(_current_api['blog_rest_set_facebook'],$('#column_left'),post_obj,null,function(){window.location.href='/facebook/';});
		}
	}, {perms:'read_stream,publish_stream,offline_access'});
}
getCurrentMenu = function(){
	_ajax(_current_api['get_rest_get_menu'],null,null,function(data){
		$('#menu ul').html(data);
		$('#a_Home').click(onClickMain);
		$('#a_About').click(onClickMain);
		$('#a_Categories').click(onClickMain);
		$('#a_Tags').click(onClickMain);
		$('#a_Languages').click(onClickMain);
		$('#a_Login').click(onClickMain);
		$('#a_Register').click(onClickMain);
		$('#a_Admin').click(onClickMain);
		$('#a_Logout').click(onLogoutNow);
	});
}
__onWindowLoad = function (){
    debug_write('(__onWindowLoad) !');
}
onDocumentReady = function () {
	getCurrentUser(false,onGetUser);
};
debug_write('(__is_onDocumentReady__).1 -> '+__is_onDocumentReady__);
if (__is_onDocumentReady__) {
	try {onDocumentReady();} catch(e){debug_write('onDocumentReady().ERROR.1 -> '+e.toString());}
} else {
	_timer2 = setInterval('checkForDocumentReady()',250);
}
