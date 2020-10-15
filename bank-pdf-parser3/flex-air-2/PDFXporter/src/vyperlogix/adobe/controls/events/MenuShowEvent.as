package vyperlogix.adobe.controls.events {
	import flash.events.Event;
	
	import mx.controls.Menu;

	public class MenuShowEvent extends Event {
		public function MenuShowEvent(type:String, menu:Menu, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
		}
		
        public static const TYPE_MENU_SHOW:String = "menuShow";

        public var menu:Menu;

        override public function clone():Event {
            return new MenuShowEvent(type, menu);
        }
	}
}