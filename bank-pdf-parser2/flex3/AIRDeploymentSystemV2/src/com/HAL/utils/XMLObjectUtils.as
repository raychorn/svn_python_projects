package com.HAL.utils {
	import mx.collections.ArrayCollection;
	
	public class XMLObjectUtils {
		public static function getValuesFromNodeOfTypeTitleWithDetails(data:Object):Array {
			var retVal:Array = [];
			if ( (data.value == null) && (data.children is Array) && (data.children.length == 2) ) {
				var ac:ArrayCollection = new ArrayCollection(data.children);
				var _f1:int = ArrayCollectionUtils.findIndexOfItem(ac,'name','title');
				var _f2:int = ArrayCollectionUtils.findIndexOfItem(ac,'name','details');
				if ( (_f1 > -1) && (_f2 > -1) ) {
					var obj:Object = ac.getItemAt(_f1);
					flattenChildrenIntoNodeValue(obj);
					retVal.push(obj.value);

					obj = ac.getItemAt(_f2);
					flattenChildrenIntoNodeValue(obj);
					retVal.push(obj.value);
				}
			}
			return retVal;
		}
		
		public static function flattenChildrenIntoNodeValue(data:Object):void {
			if ( (data.value == null) && (data.children is Array) && (data.children.length > 0) ) {
				var ar:Array = getValuesFromNodeOfTypeTitleWithDetails(data);
				if (ar.length > 0) {
					data.value = ar;
					data.children = [];
				} else {
					var val:String = '';
					var i:int;
					var o:Object;
					for (i = 0; i < data.children.length; i++) {
						o = data.children[i];
						val += o.value;
					}
					data.value = val;
					data.children = [];
				}
			}
		}

	}
}