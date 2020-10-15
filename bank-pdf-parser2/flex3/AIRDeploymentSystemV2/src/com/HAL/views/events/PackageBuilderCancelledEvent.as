package com.HAL.views.events {
	import flash.events.Event;

	public class PackageBuilderCancelledEvent extends Event {

		public function PackageBuilderCancelledEvent(type:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
		}
		
        public static const TYPE_PACKAGE_BUILDER_CANCELLED:String = "packageBuilderCancelled";

        override public function clone():Event {
            return new PackageBuilderCancelledEvent(type);
        }
	}
}