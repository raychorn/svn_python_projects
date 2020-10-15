// mya.js

/* left nav toggle */
function toggleMenu(menuId) {
	var selectedMenu = document.getElementById(menuId);
	var selectedMenuBlock = document.getElementById("sub_" + menuId);
	if (selectedMenuBlock.className == "showSubMenu") {
		selectedMenu.className = "tertMenu_Arrow";
		selectedMenuBlock.className = "hideSubMenu";
	} else {
		//selectedMenuBlock.className = "showSubMenu";
		//selectedMenu.className = "tertMenu_Arrow_on";
		showMenu(menuId);
	}
}
/* Added to solve manage payments tab in leftnav bill*/
function showMenu(menuId) {
	var menuArrowOnList = $ES('.tertMenu_Arrow_on');
	var showSubMenuList = $ES('.showSubMenu');
	//alert(saveBoxList.length);
	if (menuArrowOnList != null && showSubMenuList != null) {
		for (i = 0; i < menuArrowOnList.length; i++) {
			menuArrowOnList[i].className = "tertMenu_Arrow";;	
		}	
		for (i = 0; i < showSubMenuList.length; i++) {
			showSubMenuList[i].className = "hideSubMenu";;	
		}
	}	
	var selectedMenu = document.getElementById(menuId);
	var selectedMenuBlock = document.getElementById("sub_" + menuId);
	if (selectedMenu != null && selectedMenuBlock != null) {
		selectedMenuBlock.className = "showSubMenu";
		selectedMenu.className = "tertMenu_Arrow_on";
	}
}



/*
Added by Anuj on 3 march 2008.
New pages will use this function for displaying usage and other bar that dont require any other colour than green
*/
function pb_initNew(id,amount,clr) {	

	var bar = $(id);;//gn_engine.js must be added prior to use this function
//alert("id="+id+" amount="+amount);
	var r_g_y = 'green';
	
	if(clr=='RED')
	var r_g_y = 'red';
	
	if(clr=='YLW')
	var r_g_y = 'yellow';
	
	
	
/*	if (amount>=90)
	{
		var r_g_y = 'red';
	}

	if (yellow==true)
	{
		var r_g_y = 'yellow';
	}
*/
	var pixels = Math.round(((amount*.01)*242));//this cal will change if the length of bar is changed

	var meter = $E('.percentage_bar242_amount',bar);//gn_engine.js must be added prior to use this function
	
	meter.removeClass('percentage_bar242_amount');
	meter.addClass('percentage_bar242_'+r_g_y);
	
	var reveal = new Fx.Styles(meter, {
		duration: 1000,
		transition: Fx.Transitions.Quad.easeOut,
		wait: true,
		fps: 24
	});
	
	reveal.start({
		'width': [0,pixels],
		'opacity': [0,1]
	});
}


function call(url, data, displayResult, displayTimeOutMsg, displayHttpError, displayInProcessingMsg,customTimeOut) {
	  if (globalAccessTime != null) {
 	  	var sessionTimeout = 9 * 60 * 1000;
	  	var currentTime = new Date().getTime();
      	if( currentTime - (globalAccessTime + (sessionTimeout)) > 0 )
	  	{
			window.top.location = "/vzw/secure/router.action";
			return;
	  	}
	 	else
      	{
			globalAccessTime = new Date().getTime();
	  	}
	  } 
 
	  var timeoutID;
	  var timeout = 20000;	// timeout 20 sec
	  if(customTimeOut != null && customTimeOut != '' ){
	  	timeout = customTimeOut;
	  }
	  
  	  var XMLHttpRequestObject=false;
  	  if(!XMLHttpRequestObject) {
		  if (window.XMLHttpRequest) {
		  	XMLHttpRequestObject = new XMLHttpRequest();
		  } else if (window.ActiveXObject) {
		    XMLHttpRequestObject = new ActiveXObject("Microsoft.XMLHTTP");
		  }
	  }
	  else {
	  	  if(XMLHttpRequestObject.readyState != 0 && XMLHttpRequestObject.readyState != 4) {
	  	  	XMLHttpRequestObject.abort();
	  	  	if (window.XMLHttpRequest) {
		    	XMLHttpRequestObject = new XMLHttpRequest();
		  	} else if (window.ActiveXObject) {
		    	XMLHttpRequestObject = new ActiveXObject("Microsoft.XMLHTTP");
		  	}
	  	  }
	  }
	  
	  try {
	  	XMLHttpRequestObject.open("POST", url, true);
	  	timeoutID = setTimeout(function() {
				displayTimeOutMsg();
		}, timeout);
	  	XMLHttpRequestObject.onreadystatechange = function() {
	  		try {
	        	if (XMLHttpRequestObject.readyState == 4) {
	        		clearTimeout(timeoutID);
		        	if (XMLHttpRequestObject.status == 200) {
		        		/* Get plain string OR xmlDocument from XMLHttpRequestObject */
		        		//var rslt = XMLHttpRequestObject.responseText;	
		        		//var xmlDocument = XMLHttpRequestObject.responseXML;
		        		
		        		displayResult(XMLHttpRequestObject);
					}
					else {
						displayHttpError();
					}
				}
				else {
					displayInProcessingMsg();
			    }
			}
		    catch(err) {
		         //alert("Error detail: " + err.message);
		    }
	  	}
	  	XMLHttpRequestObject.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      	XMLHttpRequestObject.send(data);
	  	
	  }
	  catch (err) {
	     //alert("err ..."+err.message);
	  }
}



