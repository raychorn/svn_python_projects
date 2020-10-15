/* Sample usage:

private function cookies_complete():void {
	AlertPopUp.infoNoOkay(CookieUtils.cookieStr,'DEBUG: Cookies.');
}

private function onCreationComplete():void {
    menuBarCollection = new XMLListCollection(menubarXML);
    ToolTipManager.toolTipClass = HTMLToolTip;
    
    CookieUtils.debugger = this.debugger;
    CookieUtils.wait_for_browser_cookies(this.cookies_complete);
}
 */
package vyperlogix.utils {
	import flash.events.TimerEvent;
	import flash.external.ExternalInterface;
	import flash.utils.Timer;
	
	import mx.controls.TextArea;
	
	public class CookieUtils {
		public static var cookieStr:String;

		public static var debugger:TextArea = new TextArea();

		private static var callback:Function;

		public static function wait_for_browser_cookies(callback:Function):void {
			var i:Number = 1;
			var timer:Timer = new Timer(250);
			timer.addEventListener(TimerEvent.TIMER,function (event:TimerEvent):void{
				var t:Timer;
				var isReady:Boolean;
				isReady = ExternalInterface.call('isReady');
				debugger.text = '(' + i + ') :: isReady=' + isReady + '\n' + debugger.text 
				if (isReady) {
					CookieUtils.cookieStr = ExternalInterface.call('get_cookies');
					debugger.text = '(' + i + ') :: CookieUtils.cookieStr=' + CookieUtils.cookieStr + '\n' + debugger.text 
					t = event.currentTarget as Timer;
					t.stop();
					if (callback is Function) {
						callback();
					}
				}
				i += 1;
			});
			timer.start();
		}
	}
}