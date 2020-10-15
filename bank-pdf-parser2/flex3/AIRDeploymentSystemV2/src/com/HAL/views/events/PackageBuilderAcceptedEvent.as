package com.HAL.views.events {
	import flash.events.Event;

	public class PackageBuilderAcceptedEvent extends Event {

		public function PackageBuilderAcceptedEvent(type:String, fileName:String, filesList:Array, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.fileName = fileName;
			this.filesList = filesList;
		}
		
        public static const TYPE_PACKAGE_BUILDER_ACCEPTED:String = "packageBuilderAccepted";
        
        public var fileName:String = '';
        public var filesList:Array = [];

        override public function clone():Event {
            return new PackageBuilderAcceptedEvent(type, this.fileName, this.filesList);
        }
	}
}