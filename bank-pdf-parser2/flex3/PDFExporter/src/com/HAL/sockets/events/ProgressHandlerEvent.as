package com.HAL.sockets.events {
	import flash.events.Event;

	public class ProgressHandlerEvent extends Event {

		public function ProgressHandlerEvent(type:String, evnt:Event, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.evnt = evnt;
		}
		
        public static const TYPE_PROGRESS_HANDLER:String = "progressHandler";
        
        public var evnt:Event;
        
        override public function clone():Event {
            return new ProgressHandlerEvent(type, this.evnt);
        }
	}
}