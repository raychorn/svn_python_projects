package com.HAL.sockets.events {
	import flash.events.Event;

	public class DataReceivedEvent extends Event {

		public function DataReceivedEvent(type:String, data:Object, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.data = data;
		}
		
        public static const TYPE_DATA_RECEIVED:String = "dataReceived";
        
        public var data:Object;
        
        override public function clone():Event {
            return new DataReceivedEvent(type, this.data);
        }
	}
}