// ActionScript file
	private function callbackDetermineExecuteCodeCompletion(obj:Object):void {
		this.onCreationCompletePythonCode();
		this.pythonCode.htmlText += '<br><br>' + obj.item;
	}

	private function onCreationCompletePythonCode():void {
		this.pythonCode.htmlText = 'This is a Proof of Concept.<br>Click the button to find-out what Python version we used for our Python middle-tier.<br>Remember to launch the Python Server BEFORE you launch the AIR App.<br><br>You will know you have a functional AIR App when you see the "green" color in the Application bar otherwise "red" means the Python middle-tier is not running.';
	}

	private function onClickGetPythonVersionButton():void {
		var popup:Alert;
		if (this._commandsDictionary[this._const_execute_code_symbol] is String) {
			this._cacheCallbacks[this._const_execute_code_symbol] = {'obj':{'callBackFunc':this.callbackDetermineExecuteCodeCompletion},'methodName':'callBackFunc'};
			this.socketsManager.sendCommandToSocketWithArgs(this._commandsDictionary[this._const_execute_code_symbol],'sys.version');
		}
	}
	
	private function processDataFromSocket(data:Object):void {
		var i:int;
		var isCSV:Boolean = false;
		var isNumber:Boolean = false;
		var popup:Alert;
		var ac:ArrayCollection;
		var obj:Object;
		var fname:String;
		var current_target:*;
		var nodeType:String = 'UNKNOWN';
		var nodeName:String = 'UNKNOWN';
		var nodeValue:String = '';
		var fn:String;
		var children:Array;
		var aChild:Object;
		var aName:String;
		var oTarget:Object;
		var oFunc:Function;
		try {
			nodeType = data['type'];
			nodeName = data['name'];
			nodeValue = data['value'];
			children = data['children'] as Array;
			switch (nodeName) {
				case 'response':
					for (i = 0; i < children.length; i++) {
						aChild = children[i];
						this.processDataFromSocket(aChild);
					}
					break;
					
				case 'machineID':
					this._machineID = nodeValue;
					this.pushCommandOnQueue(this._handleMachineID);
					break;
					
				case 'LicenseLevels':
					ac = this.makeContentsIntoCollectionOfObjects(data);
					break;
					
				case 'license':
					// nodeValue has the value that cooresponds to the current LicenseLevel
					this.vbox01.enabled = true;
					break;
					
				case 'commands':
					var isListCompleteFromServer:Boolean = true;
					var namesFromServer:Array = [];
					for (i = 0; i < children.length; i++) {
						aChild = children[i];
						aName = aChild['name'];
						this._commandsDictionary[aName] = aChild['value'];
						if (this._list_of_expected_commands.indexOf(aName) == -1) {
							isListCompleteFromServer = false;
						}
						namesFromServer.push(aName);
					}
					
					if (isListCompleteFromServer == false) {
						popup = AlertPopUp.error("List of Commands from Server does not match the list of Commands the Client knows about.\n\nThis is a programming error that MUST be corrected.","PROGRAMMING ERROR");
						PopUpManager.centerPopUp(popup);
						popup.styleName = 'ErrorAlert';
						break;
					} else {
						var isListCompleteFromClient:Boolean = true;
						for (i = 0; i < this._list_of_expected_commands.length; i++) {
							aName = this._list_of_expected_commands[i];
							if (namesFromServer.indexOf(aName) == -1) {
									isListCompleteFromClient = false;
								break;	
							}
						}
						
						if (isListCompleteFromClient == false) {
							popup = AlertPopUp.error("List of Commands from Client does not match the list of Commands the Server knows about.\n\nThis is a programming error that MUST be corrected.","PROGRAMMING ERROR");
							PopUpManager.centerPopUp(popup);
							popup.styleName = 'ErrorAlert';
							break;
						}
					}
					
	 				// this._commandsDictionary is valid at this time...
					if (this._commandsDictionary['SHUTDOWN'] is uint) {
						this.onlineStatusIndicator.isConnected = false;
						this.onlineStatusIndicator.isOnline = false;
						this.socketsManager.terminateConnectionCommand = this._commandsDictionary['SHUTDOWN'];   
					}
					
					break;
	
	 			case 'list-head':
					if (this._current_target) {
						if (this._current_target is List) {
							var dp:ArrayCollection = ArrayCollection(List(this._current_target).dataProvider);
							if (dp) {
								dp.removeAll();
								List(this._current_target).toolTip = 'List is <u>empty</u>.';
							}
							ac = this.makeContentsIntoCollectionOfObjects(data);
						}
					}
					break;
	
	 			case 'list-item':
					if (this._current_target) {
						if (this._current_target is List) {
							ac = this.makeContentsIntoCollectionOfObjects(data);
							if (this._current_target.dataProvider == null) {
								this._current_target.dataProvider = new ArrayCollection();
	
								var sortA:Sort = new Sort();
								sortA.fields=[new SortField("item")];
								ArrayCollection(this._current_target.dataProvider).sort = sortA;
							}
							ArrayCollectionUtils.appendAllInto(this._current_target.dataProvider, ac);
							this._current_target.dataProvider.refresh();
							List(this._current_target).toolTip = '';
						}
					}
					break;
	
	 			case 'csv':
	 				isCSV = true;
	 			case 'list':
	 				try {
						ac = this.makeContentsIntoCollectionOfObjects(data,isCSV);
	 				} catch (err:Error) { ac = new ArrayCollection() }
					oTarget = this.findCachedCallbackForItem(nodeName);
					if (oTarget) {
						try {
							oFunc = oTarget.obj[oTarget.methodName];
							obj = {};
							obj.item = ac;
							obj.currentTarget = oTarget;
							oFunc(obj);
						} catch (err:Error) {
							popup = AlertPopUp.error(err.message,"CallBack ERROR in 'boolean' case for onDataReceived()");
							PopUpManager.centerPopUp(popup);
							popup.styleName = 'ErrorAlert';
						}
					} else {
						popup = AlertPopUp.error('Missing or invalid source for boolean that is "' + obj.source + '".',"Programming ERROR in 'boolean' case for onDataReceived()");
						PopUpManager.centerPopUp(popup);
						popup.styleName = 'ErrorAlert';
					}
					break;
	 
				case 'number':
					isNumber = true;
				case 'boolean':
					ac = this.makeContentsIntoCollectionOfObjects(data,isCSV);
					obj = this.collapseCollectionOfObjectsIntoSingleObject(ac);
					oTarget = this.findCachedCallbackForItem(obj.source);
					if (oTarget) {
						try {
							oFunc = oTarget.obj[oTarget.methodName];
							obj.item = ((isNumber) ? Number(obj.item) : ((obj.item.toLowerCase() == 'true') ? true : false));
							obj.currentTarget = oTarget;
							oFunc(obj);
						} catch (err:Error) {
							popup = AlertPopUp.error(err.message,"CallBack ERROR in 'boolean' case for onDataReceived()");
							PopUpManager.centerPopUp(popup);
							popup.styleName = 'ErrorAlert';
						}
					} else {
						popup = AlertPopUp.error('Missing or invalid source for boolean that is "' + obj.source + '".',"Programming ERROR in 'boolean' case for onDataReceived()");
						PopUpManager.centerPopUp(popup);
						popup.styleName = 'ErrorAlert';
					}
					break;
	
				case 'string':
					ac = this.makeContentsIntoCollectionOfObjects(data,isCSV);
					obj = this.collapseCollectionOfObjectsIntoSingleObject(ac);
					oTarget = this.findCachedCallbackForItem(obj.source);
					if (oTarget) {
						try {
							oFunc = oTarget.obj[oTarget.methodName];
							obj.currentTarget = oTarget;
							oFunc(obj);
						} catch (err:Error) {
							popup = AlertPopUp.error(err.message,"CallBack ERROR in 'string' case for onDataReceived()");
							PopUpManager.centerPopUp(popup);
							popup.styleName = 'ErrorAlert';
						}
					} else {
						popup = AlertPopUp.error('Missing or invalid source for string that is "' + obj.source + '".',"Programming ERROR in 'string' case for onDataReceived()");
						PopUpManager.centerPopUp(popup);
						popup.styleName = 'ErrorAlert';
					}
					break;
	
				case 'null':
					break;
					
				case 'error':
					this.handleErrorFromSocket();
					var errorTitle:String = 'APPLICATION ERROR';
					XMLObjectUtils.flattenChildrenIntoNodeValue(data);
					if (data['value'] is Array) {
						var _ar:Array = data['value'];
						errorTitle = StringUtils.replaceAll(_ar[0],'<br>', '\n');
						nodeValue = StringUtils.replaceAll(_ar[_ar.length-1],'<br>', '\n');
					} else {
						nodeValue = data['value'];
						nodeValue = StringUtils.replaceAll(nodeValue,'<br>', '\n');
					}
					popup = AlertPopUp.error(nodeValue,errorTitle);
					PopUpManager.centerPopUp(popup);
					popup.styleName = 'ErrorAlert';
					break;
	
				default:
					popup = AlertPopUp.info(this.dataToString(data,true) + "\n\n(" + nodeType + ")","Unknown Response");
					PopUpManager.centerPopUp(popup);
					popup.styleName = 'InfoAlert';
					break;
			}
		} catch (err:Error) {
			popup = AlertPopUp.error("Report this error to the Technical Support folks.\n\n(" + nodeType + ")\n\n" + err.message,"Application Error");
			PopUpManager.centerPopUp(popup);
			popup.styleName = 'ErrorAlert';
		}
	}
	
