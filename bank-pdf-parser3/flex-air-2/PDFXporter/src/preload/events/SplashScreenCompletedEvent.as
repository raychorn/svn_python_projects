package preload.events {
	import flash.events.Event;

	public class SplashScreenCompletedEvent extends Event {
		public function SplashScreenCompletedEvent(type:String, wcs:*, bubbles:Boolean=true, cancelable:Boolean=false) {
			this.wcs = wcs;
			super(type, bubbles, cancelable);
		}
		
		public var wcs:*;
		
        public static const TYPE_SPLASH_COMPLETED:String = "splashCompleted";

        override public function clone():Event {
            return new SplashScreenCompletedEvent(type,this.wcs);
        }
	}
}