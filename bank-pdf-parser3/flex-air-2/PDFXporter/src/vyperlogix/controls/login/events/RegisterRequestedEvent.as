package vyperlogix.controls.login.events {
	import flash.events.Event;

	public class RegisterRequestedEvent extends Event {
		public function RegisterRequestedEvent(type:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
		}
		
        public static const TYPE_REGISTER_REQUESTED:String = "registerRequested";

        override public function clone():Event {
            return new RegisterRequestedEvent(type);
        }
	}
}