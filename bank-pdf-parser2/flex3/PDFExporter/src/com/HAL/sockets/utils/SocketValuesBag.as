package com.HAL.sockets.utils {
	public class SocketValuesBag {
		private var dict:Object;
		
		public function SocketValuesBag():void {
			this.dict = {}
		}
		
		public function setValue(name:String, value:String):void {
			this.dict[name] = value;
		}
		
		public function getValue(name:String):String {
			return this.dict[name];
		}
		
		public function encode():String {
			var s:String = '';
			for (var k:String in this.dict) {
				s += k.toString() + '=' + this.dict[k] + String.fromCharCode(127); 
			}
			return s;
		}
	}
}