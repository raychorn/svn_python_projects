/*
 SmithMicroHeatMapDataModel.js
*/

SmithMicroHeatMapDataModel = function(id){
	this.id = id;				// the id is the position within the global GeonosisObj.$ array
};

SmithMicroHeatMapDataModel.$ = [];

SmithMicroHeatMapDataModel.get$ = function() {
	// the object.id is the position within the array that holds onto the objects...
	var instance = SmithMicroHeatMapDataModel.$[SmithMicroHeatMapDataModel.$.length];
	if(instance == null) {
		instance = SmithMicroHeatMapDataModel.$[SmithMicroHeatMapDataModel.$.length] = new SmithMicroHeatMapDataModel(SmithMicroHeatMapDataModel.$.length);
	}
	return instance;
};

SmithMicroHeatMapDataModel.i = function() {
	return SmithMicroHeatMapDataModel.get$(); // this is an alias that aids the transmission of code from the server to the client...
};

SmithMicroHeatMapDataModel.remove$ = function(id) {
	var ret_val = false;
	if ( (id > -1) && (id < SmithMicroHeatMapDataModel.$.length) ) {
		var instance = SmithMicroHeatMapDataModel.$[id];
		if (!!instance) {
			SmithMicroHeatMapDataModel.$[id] = object_destructor(instance);
			ret_val = (SmithMicroHeatMapDataModel.$[id] == null);
		}
	}
	return ret_val;
};

SmithMicroHeatMapDataModel.remove$s = function() {
	var ret_val = true;
	for (var i = 0; i < SmithMicroHeatMapDataModel.$.length; i++) {
		SmithMicroHeatMapDataModel.remove$(i);
	}
	SmithMicroHeatMapDataModel.$ = [];
	return ret_val;
};

SmithMicroHeatMapDataModel.prototype = {
	id : -1,
	toString : function() {
		function toStr() {
			var s = '[';
			s += ']';
			return s;
		}
		var s = 'id = [' + this.id + ']\n' + toStr();
		return s;
	},
	init : function(data) {
		return this;
	},
	destructor : function() {
		return (this.id = SmithMicroHeatMapDataModel.$[this.id] = null);
	},
	dummy : function() {
		return false;
	}
};
