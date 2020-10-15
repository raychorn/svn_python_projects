// AnchorPosition.js

ezAnchorPosition = function(id, anchorname){
	this.id = id;
	if (!!anchorname) this.getAnchorPosition(anchorname);
};

ezAnchorPosition.$ = [];

ezAnchorPosition.get$ = function(anchorname) {
	var instance = ezAnchorPosition.$[ezAnchorPosition.$.length];
	if (instance == null) {
		instance = ezAnchorPosition.$[ezAnchorPosition.$.length] = new ezAnchorPosition(ezAnchorPosition.$.length, anchorname);
	}
	return instance;
};

ezAnchorPosition.remove$ = function(id) {
	var ret_val = false;
	if ( (id > -1) && (id < ezAnchorPosition.$.length) ) {
		var instance = ezAnchorPosition.$[id];
		if (!!instance) {
			ezAnchorPosition.$[id] = ezObjectDestructor(instance);
			ret_val = (ezAnchorPosition.$[id] == null);
		}
	}
	return ret_val;
};

ezAnchorPosition.remove$s = function() {
	var ret_val = true;
	for (var i = 0; i < ezAnchorPosition.$.length; i++) {
		ezAnchorPosition.remove$(i);
	}
	return ret_val;
};

ezAnchorPosition.prototype = {
	id : -1,
	x : -1,
	y : -1,
	anchorname : '',
	use_gebi : false,
	use_css : false,
	use_layers : false,
	toString : function() {
		var s = 'ezAnchorPosition(' + this.id + ') :: \n';
		s += 'x/y = [' + this.x + ',' + this.y + ']' + '\n';
		s += 'anchorname = [' + this.anchorname + ']' + '\n';
		s += 'use_gebi = [' + this.use_gebi + ']' + ', use_css = [' + this.use_css + ']' + ', use_layers = [' + this.use_layers + ']' + '\n\n';
		return s;
	},
	getPageOffsetLeft : function(el) {
		var ol = 0;
		try {
			ol = el.offsetLeft;
			while ((el = el.offsetParent) != null) {
				ol += el.offsetLeft; 
			}
		} catch(e) {
		} finally {
		}
		return ol;
	},
	getPageOffsetTop : function(el) {
		var ot = 0;
		try {
			ot = el.offsetTop;
			while ((el = el.offsetParent) != null) {
				ot += el.offsetTop; 
			}
		} catch(e) {
		} finally {
		}
		return ot;
	},
	getWindowOffsetLeft : function(el) {
		var x = 0;
		var s = 0;
		try {
			x = this.getPageOffsetLeft(el);
			s = document.body.scrollLeft;
		} catch(e) {
		} finally {
		}
		return x - s;
	},
	getWindowOffsetTop : function(el) {
		var x = 0;
		var s = 0;
		try {
			x = this.getPageOffsetTop(el);
			s = document.body.scrollTop;
		} catch(e) {
		} finally {
		}
		return x - s;
	},
	getAnchorPosition : function(anchorname) {
		this.anchorname = anchorname;
		this.x = 0, this.y = 0;
		this.use_gebi = ((!!document.getElementById) ? true : false);
		this.use_css = ((!this.use_gebi) ? ((!!document.all) ? true : false) : false);
		this.use_layers = (((!this.use_gebi) && (!!this.use_css)) ? ((!!document.layers) ? true : false) : false);

		if (this.use_gebi && document.all) {
			this.x = this.getPageOffsetLeft(document.all[anchorname]);
			this.y = this.getPageOffsetTop(document.all[anchorname]);
		} else if (this.use_gebi) {
			var o = document.getElementById(anchorname);
			this.x = this.getPageOffsetLeft(o);
			this.y = this.getPageOffsetTop(o);
		} else if (this.use_css) {
			this.x = this.getPageOffsetLeft(document.all[anchorname]);
			this.y = this.getPageOffsetTop(document.all[anchorname]);
		} else if (this.use_layers) {
			var found = 0;
			for (var i = 0; i < document.anchors.length; i++) {
				if (document.anchors[i].name == anchorname) { found = 1; break; }
			}
			if (found == 0) {
				this.x=0; this.y=0;
			}
			x = document.anchors[i].x;
			y = document.anchors[i].y;
		} else {
			this.x = 0; this.y = 0;
		}
	},
	getAnchorWindowPosition : function(anchorname) {
		this.getAnchorPosition(anchorname);
		var x=0;
		var y=0;
		if (!!document.getElementById) {
			if (isNaN(window.screenX)) {
				x = this.x - document.body.scrollLeft + window.screenLeft;
				y = this.y - document.body.scrollTop + window.screenTop;
			} else {
				x = this.x + window.screenX + (window.outerWidth - window.innerWidth) - window.pageXOffset;
				y = this.y + window.screenY + (window.outerHeight - 24 - window.innerHeight) - window.pageYOffset;
			}
		} else if (!!document.all) {
			x = this.x - document.body.scrollLeft + window.screenLeft;
			y = this.y - document.body.scrollTop + window.screenTop;
		} else if (!!document.layers) {
			x = this.x + window.screenX + (window.outerWidth - window.innerWidth) - window.pageXOffset;
			y = this.y + window.screenY + (window.outerHeight - 24 - window.innerHeight) - window.pageYOffset;
		}
		this.x = x;
		this.y = y;
	},
	destructor : function() {
		return (this.id = ezAnchorPosition.$[this.id] = this.x = this.y = null);
	}
};

