function $(id, fromObj) {
	var obj = null;
	
	function usingGetElementById(id, fromObj) {
		return ((typeof fromObj.getElementById == const_function_symbol) ? fromObj.getElementById(id) : null);
	};
	
	function usingAll(id, fromObj) {
		return ((fromObj.all) ? fromObj.all[id] : null);
	};
	
	function usingLayers(id, fromObj) {
		return ((fromObj.layers) ? fromObj.layers[id] : null);
	};
	
	if (typeof id == const_string_symbol) {
		try { obj = usingGetElementById(id, fromObj); } catch(e) { obj = null; };
		if (obj == null) {
			try { obj = usingAll(id, fromObj); } catch(e) { obj = null; };
			if (obj == null) {
				try { obj = usingLayers(id, fromObj); } catch(e) { obj = null; };
			}
		}
	}
	return obj;
}
