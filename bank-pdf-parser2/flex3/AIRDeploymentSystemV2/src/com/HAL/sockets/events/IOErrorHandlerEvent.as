package com.HAL.sockets.events {
	import flash.events.Event;

	public class IOErrorHandlerEvent extends Event {

		public function IOErrorHandlerEvent(type:String, evnt:Event, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_IOERROR_HANDLER:String = "ioErrorHandler";
        
        public var evnt:Event;
        
        override public function clone():Event {
            return new IOErrorHandlerEvent(type, this.evnt);
        }
	}
}