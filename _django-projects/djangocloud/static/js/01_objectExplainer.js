var bool_ezObjectExplainer_insideObject_stack = [];
var bool_ezObjectExplainer_insideObject_cache = [];

function ezObjectExplainer(obj, bool_includeFuncs, _cnt) {
	var _db = '';
	var m = -1;
	var i = -1;
	var a = [];
	var cnt = ((_cnt == null) ? '1' : _cnt.toString() + '.0');
	bool_includeFuncs = ((bool_includeFuncs == true) ? bool_includeFuncs : false);
	
	function isCntComplex(c) {
		return (c.toString().indexOf('.') > -1);
	}
	
	_db = '';
	if ( (obj.toString != null) && ((typeof obj.toString) == const_function_symbol) && (obj.toString.toString().toLowerCase().indexOf('[native code]') == -1) ) {
		_db += obj.toString();
	} else {
		if ( (obj != null) && ((typeof obj) == const_object_symbol) ) {
			if (obj.length != null) {
			    for (i = 0; i < obj.length; i++) {
					if ( ( (bool_includeFuncs) && ((typeof obj[i]) == const_function_symbol) ) || ( (!bool_includeFuncs) && ((typeof obj[i]) != const_function_symbol) ) ) {
						a.push('[' + obj[i] + ']');
					}
			    }
			} else {
				for (m in obj) {
					if ((typeof obj[m]) == const_object_symbol) {
						a.push(m + ' = [' + ezObjectExplainer(obj[m], bool_includeFuncs, cnt) + ']');
					} else if ( ( (bool_includeFuncs) && ((typeof obj[m]) == const_function_symbol) ) || ( (!bool_includeFuncs) && ((typeof obj[m]) != const_function_symbol) ) ) {
						a.push(m + ' = [' + obj[m] + ']');
					}
				}
			}
			_db += a.join(((isCntComplex(cnt)) ? ',' : '\n'));
		} else if ( ( (bool_includeFuncs) && ((typeof obj) == const_function_symbol) ) || ( (!bool_includeFuncs) && ((typeof obj) != const_function_symbol) ) ) {
			_db += obj + '\n';
		}
	}
	return _db;
}

