package com.HAL.sockets.events {
	import flash.events.Event;

	public class ConnectionEstablishedEvent extends Event {

		public function ConnectionEstablishedEvent(type:String, evnt:Event, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_CONNECTION_ESTABLISHED:String = "connectionEstablished";
        
        public var evnt:Event;
        
        override public function clone():Event {
            return new ConnectionEstablishedEvent(type, this.evnt);
        }
	}
}