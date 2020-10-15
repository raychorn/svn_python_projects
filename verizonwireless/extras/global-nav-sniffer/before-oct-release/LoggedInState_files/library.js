

function rollovers_Init() {
	ro_init();
}

function tooltip_Init() {
	tt_init();
}

function pb_init(id,amount,yellow) {	
	var bar = $(id);
	var r_g_y = 'green';
	
	if (amount>=90)
	{
		var r_g_y = 'red';
	}

	if (yellow==true)
	{
		var r_g_y = 'yellow';
	}

	var pixels = Math.round(((amount*.01)*185));

	var meter = $E('.percentage_bar_amount',bar);
	
	meter.removeClass('percentage_bar_amount');
	meter.addClass('percentage_bar_'+r_g_y);
	
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

function tg_init(togglers_name,toggleds_name,active,track) {
	var preload = new Array();

	var togglers = $ES('.'+togglers_name);
	
	var toggleds = $ES('.'+toggleds_name);

	togglers.each(function(toggler,index) {
		var active_content = toggleds[index];

		if (toggler.tagName=='IMG')
		{
			toggler.addEvents({
				'click':  function() {
					if (active==true)
					{
						var handlers = $ES('.'+togglers_name);
						handlers.each(function(handler) {
							var source = handler.src;
							if (source.match('_active'))
							{
								var newSource = source.replace(/_active/, '_off');
								handler.src = newSource;
							}
						});

						var source = toggler.src;
						var newSource = source.replace(/_on/, '_active');
						toggler.src = newSource;
					}
					
					var contents = $ES('.'+toggleds_name);
					contents.each(function(content) {
						content.addClass('hidden');
						content.removeClass('visible');
					});

					active_content.removeClass('hidden');
					active_content.addClass('visible');
					
					if (track==true && toggler.id!='')
					{
						if (window._hbLink)
						{
							_hbLink(toggler.id);
						}
					}
				}
			});

			preload[index] = new Image();
			var newSource = toggler.src.replace(/_off/, '_active');
			preload[index].src = newSource;
		}
		else
		{
			if (toggler.hasClass('active'))
			{
				toggler.removeClass('active');
				toggler.removeClass(togglers_name);
				toggler.addClass(togglers_name+'_active');	
			}

			toggler.addEvents({
				'click':  function() {
					var handlers = $ES('.'+togglers_name+'_active');
					handlers.each(function(handler) {
						handler.removeClass(togglers_name+'_active');
						handler.addClass(togglers_name);
					});

					toggler.removeClass(togglers_name);
					toggler.addClass(togglers_name+'_active');

					var contents = $ES('.'+toggleds_name);
					contents.each(function(content,index) {
						content.addClass('hidden');
						content.removeClass('visible');
					});

					active_content.removeClass('hidden');
					active_content.addClass('visible');
					
					if (track==true && toggler.id!='')
					{
						if (window._hbLink)
						{
							_hbLink(toggler.id);
						}
					}
				}
			});
		}
	});
}

function ro_init() {
	var preload = new Array();

	for (i=0;i<arguments.length;i++)
	{
		var cl = arguments[i];
		var els = $ES('.'+cl);
		els.each(function(el) {
			ro_add_el(el,cl);
		});
	}

	var els = $ES('.rollover');
	els.each(function(el,index) {
		if (el.tagName == 'IMG')
		{
			preload[index] = new Image();
			var newSource = el.src.replace(/_off/, "_on");
			preload[index].src = newSource;
			ro_add_img(el);
		}
	});
	
	function ro_add_img(el) {
		el.addEvents({
			'mouseenter':  function() {
				var source = el.src;
				if (!(source.match("_active")))
				{
					var newSource = source.replace(/_off/, "_on");
					el.src = newSource;
				}
			},

			'mouseleave': function() {
				var source = el.src;
				if (!(source.match("_active")))
				{
					var newSource = source.replace(/_on/, "_off");
					el.src = newSource;
				}
			}
		});

		var pt = $(el.parentNode);

		if (pt.tagName == 'A')
		{
			pt.addEvents({
				'focus':  function() {
					var source = el.src;
					if (!(source.match("_active")))
					{
						var newSource = source.replace(/_off/, "_on");
						el.src = newSource;
					}
				},

				'blur': function() {
					var source = el.src;
					if (!(source.match("_active")))
					{
						var newSource = source.replace(/_on/, "_off");
						el.src = newSource;
					}
				}
			});
		}
	} 
		
	function ro_add_el(el,cl) {

		el.addEvents({
			'mouseenter':  function() {
				if (!(el.className.match("_active")))
				{
					el.removeClass(cl);
					el.addClass(cl+'_on');
				}
			},
			'mouseleave': function() {
				if (!(el.className.match("_active")))
				{
					el.removeClass(cl+'_on');
					el.addClass(cl);
				}
			},
			'focus':  function() {
				if (!(el.className.match("_active")))
				{	
					el.removeClass(cl);
					el.addClass(cl+'_on');
				}
			},
			'blur': function() {
				if (!(el.className.match("_active")))
				{
					el.removeClass(cl+'_on');
					el.addClass(cl);
				}
			}
		});
	}
}

function tt_init(serverPath) {

	// the tooltips image directory if you want to use tooltips
	var lib_img_dir = serverPath + '/nda/images/tooltips/';

	// mapping controls image location if you want to use mapping controls
	var pog_img_dir =  serverPath + '/nda/images/mapping_controls/';
	
	var bases = $ES('.tooltip');
	var tips = $ES('.tip');
	
	var body  = document.getElementsByTagName('body').item(0);
	var div = document.createElement('DIV');
	var div = $(div);
	div.id='tip_holder';
	div.style.left='-1000em';
	body.appendChild(div);

	var use_ishim=false;
	
	if (navigator.appVersion.indexOf("MSIE")!=-1){
	try
	{
		document.execCommand("BackgroundImageCache", false, true); 
	}
	catch(err)
	{
	}
	var temp=navigator.appVersion.split("MSIE")
	var version=parseFloat(temp[1])
		if (version>=6 && version<7)
		{
			use_ishim=true;
			body.insertAdjacentHTML('beforeEnd', '<iframe src="javascript:false" id="tt_ishim" frameborder="0" scrolling="0" style="position:absolute;top:0;left:0;width:0;height:0;display:none;z-index:99;filter:progid:DXImageTransform.Microsoft.Alpha(style=0,opacity=0);"></iframe>');
		}
	}
	
	function tt_ishim(show)
	{
		var ishim = $('tt_ishim');
		var tip_holder = $('tip_holder');
		if(show==true && use_ishim==true)
		{	
			ishim.style.display = 'block';
			var div_pos = tip_holder.getCoordinates();
			ishim.style.width = div_pos.width;
			ishim.style.height = div_pos.height;
			ishim.style.top = div_pos.top;
			ishim.style.left = div_pos.left;
		}
		
		if (show==false && use_ishim==true)
		{
			ishim.style.display = 'none';
		}
	}

	tt_dsir(div);
	
	var reveal = new Fx.Styles(div, {
		duration: 200,
		transition: Fx.Transitions.Quad.easeIn,
		wait: true,
		fps: 24
	});

	reveal.addEvent('onStart', function(){
		tt_ishim(true);
	});

	var repeal = new Fx.Styles(div, {
		duration: 200,
		transition: Fx.Transitions.Quad.easeIn,
		wait: true,
		fps: 24
	});

	repeal.addEvent('onComplete', function(){
		tt_ishim(false);
		div.style.left='-1000em';
		$('tt_arrow_up').style.visibility='hidden';
		$('tt_arrow_down').style.visibility='hidden';
	});

	function tt_locate(base) {
		var arrow_up = $('tt_arrow_up');
		var arrow_down = $('tt_arrow_down');

		arrow_down.style.left='20px';
		arrow_up.style.left='20px';
		arrow_down.style.right='';
		arrow_up.style.right='';

		var content = this.clone();
		content.style.position='relative';
		content.style.left='0';
		
		if (content.style.marginTop=='')
		{
			var mt=0;
		}
		else
		{
			var mt=content.style.marginTop.toInt();
		}

		if (content.style.marginRight=='')
		{
			var mr=0;
		}
		else
		{
			var mr=content.style.marginRight.toInt();
		}

		if (content.style.marginBottom=='')
		{
			var mb=0;
		}
		else
		{
			var mb=content.style.marginBottom.toInt();
		}

		if (content.style.marginLeft=='')
		{
			var ml=0;
		}
		else
		{
			var ml=content.style.marginLeft.toInt();
		}

		content.style.margin='0';
		var con_des = $('tip_content');
		tt_base = base;
		con_des.innerHTML='';
		con_des.appendChild(content);

		var win = {'x': window.getWidth(), 'y': window.getHeight()};
		var scroll = {'x': window.getScrollLeft(), 'y': window.getScrollTop()};
		var tip = {'x': div.offsetWidth, 'y': div.offsetHeight};
		
		var l = base.getCoordinates().left.toInt();
		var l = l+ml-mr;

		var x_total = win.x+scroll.x;
		if (!(x_total-l>tip.x))
		{	
			if (l-scroll.x>tip.x)
			{	
				var l = l-tip.x;
				arrow_down.style.left='';
				arrow_up.style.left='';
				arrow_down.style.right='20px';
				arrow_up.style.right='20px';
			}
		}

		var t = base.getCoordinates().top.toInt();
		var b = base.getCoordinates().bottom.toInt();

		var y_avail = t-scroll.y;
		if (!(y_avail>tip.y))
		{
			var t = b-5;
			arrow_down.style.visibility='hidden';
			arrow_up.style.visibility='visible';
		}
		else
		{
			var to = tip.y;
			var t = t-to+5;
			arrow_up.style.visibility='hidden';
			arrow_down.style.visibility='visible';
		}
		
		div.style.left=l+'px';
		div.style.top=t+'px';

		reveal.start({
			'opacity': [0,1]
		});
	}
		
	bases.each(function(base,index) {
		base.addEvents({
			'mouseenter':  function(e) {
				$clear(tt_locate_to);

				var relTarg = e.relatedTarget || e.fromElement;
				while (relTarg && relTarg != base && relTarg != div && relTarg.nodeName != 'BODY')
				relTarg = relTarg.parentNode
				if (relTarg == base || relTarg == div) return;

				tt_locate_to = tt_locate.delay(500,tips[index],base);	
			},

			'mouseleave': function(e) {
				$clear(tt_locate_to);
				
				var relTarg = e.relatedTarget || e.toElement;
				while (relTarg && relTarg != base && relTarg != div && relTarg.nodeName != 'BODY')
				relTarg = relTarg.parentNode
				if (relTarg == base || relTarg == div) return;

				reveal.stop();
				repeal.start({
					'opacity': [1,0]
				});
			}
		});
	});

	var tt_locate_to;

	div.addEvents({
		'mouseleave': function(e) {			
			$clear(tt_locate_to);

			var relTarg = e.relatedTarget || e.toElement;
			while (relTarg && relTarg != tt_base && relTarg != div && relTarg.nodeName != 'BODY')
			relTarg = relTarg.parentNode
			if (relTarg == tt_base || relTarg == div) return;

			reveal.stop();
			repeal.start({
				'opacity': [1,0]
			});
		}
	});

	function tt_dsir(div) {
		if (navigator.appVersion.indexOf("MSIE")!=-1){
			try
			{
				document.execCommand("BackgroundImageCache", false, true); 
			}
			catch(err)
			{
			}
		tt_pngorgif = 'gif';
		}
		else
		{
		tt_pngorgif = 'png';
		}

		var tbl = document.createElement('TABLE');
		tbl.setAttribute("cellpadding", "0");
		tbl.setAttribute("cellspacing", "0");
		tbl.setAttribute("border", "0");
		tbl.id='tip_table';
		div.appendChild(tbl);
		var tblbody = document.createElement('TBODY');
		tbl.appendChild(tblbody);

		var tr1 = document.createElement('TR');
		tblbody.appendChild(tr1);
		var tr2 = document.createElement('TR');
		tblbody.appendChild(tr2);
		var tr3 = document.createElement('TR');
		tblbody.appendChild(tr3);

		var td1 = document.createElement('TD');
		td1.setAttribute("align", "right");
		td1.setAttribute("valign", "bottom");
		var img1 = document.createElement('IMG');
		img1.src = lib_img_dir+tt_pngorgif+'/tile_top_left.'+tt_pngorgif;
		img1.style.width='15px';
		img1.style.height='15px';
		td1.appendChild(img1);
		tr1.appendChild(td1);

		var td2 = document.createElement('TD');
		td2.style.background = 'url('+lib_img_dir+tt_pngorgif+'/tile_top.'+tt_pngorgif+') repeat-x bottom left';
		var img2 = document.createElement('IMG');
		img2.src = lib_img_dir+'s.gif';
		td2.appendChild(img2);
		tr1.appendChild(td2);

		var td3 = document.createElement('TD');
		td3.setAttribute("align", "left");
		td3.setAttribute("valign", "bottom");
		var img3 = document.createElement('IMG');
		img3.src = lib_img_dir+tt_pngorgif+'/tile_top_right.'+tt_pngorgif;
		img3.style.width='15px';
		img3.style.height='15px';
		td3.appendChild(img3);
		tr1.appendChild(td3);

		var td4 = document.createElement('TD');
		td4.style.background = 'url('+lib_img_dir+tt_pngorgif+'/tile_left.'+tt_pngorgif+') repeat-y top right';
		var img4 = document.createElement('IMG');
		img4.src = lib_img_dir+'s.gif';
		td4.appendChild(img4);
		tr2.appendChild(td4);

		var td5 = document.createElement('TD');
		td5.id='tip_content';	
		tr2.appendChild(td5);

		var td6 = document.createElement('TD');
		td6.style.background = 'url('+lib_img_dir+tt_pngorgif+'/tile_right.'+tt_pngorgif+') repeat-y top left';
		var img6 = document.createElement('IMG');
		img6.src = lib_img_dir+'s.gif';
		td6.appendChild(img6);
		tr2.appendChild(td6);

		var td7 = document.createElement('TD');
		td7.setAttribute("align", "right");
		td7.setAttribute("valign", "top");
		var img7 = document.createElement('IMG');
		img7.src = lib_img_dir+tt_pngorgif+'/tile_bottom_left.'+tt_pngorgif;
		img7.style.width='15px';
		img7.style.height='15px';
		td7.appendChild(img7);
		tr3.appendChild(td7);

		var td8 = document.createElement('TD');
		td8.style.background = 'url('+lib_img_dir+tt_pngorgif+'/tile_bottom.'+tt_pngorgif+') repeat-x top left';
		var img8 = document.createElement('IMG');
		img8.src = lib_img_dir+'s.gif';
		td8.appendChild(img8);
		tr3.appendChild(td8);

		var td9 = document.createElement('TD');
		td9.setAttribute("align", "left");
		td9.setAttribute("valign", "top");
		var img9 = document.createElement('IMG');
		img9.src = lib_img_dir+tt_pngorgif+'/tile_bottom_right.'+tt_pngorgif;
		img9.style.width='15px';
		img9.style.height='15px';
		td9.appendChild(img9);
		tr3.appendChild(td9);

		var arrow_down = document.createElement('DIV');
		arrow_down.style.backgroundImage = 'url('+lib_img_dir+tt_pngorgif+'/carat_bottom.'+tt_pngorgif+')';
		div.appendChild(arrow_down);
		arrow_down.id = 'tt_arrow_down';

		var arrow_up = document.createElement('DIV');
		arrow_up.style.backgroundImage = 'url('+lib_img_dir+tt_pngorgif+'/carat_top.'+tt_pngorgif+')';
		div.appendChild(arrow_up);
		arrow_up.id = 'tt_arrow_up';

		if (tt_pngorgif=='png')
		{
			$('tip_holder').style.padding='11px 0';
		}
		else
		{
			$('tip_holder').style.padding='6px 0';
		}
	}
}

function map_pog() {
	
	var pog = 'png';
	
	if (navigator.appVersion.indexOf("MSIE")!=-1){
	var temp=navigator.appVersion.split("MSIE")
	var version=parseFloat(temp[1])
		if (version<7)
		{
			pog = 'gif';
		}
	}

	var img1 = document.createElement('IMG');
	img1.src = pog_img_dir+pog+'/topleft_off.'+pog;
	img1.style.width='19px';
	img1.style.height='19px';
	img1.className='rollover';
	$('map_pog_1').appendChild(img1);

	var img2 = document.createElement('IMG');
	img2.src = pog_img_dir+pog+'/top_off.'+pog;
	img2.style.width='17px';
	img2.style.height='19px';
	img2.className='rollover';
	$('map_pog_2').appendChild(img2);

	var img3 = document.createElement('IMG');
	img3.src = pog_img_dir+pog+'/topright_off.'+pog;
	img3.style.width='19px';
	img3.style.height='19px';
	img3.className='rollover';
	$('map_pog_3').appendChild(img3);

	var img4 = document.createElement('IMG');
	img4.src = pog_img_dir+pog+'/left_off.'+pog;
	img4.style.width='19px';
	img4.style.height='17px';
	img4.className='rollover';
	$('map_pog_4').appendChild(img4);

	var img5 = document.createElement('IMG');
	img5.src = pog_img_dir+pog+'/center_off.'+pog;
	img5.style.width='17px';
	img5.style.height='17px';
	$('map_pog_5').appendChild(img5);

	var img6 = document.createElement('IMG');
	img6.src = pog_img_dir+pog+'/right_off.'+pog;
	img6.style.width='19px';
	img6.style.height='17px';
	img6.className='rollover';
	$('map_pog_6').appendChild(img6);

	var img7 = document.createElement('IMG');
	img7.src = pog_img_dir+pog+'/bottomleft_off.'+pog;
	img7.style.width='19px';
	img7.style.height='19px';
	img7.className='rollover';
	$('map_pog_7').appendChild(img7);

	var img8 = document.createElement('IMG');
	img8.src = pog_img_dir+pog+'/bottom_off.'+pog;
	img8.style.width='17px';
	img8.style.height='19px';
	img8.className='rollover';
	$('map_pog_8').appendChild(img8);

	var img9 = document.createElement('IMG');
	img9.src = pog_img_dir+pog+'/bottomright_off.'+pog;
	img9.style.width='19px';
	img9.style.height='19px';
	img9.className='rollover';
	$('map_pog_9').appendChild(img9);

	ro_init();
}


function ol_init() {

	var flashers = $$('OBJECT','EMBED'); 
	var selects = $$('SELECT'); 
	var launchers = $ES('.launcher');
	var layers = $ES('.layer');
	var ieisevil = false;

	var body  = document.getElementsByTagName('body').item(0);
	var overlay = document.createElement('DIV');
	var overlay = $(overlay);
	overlay.id='overlay';
	body.appendChild(overlay);

	if (navigator.appVersion.indexOf("MSIE")!=-1){
	var temp=navigator.appVersion.split("MSIE")
	var version=parseFloat(temp[1])
		if (version<=6)
		{
			ieisevil=true;
		}
	}

	function ol_hide_selects(layer) {
		if ((selects.length >= 1) && ieisevil==true)
		{
			selects.each(function(select) {
				var test = select;

				while (test.nodeName != 'BODY')
				test = test.parentNode
				if (test==layer) return;
				
				select.style.visibility='hidden';
			});
		}
	}

	function ol_show_selects() {
		if ((selects.length >= 1) && ieisevil==true)
		{
			selects.each(function(select) {
				select.style.visibility='visible';
			});
		}
	}

	function ol_hide_flash(layer) {
		if ((flashers.length >= 1) && (navigator.appVersion.indexOf('Mac')!=-1))
		{
			flashers.each(function(flasher) {
				var test = flasher;

				while (test.nodeName != 'BODY')
				test = test.parentNode
				if (test==layer) return;
				
				flasher.style.visibility='hidden';
			});
		}
	}

	function ol_show_flash() {
		if ((flashers.length >= 1) && (navigator.appVersion.indexOf('Mac')!=-1))
		{
			flashers.each(function(flasher) {
				flasher.style.visibility='visible';
			});
		}
	}

	
	function ol_launch() {
		var x = window.getScrollWidth();
		var y = window.getScrollHeight();
		
		if (ieisevil==true)
		{
			var x = window.getWidth();
		}

		overlay.style.width=x+'px';
		overlay.style.height=y+'px';
		overlay.style.display='block';
	}

	launchers.each(function(launcher,index) {
		var active_content = layers[index];
		launcher.addEvents({
			'click':  function(event) {
				var event = new Event(event);
				ol_hide_flash(active_content);
				ol_launch();
				var x = window.getWidth();
				var w = active_content.getCoordinates().width.toInt();

				var l = (x/2)-(w/2);
				
				active_content.style.left=l+'px';

				if (ieisevil==true)
				{
					var t = window.getScrollTop();
					var t = t+50;
					active_content.style.top=t+'px';
					ol_hide_selects(active_content);
				}

				var close = $E('.close_primary',active_content);
				close.focus();

				event.preventDefault();
				return false;
			},
			'keydown': function(event){
				var event = new Event(event);
				if (event.key == 'enter')
				{
					ol_hide_flash(active_content);
					ol_launch();
					var x = window.getWidth();
					var w = active_content.getCoordinates().width.toInt();
										   
					var l = (x/2)-(w/2);
					
					active_content.style.left=l+'px';

					if (ieisevil==true)
					{
						var t = window.getScrollTop();
						var t = t+50;
						active_content.style.top=t+'px';
						ol_hide_selects(active_content);
					}

					var close = $E('.close_primary',active_content);
					close.focus();
					
					event.preventDefault();
					return false;	
				}
			}
		});
	});

	layers.each(function(layer) {

		var h3 = $E('h3',layer);

		var text = h3.innerHTML;
		var span1 = document.createElement('SPAN');
		var span2 = document.createElement('SPAN');
		var span3 = document.createElement('SPAN');
		var span4 = document.createElement('SPAN');
		var lnk = document.createElement('A');
		lnk.href=location.href;
		lnk.className='close_primary';
		lnk.innerHTML='Close';
		h3.innerHTML='';
		
		h3.appendChild(span1);
		span1.appendChild(span2);
		span2.appendChild(span3);
		span3.appendChild(span4);
		span3.appendChild(lnk);
		span4.innerHTML=text;

		var bl = document.createElement('DIV');
		bl.className='bl';

		var br = document.createElement('DIV');
		br.className='br';

		var bm = document.createElement('DIV');
		bm.className='bm';
		
		layer.appendChild(bl);
		bl.appendChild(br);
		br.appendChild(bm);
		bm.innerHTML='&nbsp;';

		if (ieisevil==true)
		{
			layer.style.position='absolute';
		}

		var close = $E('.close_primary',layer);
		close.addEvents({
			'click':  function(event) {
				var event = new Event(event);
				layers.each(function(layer) {
					layer.style.left='-1000em';
				});
				overlay.style.display='none';
				ol_show_flash();
				ol_show_selects();
				document.getElementsByTagName('object')[0].style.visibility='visible';

				event.preventDefault();
				return false;	
			}
		});
	});

	overlay.addEvents({
		'click':  function(event) {
			var event = new Event(event);
			layers.each(function(layer) {
				layer.style.left='-1000em';
			});
			overlay.style.display='none';
			ol_show_flash();
			ol_show_selects();
			document.getElementsByTagName('object')[0].style.visibility='visible';

			event.preventDefault();
			return false;	
		},
		'keydown': function(event){
			var event = new Event(event);
			if (event.key == 'enter')
			{
				layers.each(function(layer) {
					layer.style.left='-1000em';
				});
				overlay.style.display='none';
				ol_show_flash();
				ol_show_selects();
			}

			event.preventDefault();
			return false;	
		}
	});

}

function png_init() {
	
		var arVersion = navigator.appVersion.split("MSIE")
		var version = parseFloat(arVersion[1])
	
		if ((version >= 5.5) && (version < 7) && (document.body.filters)) 
	
		{
	 		  var img = document.getElementById('phoneImageId')
	 		  if (img!=null)
		 	  {
				  var imgName = img.src.toUpperCase()
				  if (imgName.substring(imgName.length-3, imgName.length) == "PNG")
				  {
						 var imgID = (img.id) ? "id='" + img.id + "' " : ""
						 var imgClass = (img.className) ? "class='" + img.className + "' " : ""
						 var imgTitle = (img.title) ? "title='" + img.title + "' " : "title='" + img.alt + "' "
						 var imgStyle = "display:inline-block;" + img.style.cssText 
						 if (img.align == "left") imgStyle = "float:left;" + imgStyle
						 if (img.align == "right") imgStyle = "float:right;" + imgStyle
						 if (img.parentElement.href) imgStyle = "cursor:hand;" + imgStyle
						 var strNewHTML = "<span " + imgID + imgClass + imgTitle
						 + " style=\"" + "width:" + img.width + "px; height:" + img.height + "px;" + imgStyle + ";"
						 + "filter:progid:DXImageTransform.Microsoft.AlphaImageLoader"
						 + "(src=\'" + img.src + "\', sizingMethod='scale');\"></span>" 
						 img.outerHTML = strNewHTML
						
				   }
				}
		}
	}

	function jpg_init(Id) {
	
		var arVersion = navigator.appVersion.split("MSIE")
		var version = parseFloat(arVersion[1])
	
		if ((version >= 5.5) && (version < 7) && (document.body.filters)) 
	
		{
			  var img = document.getElementById(Id);
	 		 	
	 		  if (img !=null)
		 	  {
				  var imgName = img.src.toUpperCase()
				 			 
				  if (imgName.substring(imgName.length-3, imgName.length) == "JPG")
				  {
						 var imgID = (img.id) ? "id='" + img.id + "' " : ""
						 var imgClass = (img.className) ? "class='" + img.className + "' " : ""
						 var imgTitle = (img.title) ? "title='" + img.title + "' " : "title='" + img.alt + "' "
						 var imgStyle = "display:inline-block;" + img.style.cssText 
						 if (img.align == "left") imgStyle = "float:left;" + imgStyle
						 if (img.align == "right") imgStyle = "float:right;" + imgStyle
						 if (img.parentElement.href) imgStyle = "cursor:hand;" + imgStyle
						 var strNewHTML = "<span " + imgID + imgClass + imgTitle
						 + " style=\"" + "width:" + img.width + "px; height:" + img.height + "px;" + imgStyle + ";"
						 + "filter:progid:DXImageTransform.Microsoft.AlphaImageLoader"
						 + "(src=\'" + img.src + "\', sizingMethod='scale');\"></span>" 
						 img.outerHTML = strNewHTML
						
				   }
				}
		}
	}

//set popup window options 
function popUpWin(strURL,strType,strHeight,strWidth) {
	var strOptions="";
	if (strType=="flashPopup") strOptions="resizable,height="+strHeight+",width="+strWidth;
	if (strType=="popup") strOptions="scrollbars,resizable,height="+strHeight+",width="+strWidth;
	if (strType=="fullScreen") strOptions="scrollbars,location,directories,status,menubar,toolbar,resizable";
	window.open(strURL, 'newWin', strOptions);
}
