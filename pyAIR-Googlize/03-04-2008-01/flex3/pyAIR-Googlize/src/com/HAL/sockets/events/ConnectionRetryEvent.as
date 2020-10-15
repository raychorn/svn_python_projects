package com.HAL.sockets.events {
	import flash.events.Event;

	public class ConnectionRetryEvent extends Event {

		public function ConnectionRetryEvent(type:String, evnt:Event, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_CONNECTION_RETRY:String = "connectionRetry";
        
        public var evnt:Event;
        
        override public function clone():Event {
            return new ConnectionRetryEvent(type, this.evnt);
        }
	}
}