package com.HAL.controls.navigators.events {
	import flash.events.Event;

	public class FolderNavigatorChangedEvent extends Event {

		public function FolderNavigatorChangedEvent(type:String, newPath:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.newPath = newPath;
		}
		
        public static const TYPE_FOLDER_NAVIGATOR_CHANGED:String = "folderNavigatorChanged";
        
        public var newPath:String;
        
        override public function clone():Event {
            return new FolderNavigatorChangedEvent(type, this.newPath);
        }
	}
}