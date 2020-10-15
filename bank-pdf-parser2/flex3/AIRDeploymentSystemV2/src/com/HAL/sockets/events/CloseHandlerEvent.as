package com.HAL.sockets.events {
	import flash.events.Event;

	public class CloseHandlerEvent extends Event {

		public function CloseHandlerEvent(type:String, evnt:Event, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_CLOSE_HANDLER:String = "closeHandler";
        
        public var evnt:Event;
        
        override public function clone():Event {
            return new CloseHandlerEvent(type, this.evnt);
        }
	}
}