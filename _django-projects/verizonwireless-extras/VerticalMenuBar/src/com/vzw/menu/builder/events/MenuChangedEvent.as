package com.vzw.menu.builder.events {
	import flash.events.Event;

	public class MenuChangedEvent extends Event {
		public var menu:* = {};
        public static const TYPE_MENU_CHANGED_EVENT:String = "menuChangedEvent";
		
		public function MenuChangedEvent(type:String, aMenu:*, bubbles:Boolean=false, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			this.menu = aMenu;
		}
		
        override public function clone():Event {
            return new MenuChangedEvent(type,this.menu);
        }
	}
}