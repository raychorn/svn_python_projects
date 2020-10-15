// ActionScript file
// ActionScript file
	import com.HAL.Alert.AlertPopUp;
	import com.HAL.controls.HtmlToolTip;
	import com.HAL.controls.events.*;
	import com.HAL.sockets.events.*;
	import com.HAL.utils.ArrayCollectionUtils;
	import com.HAL.utils.Misc;
	import com.HAL.utils.StringUtils;
	import com.HAL.utils.XMLObjectUtils;
	
	import flash.system.Capabilities;
	
	import mx.collections.ArrayCollection;
	import mx.collections.Sort;
	import mx.collections.SortField;
	import mx.collections.XMLListCollection;
	import mx.containers.HBox;
	import mx.containers.TitleWindow;
	import mx.containers.ViewStack;
	import mx.controls.Alert;
	import mx.controls.List;
	import mx.events.*;
	import mx.managers.PopUpManager;
	import mx.managers.ToolTipManager;
	import mx.styles.CSSStyleDeclaration;
	import mx.styles.StyleManager;
	
	private var _current_target:*;
		
	private var _menuBarCollection:XMLListCollection;
	
	private var _commandsDictionary:Object = {};
	
	private var _expectedViewStackIndex:int = -1;
	
	private var _toolTipCache:Object = {};
	
	private var _cacheCallbacks:Object = {};
				
	private var _queue:ArrayCollection;

	private var _queueContents:Array = [];
	
	private var _machineID:String = '';
	
	private function _handleMachineID():void {
		this.handleMachineID();
	}
	
	private function _onInitialize():void {
		this.onInitialize();
	}
	
	private function onInit():void {
		ToolTipManager.toolTipClass = HtmlToolTip;
		this.maxWidth = flash.system.Capabilities.screenResolutionX;
		this.maxHeight = flash.system.Capabilities.screenResolutionY;
		this.initMenuBar();
		this.socketsManager.onlineStatusCanvas = this.onlineStatusIndicator;
		this._queue = new ArrayCollection(this._queueContents);
		
		Misc.systemManager = this.systemManager;
	}
	
	private function onOnlineStatusChanged(event:OnlineStatusChangedEvent):void {
		var cssDecl:CSSStyleDeclaration = StyleManager.getStyleDeclaration('ApplicationControlBar');
		var fillColors:Array = cssDecl.getStyle('fillColors');
		var fillAlphas:Array = cssDecl.getStyle('fillAlphas');
		fillAlphas[0]= fillAlphas[1] = event.alpha;
		fillColors[0] = event.color;
		cssDecl.setStyle('fillColors', fillColors);
		cssDecl.setStyle('fillAlphas', fillAlphas);
	}
				
	private function onCreationCompleteOnlineStatusCanvas():void {
		this.onlineStatusIndicator.addEventListener(OnlineStatusChangedEvent.TYPE_ONLINE_STATUS_CHANGED, onOnlineStatusChanged);
	}
				
	private function initMenuBar():void {
		this._menuBarCollection = new XMLListCollection(this.menubarXML);
	}
	
	private function onClosing():void {
		this.socketsManager.onClosing();
	}
				
	private function onCloseConnectionTimeoutErrorDialog(event:CloseEvent):void {
		if (event.detail == Alert.OK) {
			this.exit();
		}
	}
				
	private function onConnectionTimeout(event:ConnectionTimeoutEvent):void {
		var popup:Alert = AlertPopUp.error("Unable to start this application at this time.\n\nThis Application was not designed to be launched\nfrom the Installer.\n\nTry clicking on one of the application shortcuts\nto launch this application.\n\n","Application Start-up ERROR Recovery Notice", onCloseConnectionTimeoutErrorDialog);
		PopUpManager.centerPopUp(popup);
		popup.defaultButton['enabled'] = true;
		popup.styleName = 'ErrorAlert';
	}
				
	public function get menuBarCollection():XMLListCollection {
		if (this._menuBarCollection == null) {
			this.initMenuBar(); 
		}
		return this._menuBarCollection;
	}
				
	public function commandNameID(name:String):uint {
		return this._commandsDictionary[name];
	}
				
	public function commandNameByID(id:String):String {
		var sel:String;
		for (sel in this._commandsDictionary) {
			if (this._commandsDictionary[sel] == id) {
				return sel;
			}
		}
		return '';
	}
				
	private function executeCommandFromQueue():void {
		var popup:Alert;
		var aFunc:Function;
		if (this._queue.length > 0) {
			aFunc = this._queue.removeItemAt(0) as Function;
			if (aFunc is Function) {
				try {
					aFunc();
				} catch (err:Error) {
					popup = AlertPopUp.info(err.message,"ERROR while executing command from queue.");
					PopUpManager.centerPopUp(popup);
					popup.styleName = 'ErrorAlert';
				}
			}
		}
	}
	
	private function pushCommandOnQueue(aCommand:Function):void {
		var popup:Alert;
		if (aCommand is Function) {
			this._queue.addItem(aCommand);
		} else {
			popup = AlertPopUp.info('Cannot push an item onto the Command Queue that is not a pointer to a Function.',"Programmign ERROR");
			PopUpManager.centerPopUp(popup);
			popup.styleName = 'ErrorAlert';
		}
	}

	include 'processDataFromSocket.as';
	
	private function onDataReceived(event:DataReceivedEvent):void {
		this.processDataFromSocket(event.data);
		this.onlineStatusIndicator.isOnline = true;
		this.enabled = true;	// handle the scenario where we disabled the GUI while the server is busy...
		this.executeCommandFromQueue();
	}
				
	private function onConnectionEstablished(event:ConnectionEstablishedEvent):void {
		this.onlineStatusIndicator.isConnected = true;
	}
				
	private function onIOErrorHandled(event:IOErrorHandledEvent):void {
		this.onlineStatusIndicator.isOnline = false;
	}
				
				
	private function onConnectionClosed(event:ConnectionClosedEvent):void {
		this.onlineStatusIndicator.isConnected = false;
	}
				
	private function onConnectionRetry(event:ConnectionRetryEvent):void {
		this.onlineStatusIndicator.isConnected = false;
		this.onlineStatusIndicator.toolTip = 'Retrying the Connection.';
	}
				
	private function onCreationCompleteSocketsManager():void {
		this.socketsManager.addEventListener(ConnectionTimeoutEvent.TYPE_CONNECTION_TIMEOUT, onConnectionTimeout);
		this.socketsManager.addEventListener(DataReceivedEvent.TYPE_DATA_RECEIVED, onDataReceived);
		this.socketsManager.addEventListener(ConnectionEstablishedEvent.TYPE_CONNECTION_ESTABLISHED, onConnectionEstablished);
		this.socketsManager.addEventListener(IOErrorHandledEvent.TYPE_IOERROR_HANDLED, onIOErrorHandled);
		this.socketsManager.addEventListener(ConnectionClosedEvent.TYPE_CONNECTION_CLOSED, onConnectionClosed);
		this.socketsManager.addEventListener(ConnectionRetryEvent.TYPE_CONNECTION_RETRY, onConnectionRetry);
	}
				
	private function getChildrenForArbitraryDisplayObject(dispObj:*):Array {
		if (dispObj is HBox) {
			var hb:HBox = HBox(dispObj);
			return hb.getChildren();
		} else if (dispObj is VBox) {
			var vb:VBox = VBox(dispObj);
			return vb.getChildren();
		} else if (dispObj is Canvas) {
			var c:Canvas = Canvas(dispObj);
			return c.getChildren();
		} else if (dispObj is ViewStack) {
			var v:ViewStack = ViewStack(dispObj);
			return v.getChildren();
		} else if (dispObj is TitleWindow) {
			var t:TitleWindow = TitleWindow(dispObj);
			return t.getChildren();
		} else {
			try {
				return dispObj.getChildren();
			} catch (err:Error) { }
			return []; 
		}
	}
				
	private function gatherChildrenIncludingAllGrandChildrenFor(dispObj:*):Array {
		var children:Array = this.getChildrenForArbitraryDisplayObject(dispObj);
		var ea:*;
		var i:*;
		var kids:Array = [];
		for (ea in children) {
			var _kids:Array = this.gatherChildrenIncludingAllGrandChildrenFor(children[ea]);
			for (i in _kids) {
				kids.push(_kids[i]);
			}
			kids.push(children[ea]);
		}
		return kids;
	}
				
	private function locateArbitraryDisplayObjectBasedOn(dispObj:*,func:Function,collection:Array,exclusions:Array):void {
		var children:Array = this.gatherChildrenIncludingAllGrandChildrenFor(dispObj);
		if (children) {
			var i:int;
			for (i = 0; i < children.length; i++) {
				var doesObjectMatchCriteria:Boolean = true;
				if (func is Function) {
					try {
						doesObjectMatchCriteria = func(children[i]); 
					} catch (err:Error) { }
				}
				if (doesObjectMatchCriteria) {
					if (collection) {
						var isAllowed:Boolean = true;
						if (exclusions) {
							isAllowed = (exclusions.indexOf(children[i]) == -1);
						}
						if ( (isAllowed) && (collection.indexOf(children[i]) == -1) ) {
							collection.push(children[i]);
						}
					}
				}
			}
		}
		
		if ( (dispObj is WindowedApplication) || (dispObj.parent == null) ) {
			return;
		}
		
		return this.locateArbitraryDisplayObjectBasedOn(dispObj.parent,func,collection,exclusions);
	}
				
	private function onItemClickMenuBar(event:MenuEvent):void {
		var i:int;
		var j:int;
		var packageObj:Object;
		var archObj:Object;
		var popUp:Alert;
		var data:String = event.item.@data;
		if (data != "top") {
			this.handleMenuBar(event.item.@data);
		}        
	}

	private function onExecPython(event:ExecPythonEvent):void {
		this._cacheCallbacks[event.args[0]] = event;
		this.socketsManager.sendCommandToSocketWithArgs(event.pythonCommand,event.args);
	}

	private function _refreshMenuBarMenu():void {
		var menu:XMLListCollection = XMLListCollection(this.menuBar.dataProvider);
		var i:int;
		for (i = 0; i < menu.length; i++) {
			this.refreshMenuBarMenu(XML(menu[i]).children());
		}
	}
				
	private function onCreationCompleteAppMenuBar():void {
		this._refreshMenuBarMenu();
	}
				
	private function getProperParentFrom(obj:*,func:Function):* {
		var pObj:*;
		if (func is Function) {
			try {
				if (func(obj)) {
					return obj;
				} else {
					pObj = this.getProperParentFrom(obj.parent,func);
				}
			} catch (err:Error) { }
		}
		return pObj;
	}
				
