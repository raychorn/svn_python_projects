// facebook-api.js

FB = function(){
	this.id = -1;
	this.appId = -1;
	this.status = '';
	this.cookie = false;
	this.xfbml = false;
};

FB.$ = [];

FB.get$ = function() {
	var instance = FB.$[FB.$.length];
	if (instance == null) {
		instance = FB.$[FB.$.length] = new FB(FB.$.length);
	}
	return instance;
};

FB.remove$ = function(id) {
	var ret_val = false;
	if ( (id > -1) && (id < FB.$.length) ) {
		var instance = FB.$[id];
		if (!!instance) {
			FB.$[id] = destroy(instance);
			ret_val = (FB.$[id] == null);
		}
	}
	return ret_val;
};

FB.remove$s = function() {
	var ret_val = true;
	for (var i = 0; i < FB.$.length; i++) {
		FB.remove$(i);
	}
	return ret_val;
};

FB.prototype = {
	id : -1,
	appId: -1,
	status: '',
	cookie: false,
	xfbml: false,
	toString : function() {
		var s = 'FB(' + this.id + ') :: (';
		if (this.id != null) {
			s += 'appId='+this.appId+', status='+this.status+', cookie='+cookie+', xfbml='+xfbml;
		}
		s += ')';
		return s;
	},
	init : function(obj) {
		this.appId = obj['appId'];
		this.status = obj['status'];
		this.cookie = obj['cookie'];
		this.xfbml = obj['xfbml'];
		return this;
	},
	login : function(callback) {
		var resp = {};
		var sess = {};
		sess['session_key'] = '71aacd59654a705a52ac518f-1167633888';
		sess['uid'] = '1234567890';
		sess['expires'] = 0;
		sess['secret'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
		sess['base_domain'] = 'raychorn.com';
		sess['access_token'] = '122703234439995|71aacd59654a705a52ac518f-1167633888|dawx-NVvnhrjykTCJI9CwLBnMaM.';
		sess['sig'] = '0cdf92258cbc6f79aec3a57554057032';		
		resp['session'] = sess;
		resp['perms'] = 'read_stream,publish_stream,offline_access';
		if ( (callback) && (typeof(callback) == const_function_symbol) ) {
			try {callback(resp);} catch (e) {}
		}
		return this;
	},
	logout : function(callback) {
		var resp = {};
		if ( (callback) && (typeof(callback) == const_function_symbol) ) {
			try {callback(resp);} catch (e) {}
		}
	},
	destructor : function() {
		return (this.id = FB.$[this.id] = this.appId = this.status = this.cookie = this.xfbml = null);
	}
};
