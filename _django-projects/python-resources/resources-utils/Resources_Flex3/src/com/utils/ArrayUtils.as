package com.utils {
	import flash.utils.ByteArray;

	public class ArrayUtils {

		public static function deepCopyFrom(source:Object):* {
		    var myBA:ByteArray = new ByteArray();
		    myBA.writeObject(source);
		    myBA.position = 0;
		    return(myBA.readObject());
		}

		public static function countUniques(source:Array):Number {
			var uniques:Array = [];
			var i:int;
			for (i = 0; i < source.length; i++) {
				if (uniques.indexOf(source[i]) == -1) {
					uniques.push(source[i]);
				}
			}
			return uniques.length;
		}

		public static function trim(source:Array):* {
			var i:int;
			for (i = 0; i < source.length; i++) {
				source[i] = StringUtils.trim(source[i] as String);
			}
		}
	}
}