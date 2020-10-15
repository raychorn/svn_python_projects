package com.HAL.controls.navigators.events {
	import flash.events.Event;

	public class FolderNavigatorUpEvent extends Event {

		public function FolderNavigatorUpEvent(type:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
		}
		
        public static const TYPE_FOLDER_NAVIGATOR_UP:String = "folderNavigatorUp";
        
        override public function clone():Event {
            return new FolderNavigatorUpEvent(type);
        }
	}
}