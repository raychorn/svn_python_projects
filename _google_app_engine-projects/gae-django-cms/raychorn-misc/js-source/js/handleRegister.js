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
var const_TOS = 'Terms of Service';
function showTOS(el){
	el.jDialog({
		title : "<big>"+const_TOS+"</big>",
		content : '<div id="div_TOS"></div>',
		width : 500
	});
}
function checkSubmitValidity() {
	debug_write('_isTOSValid='+_isTOSValid+', _isEmailAddrsValid='+_isEmailAddrsValid+', _isUsernameValid='+_isUsernameValid+', _isPasswordValid='+_isPasswordValid+', _isFirstNameValid='+_isFirstNameValid+', _isLastNameValid='+_isLastNameValid);
	if ( (_isTOSValid) && (_isEmailAddrsValid) && (_isUsernameValid) && (_isPasswordValid) && (_isFirstNameValid) && (_isLastNameValid) ) {
		$('#btn_submitRegister').removeAttr("disabled");
	} else {
		$('#btn_submitRegister').attr("disabled", "disabled");
	}
}
onClickTOSRead = function () {
	_isTOSValid = $(this).attr('checked');
	checkSubmitValidity();
}
function handle_checkFirstName(_obj){
	_isFirstNameValid = checkFirstLastName(_obj.attr('value'));
	checkSubmitValidity();
	setBorderColorForIn(_obj,_isFirstNameValid);
	return _isFirstNameValid;
}
function _checkFirstName(){
	return handle_checkFirstName($formInputById('formRegister','id_first_name'));
}
function handle_checkLastName(_obj){
	_isLastNameValid = checkFirstLastName(_obj.attr('value'));
	checkSubmitValidity();
	setBorderColorForIn(_obj,_isLastNameValid);
	return _isLastNameValid;
}
function _checkLastName(){
	return handle_checkLastName($formInputById('formRegister','id_last_name'));
}
onClickSubmitRegister = function () {
	var _id = $(this).attr('id');
	var username = $formInputById('formRegister','id_username').attr('value');
	var isUserNameValid = _checkUsername();
	var password1 = $formInputById('formRegister','id_password1').attr('value');
	var password2 = $formInputById('formRegister','id_password2').attr('value');
	var isPasswordValid = _checkPassword($formInputById('formRegister','id_password1'),$formInputById('formRegister','id_password2'));
	var first_name = $formInputById('formRegister','id_first_name').attr('value');
	var last_name = $formInputById('formRegister','id_last_name').attr('value');
	//var sha_password1 = hex_sha256(password1);
	//var sha_password2 = hex_sha256(password2);
	var email = $formInputById('formRegister','id_email').attr('value');
	var isEmailValid = _checkEmailAddress($formInputById('formRegister','id_email'),checkSubmitValidity);
	var tos = $formInputById('formRegister','id_tos').attr('checked');
	//debug_write('(onClickSubmitRegister) :: isUserNameValid='+isUserNameValid+', isPasswordValid='+isPasswordValid+', isEmailValid='+isEmailValid);
	if (isUserNameValid && isPasswordValid && isEmailValid && tos){
		_has_clicked_submitRegister = true;
		_post(_current_api['blog_rest_post_register'],$('#column_left'),{username:username,password1:password1,password2:password2,email:email,first_name:first_name,last_name:last_name,tos:tos},null,adjustRegisterForm);
	} else {
		jAlert('WARNING: Cannot submit your Registration due to the invalidity of one or more data elements... Please correct and try again.');
	}
}
var _tos_link_deployed = false;
var _registration_elements = ['id_username','id_password1','id_password2','first_name','last_name','id_email','id_tos'];
function adjustRegisterForm() {
	init_validations();
	debug_write('adjustRegisterForm.BEGIN !');
	try {
		var i = $("#formRegister").html().indexOf(const_TOS);
		if ((i > -1) && (!_tos_link_deployed)) {
			$("#formRegister").html($("#formRegister").html().replace(const_TOS,'<BR/><a id="a_TOS" href="#" title="'+const_TOS+'">'+const_TOS+'</a>'));
			$('#a_TOS').click(function(){
				showTOS($(this));
				_ajax(_current_api['blog_rest_register_tos'],$('#div_TOS'),null);
			});
			_tos_link_deployed = true;
		}
		$('#btn_submitRegister').click(onClickSubmitRegister).attr("disabled", "disabled");
		var heads = $("#formRegister").find("th");
		heads.each(function(index) {
			$(this).attr('align','right');
		});
		var spans;
		var delim = '-';
		var bodies = $("#formRegister").find("td");
		bodies.each(function(index) {
			spans = $(this).find("span");
			if (spans.length == 0) {
				var xN = _registration_elements[index];
				var x = 'span_required'+delim+xN;
				var xx = 'a_requiredHelp'+delim+xN;
				$(this).html($(this).html()+'<span id="'+x+'">&nbsp;required&nbsp;<a id="'+xx+'" href="#" title="Get Help"><img src="/static/images/icons/help.gif" border="0"/></a></span>');
				$('#'+x).css("color","red");
				$('#'+xx).click(function(event){
					var _this = event.currentTarget;
					var toks = _this.id.split(delim);
					var z = toks[toks.length-1];
					toks = z.split('_');
					var n = toks[toks.length-1];
					if (n == 'name'){
						n = toks[toks.length-2] + '_' + n;
					}
					showHelp($(this));
					_ajax(_current_api['blog_rest_register_help']+n+'/',$('#div_HELP'),null);
				});
			}
		});
		$formInputById('formRegister','id_username').attr('autocomplete','off').keyup(function(event) {
			handle_checkUsername($(this));
			if (event.keyCode == '13') {
				 //event.preventDefault();
			}
		});
		$formInputById('formRegister','id_first_name').attr('autocomplete','off').keyup(function(event) {
			handle_checkFirstName($(this));
			if (event.keyCode == '13') {
				 //event.preventDefault();
			}
		});
		$formInputById('formRegister','id_last_name').attr('autocomplete','off').keyup(function(event) {
			handle_checkLastName($(this));
			if (event.keyCode == '13') {
				 //event.preventDefault();
			}
		});
		$formInputById('formRegister','id_password1').attr('autocomplete','off').keyup(function(event) {
			handle_checkPassword($(this),$formInputById('formRegister','id_password2'),checkSubmitValidity);
			if (event.keyCode == '13') {
				 //event.preventDefault();
			}
		});
		$formInputById('formRegister','id_password2').attr('autocomplete','off').keyup(function(event) {
			handle_checkPassword($formInputById('formRegister','id_password1'),$(this),checkSubmitValidity);
			if (event.keyCode == '13') {
				 //event.preventDefault();
			}
		});
		$formInputById('formRegister','id_email').attr('autocomplete','off').keyup(function(event) {
			handle_checkEmailAddress($(this),checkSubmitValidity);
			if (event.keyCode == '13') {
				 //event.preventDefault();
			}
		});
		$formInputById('formRegister','id_tos').click(onClickTOSRead);
		_checkUsername();
		_checkFirstName();
		_checkLastName();
		_checkPassword($formInputById('formRegister','id_password1'),$formInputById('formRegister','id_password2'),checkSubmitValidity);
		_checkEmailAddress($formInputById('formRegister','id_email'),checkSubmitValidity);
		linkUpSelfHelp();
	} catch (e) {debug_write('(adjustRegisterForm) -> ERROR.2: '+e.toString());}
	debug_write('adjustRegisterForm.END !');
}
