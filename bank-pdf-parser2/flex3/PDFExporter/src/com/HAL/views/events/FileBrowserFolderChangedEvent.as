package com.HAL.views.events {
	import flash.events.Event;

	public class FileBrowserFolderChangedEvent extends Event {

		public function FileBrowserFolderChangedEvent(type:String, folder:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.folder = folder;
		}
		
        public static const FILE_BROWSER_FOLDER_CHANGED:String = "FileBrowserFolderChanged";
        
        public var folder:String = '';

        override public function clone():Event {
            return new FileBrowserFolderChangedEvent(type, this.folder);
        }
	}
}