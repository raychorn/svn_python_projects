package vyperlogix.controls.login.events {
	import flash.events.Event;

	public class LoginCompletedEvent extends Event {
		public function LoginCompletedEvent(type:String, username:String, password:String, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);

            this.username = username;
            this.password = password;
		}
		
        public static const TYPE_LOGIN_COMPLETED:String = "loginCompleted";

        public var username:String;
        public var password:String;

        override public function clone():Event {
            return new LoginCompletedEvent(type, username, password);
        }
	}
}