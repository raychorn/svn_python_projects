package com.HAL.sockets.events {
	import flash.events.Event;

	public class ConnectionTimeoutEvent extends Event {

		public function ConnectionTimeoutEvent(type:String, evnt:Event, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_CONNECTION_TIMEOUT:String = "connectionTimeout";
        
        public var evnt:Event;
        
        override public function clone():Event {
            return new ConnectionTimeoutEvent(type, this.evnt);
        }
	}
}