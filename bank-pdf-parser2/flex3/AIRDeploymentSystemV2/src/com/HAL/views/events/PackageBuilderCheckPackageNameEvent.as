package com.HAL.views.events {
	import flash.events.Event;

	public class PackageBuilderCheckPackageNameEvent extends Event {

		public function PackageBuilderCheckPackageNameEvent(type:String, fileName:String, callback:Function, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.fileName = fileName;
			this.callback = callback;
		}
		
        public static const TYPE_PACKAGE_BUILDER_CHECK_PACKAGE_NAME:String = "packageBuilderCheckPackageName";
        
        public var fileName:String = '';
        public var callback:Function;

        override public function clone():Event {
            return new PackageBuilderCheckPackageNameEvent(type, this.fileName, this.callback);
        }
	}
}