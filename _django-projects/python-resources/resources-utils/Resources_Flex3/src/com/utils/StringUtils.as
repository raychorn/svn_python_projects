package com.utils {
	public class StringUtils {
		public static function trim(value:String):String {
			return value.match(/^\s*(.*?)\s*$/)[1];
		}

		public static const mode_OBSCURE_ALL:uint = 0x0000;
		public static const mode_OBSCURE_PARTIAL:uint = 0x0001;

		public static function isAlpha(char:uint):Boolean {
			return ( ( (char >= 0x41) && (char <= 0x5a) ) || ( (char >= 0x61) && (char <= 0x7a) ) );
		}
		
		public static function isNumeric(char:uint):Boolean {
			return ( (char >= 0x30) && (char <= 0x39) );
		}
		
		public static function isAlphaNumeric(char:uint):Boolean {
			return (isAlpha(char) || isNumeric(char));
		}
		
		public static function isStringNumeric(s:String):Boolean {
			var i:int;
			for (i = 0; i < s.length; i++) {
				if (!isNumeric(s.charCodeAt(i))) {
					return false;
				}
			}
			return true;
		}

		public static function numericString(s:String):String {
			var i:int;
			var value:String = '';
			var ch:uint;
			for (i = 0; i < s.length; i++) {
				ch = s.charCodeAt(i);
				if ( (isNumeric(ch)) || (s.substr(i,1) == '.') ) {
					value += String.fromCharCode(ch);
				}
			}
			return value;
		}

		public static function replaceAll(source:String, pattern:String, newPattern:String):String {
			var ar:Array = source.split(pattern);
			return (ar.join(newPattern));
		}
		
		public static function obscure(value:String, mode:uint = mode_OBSCURE_PARTIAL):String {
			var i:int;
			var s:String = "";
			for (i = 0; i < value.length; i++) {
				s += ((mode = mode_OBSCURE_PARTIAL) ? ((isAlphaNumeric(value.charCodeAt(i))) ? String.fromCharCode(value.charCodeAt(i)) : String.fromCharCode(value.charCodeAt(i) | 0x80)) : String.fromCharCode(value.charCodeAt(i) | 0x80));
			}
			return s;
		}

		public static function deobscure(value:String):String {
			var i:int;
			var s:String = "";
			for (i = 0; i < value.length; i++) {
				s += String.fromCharCode(value.charCodeAt(i) & 0x7f);
			}
			return s;
		}

		public static function truncateNumberRightOfDecimalPoint(value:String):String {
			var toks:Array = value.split('.');
			if ( (toks.length > 1) && (int(toks[toks.length-1]) == 0) ) {
				toks.pop();
			}
			return toks.join('.');
		}
		
		public static function spaceToUnderscore(value:String):String {
			var toks:Array = value.split(' ');
			return toks.join('_');
		}
		
		public static function underscoreToSpace(value:String):String {
			var toks:Array = value.split('_');
			return toks.join(' ');
		}
	}
}