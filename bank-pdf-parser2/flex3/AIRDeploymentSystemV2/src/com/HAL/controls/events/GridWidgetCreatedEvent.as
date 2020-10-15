package com.HAL.controls.events {
	import flash.events.Event;

	public class GridWidgetCreatedEvent extends Event {

		public function GridWidgetCreatedEvent(type:String, event:*, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.event = event;
		}
		
        public static const TYPE_GRID_WIDGET_CREATED:String = "gridWidgetCreated";
        
        public var event:*;
        
        override public function clone():Event {
            return new GridWidgetCreatedEvent(type, this.event);
        }
	}
}