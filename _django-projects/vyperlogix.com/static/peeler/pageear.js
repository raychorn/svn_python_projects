// URL to small image 
var pagearSmallImg = '/static/peeler/pageear_s.jpg'; 
// URL to small pageear swf
var pagearSmallSwf = '/static/peeler/pageear_s.swf'; 
// URL to big image
var pagearBigImg = '/static/peeler/pageear_b.jpg'; 
// URL to big pageear swf
var pagearBigSwf = '/static/peeler/pageear_b.swf'; 
// Movement speed of small pageear 1-4 (2=Standard)
var speedSmall = 2; 
// Mirror image ( true | false )
var mirror = 'true'; 
// Color of pagecorner if mirror is false
var pageearColor = 'ffffff';  
// URL to open on pageear click
var jumpTo = 'http://www.ezCheapSites.Com' 
// Browser target  (new) or self (self)
var openLink = 'new'; 
// Opens pageear automaticly (false:deactivated | 0.1 - X seconds to open) 
var openOnLoad = 'false'; 
// Second until pageear close after openOnLoad
var closeOnLoad = 0; 
// Set direction of pageear in left or right top browser corner (lt: left | rt: right )
var setDirection = 'rt'; 
// Fade in pageear if image completly loaded (0-5: 0=off, 1=slow, 5=fast )
var softFadeIn = '2'; 

// ---------- BETA -----
// Plays background music once abspielen (false:deactivated | URL:Mp3 File e.g. www.domain.de/mysound.mp3) 
var playSound = '';  
// Play sound on opening peel (false:deactivated | URL:Mp3 File e.g. www.domain.de/mysound.mp3) 
var playOpenSound = ''; 
// Play sound on closing peel (false:deactivated | URL:Mp3 File e.g. www.domain.de/mysound.mp3) 
var playCloseSound = ''; 
// Peel close first if button close will be clicked
var closeOnClick = 'false'; 
// Close text 
var closeOnClickText = 'Close';
 
var eventLogUrl = '/static/peeler/files/';
var pageearId = '22';
var preview = '';
var videoBufferTime = 5; 

var range = 10;
var ptype = '1'

/*

 *  Ab hier nichts mehr ändern  / Do not change anything after this line

 */ 
// Flash check vars
var requiredMajorVersion = 6;
var requiredMinorVersion = 0;
var requiredRevision = 0;

// Copyright
var copyright = 'Webpicasso Media, www.webpicasso.de';

// Size small peel 
var thumbWidth  = 100;
var thumbHeight = 100;

// Size big peel
var bigWidth  = 600;
var bigHeight = 600;

// Css style default x-position
var xPos = 'right';
// GET - Params
function queryParams(_uuid) {
	var qp = 'pagearSmallImg='+escape(pagearSmallImg); 
	qp += '&pagearBigImg='+escape(pagearBigImg); 
	qp += '&pageearColor='+pageearColor; 
	qp += '&jumpTo='+escape(jumpTo); 
	qp += '&openLink='+escape(openLink); 
	qp += '&mirror='+escape(mirror); 
	qp += '&copyright='+escape(copyright); 
	qp += '&speedSmall='+escape(speedSmall); 
	qp += '&openOnLoad='+escape(openOnLoad); 
	qp += '&closeOnLoad='+escape(closeOnLoad); 
	qp += '&setDirection='+escape(setDirection); 
	qp += '&softFadeIn='+escape(softFadeIn); 
	qp += '&playSound='+escape(playSound); 
	qp += '&playOpenSound='+escape(playOpenSound); 
	qp += '&playCloseSound='+escape(playCloseSound);  
	qp += '&closeOnClick='+escape(closeOnClick); 
	qp += '&closeOnClickText='+escape(utf8encode(closeOnClickText)); 
	qp += '&eventLogUrl='+escape(eventLogUrl); 
	qp += '&pageearId='+escape(pageearId); 
	qp += '&lcKey='+escape(Math.random()); 
	qp += '&sKey=changeingtext'; 
	qp += '&bigWidth='+escape(bigWidth); 
	qp += '&thumbWidth='+escape(thumbWidth); 
	qp += '&videoBufferTime='+escape(videoBufferTime); 
	qp += '&preview='+escape(preview); 
	qp += '&range='+escape(range);  
	qp += '&ptype='+escape(ptype);
	qp += '&x='+escape(_uuid);
	return qp;
}

