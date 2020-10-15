package com.HAL.views.events {
	import flash.events.Event;

	public class FileBrowserFileSelectedEvent extends Event {

		public function FileBrowserFileSelectedEvent(type:String, fileName:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.fileName = fileName;
		}
		
        public static const FILE_BROWSER_FILE_SELECTED:String = "FileBrowserFileSelected";
        
        public var fileName:String = '';

        override public function clone():Event {
            return new FileBrowserFileSelectedEvent(type, this.fileName);
        }
	}
}