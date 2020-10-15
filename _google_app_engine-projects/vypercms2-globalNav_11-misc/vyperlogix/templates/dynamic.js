
var css;function include_css(css_file){var html_doc=document.getElementsByTagName('head')[0];css=document.createElement('link');css.setAttribute('rel','stylesheet');css.setAttribute('type','text/css');css.setAttribute('href',css_file);html_doc.appendChild(css);css.onreadystatechange=function(){if(css.readyState=='complete'){}}
css.onload=function(){}
return false;}
var js;function include_js(file,callback){var html_doc=document.getElementsByTagName('head')[0];js=document.createElement('script');js.setAttribute('type','text/javascript');js.setAttribute('src',file);html_doc.appendChild(js);js.onreadystatechange=function(){if(js.readyState=='complete'){try{callback();}catch(e){};}}
js.onload=function(){try{callback();}catch(e){};}
return false;}