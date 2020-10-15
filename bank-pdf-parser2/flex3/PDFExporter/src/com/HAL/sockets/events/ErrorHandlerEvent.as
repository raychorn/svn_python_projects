package com.HAL.sockets.events {
	import flash.events.Event;

	public class ErrorHandlerEvent extends Event {

		public function ErrorHandlerEvent(type:String, data:*, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.data = data;
		}
		
        public static const TYPE_ERROR_HANDLER:String = "errorHandler";
        
        public var data:*;
        
        override public function clone():Event {
            return new ErrorHandlerEvent(type, this.data);
        }
	}
}