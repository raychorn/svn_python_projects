package vyperlogix.controls.login.events {
	import flash.events.Event;

	public class RegisterCompletedEvent extends Event {
		public function RegisterCompletedEvent(type:String, datum:Object, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.datum = datum;
		}
		
        public static const TYPE_REGISTER_COMPLETED:String = "registerCompleted";
        
        public var datum:Object;

        override public function clone():Event {
            return new RegisterCompletedEvent(type, datum);
        }
	}
}