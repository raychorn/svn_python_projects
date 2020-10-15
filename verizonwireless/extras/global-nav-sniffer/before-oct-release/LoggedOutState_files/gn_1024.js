window.addEvent('load',function(){
	gn_init();
});

var newwindow = '';
var lastOpened = '';


function navInit() {
	gn_init();
}

// prepares the regular version of the global navigation with full functionality
function gn_init() {
	
	var gonogo=true;
	var use_ishim=false;
	var active_ishim=null;
	
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
		if (version<=5.9)
		{
			gonogo=false;
		}
		if (version>=6 && version<7)
		{
			use_ishim=true;
			$('gn').insertAdjacentHTML('beforeEnd', '<iframe src="'+gn_iframe+'" id="gn_ishim" frameborder="0" scrolling="0" style="position:absolute;top:0;left:0;width:0;height:0;display:none;z-index:498;filter:progid:DXImageTransform.Microsoft.Alpha(style=0,opacity=0);"></iframe>');
			var gn = $('gn');
			var lis = $ES('li',gn);
			lis.each(function(li) {
				var lnk = li.getFirst();
				lnk.style.height='1%';
			});
		}
	}
	
	function gn_ishim(show,d_2)
	{
		var ishim = $('gn_ishim');
		if(show==true && use_ishim==true)
		{	
			ishim.style.display = 'block';
			var d_2_pos = d_2.getCoordinates();
			ishim.style.width = d_2_pos.width;
			ishim.style.height = d_2_pos.height;
			ishim.style.top = d_2_pos.top;
			ishim.style.left = d_2_pos.left;
		}
		
		if (active_ishim==d_2 && show==false && use_ishim==true)
		{
			ishim.style.display = 'none';
		}
		active_ishim=d_2;
	}
	
	var userAgent = navigator.userAgent.toLowerCase();
	if (userAgent.indexOf('mac') != -1 && userAgent.indexOf('firefox')!=-1) {
		gonogo=false;
	}

	if (gonogo==true)
	{
		if (typeof gnCategory!='undefined')
		{
			var t = 0;
			var g = gnCategory*1;
			var headers = $$('#gn h2');
			headers.each(function(header) {
				if (g==t)
				{
					var a = $E('a',header);
					a.addClass('gn_selected');
				}
				t++;
			});
		}

		var headers = $$('#gn h2');
		headers.each(function(header) {
			
			var a_1 = $E('a',header);
			var d_2 = header.getNext();
			var u_2 = $E('ul',d_2);
			var l_2s = u_2.getChildren();
			var u_3s = $ES('ul',u_2);
			
			l_2s.each(function(l_2) {
				if (l_2.getNext()==null)
				{
					l_2.style.paddingBottom='10px';
				}
			});

			u_3s.each(function(u_3) {
				var l_3s=u_3.getChildren();
				l_3s.each(function(l_3) {
					if (l_3.getNext()==null)
					{
						l_3.style.marginBottom='10px';
					}
				});
			});

			if (header.className=='gn_right')
			{
				var gn_right=true;
				u_2.setStyle('float', 'right');
			}
			else
			{
				var gn_right=false;
			}

			d_2.setStyle('opacity',0);

			function d_2_show(a_1,d_2) {
				var a_1_pos = a_1.getCoordinates();
				var h = a_1_pos.height;
				var w = a_1_pos.width;
				var l = a_1_pos.left;
				var t = a_1_pos.top;

				var gn = $('gn');
				var d_2_cs = $ES('div.gn_dd',gn);
				d_2_cs.each(function(d_2_c) {
					if (d_2_c.style.zIndex='500')
					{
						var h_c = d_2_c.getPrevious();
						var a_1_c = $E('a',h_c);
						d_2_hide(a_1_c,d_2_c);
					}
				});

				d_2.setStyle('top', (t+h));
				if (gn_right==true)
				{
					d_2.setStyle('left', l+w-220);
				}
				else
				{
					d_2.setStyle('left', l);
				}
				d_2.setStyle('z-index', '500');
				a_1.addClass('gn_active');
				gn_ishim(true,d_2);
			}

			function d_2_hide(a_1,d_2) {
				d_2.setStyle('margin-left', '0');
				d_2.setStyle('width', '220px');
				d_2.setStyle('height', 'auto');
				d_2.setStyle('left', '-1000em');
				d_2.setStyle('z-index', '499');
				a_1.removeClass('gn_active');
				gn_ishim(false,d_2);
			}

			a_1.addEvents({	
				'focus': function() {
					d_2_show(a_1,d_2);
					d_2.setStyle('opacity',1);
				},
				
				'blur': function() {
					d_2_hide(a_1,d_2);
				},

				'keydown': function(event) {
					event = new Event(event);
					if (event.key=='down')
					{
						u_2.getFirst().getFirst().focus();
					}
					else if (event.key=='left' && header.getPrevious())
					{
						$E('a',header.getPrevious().getPrevious()).focus();
					}
					else if (event.key=='right' && header.getNext().getNext())
					{
						$E('a',header.getNext().getNext()).focus();
					}
				}
			});

			var reveal = new Fx.Styles(d_2, {
				duration: 300,
				transition: Fx.Transitions.Quad.easeIn,
				fps: 30
			});

			reveal.addEvent('onStart', function(){
				d_2_show(a_1,d_2);
			});
			
			var repeal = new Fx.Styles(d_2, {
				duration: 300,
				transition: Fx.Transitions.Quad.easeOut,
				fps: 30
			});
			
			repeal.addEvent('onStart', function(){
				d_2.setStyle('z-index', '499');
				a_1.removeClass('gn_active');
				gn_fo(a_1);
			});

			repeal.addEvent('onComplete', function(){
				d_2_hide(a_1,d_2);
			});

			a_1.addEvent('mouseenter', function(event){
				var rt = event.relatedTarget;
				while (rt && rt != d_2 && rt.nodeName != 'BODY')
				rt = rt.parentNode
				if (rt == d_2) return;
				
				repeal.stop();
				d_2.setStyle('opacity',0);
				reveal.start({
					'opacity': [0,1]
				});
			});

			a_1.addEvent('mouseleave', function(event){
				var rt = event.relatedTarget;
				while (rt && rt != d_2 && rt.nodeName != 'BODY')
				rt = rt.parentNode
				if (rt == d_2) return;
				
				reveal.stop();
				repeal.start({
					'opacity': [1,0]
				});
			});

			d_2.addEvent('mouseleave', function(event){
				var rt = event.relatedTarget;
				while (rt && rt != a_1 && rt.nodeName != 'BODY')
				rt = rt.parentNode
				if (rt == a_1) return;
				
				reveal.stop();
				repeal.start({
					'opacity': [1,0]
				});
			});

			l_2s.each(function(l_2) {
				
				var a_2 = l_2.getFirst();

				if (gn_right==true)
				{
					if (a_2.getNext()!=null)
					{	
						a_2.addClass('left_arrow');
					}
				}
				else
				{
					if (a_2.getNext()!=null)
					{
						a_2.addClass('right_arrow');
					}
					a_2.style.paddingLeft='10px';
				}

				var rollover = new Fx.Styles(a_2, {
					duration: 300,
					transition: Fx.Transitions.Quad.easeOut,
					fps: 30,
					wait: false
				});

				var rolloff = new Fx.Styles(a_2, {
					duration: 300,
					transition: Fx.Transitions.linear,
					fps: 30,
					wait: false
				});

				var gn_foto;

				a_2.addEvents({
					'mouseenter':  function() {
					gn_foto = gn_fo.delay(300,gn_fo,a_2);
						rollover.stop();
						rollover.start({
							'background-color': '#990000'
						});
					},

					'mouseleave': function(event) {
					$clear(gn_foto);
						if (!(a_2.hasClass('gn_out')))
						{
							rollover.stop();
							rolloff.start({
								'background-color': '#000'
							});
						}
					},

					'focus': function() {
						d_2_show(a_1,d_2);
						a_2.setStyle('background-color', '#990000');
						d_2.setStyle('opacity',1);
					},

					'blur': function() {
						d_2_hide(a_1,d_2);
						a_2.setStyle('background-color', '#000');
					},

					'keydown': function(event) {
						event = new Event(event);
						if (event.key=='up' && l_2.getPrevious())
						{
							l_2.getPrevious().getFirst().focus();
						}
						else if (event.key=='up' && !(l_2.getPrevious()))
						{
							a_1.focus();
						}
						else if (event.key=='down' && l_2.getNext())
						{
							l_2.getNext().getFirst().focus();
						}
						else if (event.key=='left' && header.getPrevious())
						{
							$E('a',header.getPrevious().getPrevious()).focus();
						}
						else if (event.key=='right' && header.getNext().getNext())
						{
							$E('a',header.getNext().getNext()).focus();
						}
					}
				});
			});

			function gn_fo(a_2) { 
				
				var u_2_h = u_2.getCoordinates().height;

				u_3s.each(function(u_3) {
					
					if (u_3.style.left=='auto' && u_3!=a_2.getNext())
					{
						var flyin = new Fx.Styles(u_3, {
							duration: 300,
							transition: Fx.Transitions.linear,
							fps: 30
						});

						flyin.addEvent('onStart', function(){
							u_3.getPrevious().removeClass('gn_out');
						});

						flyin.addEvent('onComplete', function(){
							u_3.setStyle('left', '-1000em');
							u_3.setStyle('height', 'auto');
							if (!(a_2.getNext()))
							{
								d_2.setStyle('margin-left', '0');
								d_2.setStyle('width', '220px');
								d_2.setStyle('height', 'auto');
								gn_ishim(true,d_2);
							}
						});

						var u_3_h = u_3.getCoordinates().height;

						if (gn_right==true)
						{
							flyin.start({
								'width': [220,0],
								'height': [u_3_h,0],
								'opacity': [1,0],
								'margin-left': [-220,0]
							})
						}
						else
						{
							flyin.start({
								'width': [220,0],
								'height': [u_3_h,0],
								'opacity': [1,0]
							})
						}
						
						var rollover = new Fx.Styles(u_3.getPrevious(), {
							duration: 300,
							transition: Fx.Transitions.linear,
							fps: 30,
							wait: false
						});

						rollover.start({
							'background-color': '#000'
						});
					}

					if (u_3==a_2.getNext() && u_3.style.left!='auto')
					{
						var u_3_h = u_3.getCoordinates().height;

						var flyout = new Fx.Styles(u_3, {
							duration: 300,
							transition: Fx.Transitions.linear,
							fps: 30
						});

						flyout.addEvent('onStart', function(){
							a_2.addClass('gn_out');
							u_3.setStyle('left', 'auto');
							d_2.setStyle('width', '440px');
							if (gn_right==true)
							{
								d_2.setStyle('margin-left', '-220px');
							}
							if (u_3_h>u_2_h)
							{
								d_2.setStyle('height', u_3_h+30);
							}
							else 
							{
								d_2.setStyle('height', 'auto');
								var d_2_h = d_2.getCoordinates().height;
								d_2.setStyle('height', d_2_h+30);
							}
							gn_ishim(true,d_2);
						});

						if (gn_right==true)
						{
							flyout.start({
								'width': [0,220],
								'height': [0,u_3_h],
								'opacity': [0,1],
								'margin-left': [0,-220]
							})
						}
						else
						{
							flyout.start({
								'width': [0,220],
								'height': [0,u_3_h],
								'opacity': [0,1]
							})
						}
					}
				})
			}
		});
	}
	else
	{
		if (typeof gnCategory!='undefined')
		{
			var t = 0;
			var g = gnCategory*1;
			var headers = $$('#gn h2');
			headers.each(function(header) {
				if (g==t)
				{
					var a = $E('a',header);
					a.addClass('gn_selected');
				}
				t++;
			});
		}

		var headers = $$('#gn h2');
		headers.each(function(header) {
			
			var a_1 = $E('a',header);
			var d_2 = header.getNext();
			var u_2 = $E('ul',d_2);
			var l_2s = u_2.getChildren();
			var u_3s = $ES('ul',u_2);
			
			l_2s.each(function(l_2) {
				if (l_2.getNext()==null)
				{
					l_2.style.paddingBottom='10px';
				}
			});

			u_3s.each(function(u_3) {
				var l_3s=u_3.getChildren();
				l_3s.each(function(l_3) {
					if (l_3.getNext()==null)
					{
						l_3.style.marginBottom='10px';
					}
				});
			});

			if (header.className=='gn_right')
			{
				var gn_right=true;
				u_2.setStyle('float', 'right');
			}
			else
			{
				var gn_right=false;
			}

			function d_2_show(a_1,d_2) {
				var a_1_pos = a_1.getCoordinates();
				var h = a_1_pos.height;
				var w = a_1_pos.width;
				var l = a_1_pos.left;
				var t = a_1_pos.top;

				var gn = $('gn');
				var d_2_cs = $ES('div.gn_dd',gn);
				d_2_cs.each(function(d_2_c) {
					if (d_2_c.style.zIndex='500')
					{
						var h_c = d_2_c.getPrevious();
						var a_1_c = $E('a',h_c);
						d_2_hide(a_1_c,d_2_c);
					}
				});

				d_2.setStyle('top', (t+h));
				if (gn_right==true)
				{
					d_2.setStyle('left', l+w-220);
				}
				else
				{
					d_2.setStyle('left', l);
				}
				d_2.setStyle('z-index', '500');
				a_1.addClass('gn_active');
				gn_ishim(true,d_2);
			}

			function d_2_hide(a_1,d_2) {
				d_2.setStyle('margin-left', '0');
				d_2.setStyle('width', '220px');
				d_2.setStyle('height', 'auto');
				d_2.setStyle('left', '-1000em');
				d_2.setStyle('z-index', '499');
				a_1.removeClass('gn_active');
				gn_ishim(false,d_2);
			}

			a_1.addEvents({	
				'focus': function() {
					d_2_show(a_1,d_2);
				},
				
				'blur': function() {
					d_2_hide(a_1,d_2);
				},

				'keydown': function(event) {
					event = new Event(event);
					if (event.key=='down')
					{
						u_2.getFirst().getFirst().focus();
					}
					else if (event.key=='left' && header.getPrevious())
					{
						$E('a',header.getPrevious().getPrevious()).focus();
					}
					else if (event.key=='right' && header.getNext().getNext())
					{
						$E('a',header.getNext().getNext()).focus();
					}
				}
			});

			a_1.addEvent('mouseenter', function(event){
				var rt = event.relatedTarget;
				while (rt && rt != d_2 && rt.nodeName != 'BODY')
				rt = rt.parentNode
				if (rt == d_2) return;
				d_2_show(a_1,d_2);
			});

			a_1.addEvent('mouseleave', function(event){
				var rt = event.relatedTarget;
				while (rt && rt != d_2 && rt.nodeName != 'BODY')
				rt = rt.parentNode
				if (rt == d_2) return;
				
				a_1.removeClass('gn_active');
				d_2_hide(a_1,d_2);
				gn_fo(a_1);
			});

			d_2.addEvent('mouseleave', function(event){
				var rt = event.relatedTarget;
				while (rt && rt != a_1 && rt.nodeName != 'BODY')
				rt = rt.parentNode
				if (rt == a_1) return;
				
				a_1.removeClass('gn_active');
				d_2_hide(a_1,d_2);
				gn_fo(a_1);
			});

			l_2s.each(function(l_2) {
				
				var a_2 = l_2.getFirst();

				if (gn_right==true)
				{
					if (a_2.getNext()!=null)
					{	
						a_2.addClass('left_arrow');
					}
				}
				else
				{
					if (a_2.getNext()!=null)
					{
						a_2.addClass('right_arrow');
					}
					a_2.style.paddingLeft='10px';
				}

				a_2.addEvents({
					'mouseenter':  function() {
						gn_fo(a_2);
						a_2.setStyle('background-color', '#990000');
					},

					'mouseleave': function() {
						gn_fo(a_2);
						a_2.setStyle('background-color', '#000');
					},

					'focus': function() {
						d_2_show(a_1,d_2);
						a_2.setStyle('background-color', '#990000');
					},

					'blur': function() {
						d_2_hide(a_1,d_2);
						a_2.setStyle('background-color', '#000');
					},

					'keydown': function(event) {
						event = new Event(event);
						if (event.key=='up' && l_2.getPrevious())
						{
							l_2.getPrevious().getFirst().focus();
						}
						else if (event.key=='up' && !(l_2.getPrevious()))
						{
							a_1.focus();
						}
						else if (event.key=='down' && l_2.getNext())
						{
							l_2.getNext().getFirst().focus();
						}
						else if (event.key=='left' && header.getPrevious())
						{
							$E('a',header.getPrevious().getPrevious()).focus();
						}
						else if (event.key=='right' && header.getNext().getNext())
						{
							$E('a',header.getNext().getNext()).focus();
						}
					}
				});
			});

			function gn_fo(a_2) { 
				var u_2_h = u_2.getCoordinates().height;

				u_3s.each(function(u_3) {
					
					if (u_3.style.left=='auto' && u_3!=a_2.getNext())
					{
						var u_3_h = u_3.getCoordinates().height;

						if (gn_right==true)
						{
							u_3.setStyle('margin-left', '-220px');
						}
						
						u_3.getPrevious().removeClass('gn_out');
						u_3.setStyle('left', '-1000em');
						u_3.setStyle('height', 'auto');
						if (!(a_2.getNext()))
						{
							d_2.setStyle('margin-left', '0');
							d_2.setStyle('width', '220px');
							d_2.setStyle('height', 'auto');
							gn_ishim(true,d_2);
						}
					}

					if (u_3==a_2.getNext() && u_3.style.left!='auto')
					{
						var u_3_h = u_3.getCoordinates().height;
						
						if (gn_right==true)
						{
							u_3.setStyle('margin-left', '-220px');
						}

						a_2.addClass('gn_out');
						u_3.setStyle('left', 'auto');
						u_3.setStyle('height', 'auto');
						u_3.setStyle('width', '220px');
						d_2.setStyle('width', '440px');
						if (gn_right==true)
						{
							d_2.setStyle('margin-left', '-220px');
						}
						if (u_3_h>u_2_h)
						{
							d_2.setStyle('height', u_3_h+30);
						}
						else 
						{
							d_2.setStyle('height', 'auto');
							var d_2_h = d_2.getCoordinates().height;
							d_2.setStyle('height', d_2_h+30);
						}
						gn_ishim(true,d_2);
					}
				})
			}
		});
	}
}