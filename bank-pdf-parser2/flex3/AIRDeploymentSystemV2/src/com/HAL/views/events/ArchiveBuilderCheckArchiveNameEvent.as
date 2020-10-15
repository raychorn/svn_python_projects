package com.HAL.views.events {
	import flash.events.Event;

	public class ArchiveBuilderCheckArchiveNameEvent extends Event {

		public function ArchiveBuilderCheckArchiveNameEvent(type:String, fileName:String, callback:Function, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.fileName = fileName;
			this.callback = callback;
		}
		
        public static const TYPE_ARCHIVE_BUILDER_CHECK_ARCHIVE_NAME:String = "archiveBuilderCheckArchiveName";
        
        public var fileName:String = '';
        public var callback:Function;

        override public function clone():Event {
            return new ArchiveBuilderCheckArchiveNameEvent(type, this.fileName, this.callback);
        }
	}
}