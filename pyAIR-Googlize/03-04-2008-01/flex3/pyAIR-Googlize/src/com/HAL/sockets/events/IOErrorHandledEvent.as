package com.HAL.sockets.events {
	import flash.events.Event;

	public class IOErrorHandledEvent extends Event {

		public function IOErrorHandledEvent(type:String, evnt:Event, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_IOERROR_HANDLED:String = "ioErrorHandled";
        
        public var evnt:Event;
        
        override public function clone():Event {
            return new IOErrorHandledEvent(type, this.evnt);
        }
	}
}