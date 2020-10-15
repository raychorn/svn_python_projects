//auther: leon
//gsmstock modify 2008.6.12
var public_link_data = "";
if(typeof(bookmark_url)=="undefined" ||  bookmark_url=="")
{
    public_link_data=window.location;
}
else
  public_link_data = bookmark_url;
    
var data=public_link_data;
var encodeData=encodeURIComponent(data);
var name="";


if(typeof(bookmark_title)=="undefined" ||  bookmark_title=="")
{
   try { name=document.title; }catch(err) { }
}
else
   name = bookmark_title;

var comment="";
try {
	var objMeta = document.getElementsByTagName("meta");
	for(var j=0;j<objMeta.length;j++) {
	   if ( objMeta[j].name == "description")
		comment += objMeta[j].content;
	}
}
catch(err) { }
//alert(comment);

function showBookmarks()
{
  
	if (document.getElementById("bookmark").style.display != "block") document.getElementById("bookmark").style.display = "block";
}
function hideBookmarks()
{
	if (document.getElementById("bookmark").style.display != "none") document.getElementById("bookmark").style.display = "none";
}
function addfavorite(){
	if (document.all){
		window.external.addFavorite(public_link_data, name);
	}
	else if (window.sidebar){
		window.sidebar.addPanel(name, public_link_data,"");
	}
}
function findOffsetTop(o)
{
    var t = 0;
    if (o.offsetParent)
    {
        while (o.offsetParent)
        {
            t += o.offsetTop;
            o  = o.offsetParent;
        }
    }
    return t;
}
function findOffsetLeft(o)
{
    var t = 0;
    if (o.offsetParent)
    {
        while (o.offsetParent)
        {
            t += o.offsetLeft;
            o  = o.offsetParent;
        }
    }
    return t;
}
// locate the bookmark
var _position = "";
if (typeof(bookmark_position)=="undefined" || bookmark_position == ""){
	//_position = "position: absolute; top:5px; right: 5px;";
	_position = "";
}
else
	_position = bookmark_position;

document.write("<style>");
document.write("#bookmarkIcon { background: url(/media/bookmarkimages/button4-bm.gif) left top no-repeat; width: 125px; height: 16px;  cursor: pointer;display: inline; "+_position+" }");
document.write("#bookmark { border: 1px solid gray; background: white; width: 245px; display: none; }");
document.write("#bookmark ul { padding: 0; margin: 0; }");
document.write("#bookmark li { list-style: none; margin: 2px 0; padding:0; padding-left: 12px; float: left; width: 98px; height: 18px; line-height: 18px; text-align:left; }");
document.write("#bookmark li a { font-size: 12px; font-weight: normal; font-style: normal; font-family: Tahoma, Verdana, Arial; font-variant: normal; text-transform: capitalize; }");
document.write("</style>");

