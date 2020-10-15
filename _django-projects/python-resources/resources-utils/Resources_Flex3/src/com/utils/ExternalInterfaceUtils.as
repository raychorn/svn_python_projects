package com.utils {
	import flash.external.ExternalInterface;
	
	public class ExternalInterfaceUtils {

		public static var _url:String;
		
		public static function get isRunningLocal():Boolean {
			var bool:Boolean = true;
			try {
				bool = (_url.indexOf("file://") > -1);
			} catch (err:Error) { }
			return (bool);
		}

		public static function CallJavaScript(funcName:String, ...args):* {
			var win:Object = new Object();
			for (var i:uint = 0; i < args.length; i++) {
				win['arg_'+i.toString()] = args[i];
			}
		    return ExternalInterface.call(funcName,win); 
		}

	}
}