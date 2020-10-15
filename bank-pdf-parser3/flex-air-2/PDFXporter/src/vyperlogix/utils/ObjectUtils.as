package vyperlogix.utils {
	import mx.collections.ArrayCollection;
	import mx.collections.Sort;
	import mx.collections.SortField;
	import mx.utils.ObjectProxy;
	
	
	public class ObjectUtils {

		public static function isEmpty(anObject:Object):Boolean {
			return ObjectUtils.keys(anObject).length == 0;
		}
		
		public static function makeEmpty(anObject:Object):void {
			var keys:Array = ObjectUtils.keys(anObject);
			for (var i:String in keys) {
				delete anObject[keys[i]];
			}
		}
		
		public static function containsUnNecessaryData(obj:*):Boolean {
			for (var i:String in obj) {
				if ( (obj[i] == null) || ( (obj[i] is String) && (obj[i].length == 0) ) ) {
					return true;
				}
			}
			return false;
		}

		public static function cloneIfNecessary(obj:*,always:Boolean=false):Object {
			var newObject:Object = {};
			if (!always) {
				if (ObjectUtils.containsUnNecessaryData(obj) == false) {
					return obj;
				}
			}
			for (var i:String in obj) {
				if ( (obj[i] != null) && (obj[i].toString().length > 0) ) {
					newObject[i] = obj[i];
				}
			}
			return newObject;
		}
		
		public static function cloneWithoutThese(source:Object,these:*):Object {
			var i:int;
			var j:String;
			var k:String;
			var aKey:String;
        	var keys:Array = ObjectUtils.keys(source);
    		var anObj:Object = {};
        	if (these is String) {
        		these = [new String(these)];
        	}
        	for (j in these) {
        		aKey = these[j];
	        	i = keys.indexOf(aKey);
	        	if (i > -1) {
	        		keys.splice(i,1);
	        	}
        	}
    		for (k in keys) {
    			anObj[keys[k]] = source[keys[k]];
    		}
        	return anObj;
		}

		public static function cloneWithThese(source:Object,these:*):Object {
			var i:int;
			var j:String;
			var k:String;
			var aKey:String;
    		var anObj:Object = {};
        	if (these is String) {
        		these = [new String(these)];
        	}
        	var keys:Array = these;
    		for (k in keys) {
    			anObj[keys[k]] = source[keys[k]];
    		}
        	return anObj;
		}
		
		public static function replicateDataFromInto(source:Object,target:Object):void {
        	var keys:Array = ObjectUtils.keys(source);
    		for (var k:String in keys) {
    			target[keys[k]] = source[keys[k]];
    		}
		}

		public static function asArrayOfObjects(anObject:Object):Array {
			var a:Array = [];
			var obj:Object = {};
			for (var i:String in anObject) {
				obj = {'label':anObject[i],'data':i};
				a.push(obj);
			}
			return a;
		}
		
		public static function asArrayOfObjectsCollection(anObject:Object):ArrayCollection {
			var ar:Array = ObjectUtils.asArrayOfObjects(anObject);
			var ac:ArrayCollection = new ArrayCollection(ar);
			return ac;
		}
		
		public static function asSortedArrayOfObjectsCollection(anObject:Object):ArrayCollection {
			var ac:ArrayCollection = ObjectUtils.asArrayOfObjectsCollection(anObject);
			var sort:Sort = new Sort();
			sort.fields = [new SortField("label",true)];
			ac.sort = sort;
			ac.refresh();
			return ac;
		}
		
		public static function asArray(anObject:Object):Array {
			var a:Array = [];
			for (var i:String in anObject) {
				a.push(anObject[i]);
			}
			return a;
		}
		
		public static function asArrayCollection(anObject:Object):ArrayCollection {
			var ar:Array = ObjectUtils.asArray(anObject);
			var ac:ArrayCollection = new ArrayCollection(ar);
			return ac;
		}
		
		public static function asSortedArrayCollection(anObject:Object):ArrayCollection {
			var ac:ArrayCollection = ObjectUtils.asArrayCollection(anObject);
			var sort:Sort = new Sort();
			ac.sort = sort;
			ac.refresh();
			return ac;
		}
		
		public static function copy(source:ArrayCollection):ArrayCollection {
			var aCopy:ArrayCollection = new ArrayCollection();
			var i:int = 0;
			for (; i < source.length-1; i++) {
				aCopy.addItem(source.getItemAt(i));
			}
			return aCopy;
		}
		
		public static function keys(data:Object,criteria:Function=null):Array {
			var a:Array = [];
			try {
				for (var i:String in data) {
					if ( (criteria == null) || ( (criteria is Function) && (criteria(data[i])) ) ) {
						a.push(i);
					}
				}
			} catch (e:Error) {}
			return a;
		}
		
		public static function keys_filtered(data:Object,filter:Function=null):Array {
			var a:Array = [];
			try {
				for (var i:String in data) {
					a.push((filter is Function) ? filter(i) : i);
				}
			} catch (e:Error) {}
			return a;
		}
		
		public static function criteria_unpack_isSomeKindOfObject(data:*):Boolean {
			var bool:Boolean = (data is Array) || (data is ArrayCollection);
			return bool != true;
		}

		public static function criteria_isSomeKindOfObject(data:*):Boolean {
			var bool:Boolean = (data is Array) || (data is ArrayCollection);
			return bool == true;
		}
		
		public static function criteria_isOfTypeObject(data:*):Boolean {
			var bool:Boolean = typeof(data) == 'object';
			return bool;
		}

		public static function criteria_isOfTypeObjectOrSomeKindOfObject(data:*):Boolean {
			var bool:Boolean = criteria_isOfTypeObject(data) || criteria_isSomeKindOfObject(data);
			return bool;
		}

		public static function criteria_isSomeKindOfRootObject(data:*):Boolean {
			var bool:Boolean = (data is Array) || (data is ArrayCollection);
			var keys:Array = ObjectUtils.keys(data);
			return ( (bool == true) || (keys.indexOf('metafield') == -1) || (keys.indexOf('datafield') == -1) );
		}

		public static function criteria_unpack_isSomeKindOfObjectProxy(data:*):Boolean {
			var bool:Boolean = (data is ObjectProxy);
			return bool != true;
		}

		public static function unpack(data:*,criteria:Function,criteria_for_keys:Function=null):* {
			var anObj:* = data;
			var i_descender:int;
			function can_descend_lower(obj:Object,keys:Array):int {
				var resp:int = -1; // if cannot descend lower than return -1 otherwise return the key's index that descends lower...
				var aKey:String;
				for (var i:int = 0; i < keys.length; i++) {
					try {
						aKey = keys[i];
						if (criteria_isSomeKindOfObject(obj[aKey])) {
							resp = i;
							return resp;
						}
					} catch (e:Error) {}
				}
				return resp;
			}
			do {
				anObj = (anObj is ObjectProxy) ? anObj.valueOf() : anObj;
				var keys:Array = ObjectUtils.keys(anObj,criteria_for_keys);
				i_descender = can_descend_lower(anObj,keys);
				if ( (criteria == null) || (anObj == null) || ( (keys.indexOf('dataField') > -1) && (keys.indexOf('metaField') > -1) ) || (i_descender == -1) ) {
					break;
				}
				anObj = anObj[keys[i_descender]];
			} while (criteria(anObj));
			return ((anObj is ObjectProxy) ? anObj.valueOf() : ((anObj is ArrayCollection) ? anObj : (anObj is Array) ? new ArrayCollection(anObj) : anObj));
		}

		public static function collect(data:*,criteria:Function=null):ArrayCollection {
			var datum:ArrayCollection = new ArrayCollection()
			var anObj:* = data;
			do {
				anObj = (anObj is ObjectProxy) ? anObj.valueOf() : anObj;
				var keys:Array = ObjectUtils.keys(anObj);
				anObj = (keys.length > 0) ? anObj[keys[0]] : null;
				if ( (criteria == null) || (anObj == null) ) {
					break;
				}
				datum.addItem((anObj is ObjectProxy) ? anObj.valueOf() : anObj);
			} while (criteria(anObj));
			return datum;
		}
		
		public static function count_array_objects(keys:Array,data:*):int {
			var num:int = -1;
			var obj:*;
			for (var i:String in keys) {
				obj = data[keys[i]];
				if (criteria_isSomeKindOfObject(obj)) {
					num++;
				}
			}
			return num;
		}
		
		public static function locate_root(data:*):* {
			var anObj:* = data;
			var keys_arrays:Array;
			var count_arrays:int;
			var keys_objects:Array;
			var count_objects:int;
			var can_descend:Boolean;
			var selector:String;
			do {
				anObj = (anObj is ObjectProxy) ? anObj.valueOf() : anObj;
				keys_arrays = ObjectUtils.keys(anObj,criteria_isSomeKindOfObject);
				count_arrays = keys_arrays.length;
				keys_objects = ObjectUtils.keys(anObj,criteria_isOfTypeObject);
				count_objects = keys_objects.length;
				can_descend = (count_arrays == 0) && (count_objects >= 1);
				if ( (anObj == null) || (can_descend == false) ) {
					break;
				}
				selector = (count_arrays > 0) ? keys_arrays[count_arrays-1] : keys_objects[count_objects-1];
				anObj = anObj[ selector ];
			} while (1);
			return ((anObj is ObjectProxy) ? anObj.valueOf() : ((anObj is ArrayCollection) ? anObj : (anObj is Array) ? new ArrayCollection(anObj) : anObj));
		}

		public static function urlEncode(anItem:*):* {
			if (anItem is String) {
				return StringUtils.urlEncode(anItem);
			} else {
				return ((anItem is ObjectProxy) ? anItem.valueOf() : anItem);
			}
		}
		
		public static function urlDecode(anItem:*):* {
			if (anItem is String) {
				return StringUtils.urlDecode(anItem).replace('%26','&').replace('%3B',';').replace('&nbsp;',' ').replace('&amp;','&');
			} else {
				return ((anItem is ObjectProxy) ? anItem.valueOf() : anItem);
			}
		}
		
		public static function collector(source:*,callback:Function=null):Object {
			var container:Object = {};
			
			function collect_from_object(obj:*):void {
				var type:String;
				var c:Object;
				var blob:Object;
				var j:String;
				obj = (obj is ObjectProxy) ? obj.valueOf() : obj;
				var is_really_an_array:Boolean = IterTools.all(ObjectUtils.keys(obj),StringUtils.isStringNumeric);
				for (var i:String in obj) {
					c = ( (callback is Function) && (callback != null) ) ? callback(obj[i]) : obj[i];
					type = typeof(c);
					if (type.toLowerCase() == 'object') {
						if (is_really_an_array) {
							for (j in c) {
								container[j] = c[j];
							}
						} else {
							blob = (container[i] == null) ? {} : container[i];
							for (j in c) {
								blob[j] = c[j];
							}
							container[i] = blob;
						}
					} else {
						container[i] = c;
					}
				}
			}
			
			if ( (source is ArrayCollection) || (source is Array) ) {
				for (var i:String in source) {
					collect_from_object(source[i]);
				}
			} else if (source != null) {
				collect_from_object(source);
			}
			return container;
		}

		public static function processor(source:*,callback:Function=null):Object {
			function iterate(obj:*):void {
				for (var i:String in obj) {
					obj[i] = ( (callback is Function) && (callback != null) ) ? callback(obj[i]) : obj[i];
					if ( (obj[i] is ArrayCollection) || (obj[i] is Array) ) {
						processor(obj[i],callback)
					}
				}
			}
			
			if ( (source is ArrayCollection) || (source is Array) ) {
				for (var i:String in source) {
					source[i] = (source[i] is ObjectProxy) ? source[i].valueOf() : source[i];
					iterate(source[i]);
				}
			} else if (source != null) {
				source = (source is ObjectProxy) ? source.valueOf() : source;
				iterate(source);
			}
			return source;
		}

		public static function findImplementorOfFromParentDocumentChain(dispObj:*,aMethod:String):* {
			try {
				var p:* = dispObj;
				while (p) {
					p = p.parentDocument;
					if ( (p) && (p[aMethod] is Function) ) {
						return p;
					}
				}
			} catch (e:Error) {}
			return null;
		}

		public static function getChildUntilFoundByName(name:String,parent:*):* {
			try {
				var obj:*;
				var aChild:*;
				var children:Array = parent.getChildren();
				for (var i:String in children) {
					aChild = children[i].getChildByName(name);
					if (aChild) {
						return aChild;
					}
					obj = getChildUntilFoundByName(name,children[i]);
					if (obj) {
						return obj;
					}
				}
			} catch (e:Error) {}
			return null;
		}

		public static function getChildUntilFoundByClassName(className:String,parent:*):* {
			try {
				var obj:*;
				var child:*;
			    for (var i:uint=0; i < parent.numChildren; i++) {
			    	child = parent.getChildAt(i);
					if (child.className == className) {
						return child;
					}
					obj = getChildUntilFoundByClassName(className,child);
					if (obj) {
						return obj;
					}
			    }
			} catch (e:Error) {}
			return null;
		}

		public static function getChildUntilFoundById(id:String,parent:*):* {
			try {
				var child:*;
				var obj:*;
			    for (var i:uint=0; i < parent.numChildren; i++) {
			    	child = parent.getChildAt(i);
					if (child.id == id) {
						return child;
					}
					obj = getChildUntilFoundById(id,child);
					if (obj) {
						return obj;
					}
			    }
			} catch (e:Error) {}
			return null;
		}

		public static function deepCopy(src:* = null):* {
			var o:* = {};
			var anObj:* = src;
			for (var v:Object in anObj) {
				if ( (anObj[v] is String) || (anObj[v] is Number) || (anObj[v] is int) ) {
					o[v] = anObj[v];
				} else {
					o[v] = deepCopy(anObj[v]);
				}
			}
			return o;
		}

		public static function indexOf(source:*,target:*):int {
			var anObj:*;
			var aKey:String;
			var keys1:Array;
			var keys2:Array;
			var aValue1:String;
			var aValue2:String;
			var isEqual:Boolean = false;
			var index:int = -1;
			var j:String;
			try {
				for (var i:int = 0; i < source.length; i++) {
					anObj = source.getItemAt(i);
					keys1 = ObjectUtils.keys(anObj);
					keys2 = ObjectUtils.keys(target);
					if ( (keys1.length > 0) && (keys2.length > 0) ) {
						isEqual = true;
						for (j in keys1) {
							aKey = keys1[j];
							if (keys2.indexOf(aKey) == -1) {
								isEqual = false;
								break;
							} else {
								aValue1 = anObj[aKey];
								aValue2 = target[aKey];
								if (aValue1 != aValue2) {
									isEqual = false;
									break;
								}
							}
						}
						if (isEqual) {
							index = i;
							break;
						}
					} else if (keys1.length > 0) {
						isEqual = false;
						for (j in keys1) {
							aKey = keys1[j];
							if (anObj[aKey] == target) {
								isEqual = true;
								break;
							}
						}
						if (isEqual) {
							index = i;
							break;
						}
					}
			}
			} catch (e:Error) { }
			return index;
		}

	}
}