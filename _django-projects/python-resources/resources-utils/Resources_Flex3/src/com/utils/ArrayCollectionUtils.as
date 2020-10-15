package com.utils {
	import mx.collections.ArrayCollection;
	
	public class ArrayCollectionUtils {
		public static function totalAll(source:*):Number {
			var total:Number = 0;
			if (source != null) {
				var i:int;
				var ac:ArrayCollection;
				if (source is ArrayCollection) {
					ac = source;
				} else if (source is Array) {
					ac = new ArrayCollection(source);
				} else {
					ac = ArrayCollection(source);
				}
				var val:*;
				for (i = 0; i < ac.length; i++) {
					val = ac.getItemAt(i);
					if (val is Number) {
						total += val;
					} else {
						total += Number(val);
					}
				}
			}
			return total;
		}
		
		public static function appendAll(target:ArrayCollection, source:*):void {
			if ( (target != null) && (source != null) ) {
				var i:int;
				var ac:ArrayCollection;
				if (source is ArrayCollection) {
					ac = source;
				} else if (source is Array) {
					ac = new ArrayCollection(source);
				} else {
					ac = ArrayCollection(source);
				}
				var val:*;
				var _val:*;
				for (i = 0; i < ac.length; i++) {
					val = ac.getItemAt(i);
					if (val is Object) {
						_val = {};
						for (var o:* in val) {
							_val[o] = val[o];	// shallow copy of objects...
						}
					} else {
						_val = val;
					}
					target.addItem(_val);
				}
			}
		}
		
		public static function replaceAll(target:ArrayCollection, source:*):void {
			if ( (target != null) && (source != null) ) {
				target.removeAll();
				appendAll(target,source);
			}
		}
		
		public static function findIndexOfItem(dp:*, selector:String, pattern:String):int {
			var i:int;
			var ac:ArrayCollection;
			if (dp is ArrayCollection) {
				ac = dp;
			} else if (dp is Array) {
				ac = new ArrayCollection(dp);
			} else {
				ac = ArrayCollection(dp);
			}
			var obj:*;
			for (i = 0; i < ac.length; i++) {
				obj = ac.getItemAt(i);
				if ( ((obj is String) == false) && (selector != null) && (selector is String) ) {
					if (obj[selector] == pattern) {
						return i;
					}
				} else {
					if (obj == pattern) {
						return i;
					}
				}
			}
			return -1;
		}

		public static function findIndexOfItemCaseless(dp:*, selector:String, pattern:String):int {
			var i:int;
			var ac:ArrayCollection;
			if (dp is ArrayCollection) {
				ac = dp;
			} else if (dp is Array) {
				ac = new ArrayCollection(dp);
			} else {
				ac = ArrayCollection(dp);
			}
			var obj:*;
			pattern = pattern.toLowerCase();
			for (i = 0; i < ac.length; i++) {
				obj = ac.getItemAt(i);
				if ( ((obj is String) == false) && (selector != null) && (selector is String) ) {
					if (String(obj[selector]).toLowerCase() == pattern) {
						return i;
					}
				} else {
					if (String(obj).toLowerCase() == pattern) {
						return i;
					}
				}
			}
			return -1;
		}
	}
}