document.write("<div id=\"bookmarkIcon\" onmouseover=\"showBookmarks();\"><img src=\"/media/bookmarkimages/button4-bm.gif\" border=\"0\" alt=\"\" /></div>");
document.write("<div id=\"bookmark\" onmouseout=\"hideBookmarks();\" onmouseover=\"showBookmarks();\">");
document.write("<ul><li><img src=\"/media/bookmarkimages/favorites.png\" alt=\"添到本机收藏夹\" align=\"absmiddle\" border=\"0\">&nbsp;<a id=\"Favorite\" href=\"javaScript:addfavorite();\">添到收藏夹</a></li>");
document.write("<li><img src=\"/media/bookmarkimages/baidu.jpg\" alt=\"添加到百度搜藏\" align=\"absmiddle\" border=\"0\">&nbsp;<a id=\"baidu\" href=\"javascript:u=location.href;t=document.title;c = %22%22 + (window.getSelection ? window.getSelection() : document.getSelection ? document.getSelection() : document.selection.createRange().text);location=%22http://cang.baidu.com/do/add?it=%22+encodeURIComponent(name)+%22&iu=%22+encodeURIComponent(data)+%22&dc=%22+encodeURIComponent(comment)+%22&fr=ieo%22;\">百度搜藏</a></li>");
document.write("<li><img src='/media/bookmarkimages/delicious.gif' alt='Del.icio.us' border='0' align=\"absmiddle\" >&nbsp;<a id=\"delicious\" href=\"javascript:location.href='http://del.icio.us/post?url='+encodeURIComponent(data)+'&title='+encodeURIComponent(name)+'&notes='+encodeURIComponent(comment)\">Del.icio.us</a></li>");
document.write("<li><img src='/media/bookmarkimages/shuqianqq.gif' alt='收藏到QQ书签' border='0' align=\"absmiddle\" >&nbsp;<a id=\"qq\" href=\"javascript:location.href='http://shuqian.qq.com/users/addBookmark/?jumpback=1&title='+encodeURIComponent(name)+'&uri='+encodeURIComponent(data)+'&desc='+encodeURIComponent(comment);void(0);\">QQ书签</a></li>");
document.write("<li><img src='/media/bookmarkimages/digg.png' alt='收藏到 digg' border='0' align=\"absmiddle\" >&nbsp;<a id=\"digg\" href=\"javascript:location.href='http://digg.com/submit?phase=2&url='+encodeURIComponent(name)+'&title='+encodeURIComponent(name);void(0);\">Digg</a></li>");
document.write("<li><img src='/media/bookmarkimages/vivi.gif' alt='新浪ViVi' border='0' align=\"absmiddle\" >&nbsp;<a href=\"javascript:d=document;t=d.selection?(d.selection.type!='None'?d.selection.createRange().text:''):(d.getSelection?d.getSelection():'');void(vivi=window.open('http://vivi.sina.com.cn/collect/icollect.php?pid=28&title='+escape(name)+'&url='+escape(public_link_data)+'&desc='+escape(t),'vivi','scrollbars=no,width=480,height=480,left=75,top=20,status=no,resizable=yes'));vivi.focus();\">新浪ViVi</a></li> ");
document.write("<li><img src=\"/media/bookmarkimages/technorati2.png\" alt=\"technorati.com\" border=\"0\" align=\"absmiddle\" >&nbsp;<a id=\"technorati\" href=\"javascript:location.href='http://www.technorati.com/faves?add='+encodeURIComponent(name)\">Technorati</a></li>");
document.write("<li><img src='/media/bookmarkimages/goog.png' alt='Google书签' border='0' align=\"absmiddle\" >&nbsp;<a id=\"google\" href=\"javascript:location.href='http://www.google.com/bookmarks/mark?op=add&bkmk='+encodeURIComponent(data)+'&title='+encodeURIComponent(name)+'&annotation='+encodeURIComponent(comment)\">Google书签</a></li>");
document.write("<li><img src=\"/media/bookmarkimages/furl.gif\" alt=\"furl.com\" border=\"0\" align=\"absmiddle\" />&nbsp;<a id=\"furl\" href=\"javascript:location.href='http://furl.net/storeIt.jsp?u='+escape(data)+'&t='+escape(name)\">Furl</a></li>");
document.write("<li><img src=\"/media/bookmarkimages/yahoo.png\" border=0 align=\"absmiddle\" >&nbsp;<a id=\"yahoo\" href=\"javascript:location.href='http://myweb.cn.yahoo.com/addp.html?method=add&url='+encodeURIComponent(data)+'&title='+encodeURIComponent(name)+'&src=iebookmark&summary='+encodeURIComponent(comment);void(0);\">雅虎搜藏</a></li>");
document.write("<li><img src=\"/media/bookmarkimages/su.png\" border=\"0\" align=\"absmiddle\" alt=\"stumbleupon.com\" />&nbsp;<a href=\"javascript:location.href='http://www.stumbleupon.com/submit?url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title)\">Stumbleupon</a></li>");
document.write("<li><img src=\"/media/bookmarkimages/sk-cl5.gif\" border=\"0\" align=\"absmiddle\" alt=\"收藏到收客shouker.com\" />&nbsp;<a id=\"shouker\" href=\"http://www.shouker.com/\" onclick=\"javascript:var js=document.createElement('scri'+'pt');if(typeof(js)!='object')js=document.standardCreateElement('scri'+'pt');js.type='text/javascript';js.src='http://www.shouker.com/js/capageb.js';document.getElementsByTagName('html')[0].appendChild(js);return false;\" title=\"收藏到收客网shouker.com\">收客网</a></li>");

document.write("<li><img src=\"/media/bookmarkimages/sphere.gif\" border=\"0\" align=\"absmiddle\" alt=\"sphere.com\" />&nbsp;<a href=\"javascript:location.href='http://www.sphere.com/search?q=sphereit:'+encodeURIComponent(location.href)\">Sphere</a> ");

document.write("<li><img src=\"/media/bookmarkimages/9fav_16_16_logo.gif\" alt=\"收藏到〖就喜欢〗智能网络收藏夹\" border=\"0\" align=\"absmiddle\" >&nbsp;<a href=\"javascript:{var o=document.createElement('scri'+'pt');o.setAttribute('src','http://www.9fav.com/fav/starter?url='+encodeData);o.setAttribute('id','fav_bookmark_scripts');o.setAttribute('type','text/javascript');o.setAttribute('charset', 'utf-8');document.body.appendChild(o);void(0);}\" title=\"收藏到就喜欢\" class=\"outer_link\">就喜欢</a></li>");
document.write("<li><img src='/media/bookmarkimages/live.gif' alt='live.com' border='0' align=\"absmiddle\" >&nbsp;<a id=\"live\" href=\"javascript:location.href='https://favorites.live.com/quickadd.aspx?marklet=1&mkt=en-us&top=1&url='+encodeURIComponent(data)+'&title='+encodeURIComponent(name)\">Windows Live</a></li>");
document.write("<li><img src=\"/media/bookmarkimages/hexun.jpg\" alt=\"和讯网摘\" border=\"0\" align=\"absmiddle\" >&nbsp;<a id=\"hexun\" href=\"javascript:location.href='http://bookmark.hexun.com/post.aspx?title='+escape(name)+'&url='+escape(data)+'&excerpt='+escape(comment)\">和讯网摘</a></li>");
document.write("</ul></div>");

// locate the bookmark_body
bi = document.getElementById("bookmarkIcon");
b = document.getElementById("bookmark");
showBookmarks();
b.style.position = "absolute";
//b.style.position ="";
b.style.top = findOffsetTop(bi) - 100 + "px";
//b.style.top =  18 + "px";
if (document.all)
	b.style.left = findOffsetLeft(bi) -155 + "px";
else
	b.style.left = findOffsetLeft(bi) - 155 + "px";
	

hideBookmarks();
