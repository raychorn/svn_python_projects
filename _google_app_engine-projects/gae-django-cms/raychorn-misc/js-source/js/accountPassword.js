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
function __onLoadSWFObject__(){}
onGetUser = function(is_logged_in,wasClicked,current_user){
	debug_write('(onGetUser).1 !');
	adjustLoginForm();
}
onClickSubmitForgotPassword = function(){
	var email = $formInputById('formForgotPassword','id_email').attr('value');
	var password1 = $formInputById('formForgotPassword','id_password1').attr('value');
	var password2 = $formInputById('formForgotPassword','id_password2').attr('value');
	debug_write('(onClickSubmitForgotPassword) :: email='+email);
	debug_write('(onClickSubmitForgotPassword) :: password1='+password1);
	debug_write('(onClickSubmitForgotPassword) :: password2='+password2);
	if (_isEmailAddrsValid){
		_post(_current_api['blog_rest_forgot_password'],$('#column_left'),{email:email,password1:password1,password2:password2},null,adjustForgotPasswordForm);
	} else {
		jAlert(const_defaultReason);
	}
}
function checkForgotPasswordSubmitValidity() {
	debug_write('(checkForgotPasswordSubmitValidity) _isEmailAddrsValid='+_isEmailAddrsValid);
	if ( (_isEmailAddrsValid) && (_isPasswordValid) ) {
		$('#btn_submitForgotPassword').removeAttr("disabled");
	} else {
		$('#btn_submitForgotPassword').attr("disabled", "disabled");
	}
}
function adjustForgotPasswordForm(){
	debug_write('(adjustForgotPasswordForm).BEGIN !');
	$('#btn_submitForgotPassword').click(onClickSubmitForgotPassword).attr("disabled", "disabled");
	try {
		$formInputById('formForgotPassword','id_email').attr('autocomplete','off').keyup(function(event) {
			handle_checkEmailAddress($(this),checkForgotPasswordSubmitValidity);
		});
		debug_write('(adjustForgotPasswordForm).1 !');
		_checkEmailAddress($formInputById('formForgotPassword','id_email'),checkForgotPasswordSubmitValidity);
		$formInputById('formForgotPassword','id_password1').attr('autocomplete','off').keyup(function(event) {
			handle_checkPassword($(this),$formInputById('formForgotPassword','id_password2'),checkForgotPasswordSubmitValidity);
		});
		$formInputById('formForgotPassword','id_password2').attr('autocomplete','off').keyup(function(event) {
			handle_checkPassword($formInputById('formForgotPassword','id_password1'),$(this),checkForgotPasswordSubmitValidity);
		});
		debug_write('(adjustForgotPasswordForm).2 !');
		_checkPassword($formInputById('formForgotPassword','id_password1'),$formInputById('formForgotPassword','id_password2'),checkForgotPasswordSubmitValidity);
	} catch (e) {debug_write('(adjustForgotPasswordForm).ERROR '+e.toString());}
	debug_write('(adjustForgotPasswordForm).END !');
	linkUpSelfHelp();
}
adjustAnchors = function(){
	adjustForgotPasswordForm();
}
onDocumentReady = function () {
	debug_write('(onDocumentReady).1 !');
	getCurrentUser(false,onGetUser);
	//adjustSSLAnchors();
};
debug_write('(__is_onDocumentReady__).1 -> '+__is_onDocumentReady__);
if (__is_onDocumentReady__) {
	try {onDocumentReady();} catch(e){debug_write('onDocumentReady().ERROR.1 -> '+e.toString());}
} else {
	_timer2 = setInterval('checkForDocumentReady()',250);
}
