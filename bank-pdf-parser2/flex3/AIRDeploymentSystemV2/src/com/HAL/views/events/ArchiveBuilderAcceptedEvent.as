package com.HAL.views.events {
	import flash.events.Event;

	public class ArchiveBuilderAcceptedEvent extends Event {

		public function ArchiveBuilderAcceptedEvent(type:String, fileName:String, filesList:Array, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.fileName = fileName;
			this.filesList = filesList;
		}
		
        public static const TYPE_ARCHIVE_BUILDER_ACCEPTED:String = "archiveBuilderAccepted";
        
        public var fileName:String = '';
        public var filesList:Array = [];

        override public function clone():Event {
            return new ArchiveBuilderAcceptedEvent(type, this.fileName, this.filesList);
        }
	}
}