package com.HAL.sockets.events {
	import flash.events.Event;
	
	public class ExecPythonEvent extends Event {

		public function ExecPythonEvent(type:String, obj:*, methodName:String, pythonCommand:int, args:Array, bubbles:Boolean=true, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
			
			this.obj = obj;
			this.methodName = methodName;
			this.pythonCommand = pythonCommand;
			this.args = args;
		}
		
        public static const TYPE_EXEC_PYTHON:String = "execPython";
        
        public var obj:*;
        public var methodName:String;
        public var pythonCommand:int;
        public var args:Array;
        
        override public function clone():Event {
            return new ExecPythonEvent(type, this.obj, this.methodName, this.pythonCommand, this.args);
        }
	}
}