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
onClickSubmitLogin = function () {
	try {
		var _id = $(this).attr('id');
		var username = $formInputById('formLogin','id_username').attr('value');
		var isUserNameValid = _checkLoginUsername();
		var password = $formInputById('formLogin','id_password').attr('value');
		var isPasswordValid = _checkLoginPassword();
		debug_write('(onClickSubmitLogin) :: isUserNameValid='+isUserNameValid+', isPasswordValid='+isPasswordValid);
		if (isUserNameValid && isPasswordValid){
			_post(_current_api['blog_rest_post_login'],$('#column_left'),{username:username,password:password},null,adjustLoginForm);
		} else {
			jAlert('WARNING: Cannot submit your Login due to the invalidity of one or more data elements... Please correct and try again.');
		}
	} catch (e) {debug_write('(onClickSubmitLogin) -> ERROR.1: '+e.toString());}
}
function adjustLoginForm(){
	init_validations();
	debug_write('adjustLoginForm.BEGIN !');
	var btn = $('#btn_submitLogin');
	debug_write('(adjustLoginForm).1 -> btn.length='+btn.length);
	try {
		if (btn.length > 0){
			btn.click(onClickSubmitLogin).attr("disabled", "disabled");
			var spans;
			var bodies = $("#formLogin").find("td");
			debug_write('(adjustLoginForm).2 -> bodies.length='+bodies.length);
			bodies.each(function(index) {
				var delim = '-login-';
				spans = $(this).find("span");
				if (spans.length == 0) {
					var xN = _login_elements[index];
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
						showHelp($(this));
						_ajax(_current_api['blog_rest_login_help']+n+'/',$('#div_HELP'),null);
					});
				}
			});
			debug_write('(adjustLoginForm).3 !');
			try {
				$formInputById('formLogin','id_username').attr('autocomplete','off').keyup(function(event) {
					handle_checkLoginUsername($(this));
					if (event.keyCode == '13') {
						 //event.preventDefault();
					}
				});
				$formInputById('formLogin','id_password').attr('autocomplete','off').keyup(function(event) {
					handle_checkLoginPassword($(this));
					if (event.keyCode == '13') {
						 onClickSubmitLogin();
					}
				});
				debug_write('(adjustLoginForm) -> bodies.length='+bodies.length);
				if (bodies.length > 0){
					_checkLoginUsername();
					_checkLoginPassword();
				}
			} catch (e) {debug_write('(adjustLoginForm) -> ERROR.1: '+e.toString());}
			//debug_write('(adjustLoginForm) -> getCurrentUser() !');
			//getCurrentUser(false,onGetUser);
			linkUpSelfHelp();
		} else {
			var url = _current_api['secure_endpoint'];
			debug_write('(adjustLoginForm) -> url='+url);
			top.location.href = (url.length == 0) ? '/' : url;
		}
	} catch (e) {debug_write('(adjustLoginForm) -> ERROR.2: '+e.toString());}
	debug_write('adjustLoginForm.END !');
}
