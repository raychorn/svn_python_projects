package vyperlogix.controls.Alert {
	import mx.controls.Alert;

	public class AlertPopUp extends Alert {
		
		private static const chars_per_line:int = 32;
		
		[Embed(source="alert_error.gif")]
		private static var iconError:Class;
		
		[Embed(source="alert_info.gif")]
		private static var iconInfo:Class;
		
		[Embed(source="alert_confirm.gif")]
		private static var iconConfirm:Class;
		
		private static var spaces:String = "           ";
		
		private static function formatText(s:String):String {
			var t:String = "";
			var tx:String = "";
			var i:int;
			var ch:String;
			var _ch:uint;
			return s; // come back to this later - turn the string into an array and then walk the array inserting "\n" where appropriate...
			for (i = 0; i < s.length; i++) {
				ch = s.charAt(i);
				_ch = s.charCodeAt(i);
				if (_ch < 32) {
					t += " ";
					continue;
				}
				if (t.length >= chars_per_line) {
					_ch = s.charCodeAt(t.length - 1);
					if ( (_ch > 32) && (_ch < 127) ) {
						_ch = t.charCodeAt(t.length - 1);
						for (; ( (i > 0) && ( (_ch > 32) && (_ch < 127) ) ); i--) {
							ch = s.charAt(t.length - 1);
							_ch = t.charCodeAt(t.length - 1);
							t = t.substring(0,t.length - 1)
						}
						t += "\n";
						tx += t;
						t = "";
					}
				}
				t += ch;
			}
			return "\n" + tx;
		}

		public static function infoNoOkay(message:String, title:String = "Information", closehandler:Function=null):Alert {
			var popup:Alert = show("\n\n" + formatText(message), spaces + title, 0, null, closehandler, iconInfo);
			return popup;
		}
		
		public static function info(message:String, title:String = "Information", closehandler:Function=null):Alert {
			var popup:Alert = show("\n\n" + formatText(message), spaces + title, Alert.OK, null, closehandler, iconInfo);
			return popup;
		}
		
		public static function errorNoOkay(message:String, title:String = "Error", parent:*=null, closehandler:Function=null):Alert {
			var popup:Alert = show("\n\n" + formatText(message), spaces + title, 0, parent, closehandler, iconError);
			return popup;
		}
		
		public static function error(message:String, title:String = "Error", closehandler:Function=null):Alert {
			var popup:Alert = show("\n\n" + formatText(message), spaces + title, Alert.OK, null, closehandler, iconError);
			return popup;
		}
		
		public static function confirm(message:String, title:String = "Confirmation", closehandler:Function=null, okLabel:String=null, cancelLabel:String=null):Alert {
			var isOkayUsed:Boolean = false;
			if ( (okLabel is String) && (okLabel.length > 0) ) {
				isOkayUsed = true;
				Alert.okLabel = okLabel;
			}
			var isCancelUsed:Boolean = false;
			if ( (cancelLabel is String) && (cancelLabel.length > 0) ) {
				isCancelUsed = true;
				Alert.cancelLabel = cancelLabel;
			}
			var popup:Alert = show("\n\n" + formatText(message), spaces + title, ((isOkayUsed) ? Alert.OK : Alert.YES) | ((isCancelUsed) ? Alert.CANCEL : Alert.NO), null, closehandler, iconConfirm);
			return popup;
		}

		public function AlertPopUp() {
			super();
		}
	}
}