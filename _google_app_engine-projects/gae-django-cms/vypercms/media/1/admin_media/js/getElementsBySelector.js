function getAllChildren(a){return a.all?a.all:a.getElementsByTagName("*")}document.getElementsBySelector=function(v){if(!document.getElementsByTagName){return new Array()}var p=v.split(" ");var g=new Array(document);for(var x=0;x<p.length;x++){token=p[x].replace(/^\s+/,"").replace(/\s+$/,"");if(token.indexOf("#")>-1){var s=token.split("#");var d=s[0];var r=s[1];var b=document.getElementById(r);if(d&&b.nodeName.toLowerCase()!=d){return new Array()}g=new Array(b);continue}if(token.indexOf(".")>-1){var s=token.split(".");var d=s[0];var c=s[1];if(!d){d="*"}var m=new Array;var l=0;for(var y=0;y<g.length;y++){var n;if(d=="*"){n=getAllChildren(g[y])}else{try{n=g[y].getElementsByTagName(d)}catch(z){n=[]}}for(var u=0;u<n.length;u++){m[l++]=n[u]}}g=new Array;var q=0;for(var t=0;t<m.length;t++){if(m[t].className&&m[t].className.match(new RegExp("\\b"+c+"\\b"))){g[q++]=m[t]}}continue}if(token.match(/^(\w*)\[(\w+)([=~\|\^\$\*]?)=?"?([^\]"]*)"?\]$/)){var d=RegExp.$1;var w=RegExp.$2;var a=RegExp.$3;var o=RegExp.$4;if(!d){d="*"}var m=new Array;var l=0;for(var y=0;y<g.length;y++){var n;if(d=="*"){n=getAllChildren(g[y])}else{n=g[y].getElementsByTagName(d)}for(var u=0;u<n.length;u++){m[l++]=n[u]}}g=new Array;var q=0;var f;switch(a){case"=":f=function(h){return(h.getAttribute(w)==o)};break;case"~":f=function(h){return(h.getAttribute(w).match(new RegExp("\\b"+o+"\\b")))};break;case"|":f=function(h){return(h.getAttribute(w).match(new RegExp("^"+o+"-?")))};break;case"^":f=function(h){return(h.getAttribute(w).indexOf(o)==0)};break;case"$":f=function(h){return(h.getAttribute(w).lastIndexOf(o)==h.getAttribute(w).length-o.length)};break;case"*":f=function(h){return(h.getAttribute(w).indexOf(o)>-1)};break;default:f=function(h){return h.getAttribute(w)}}g=new Array;var q=0;for(var t=0;t<m.length;t++){if(f(m[t])){g[q++]=m[t]}}continue}d=token;var m=new Array;var l=0;for(var y=0;y<g.length;y++){var n=g[y].getElementsByTagName(d);for(var u=0;u<n.length;u++){m[l++]=n[u]}}g=m}return g};