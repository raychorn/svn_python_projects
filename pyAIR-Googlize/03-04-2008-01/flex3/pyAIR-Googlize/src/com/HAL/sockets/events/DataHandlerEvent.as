package com.HAL.sockets.events {
	import flash.events.Event;

	public class DataHandlerEvent extends Event {

		public function DataHandlerEvent(type:String, evnt:*, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_DATA_HANDLER:String = "dataHandler";
        
        public var evnt:*;
        
        override public function clone():Event {
            return new DataHandlerEvent(type, this.evnt);
        }
	}
}