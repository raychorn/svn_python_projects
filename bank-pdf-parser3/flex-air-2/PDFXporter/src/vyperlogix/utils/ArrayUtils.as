package vyperlogix.utils {
	import flash.utils.ByteArray;
	
	import mx.utils.ArrayUtil;

	public class ArrayUtils extends ArrayUtil {
		public static function collectUsingSelector(source:Array,selector:String):Array {
			var ar:Array = [];
			var datum:String;
			for (var i:String in source) {
				datum = source[i][selector];
				if (datum is String) {
					ar.push(datum);
				}
			}
			return ar;
		}
		
		public static function removeThisItemFrom(item:*,source:Array):void {
			var i:int = source.indexOf(item);
			if (i > -1) {
				source.splice(i,1);
			}
		}

		public static function pruneEmptyItems(source:Array):Array {
			var copy:Array = [];
			for (var i:int = 0; i < source.length; i++) {
				if (String(source[i]).length > 0) {
					copy.push(source[i]);
				}
			}
			return copy;
		}

		public static function deepCopyFrom(source:Object):* {
		    var myBA:ByteArray = new ByteArray();
		    myBA.writeObject(source);
		    myBA.position = 0;
		    var o:Object = myBA.readObject();
		    return(o);
		}

		public static function trimAll(source:Array):void {
			var i:int;
			if (source != null) {
				try {
					for (i = 0; i < source.length; i++) {
						source[i] = StringUtils.trim(String(source[i]))
					}
				} catch (err:Error) { }
			}
		}

		public static function addAllInto(target:Array, source:Array, whenTrue:Function = null):void {
			var i:int;
			if ( (source != null) && (target != null) ) {
				try {
					for (i = 0; i < source.length; i++) {
						if ( (whenTrue == null) || ( (whenTrue != null) && (whenTrue is Function) && (whenTrue(source[i])) ) ) {
							target.push(source[i]);
						}
					}
				} catch (err:Error) { }
			}
		}
		
		public static function inclusiveJoin(source:Array, delim:String):String {
			var result:String = "";
			if ( (source != null) && (source.length > 0) && (delim != null) && (delim.length > 0) ) {
				for (var i:int = 0; i < source.length; i++) {
					result += source[i] + delim;
				}
			}
			return result;
		}
			
		public static function popFromFront(source:Array):* {
			if ( (source != null) && (source.length > 0) ) {
				var datum:* = source[0];
				source.splice(0,1);
				return datum;
			}
			return null;
		}
		
		public static function spliceIf(source:Array, func:Function):void {
			if ( (source != null) && (source.length > 0) ) {
				for (var i:int = 0; i < source.length; ) {
					if ( (func != null) && (func is Function) ) {
						var bool:Boolean = false;
						try { bool = func(source[i], i, source); } catch (err:Error) { }
						if (bool) {
							source.splice(i,1);
						} else {
							i++;
						}
					}
				}
			}
		}
		
		public static function findIf(source:Array, func:Function, selector:String, aValue:*, actionFunc:Function = null):* {
			if ( (source != null) && (source.length > 0) ) {
				for (var i:int = 0; i < source.length; ) {
					if ( (func != null) && (func is Function) ) {
						var bool:Boolean = false;
						try { bool = func(source[i], i, source, selector, aValue); } catch (err:Error) { }
						if (bool) {
							var retVal:* = source[i];
							if ( (actionFunc != null) && (actionFunc is Function) ) {
								try { actionFunc(i, source); } catch (err:Error) { }
							}
							return retVal;
						} else {
							i++;
						}
					}
				}
			}
			return null;
		}
	}
}