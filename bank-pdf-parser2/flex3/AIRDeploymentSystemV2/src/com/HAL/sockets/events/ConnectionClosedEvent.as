package com.HAL.sockets.events {
	import flash.events.Event;

	public class ConnectionClosedEvent extends Event {

		public function ConnectionClosedEvent(type:String, evnt:Event, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_CONNECTION_CLOSED:String = "connectionClosed";
        
        public var evnt:Event;
        
        override public function clone():Event {
            return new ConnectionClosedEvent(type, this.evnt);
        }
	}
}