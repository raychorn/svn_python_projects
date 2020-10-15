package vyperlogix.utils {
	import mx.collections.ArrayCollection;
	import mx.controls.Alert;
	import mx.rpc.events.*;
	import mx.rpc.http.mxml.HTTPService;
	import mx.utils.ArrayUtil;
	
	import vyperlogix.adobe.serialization.json.JSON;
	import vyperlogix.controls.Alert.AlertPopUp;
	
	public class EzHTTPService {
		public var srvc:HTTPService = new HTTPService;
		public var requestObj:Object = new Object;

		public var isDebugMode:Boolean = false;

		public var isRunningLocal:Boolean = true;
		
		public var userID:String = "";

		public const arrayResultType:String = "array";
		public const objectResultType:String = "object";
		public const xmlResultType:String = "xml";
		public const e4xResultType:String = "e4x";
		public const flashvarsResultType:String = "flashvars";
		public const textResultType:String = "text";

		public var allowedResultTypes:Array = [];
		
		public const jsonResultType:String = "json";
		public var specialResultTypes:Array = [];

		public const DEBUG_MODE_ON:Boolean = true;
		public const DEBUG_MODE_OFF:Boolean = false;
		
		public const RUNNING_LOCAL:Boolean = true;
		public const RUNNING_REMOTE:Boolean = false;

		public var alertShowFunc:Function;

		public var faultCallBack:Function;

		private var callback:Function;
		
		private var resultFormats:Array = [];

		public function makeIntoArrayCollection(obj:*):ArrayCollection {
			var ar:Array = new Array;
			if (obj != null) {
				if (obj is Array) {
					ar = obj;
				} else if (obj is ArrayCollection) {
					ar = obj.source;
				} else {
					ar = mx.utils.ArrayUtil.toArray(obj);
				}
			}
			return new ArrayCollection(ar);
		}
		
		public function makeEventResultIntoArrayCollection(event:ResultEvent):ArrayCollection {
			return makeIntoArrayCollection(event.result.source);
		}
		
		public function htmlForAspConversion(inStr:String = ""):String {
			var patLT:RegExp = /\</g;
			var patGT:RegExp = /\>/g;
			return inStr.replace(patLT,"&lt;").replace(patGT,"&gt;");
		}
		
		public function myCallback(event:*):void { // NOTE - event data type here is "*" to allow soft errors to be redirected into the incoming data stream...
			var ac:ArrayCollection = event.result as ArrayCollection;
			try {
				for (var i:int = 0; i < ac.length; i++) {
					ac.source[i] = JSON.decode(ac.source[i]);
				}
			} catch (err:Error) {} // ignore the errors from this - soft complaints all.
			this.callback(event);
		}

		public function onFaultHandler(event:FaultEvent):void {
			var reason:String = event.toString();
			AlertPopUp.errorNoOkay('Reason:\n\n'+reason,'WARNING');
		}
		
		private function myFaultCallback(event:FaultEvent):void {
			if (this.faultCallBack is Function) {
				this.faultCallBack(event);
			} else {
				this.onFaultHandler(event);
			}
		}
		
		public function EzHTTPService(_isDebugMode:Boolean = this.DEBUG_MODE_OFF, _isRunningLocal:Boolean = this.RUNNING_LOCAL):void {
			this.isDebugMode = _isDebugMode;
			this.isRunningLocal = _isRunningLocal;
			// BEGIN:  DO NOT PLACE A MIME TYPE HERE OR BAD EVIL THINGS CAN HAPPEN...
			//this.srvc.contentType = 'application/json';
			// END!    DO NOT PLACE A MIME TYPE HERE OR BAD EVIL THINGS CAN HAPPEN...
			this.srvc.addEventListener(ResultEvent.RESULT, this.myCallback);
			this.srvc.addEventListener(FaultEvent.FAULT, this.myFaultCallback);
			this.allowedResultTypes.push(this.arrayResultType);
			this.allowedResultTypes.push(this.objectResultType);
			this.allowedResultTypes.push(this.xmlResultType);
			this.allowedResultTypes.push(this.e4xResultType);
			this.allowedResultTypes.push(this.flashvarsResultType);
			this.allowedResultTypes.push(this.textResultType);
			this.specialResultTypes.push(this.jsonResultType);
		}
		
		private function invokeHTTPService(url:String, data:*, callback:Function, resultFormat:String = this.arrayResultType):void {
			var title:String = "";
			var msg:String = "";
			this.srvc.showBusyCursor = true;
			this.srvc.url = url;
			this.srvc.useProxy = false;
			try {
				this.srvc.resultFormat = resultFormat;
			} catch (e:Error) {
				this.srvc.resultFormat = 'array';
			}
			this.srvc.method = "POST";
			this.callback = callback;
			this.srvc.concurrency = "multiple"; // "multiple|single|last"
			this.srvc.makeObjectsBindable = true;
			this.srvc.request = this.requestObj;
			if (this.requestObj != null) {
				if (this.isDebugMode) {
					this.srvc.request.debugMode = "1";
				}
				if (this.isRunningLocal) {
					this.srvc.request.runningLocal = "1";
				}
				if ( (this.userID is String) && (this.userID.length > 0) ) {
					this.srvc.request.userid = this.userID;
				}
				try {
					for (var i:String in data) {
						this.srvc.request[i] = data[i];
					}
				} catch (err:Error) {}
			}
			try {
				this.srvc.send();
			} catch (err:Error) {
				title = "Error :: invokeHTTPService()";
				msg = err.toString();
				if (this.alertShowFunc is Function) {
					this.alertShowFunc(msg, title);
				} else {
					mx.controls.Alert.show(msg, title);
				}
			}
		}

		public function post(url:String, data:*, callback:Function, resultFormat:String = this.arrayResultType):void {
			var toks:Array = resultFormat.split('|');
			toks.forEach(function (element:*, index:int, arr:Array):void{ arr[index] = StringUtils.trim(element as String); });
			if (toks.indexOf(this.arrayResultType) == -1) {
				toks.push(this.arrayResultType);
			}
			this.resultFormats = toks;
			var toks2:ArrayCollection = new ArrayCollection();
			ArrayCollectionUtils.appendAllInto(toks2,toks);
			for (var i:int = toks2.length-1; i >= 0; i--) {
				if (this.allowedResultTypes.indexOf(toks2[i]) == -1) {
					toks2.removeItemAt(i);
				}
			}
			resultFormat = toks2.source.join('');
			this.invokeHTTPService(url, data, callback, resultFormat);
		}
		
		public function send(url:String, callback:Function, resultFormat:String = this.arrayResultType):void {
			return this.post(url,{},callback,resultFormat);
		}
	}
}