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
onClickMainSite = function () {
	debug_write('(onClickMainSite).1 !');
	window.location.href = '/';
}
onClickMain = function () {
	var _id = $(this).attr('id');
	if (_id == 'a_Home') {
		window.location.href = '/';
	}
}
onGetUser = function(is_logged_in,wasClicked,current_user){
	$('#a_Main').click(onClickMainSite);
	$('#a_Home').click(onClickMain);
}
adjustAnchors = function(){}
onDocumentReady = function () {
	debug_write('(onDocumentReady).1 !');
	getCurrentUser(false,onGetUser);
};
debug_write('(__is_onDocumentReady__).1 -> '+__is_onDocumentReady__);
if (__is_onDocumentReady__) {
	try {onDocumentReady();} catch(e){debug_write('onDocumentReady().ERROR.1 -> '+e.toString());}
} else {
	_timer2 = setInterval('checkForDocumentReady()',250);
}
