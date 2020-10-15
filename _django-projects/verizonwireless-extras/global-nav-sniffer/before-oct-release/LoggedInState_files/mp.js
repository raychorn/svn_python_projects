/*
	This function (switchLanguage) is provided by MotionPoint, it will be called when customer clicks on Espaneol or English link.
	Purpose of this function is to send all the cookies from client browser to MotionPoint translation server
	and redirect the page to MotionPoint translation server for spanish pages. Cookies are passed to avoid relogin.
	All the cookies are read and concatenated in a long string and passed to motionpoint server in scookies variable
	thru post submit(refer postcookies) method.
	oh variable defines the orgin host. and tsh variable defines the translation host.
	*/
	function switchLanguage() {
	document.getElementById("spanish1").style.cursor = "wait"; 
	var chost = new Array();
	idx=location.href.indexOf(tsh);
	if(idx==-1)
	{
		idx=location.href.indexOf(oh);
		if(idx>-1)
		{
			idx=idx+oh.length;
			hname=tsh+tsd;
						tsh=hname;
					        chost[0] = '.verizonwireless.com';
					}
				}
	else
	{
		idx=location.href.indexOf(tsd);
		if(idx>-1)
		{
			idx=idx+tsd.length;
			hname=oh;
					chost[0] = null;
					}
				}
	
		path=location.href.substring(idx);
		hend=hname.charAt(hname.length-1); pstart=path.charAt(0);
		if(hend=='/' && pstart=='/') path=path.substring(path.indexOf('/')+1);
		if(hend!='/' && pstart!='/') path='/'+path;
	
		if (hname != tsh) {
		//remove mp_params & mpactionid from query string if present
			idx = path.indexOf('mpactionid=');
			if (idx>0)
				path = path.substring(0,idx-1);
			idx=path.indexOf(';mp_params=');
			if (idx>0) {
				var qryString = path.substring(idx+11);
				idx = path.indexOf('?');
				if (idx > 0) {
					path = path.substring(0,idx);
					if (qryString != null)
						path = path+'?'+qryString;
				}
			}
		}
		
	var scookieStr = document.cookie;  //reads all cookies
			var postUrl = null;
			if (hname == tsh) {
				//SEND COOKIES VIA POST to pre-establish translated site session using url format: /path/page?pageparams&mpactionid=56
				var qryString = 'mpactionid=56';
			idx = path.indexOf('?');
			if (idx > 0) {
				qryString = path.substring(idx+1)+'&'+qryString;
				path = path.substring(0,idx);
			}
				postUrl = location.protocol+'//'+hname+path+'?'+qryString;
			} else {
				//SEND COOKIES VIA POST to pre-establish english site session using ohs
				scookieStr = scookieStr + '; mptargeturl=' + location.protocol+'//'+hname+path;
				postUrl = ohs;
			}
	for (i=0;i<chost.length;i++){
		deleteCookie('dough', '/', chost[i]);
	}
			postCookies(postUrl, scookieStr);
		return false;
	}
	
	
	function postCookies(url, scookieStr) {
		cform=document.createElement('form'); 
		document.body.appendChild(cform);
		cform.name = 'mpsessionform';
		cform.method='POST'; 
		cform.action=url;

		cinput=document.createElement('input');
		cinput.type='hidden';
		cinput.name='scookies';
		cinput.value=scookieStr;
		cform.appendChild(cinput);
		cform.submit();
	}
	
	function isCookie(name) { 
		return (document.cookie.indexOf(name+'=') > -1); 
	} 
	
	function readCookie(name) { 
	   var start = document.cookie.indexOf(name+'='); 
	   if (start == -1) return null; 
	   var len = start+name.length+1; 
	   var end = document.cookie.indexOf(';',len); 
	   if (end == -1) end = document.cookie.length;
	   while (document.cookie.charAt(len)==' ') len++;
	   return unescape(document.cookie.substring(len,end)); 
	}
	
	function getCookieNameStartingWith(name) { 
	   var start = document.cookie.indexOf(name); 
	   if (start == -1) return null;
	   var end = document.cookie.indexOf('=',start+name.length);
	   if (end == -1) return null;
	   return document.cookie.substring(start,end);
	}
	
	function setCookie(name,value,path,domain) {
		var setcookie = name+'='+escape(value);
		if (path != null) setcookie = setcookie+'; path=' + path;
		if (domain != null)	setcookie = setcookie+'; domain=' + domain;
		document.cookie = setcookie;
	}

function deleteCookie(name, path, domain) {
	document.cookie = name + '=' +
		((path) ? '; path=' + path : '') +
		((domain) ? '; domain=' + domain : '') +
		'; expires=Thu, 01-Jan-1970 00:00:01 GMT';
}
