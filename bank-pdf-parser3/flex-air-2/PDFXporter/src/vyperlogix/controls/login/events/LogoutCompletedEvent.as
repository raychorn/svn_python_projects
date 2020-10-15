package vyperlogix.controls.login.events {
	import flash.events.Event;

	public class LogoutCompletedEvent extends Event {
		public function LogoutCompletedEvent(type:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
		}
		
        public static const TYPE_LOGOUT_COMPLETED:String = "LogoutCompleted";

        override public function clone():Event {
            return new LogoutCompletedEvent(type);
        }
	}
}