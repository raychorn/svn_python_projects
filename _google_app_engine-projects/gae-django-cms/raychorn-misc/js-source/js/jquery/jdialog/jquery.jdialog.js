/*
 * jDialog v 0.3.1
 * Ytrip Dev Team. Jason Lee 2008-03-26
 * a dialog like facebook.com
 * http://www.ytrip.com
 */
var jDialog = {

  owner : undefined,
  
  hovered : false,
  
  settings : {      
    idName : "paneljDialog",
    title : "Dialog",
    content : "",
    width : 250,
    close_on_body_click : true
  },   
  
  show : function(settings){        
    var pos = jDialog.getPos();
    $.extend(jDialog.settings,settings);
      
    jDialog.close();
    
    var dialog = $("#"+jDialog.settings.idName);
        
    if(dialog.size() == 0){
      var cssArrow = "contextual_arrow_rev";
      var posTop =  pos.top + pos.height + 2;
      var posLeft = pos.left + 1;
      var browserHalfSize = jDialog.getBrowserHafeSize();

      if(posLeft > browserHalfSize.width){
          posLeft =  pos.left;
          cssArrow = "contextual_arrow";
      }
      
      var cssPosition = 'top:'+ posTop + 'px;left:'+ posLeft +'px;';
      
      var html = '';
      html += '<div id="'+jDialog.settings.idName+'" class="jdialog_outterbox" style="position:absolute;display:none;'+ cssPosition+ '">';
      html += '   <div class="jdialog_dialog_popup" style="width:'+ jDialog.settings.width +'px">';
      html += '       <div class="'+ cssArrow +'"></div>';
      html += '       <div class="contextual_dialog_shadow">'
      html += '           <div class="contextual_dialog_content">';
      html += '               <h2><span>'+jDialog.settings.title+'</span></h2>';
      html += '               <div class="jdialog_close" onclick="jDialog.close();" title="Close"></div>';
      html += '               <div class="dialog_content">';
      html += '                   <div class="dialog_body clearfix">';
      html += '                       '+jDialog.settings.content;
      html += '                   </div>';
      html += '               </div>';
      html += '           </div>';
      html += '       </div>';
      html += '   </div>';
      html += '</div>';
      
      $("body").append($(html));
      
      dialog = $("#"+jDialog.settings.idName);
      dialog.hover(function(){ jDialog.hovered = true; },function(){ jDialog.hovered = false; });
    }
    dialog.show();
    
    // auto close when body click
    if(jDialog.settings.close_on_body_click){
      $(document).mousedown(function(){
        jDialog.close();
      });
    
      dialog.mousedown(function(){ return false; });
    }
  },
  
  update : function(content){
    $("#"+ jDialog.settings.idName +" .dialog_body").html(content);      
  },
  
  close : function(){
    var dialog = $("#"+jDialog.settings.idName);
    dialog.hide();
    dialog.remove();
  },
  
  getBrowserHafeSize : function(){        
		var browserWidth = window.innerWidth || document.documentElement.clientWidth ||
			document.body.clientWidth;
		var browserHeight = window.innerHeight || document.documentElement.clientHeight ||
			document.body.clientHeight;
		var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
		var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
		return {width: ( browserWidth / 2) - 150 + scrollX,height: ( browserHeight / 2) - 100 + scrollY};
  },
  
  getPos : function(){    
    if(jDialog.owner == undefined){
      return {top : 0, left:0 , width : 0, height : 0};
    }
    
    var e = jDialog.owner;
    var oTop = e.offsetTop; 
    var oLeft = e.offsetLeft; 
    var oWidth = e.offsetWidth; 
    var oHeight = e.offsetHeight; 
    while(e = e.offsetParent) 
    { 
	    oTop += e.offsetTop; 
	    oLeft += e.offsetLeft; 
    }
    
    return {
      top : oTop,
      left : oLeft,
      width : oWidth,
      height : oHeight
    }
  }
    
};

jQuery.fn.jDialog = function(settings){   
  jDialog.owner = this[0]; 
  jDialog.show(settings);
}

jQuery.fn.jDialog.close = function(){
  jDialog.close();
}

jQuery.fn.jDialog.update = function(content){
  jDialog.update(content);
}
