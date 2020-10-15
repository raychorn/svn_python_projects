package com.HAL.sockets.events {
	import flash.events.Event;

	public class ConnectHandlerEvent extends Event {

		public function ConnectHandlerEvent(type:String, evnt:Event, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_CONNECT_HANDLER:String = "connectHandler";
        
        public var evnt:Event;
        
        override public function clone():Event {
            return new ConnectHandlerEvent(type, this.evnt);
        }
	}
}