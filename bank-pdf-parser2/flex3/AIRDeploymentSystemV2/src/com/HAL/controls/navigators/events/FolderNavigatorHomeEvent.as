package com.HAL.controls.navigators.events {
	import flash.events.Event;

	public class FolderNavigatorHomeEvent extends Event {

		public function FolderNavigatorHomeEvent(type:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
		}
		
        public static const TYPE_FOLDER_NAVIGATOR_HOME:String = "folderNavigatorHome";
        
        override public function clone():Event {
            return new FolderNavigatorHomeEvent(type);
        }
	}
}