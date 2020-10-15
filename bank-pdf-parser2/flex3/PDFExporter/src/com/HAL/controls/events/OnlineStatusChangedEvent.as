package com.HAL.controls.events {
	import flash.events.Event;

	public class OnlineStatusChangedEvent extends Event {

		public function OnlineStatusChangedEvent(type:String, color:uint, alpha:Number, status:Boolean, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.color = color;
			this.alpha = alpha;
			this.status = status;
		}
		
        public static const TYPE_ONLINE_STATUS_CHANGED:String = "onlineStatusChanged";

        public var color:uint;
        public var alpha:Number;
        public var status:Boolean;
        
        override public function clone():Event {
            return new OnlineStatusChangedEvent(type, this.color, this.alpha, this.status);
        }
	}
}