var bool_ezObjectExplainer_insideObject_stack = [];
var bool_ezObjectExplainer_insideObject_cache = [];

function ezObjectExplainer(obj, bool_includeFuncs) {
	var _db = '';
	var m = -1;
	var i = -1;
	var a = [];
	bool_includeFuncs = ((bool_includeFuncs == true) ? bool_includeFuncs : false);
	
	_db = '';
	if (obj) {
       	s_obj = obj.toString;
       	t_obj = typeof obj;
		if ( (s_obj != null) && ((t_obj.toString) == const_function_symbol) && (s_obj.toString().toLowerCase().indexOf('[native code]') == -1) ) {
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
						if (obj[m]) {
							if ((typeof obj[m]) == const_object_symbol) {
								a.push(m + ' = [' + ((obj[m]) ? obj[m].toString() : 'null') + ']');
							} else if ( ( (bool_includeFuncs) && ((typeof obj[m]) == const_function_symbol) ) || ( (!bool_includeFuncs) && ((typeof obj[m]) != const_function_symbol) ) ) {
								a.push(m + ' = [' + obj[m] + ']');
							}
						}
					}
				}
				_db += a.join(', ');
			} else if ( ( (bool_includeFuncs) && ((typeof obj) == const_function_symbol) ) || ( (!bool_includeFuncs) && ((typeof obj) != const_function_symbol) ) ) {
				_db += obj + '\n';
			}
		}
	}
	return _db;
}