function openPeel(){
	document.getElementById('bigDiv').style.top = '0px'; 
	document.getElementById('bigDiv').style[xPos] = '0px';
	document.getElementById('thumbDiv').style.top = '-1000px';
}
function closePeel(){
	document.getElementById("thumbDiv").style.top = "0px";
	document.getElementById("bigDiv").style.top = "-1000px";
}
function writeObjects (_uuid) { 
    // Get installed flashversion
	var _content = '';
    var hasReqestedVersion = DetectFlashVer(requiredMajorVersion, requiredMinorVersion, requiredRevision);
    // Check direction 
    if(setDirection == 'lt') {
        xPosBig = 'left:-1000px';  
        xPos = 'left';   
    } else {
        xPosBig = 'right:1000px';
        xPos = 'right';              
    }
    // Write div layer for big swf
	_content += '<div id="bigDiv" style="position:absolute;width:'+ (bigWidth+50) +'px;height:'+ bigHeight +'px;z-index:9999;'+xPosBig+';top:-100px;">';
	var _queryParams = queryParams(_uuid);
   // Check if flash exists/ version matched
    if (hasReqestedVersion) {    	
    	_content += _AC_FL_RunContent(
						"src", pagearBigSwf+'?'+ _queryParams,
						"width", bigWidth+50,
						"height", bigHeight+50,
						"align", "middle",
						"id", "bigSwf",
						"quality", "high",
						"bgcolor", "#FFFFFF",
						"name", "bigSwf",
						"wmode", "transparent",
						"scale", "noscale",
						"salign", "tr",
						"allowScriptAccess","always",
						"type", "application/x-shockwave-flash",
						'codebase', 'http://fpdownload.macromedia.com/get/flashplayer/current/swflash.cab',
						"pluginspage", "http://www.adobe.com/go/getflashplayer"
    	);
    } else {  // otherwise do nothing or write message ...    	 
    	_content += 'no flash installed';  // non-flash content
    } 
    // Close div layer for big swf
    _content += '</div>'; 
    // Write div layer for small swf
    _content += '<div id="thumbDiv" style="position:absolute;width:'+ (thumbWidth+50) +'px;height:'+ thumbHeight +'px;z-index:9999;'+xPos+':0px;top:0px;">';
    // Check if flash exists/ version matched
    if (hasReqestedVersion) {    	
    	_content += _AC_FL_RunContent(
						"src", pagearSmallSwf+'?'+ _queryParams,
						"width", thumbWidth+50,
						"height", thumbHeight+50,
						"align", "middle",
						"id", "smallSwf",
						"scale", "noscale",
						"quality", "high",
						"bgcolor", "#FFFFFF",
						"name", "bigSwf",
						"wmode", "transparent",
						"allowScriptAccess","always",
						"type", "application/x-shockwave-flash",
						'codebase', 'http://fpdownload.macromedia.com/get/flashplayer/current/swflash.cab',
						"pluginspage", "http://www.adobe.com/go/getflashplayer"
    	);
    } else {  // otherwise do nothing or write message ...    	 
    	_content += 'no flash installed';  // non-flash content
    } 
    _content += '</div>';
	alert(_content);
    document.write(_content);
    setTimeout('document.getElementById("bigDiv").style.top = "-1000px";',100);
}
function utf8encode(txt) { 
    txt = txt.replace(/\r\n/g,"\n");
    var utf8txt = "";
    for(var i=0;i<txt.length;i++) {        
        var uc=txt.charCodeAt(i); 
        if (uc<128) {
            utf8txt += String.fromCharCode(uc);        
        } else if((uc>127) && (uc<2048)) {
            utf8txt += String.fromCharCode((uc>>6)|192);
            utf8txt += String.fromCharCode((uc&63)|128);
        } else {
            utf8txt += String.fromCharCode((uc>>12)|224);
            utf8txt += String.fromCharCode(((uc>>6)&63)|128);
            utf8txt += String.fromCharCode((uc&63)|128);
        }        
    }
    return utf8txt;
}
