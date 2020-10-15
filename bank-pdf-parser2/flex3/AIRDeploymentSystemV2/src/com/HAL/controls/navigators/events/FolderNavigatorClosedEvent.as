package com.HAL.controls.navigators.events {
	import flash.events.Event;

	public class FolderNavigatorClosedEvent extends Event {

		public function FolderNavigatorClosedEvent(type:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
		}
		
        public static const TYPE_FOLDER_NAVIGATOR_CLOSED:String = "folderNavigatorClosed";
        
        override public function clone():Event {
            return new FolderNavigatorClosedEvent(type);
        }
	}
}