/* General Util Functions added by EC */
/* vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv */
function getLikeElements(tagName, attrName, attrValue) {
    var startSet;
    var endSet = new Array();
    if (tagName) {
        startSet = document.getElementsByTagName(tagName);    
    } else {
        startSet = (document.all) ? document.all : document.getElementsByTagName("*");
    }
    if (attrName) {
        for (var i = 0; i < startSet.length; i++) {
            if (startSet[i].getAttribute(attrName)) {
                if (attrValue) {
                    if (startSet[i].getAttribute(attrName) == attrValue) {
                        endSet[endSet.length] = startSet[i];
                    }
                } else {
                    endSet[endSet.length] = startSet[i];
                }
            }
        }
    } else {
        endSet = startSet;
    }
    return endSet;
}

function trim(stringToTrim) {
	return stringToTrim.replace(/^\s+|\s+$/g,"");
}
function ltrim(stringToTrim) {
	return stringToTrim.replace(/^\s+/,"");
}
function rtrim(stringToTrim) {
	return stringToTrim.replace(/\s+$/,"");
}
/* ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ */
/* General Util Functions added by EC */


/* Added by shashi from Auto pay */

function addSuffix(dateValue) {

	if (dateValue==1 ||dateValue==21 || dateValue==31) suffix=("st");
		else if (dateValue==2 || dateValue==22) suffix=("nd");	
		else if (dateValue==3 || dateValue==23) suffix=("rd");
		else suffix=("th");
		
	
		return (dateValue+suffix);
}

/* Added by tim for disabling autocomplete functionality*/
function setNodeAttribute(nodeObj, attrName, attrValue) {
	var attributeNode = nodeObj.getAttributeNode(attrName);
	
	if (attributeNode)
		attributeNode.value = attrValue;
	else 
		nodeObj.setAttribute(attrName, attrValue);
}

function disableAutocompleteById(objId) {
	var obj = document.getElementById(objId);
	if (obj == null)
		return;
	setNodeAttribute(obj, 'autocomplete', 'off');
}

function disableAutocompleteByElem(elem) {
	if (elem == null)
		return;
	setNodeAttribute(elem, 'autocomplete', 'off');
}

/* Added by Niral for Alltel Handset Conversion */
function aspRedirect(url, loginDevice, alwaysNewWindow) {
	if (loginDevice == 'ATL') {
		if ((url.indexOf('support.vzw.com') != -1) || (url.indexOf('stage-support.vzw.com') != -1)
			|| (url.indexOf('text.vzw.com') != -1) || (url.indexOf('products.vzw.com'))!= -1 ) {
			window.location.href = url;
		} else {
		window.open(url);
	}
	}
	else {
		if (alwaysNewWindow) {
			window.open(url);
		} else {
			window.location.href = url;
		}
	}
}
/* Added by Neha for My Services Left Nav for Federated Customers*/
var phone_url;
var tv_url;
var internet_url;

function setLeftNavUrl(type, passedURL){
	if (type == 'phone')
	  phone_url = passedURL;
	else if (type == 'tv')
	  tv_url = passedURL;
	else if (type == 'internet')
	  internet_url = passedURL;
	  var displayURL = "";
	  
	if(phone_url != null && phone_url != "")
		 displayURL = displayURL + '<a class="tertMenu" onclick="javascript:window.open(getURL(\'phone\'),\'_self\');">My Home Phone</a>';
	if(tv_url != null && tv_url != "")
		 displayURL = displayURL + '<a class="tertMenu" onclick="javascript:window.open(getURL(\'tv\'),\'_self\');">My TV</a>';
	if(internet_url != null && internet_url != "")
		 displayURL = displayURL + '<a class="tertMenu" onclick="javascript:window.open(getURL(\'internet\'),\'_self\');">My Internet</a>';

	document.getElementById('leftNavFed').innerHTML = displayURL;
}

function getURL(type){
	if (type == 'phone')
		return phone_url;
	else if (type == 'tv')
	  return tv_url;
	else if (type == 'internet')
	  return internet_url;
}	
