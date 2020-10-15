package com.REST {
	import mx.utils.ArrayUtil;
	import flash.utils.ByteArray;

	public class EzArrayUtils {

		public static function deepCopyFrom(source:Object):* {
		    var myBA:ByteArray = new ByteArray();
		    myBA.writeObject(source);
		    myBA.position = 0;
		    return(myBA.readObject());
		}
	}
}