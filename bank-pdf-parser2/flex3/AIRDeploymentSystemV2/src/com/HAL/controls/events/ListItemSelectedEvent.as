package com.HAL.controls.events {
	import flash.events.Event;

	public class ListItemSelectedEvent extends Event {

		public function ListItemSelectedEvent(type:String, event:*, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.event = event;
		}
		
        public static const TYPE_LIST_ITEM_SELECTED:String = "listItemSelected";
        
        public var event:*;
        
        override public function clone():Event {
            return new ListItemSelectedEvent(type, this.event);
        }
	}
}