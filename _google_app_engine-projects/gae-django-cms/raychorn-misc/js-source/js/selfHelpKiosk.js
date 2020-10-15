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
var _login_elements = ['id_username','id_password'];
var _isEmailAddrsValid = false;
var _isTOSValid = false;
var _isUsernameValid = false;
var _isPasswordValid = false;
var _isFirstNameValid = false;
var _isLastNameValid = false;
var _id_email_value = '';
function init_validations(){
	_isEmailAddrsValid = _isTOSValid = _isUsernameValid = _isPasswordValid = _isFirstNameValid = _isLastNameValid = false;
	_id_email_value = '';
}
function checkEmailAddress(value) {
	return value.match(/[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/gi);
}
function checkUserName(value){
	return (value.length > 3) && (value.match(/^[\w'_]+\s?[\w'_]+$/gi)) && (value.length < 30);
}
function checkFirstLastName(value){
	return (value.length > 0) && (value.match(/^[\w'-]+\s?[\w'-]+$/gi)) && (value.length < 30);
}
function checkPassword(value){
	return value.match(/^(?=[\-_a-zA-Z0-9]*?[A-Z])(?=[\-_a-zA-Z0-9]*?[a-z])(?=[\-_a-zA-Z0-9]*?[0-9])[\-_a-zA-Z0-9]{6,}$/gi);
}
function checkSubmitLoginValidity() {
	debug_write('_isUsernameValid='+_isUsernameValid+', _isPasswordValid='+_isPasswordValid);
	if ( (_isUsernameValid) && (_isPasswordValid) ) {
		$('#btn_submitLogin').removeAttr("disabled");
	} else {
		$('#btn_submitLogin').attr("disabled", "disabled");
	}
}
function handle_checkUsername(_obj){
	_isUsernameValid = checkUserName(_obj.attr('value'));
	checkSubmitValidity();
	setBorderColorForIn(_obj,_isUsernameValid);
	return _isUsernameValid;
}
function _checkUsername(){
	return handle_checkUsername($formInputById('formRegister','id_username'));
}
function handle_checkLoginUsername(_obj){
	_isUsernameValid = checkUserName(_obj.attr('value'));
	checkSubmitLoginValidity();
	setBorderColorForIn(_obj,_isUsernameValid);
	return _isUsernameValid;
}
function _checkLoginUsername(){
	return handle_checkLoginUsername($formInputById('formLogin','id_username'));
}
function handle_checkLoginPassword(_obj){
	_isPasswordValid = (checkPassword(_obj.attr('value')));
	checkSubmitLoginValidity();
	setBorderColorForIn(_obj,_isPasswordValid);
	return _isPasswordValid;
}
function _checkLoginPassword(){
	return handle_checkLoginPassword($formInputById('formLogin','id_password'));
}
function handle_checkPassword(_obj1,_obj2,callback){
	var _val1 = _obj1.attr('value');
	var _val2 = _obj2.attr('value');
	_isPasswordValid = (checkPassword(_val1)) && (checkPassword(_val2)) && (_val1 == _val2);
	if ( (callback) && (typeof(callback) == const_function_symbol) ) {
		try {callback();} catch (e) {}
	}
	setBorderColorForIn(_obj1,_isPasswordValid);
	setBorderColorForIn(_obj2,_isPasswordValid);
	return _isPasswordValid;
}
function _checkPassword(obj1,obj2,callback){
	return handle_checkPassword(obj1,obj2,callback);
}
function handle_checkEmailAddress(_obj,callback){
	_isEmailAddrsValid = (checkEmailAddress(_obj.attr('value'))) ? true : false;
	if ( (callback) && (typeof(callback) == const_function_symbol) ) {
		try {callback();} catch (e) {}
	}
	setBorderColorForIn(_obj,_isEmailAddrsValid);
	return _isEmailAddrsValid;
}
function _checkEmailAddress(obj,callback){
	return handle_checkEmailAddress(obj,callback);
}
function checkSendPasswordSubmitValidity() {
	debug_write('(checkSendPasswordSubmitValidity) _isEmailAddrsValid='+_isEmailAddrsValid);
	if (_isEmailAddrsValid) {
		$('#btn_submitSendPassword').removeAttr("disabled");
	} else {
		$('#btn_submitSendPassword').attr("disabled", "disabled");
	}
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
function checkResendRegistrationSubmitValidity() {
	debug_write('(checkResendRegistrationSubmitValidity) _isEmailAddrsValid='+_isEmailAddrsValid);
	if (_isEmailAddrsValid) {
		$('#btn_submitResendRegister').removeAttr("disabled");
	} else {
		$('#btn_submitResendRegister').attr("disabled", "disabled");
	}
}
function adjustResendRegisterForm(){
	debug_write('(adjustResendRegisterForm).BEGIN !');
	$('#btn_submitResendRegister').click(onClickSubmitResendRegister).attr("disabled", "disabled");
	$formInputById('formResendRegister','id_email').attr('autocomplete','off').keyup(function(event) {
		handle_checkEmailAddress($(this),checkResendRegistrationSubmitValidity);
	});
	_checkEmailAddress($formInputById('formResendRegister','id_email'),checkResendRegistrationSubmitValidity);
	debug_write('(adjustResendRegisterForm).END !');
	linkUpSelfHelp();
}
function getForgotPasswordForm() {
	init_validations();
	_ajax(_current_api['blog_rest_send_password'],$('#column_left'),'',adjustSendPasswordForm);
}
function getResendRegisterForm() {
	init_validations();
	_ajax(_current_api['blog_rest_resend_register'],$('#column_left'),'',adjustResendRegisterForm);
}
function linkUpSelfHelp(){
	debug_write('(linkUpSelfHelp).1 -> length='+$('#a_forgotPassword').length);
	$('#a_forgotPassword').click(function(){
		getForgotPasswordForm();
	});
	debug_write('(linkUpSelfHelp).2 -> length='+$('#a_resendRegistration').length);
	$('#a_resendRegistration').click(function(){
		getResendRegisterForm();
	});
}
onClickSubmitSendPassword = function(){
	var email = $formInputById('formSendPassword','id_email').attr('value');
	debug_write('(onClickSubmitSendPassword) :: email='+email);
	if (_isEmailAddrsValid){
		_post(_current_api['blog_rest_send_password'],$('#column_left'),{email:email},null,adjustSendPasswordForm);
	} else {
		jAlert(const_defaultReason);
	}
}
function adjustSendPasswordForm(){
	debug_write('(adjustSendPasswordForm).BEGIN !');
	$('#btn_submitSendPassword').click(onClickSubmitSendPassword).attr("disabled", "disabled");
	try {
		$formInputById('formSendPassword','id_email').attr('autocomplete','off').keyup(function(event) {
			handle_checkEmailAddress($(this),checkSendPasswordSubmitValidity);
		});
		_checkEmailAddress($formInputById('formSendPassword','id_email'),checkSendPasswordSubmitValidity);
	} catch (e) {debug_write('(adjustSendPasswordForm).ERROR '+e.toString());}
	debug_write('(adjustSendPasswordForm).END !');
	linkUpSelfHelp();
}
onClickSSLAnchor = function (){
	showHelp($(this));
	_ajax(_current_api['blog_rest_ssl_help'],$('#div_HELP'),null);
}
function adjustSSLAnchors() {
	var _id, _val;
	var anchors = $("#ssl-icon").find("img");
	debug_write('(adjustSSLAnchors).1 anchors.length='+anchors.length);
	anchors.each(function(index) {
		_id = $(this).attr('id');
		debug_write('(adjustSSLAnchors).2 _id='+_id);
		$(this).click(onClickSSLAnchor);
	});
}
