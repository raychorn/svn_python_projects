package com.HAL.controls.navigators.events {
	import flash.events.Event;

	public class FileListInitContextMenuEvent extends Event {

		public function FileListInitContextMenuEvent(type:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
		}
		
        public static const TYPE_FILE_LIST_INIT_CONTEXT_MENU:String = "fileListInitContextMenu";
        
        override public function clone():Event {
            return new FileListInitContextMenuEvent(type);
        }
	}
}