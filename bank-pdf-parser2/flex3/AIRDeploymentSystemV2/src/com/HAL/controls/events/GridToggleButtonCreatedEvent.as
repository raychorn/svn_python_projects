package com.HAL.controls.events {
	import flash.events.Event;

	public class GridToggleButtonCreatedEvent extends Event {

		public function GridToggleButtonCreatedEvent(type:String, event:*, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.event = event;
		}
		
        public static const TYPE_GRID_TOGGLE_BUTTON_CREATED:String = "gridToggleButtonCreated";
        
        public var event:*;
        
        override public function clone():Event {
            return new GridToggleButtonCreatedEvent(type, this.event);
        }
	}
}