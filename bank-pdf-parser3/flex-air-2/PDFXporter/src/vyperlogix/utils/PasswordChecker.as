package vyperlogix.utils {
	import flash.text.TextField;
	import mx.controls.TextInput;
	
	public class PasswordChecker {
		private var isWeak:Boolean = false;
		private var isMedium:Boolean = false;
		private var isStrong:Boolean = false;

		private function analyzePassword(s:String):Object {
			var i:int = -1;
			var ch:Number = -1;
			var alphaCount:int = 0;
			var numericCount:int = 0;
			var specialCount:int = 0;
			var o:Object = new Object();
			
			for (i = 0; i < s.length; i++) {
				ch = s.charCodeAt(i);
				alphaCount += (((ch >= 65) && (ch <= 90)) ? 1 : 0);
				alphaCount += (((ch >= 97) && (ch <= 122)) ? 1 : 0);
				numericCount += (((ch >= 48) && (ch <= 57)) ? 1 : 0);
				specialCount += (((ch >= 33) && (ch <= 47)) ? 1 : 0);
				specialCount += (((ch >= 58) && (ch <= 64)) ? 1 : 0);
				specialCount += (((ch >= 123) && (ch <= 126)) ? 1 : 0);
			}
			o.sInput = s;
			o.alphaCount = alphaCount;
			o.numericCount = numericCount;
			o.specialCount = specialCount;
			return o;
		}
		
		public function PasswordChecker():void {
			return;
		}
		
		private function _isWeakPassword(ap:Object):Boolean {
			this.isWeak = ( ( (ap.alphaCount > 0) || (ap.numericCount > 0) || (ap.specialCount > 0) ) && (ap.sInput.length > 1) );
			return this.isWeak;
		}
		
		public function isWeakPassword(s:String):Boolean {
			var ap:Object = this.analyzePassword(s);
			
			return this._isWeakPassword(ap);
		}
		
		private function _isMediumPassword(ap:Object):Boolean {
			this.isMedium = ( ( (ap.alphaCount > 0) && (ap.specialCount > 0) ) || ( (ap.alphaCount > 0) && (ap.numericCount > 0) ) || ( (ap.specialCount > 0) && (ap.numericCount > 0) ) && (ap.sInput.length > 5) );
			return this.isMedium;
		}
		
		public function isMediumPassword(s:String):Boolean {
			var ap:Object = this.analyzePassword(s);
			
			return (this._isWeakPassword(ap) && this._isMediumPassword(ap));
		}
		
		private function _isStrongPassword(ap:Object):Boolean {
			this.isStrong = ( (ap.alphaCount > 0) && (ap.numericCount > 0) && (ap.specialCount > 0) && (ap.sInput.length > 12) );
			return this.isStrong;
		}
		
		public function isStrongPassword(s:String):Boolean {
			var ap:Object = this.analyzePassword(s);
			
			return (this._isMediumPassword(ap) && this._isStrongPassword(ap));
		}
	}
}

