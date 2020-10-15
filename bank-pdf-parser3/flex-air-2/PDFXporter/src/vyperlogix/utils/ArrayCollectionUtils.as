package vyperlogix.utils {
	import mx.collections.ArrayCollection;
	
	public class ArrayCollectionUtils {
		public static function touchAll(target:ArrayCollection, aFunc:Function, aSelector:String):void {
			if (aFunc is Function) {
				var i:int;
				var anItem:Object;
				for (i = 0; i < target.length; i++) {
					anItem = target.getItemAt(i);
					try {
						anItem = aFunc(anItem,aSelector);
						target.setItemAt(anItem,i);
					} catch (e:Error) {}
				}
			}
		}
		
		public static function clone(source:ArrayCollection,aFunc:Function=null):ArrayCollection {
			var ac:ArrayCollection = new ArrayCollection();
			if (source is ArrayCollection) {
				var item:*;
				var isOkay:Boolean = true;
				for (var i:String in source.source) {
					item = source.source[i];
					isOkay = (aFunc is Function) ? aFunc(item): isOkay;
					if (isOkay) {
						ac.addItem(item);
					}
				}
			}
			return ac;
		}
		
		public static function appendAllInto(target:ArrayCollection, source:*, aFunc:Function=null):void {
			if ( (target != null) && (source != null) ) {
				var i:int;
				var item:*;
				var isAdding:Boolean = true;
				var ac:ArrayCollection;
				if (source is ArrayCollection) {
					ac = source;
				} else if (source is Array) {
					ac = new ArrayCollection(source);
				} else if (source != null) {
					ac = ArrayCollection(source);
				}
				if (ac != null) {
					for (i = 0; i < ac.length; i++) {
						item = ac.getItemAt(i);
						if (aFunc is Function) {
							isAdding = aFunc(item);
						}
						if (isAdding) {
							target.addItem(item);
						}
					}
				}
			}
		}
		
		public static function replaceAll(target:ArrayCollection, source:*):void {
			if ( (target != null) && (source != null) ) {
				target.removeAll();
				appendAllInto(target,source);
			}
		}
		
		public static function findIndexOfItem(dp:*, selector:String, pattern:*):int {
			var i:int;
			var ac:ArrayCollection;
			if (dp is ArrayCollection) {
				ac = dp;
			} else if (dp is Array) {
				ac = new ArrayCollection(dp);
			} else if (dp != null) {
				ac = ArrayCollection(dp);
			}
			if (ac != null) {
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
			} else if (dp != null) {
				ac = ArrayCollection(dp);
			}
			if ( (ac != null) && (pattern != null) ) {
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
			}
			return -1;
		}
	}
}