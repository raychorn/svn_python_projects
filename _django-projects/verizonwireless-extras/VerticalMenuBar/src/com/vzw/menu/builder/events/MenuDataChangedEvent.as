package com.vzw.menu.builder.events {
	import flash.events.Event;

	public class MenuDataChangedEvent extends Event {
        public static const TYPE_MENU_DATA_CHANGED_EVENT:String = "MenuDataChangedEvent";
		
		public function MenuDataChangedEvent(type:String, bubbles:Boolean=false, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
		}
		
        override public function clone():Event {
            return new MenuDataChangedEvent(type);
        }
	}
}