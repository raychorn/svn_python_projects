package com.HAL.sockets.events {
	import flash.events.Event;

	public class SecurityErrorHandlerEvent extends Event {

		public function SecurityErrorHandlerEvent(type:String, evnt:Event, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_SECURITY_ERROR_HANDLER:String = "securityErrorHandler";
        
        public var evnt:Event;
        
        override public function clone():Event {
            return new SecurityErrorHandlerEvent(type, this.evnt);
        }
	}
}