package com.HAL.controls.events {
	import flash.events.Event;

	public class ListInFocusEvent extends Event {

		public function ListInFocusEvent(type:String, event:*, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.event = event;
		}
		
        public static const TYPE_LIST_IN_FOCUS:String = "listInFocus";
        
        public var event:*;
        
        override public function clone():Event {
            return new ListInFocusEvent(type, this.event);
        }
	}
}