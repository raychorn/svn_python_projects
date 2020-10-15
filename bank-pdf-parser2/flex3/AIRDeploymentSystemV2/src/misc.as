// ActionScript file
	import com.HAL.Alert.AlertPopUp;
	import com.HAL.controls.HtmlToolTip;
	import com.HAL.controls.ListGridCanvas;
	import com.HAL.controls.events.*;
	import com.HAL.controls.navigators.events.*;
	import com.HAL.sockets.events.*;
	import com.HAL.utils.ArrayCollectionUtils;
	import com.HAL.utils.ArrayUtils;
	import com.HAL.utils.FileListUtils;
	import com.HAL.utils.FileUtils;
	import com.HAL.utils.LicenseUtils;
	import com.HAL.utils.Misc;
	import com.HAL.utils.StringUtils;
	import com.HAL.utils.XMLObjectUtils;
	import com.HAL.views.PackageContentsView;
	import com.HAL.views.PackagesView;
	import com.HAL.views.events.ArchiveBuilderAcceptedEvent;
	import com.HAL.views.events.ArchiveBuilderCheckArchiveNameEvent;
	import com.HAL.views.events.PackageBuilderAcceptedEvent;
	import com.HAL.views.events.PackageBuilderCancelledEvent;
	import com.HAL.views.events.PackageBuilderCheckPackageNameEvent;
	
	import flash.events.MouseEvent;
	import flash.filesystem.File;
	import flash.system.Capabilities;
	import flash.ui.ContextMenu;
	import flash.ui.ContextMenuItem;
	
	import mx.collections.ArrayCollection;
	import mx.collections.Sort;
	import mx.collections.SortField;
	import mx.collections.XMLListCollection;
	import mx.containers.HBox;
	import mx.containers.HDividedBox;
	import mx.containers.TitleWindow;
	import mx.containers.ViewStack;
	import mx.controls.Alert;
	import mx.controls.Button;
	import mx.controls.List;
	import mx.events.*;
	import mx.managers.PopUpManager;
	import mx.managers.ToolTipManager;
	import mx.styles.CSSStyleDeclaration;
	import mx.styles.StyleManager;
	
//	include 'imports.as';
	
	[Bindable]
	private var _building_package:*;
	
	[Bindable]
	private var _building_archive:*;
	
	[Bindable]
	private var _current_target:*;
	
	[Bindable]
	private var _current_folder:String;
	
	[Bindable]
	private var _original_current_folder:String;
	
	[Bindable]
	private var _current_action:String;
	
	[Bindable]
	private var _current_action2:String;
	
	[Bindable]
	private var _packagesView:PackagesView;
	
	[Bindable]
	private var _packageContentsView:PackageContentsView;
	
	private var _current_archive_name:String = '';
	private var _current_package_name:String = '';
	
	private var _menuBarCollection:XMLListCollection;
	
	private var _commandsDictionary:Object = {};
	
	private var _queueContents:Array = [onClickListArchivesButton];
	
	private var _queue:ArrayCollection;
	
	private var _expectedViewStackIndex:int = -1;
	
	private var _toolTipCache:Object = {};
	
	private var _baseState:String = '';
	
	private var _cacheCallbacks:Object = {};
				
	[Bindable]
	private var _runtimeVersion:String;
	
	[Bindable]
	private var menubarXML:XMLList =
	    <>
	        <menuitem label="Archive File Menu" data="top">
	            <menuitem label="Find Archives" data="findArchives"/>
	            <menuitem type="separator"/>
	            <menuitem label="Create" data="createArchive" enabled="true"/>
	        </menuitem>
	        <menuitem label="Package File Menu" data="top" enabled="true">
	            <menuitem label="Export" data="exportPackage" enabled="false"/>
	            <menuitem type="separator"/>
	            <menuitem label="Create" data="createPackage" enabled="true"/>
	        </menuitem>
	        <menuitem label="Help" data="top">
	            <menuitem label="About" data="aboutInfo"/>
	            <menuitem type="separator"/>
	            <menuitem label="About {LicenseUtils.licenseLevel}" data="aboutLicense"/>
	        </menuitem>
	    </>;
	    
	/*  These menu items are no longer being used... Handled by other functions.
	            <menuitem type="separator"/>
	            <menuitem label="Add" data="addPackage" enabled="true"/>
	            <menuitem type="separator"/>
	            <menuitem label="Remove" data="removePackage" enabled="false"/>
	*/

	public const _const_list_archives_symbol:String = 'list_archives'; 
	public const _const_open_archive_symbol:String = 'open_archive'; 
	public const _const_open_package_symbol:String = 'open_package';
	public const _const_shutdown_symbol:String = 'SHUTDOWN';
	public const _const_export_package_from_archive_symbol:String = 'export_package_from'; 
	public const _const_check_package_name_symbol:String = 'check_package_name'; 
	public const _const_build_package_symbol:String = 'build_package';
	public const _const_count_archives_symbol:String = 'count_archives';
	public const _const_build_archive_symbol:String = 'build_archive';
	public const _const_check_archive_name_symbol:String = 'check_archive_name'; 
	public const _const_remove_package_from_symbol:String = 'remove_package_from'; 
	
	[Embed(source='assets/fonts/NeoSansIntel-Light.ttf', fontName='NeoSansIntel', mimeType='application/x-font')] 
	private var primaryFont:Class;
	
	private var _list_of_expected_commands:Array = [_const_list_archives_symbol, _const_open_archive_symbol, _const_open_package_symbol, _const_shutdown_symbol, _const_export_package_from_archive_symbol, _const_check_package_name_symbol,_const_build_package_symbol,_const_count_archives_symbol,_const_check_package_name_symbol,_const_build_archive_symbol,_const_check_archive_name_symbol,_const_remove_package_from_symbol]; 
	  
	private function onInit():void {
		ToolTipManager.toolTipClass = HtmlToolTip;
		this.maxWidth = flash.system.Capabilities.screenResolutionX;
		this.maxHeight = flash.system.Capabilities.screenResolutionY;
		this.initMenuBar();
		this.socketsManager.onlineStatusCanvas = this.onlineStatusIndicator;
		this._queue = new ArrayCollection(this._queueContents);
		this.addEventListener(StateChangeEvent.CURRENT_STATE_CHANGE, onStateChange);
		
		Misc.systemManager = this.systemManager;
	}
	
	public function set baseState(baseState:String):void {
		this._baseState = baseState;
	}
	
	public function get baseState():String {
		return this._baseState;
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
				
	private function showHideDividerAt(index:int, isVisible:Boolean):void {
		try {
			var div:* = this.hdiv01.getDividerAt(index);
			div.visible = isVisible;
		} catch (err:Error) {
		}
	}
				
	private function onChildAddHDividedBox1(event:ChildExistenceChangedEvent):void {
	}
	
	private function activateArchiveSelected():void {
		var children:Array = this.hdiv01.getChildren();
		if (this._packagesView == null) {
			var hbox:PackagesView = new PackagesView();
			hbox.id = 'hbox_list2';
			hbox.width = 215;
			hbox.minWidth = 215;
			hbox.percentHeight = 100;
			hbox.visible = false;
			this.hdiv01.addChildAt(hbox,children.length);
			this._packagesView = hbox;
			this._packagesView.btn_ArchiveContentsGridToggle.addEventListener(MouseEvent.CLICK, onClickGridToggleButton);
			this._packagesView.addEventListener(FlexEvent.CREATION_COMPLETE, onCreationCompleteListGridCanvas);
	//		this.viewStack1.width += 215;
			this.viewStack1.width += 250;
		}
	
		children = this.hdiv01.getChildren();
		if (this._packageContentsView == null) {
			var hbox2:PackageContentsView = new PackageContentsView();
			hbox2.id = 'hbox_list3';
			hbox2.width = 215;
			hbox2.minWidth = 215;
			hbox2.percentHeight = 100;
			hbox2.visible = false;
			this.hdiv01.addChildAt(hbox2,children.length);
			this._packageContentsView = hbox2;
			this._packageContentsView.btn_ArchivePkgContentsGridToggle.addEventListener(MouseEvent.CLICK, onClickGridToggleButton);
			this._packageContentsView.listGridCanvasPkgContents.addEventListener(FlexEvent.CREATION_COMPLETE, onCreationCompleteListGridCanvas);
			this.viewStack1.width += 215;
		}
	}
				
	private function onChildRemoveHDividedBox1(event:ChildExistenceChangedEvent):void {
		if (event.relatedObject['id'] == 'logoSWF') {
			this.activateArchiveSelected();
		}
	}
				
	private function onCreationCompleteHDividedBox1():void {
		this.showHideDividerAt(1,false);
	}
	
	private function refreshArchivesPackagesList(pathName:String):void {
		this._current_target = this.list_Archives;
		this.socketsManager.sendCommandToSocketWithArgs(this.commandNameID(this._const_list_archives_symbol),pathName);
	}
	
	private function onClosedConfirmationFolderNavigatorHomeFolderChanged(event:CloseEvent):void {
		if (event.detail == Alert.YES) {
			this._current_folder = this.folderNavigator.fileList.directory.nativePath;
			this.refreshArchivesPackagesList(this._current_folder);
			this.folderNavigator.homePath = this._current_folder;
		} else {
			this.folderNavigator.homePath = this._original_current_folder;
			this.refreshArchivesPackagesList(this._original_current_folder);
		}
	}
	
	private function onStateChange(event:StateChangeEvent):void {
		if (event.newState == 'FolderNavigatorState') {
			this._original_current_folder = this._current_folder;
		}
	}
	
	private function onFolderNavigatorClosed(event:FolderNavigatorClosedEvent):void {
		if ( (this.folderNavigator) && (this._original_current_folder != this.folderNavigator.fileList.directory.nativePath) ) {
			var popUp:Alert = AlertPopUp.confirm('Are you sure you want to make the "' + this.folderNavigator.fileList.directory.nativePath + '" folder the home folder ?', "Confirm", onClosedConfirmationFolderNavigatorHomeFolderChanged);
			popUp.styleName = 'ConfirmAlert';
		} else {
			this.refreshArchivesPackagesList(this._current_folder);
		}
	}
	
	private function callbackCountArchives(obj:Object):void {
		if (this._current_target is List) {
			var ac:ArrayCollection;
			var listWidget:List = List(this._current_target);
			if (obj['source'] == this._const_count_archives_symbol) {
				if (listWidget.dataProvider == null) {
					ac = new ArrayCollection();
					listWidget.dataProvider = ac;
				} else {
					ac = ArrayCollection(listWidget.dataProvider);
				}
				var target:Object = obj['currentTarget'];
				var newPath:String = target['newPath'];
				var detail:String = Number(obj['item']).toString() + ' Archives/Packages';
				var data:String = detail + ' Available';
				var o:Object = {};
				o[listWidget.labelField] = data;
				o['fname'] = data;
				ac.addItem(o);
				listWidget.toolTip = 'There are ' + data + ' in the currently selected folder "' + newPath + '".<br><br>Click the blue file cabinet button (to the right of the label that says "Archives and Packages") to close the Folder Brower and choose the currently selected folder as your Home Folder to make these ' + detail + ' able to be inspected and managed.';
			}
		}
	}
	
	private function onFolderNavigatorChanged(event:FolderNavigatorChangedEvent):void {
		if (event.newPath.toLowerCase().indexOf('root$:') == -1) {
			this._current_target = this.list_Archives;
			this._cacheCallbacks[this._const_count_archives_symbol] = {'obj':{'callBackFunc':this.callbackCountArchives},'methodName':'callBackFunc','newPath':event.newPath};
			this.socketsManager.sendCommandToSocketWithArgs(this.commandNameID(this._const_count_archives_symbol),event.newPath);
		}
		this.archivesFolderNavigator.proposedHomeFolder = ((this._current_folder != this.folderNavigator.fileList.directory.nativePath) ? event.newPath : '');
	}

	private function abstractCheckArchivePackageName(obj:Object):void {
		var currentTarget:Object = obj.currentTarget;
		var oCallback:Function = currentTarget.callback;
		oCallback(obj.item);
	}
	
	private function callbackCheckPackageName(obj:Object):void {
		this.abstractCheckArchivePackageName(obj);
	}

	private function callbackCheckArchiveName(obj:Object):void {
		this.abstractCheckArchivePackageName(obj);
	}

	private function onPackageBuilderCheckPackageName(event:PackageBuilderCheckPackageNameEvent):void {
		this._cacheCallbacks[event.fileName] = {'obj':{'callBackFunc':this.callbackCheckPackageName},'methodName':'callBackFunc','callback':event.callback};
		this.socketsManager.sendCommandToSocketWithArgs(this.commandNameID(this._const_check_package_name_symbol),event.fileName);
	}
	
	private function onArchiveBuilderCheckArchiveName(event:ArchiveBuilderCheckArchiveNameEvent):void {
		this._cacheCallbacks[event.fileName] = {'obj':{'callBackFunc':this.callbackCheckArchiveName},'methodName':'callBackFunc','callback':event.callback};
		this.socketsManager.sendCommandToSocketWithArgs(this.commandNameID(this._const_check_archive_name_symbol),event.fileName);
	}

	private function onCreationCompleteFolderNavigatorButton():void {
		this.archivesFolderNavigator.addEventListener(FolderNavigatorClosedEvent.TYPE_FOLDER_NAVIGATOR_CLOSED, onFolderNavigatorClosed);
		this.addEventListener(FolderNavigatorChangedEvent.TYPE_FOLDER_NAVIGATOR_CHANGED, onFolderNavigatorChanged);
	}
	
	private function onCreationCompleteFolderNavigatorCanvas():void {
		this.folderNavigator.homePath = this._current_folder;
	//	this.folderNavigator.addEventListener(FolderNavigatorChangedEvent.TYPE_FOLDER_NAVIGATOR_CHANGED, onFolderNavigatorChanged);
	}
				
	private function fileListContextMenu():ContextMenu {
		var item:ContextMenuItem = new ContextMenuItem('1');
		var menu:ContextMenu = new ContextMenu();
		menu.addItem(item);
		return menu;
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
		var popup:Alert = AlertPopUp.error("Unable to start this application at this time.\n\nThis Application was not designed to be launched\nfrom the Installer.\n\nTry clicking on one of the application shortcuts\nto launch this application.\n\nYou may be able to get\nTechnical Support at http://www.sexyblondessoftware.com.\n\nClose this instance of the Application\nand re-launch to begin using this Application.","Application Start-up ERROR Recovery Notice", onCloseConnectionTimeoutErrorDialog);
		PopUpManager.centerPopUp(popup);
		popup.defaultButton['enabled'] = true;
		popup.styleName = 'ErrorAlert';
	}
				
	private function updateCanvasLabel():void {
		if (this.canvas01) {
			var toks:Array = this.canvas01.label.split(' ');
			toks.pop();
			toks.push('(' + this.current_archive_name + '::' + this.current_package_name + ')');
			this.canvas01.label = toks.join(' ');
		}
	}
				
	public function get menuBarCollection():XMLListCollection {
		if (this._menuBarCollection == null) {
			this.initMenuBar(); 
		}
		return this._menuBarCollection;
	}
				
	public function set current_archive_name(name:String):void {
		this._current_archive_name = name;
		this.updateCanvasLabel();
	}
				
	[Bindable]
	public function get current_archive_name():String {
		return ((this._current_archive_name.length > 0) ? this._current_archive_name : 'NO_SELECTION');
	}
				
	public function set current_package_name(name:String):void {
		this._current_package_name = name;
		this.updateCanvasLabel();
	}
				
	[Bindable]
	public function get current_package_name():String {
		return ((this._current_package_name.length > 0) ? this._current_package_name : 'NO_SELECTION');
	}
	
	private function dataToString(data:*,isCSV:Boolean=false):String {
		var i:int;
		var s:String = '';
		if (data is ArrayCollection) {
			for (i = 0; i < data.length; i++) {
				s += data.getItemAt(i);
				if ( (isCSV) && (i < (data.length-1)) ) {
					s += ',';
				}
			}
		} else if (data is Object) {
			s += '{'
			var list:Array = [];
			for (var name:String in data) {
				if (name != 'children') {
					list.push(name + '=' + data[name]);
				}
			}
			s += list.join(',');
			s += ',';
			s += 'children=[';
			try {
				var children:Array = data['children'];
				for (i = 0; i < children.length; i++) {
					s += this.dataToString(children[i],isCSV);
				}
			} catch (err:Error) { }
			s += ']}\n'
		}
		return s;
	}
				
	private function makeContentsIntoCollectionOfObjects(data:Object,isCSV:Boolean=false):ArrayCollection {
		var i:int;
		var obj:Object;
		var ac:ArrayCollection = new ArrayCollection();
		var children:Array = data['children'];
		var aChild:Object;
		if (isCSV) {
			aChild = children[0];
			var values:Array;
			var names:Array = aChild['value'].split(',');
			ArrayUtils.trimAll(names);
			for (i = 1; i < children.length; i++) {
				aChild = children[i];
				obj = {};
				values = aChild['value'].split(',');
				for (var j:int = 0; j < values.length; j++) {
					obj[names[j]] = values[j];
				}
				ac.addItem(obj);
			}
		} else {
			for (i = 0; i < children.length; i++) {
				aChild = children[i];
				obj = {};
				obj[aChild['name']] = aChild['value'];
				ac.addItem(obj);
			}
		}
		return ac;
	}
				
	private function collapseCollectionOfObjectsIntoSingleObject(source:ArrayCollection):Object {
		var i:int;
		var obj:Object = {};
		var o:Object;
		for (i = 0; i < source.length; i++) {
			o = source.getItemAt(i);
			for (var n:* in o) {
				obj[n] = o[n];
			}
		}
		return obj;
	}
				
	private function collapseObjectIntoCSV(source:Object):Array {
		var val:Array = [];
		var selector:String;
		if (source) {
			for (selector in source) {
				val.push(selector);
				val.push(source[selector]);
			}
		}
		return val;
	}
				
	private function findCachedCallbackForItem(item:String):Object {
		for (var n:String in this._cacheCallbacks) {
			var pItem:String = ArrayUtils.pruneEmptyItems(item.split(File.separator)).join(File.separator);
			var pN:String = ArrayUtils.pruneEmptyItems(n.split(File.separator)).join(File.separator);
			if (pN == pItem) {
				return this._cacheCallbacks[n];
			}
		}
		return null;
	}
				
	public function commandNameID(name:String):uint {
		return this._commandsDictionary[name];
	}
				
	private function labelForArchiveList(obj:Object):String {
		var label:String = String(obj[this.list_Archives.labelField]);
		var fname:String = String(obj.fname);
		var toks:Array = label.split(File.separator);
		var fName:String = toks.pop();
		var fPath:String = toks.join(File.separator); 
		if (obj['path'] != fPath) {
			obj['path'] = fPath;
		}
		return '.'+fname;
	}
	
	private function executeCommandFromQueue():void {
		var aFunc:Function;
		if (this._queue.length > 0) {
			aFunc = this._queue.removeItemAt(0) as Function;
			if (aFunc is Function) {
				try {
					aFunc();
				} catch (err:Error) { }
			}
		}
	}
				
	private function onDataReceived(event:DataReceivedEvent):void {
		var i:int;
		var isCSV:Boolean = false;
		var isNumber:Boolean = false;
		var popup:Alert;
		var ac:ArrayCollection;
		var obj:Object;
		var fname:String;
		var current_target:ListGridCanvas;
		var nodeType:String = 'UNKNOWN';
		var nodeName:String = 'UNKNOWN';
		var nodeValue:String = '';
		var fn:String;
		try {
			nodeType = event.data['type'];
			nodeName = event.data['name'];
			nodeValue = event.data['value'];
			switch (nodeName) {
				case 'commands':
					var aChild:Object;
					var aName:String;
					var children:Array = event.data['children'] as Array;
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
					
					this.executeCommandFromQueue();
					break;
	
	 			case 'list-head':
					if (this._current_target) {
						if (this._current_target is List) {
							var dp:ArrayCollection = ArrayCollection(List(this._current_target).dataProvider);
							if (dp) {
								dp.removeAll();
								List(this._current_target).toolTip = 'List is <u>empty</u>.';
							}
							ac = this.makeContentsIntoCollectionOfObjects(event.data);
							if (this._current_target.id == this.list_Archives.id) {
								obj = ac.getItemAt(0);
								fn = String(obj[this.list_Archives.labelField]);
								if (new File(fn).isDirectory) {
									this._current_folder = fn.toLowerCase();
								}
							}
						}
					}
					break;
	
	 			case 'list-item':
					if (this._current_target) {
						if (this._current_target is List) {
							ac = this.makeContentsIntoCollectionOfObjects(event.data);
							if (this._current_target.id == this.list_Archives.id) {
								for (i = 0; i < ac.length; i++) {
									obj = ac.getItemAt(i);
									var s:String = String(obj[this.list_Archives.labelField]);
									fname = StringUtils.replaceCaseless(s,((this._current_folder) ? this._current_folder : ''),'');
					//				fname = s.replace(((this._current_folder) ? this._current_folder : ''),'');
									obj.fname = fname;
									ac.setItemAt(obj,i);
								}
							}
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
						if (this._current_target) {
							if (this._current_target is List) {
								try {
									ac = this.makeContentsIntoCollectionOfObjects(event.data,isCSV);
									if (this._current_target.id == this.list_Archives.id) {
										obj = ac.getItemAt(0);
										fn = String(obj[this.list_Archives.labelField]);
										if (new File(fn).isDirectory) {
											this._current_folder = fn;
											ac.removeItemAt(0);
										}
										for (i = 0; i < ac.length; i++) {
											obj = ac.getItemAt(i);
											fname = String(obj[this.list_Archives.labelField]).replace(this._current_folder,'');
											obj.fname = fname;
											ac.setItemAt(obj,i);
										}
									}
									ArrayCollectionUtils.appendAllInto(ArrayCollection(List(this._current_target).dataProvider),ac);
								} catch (err:Error) { }
							} else {
								switch (this._current_target.id) {
									case this._packagesView.listGridCanvasPkgs.id:
										ac = this.makeContentsIntoCollectionOfObjects(event.data,isCSV);
										current_target = ListGridCanvas(this._current_target);
	
										var ar:Array = ArrayUtils.deepCopyFrom(ac.source);
										ArrayUtils.popFromFront(ar);
										var _ac:ArrayCollection = new ArrayCollection(ar);
										current_target.list_dataProvider = ac;
	
										current_target.grid_dataProvider = ac;
										this._packagesView.visible = true;
										this._packageContentsView.visible = (this._packageContentsView.listGridCanvasPkgContents.listWidget.selectedIndex > -1);
										if (this._packageContentsView.visible == false) {
											this.hdiv01.removeChildAt(2);
											this.hdiv01.removeChildAt(1);
											this.hdiv01.addChildAt(this._packagesView,1);
											this.hdiv01.addChildAt(this._packageContentsView,2);
										}
										break;
									case this._packageContentsView.listGridCanvasPkgContents.id:
										ac = this.makeContentsIntoCollectionOfObjects(event.data,isCSV);
										current_target = ListGridCanvas(this._current_target);
										current_target.list_dataProvider = ac;
										current_target.grid_dataProvider = ac;
										this._packagesView.visible = (this._packagesView.listGridCanvasPkgs.listWidget.selectedIndex > -1);
										this._packageContentsView.visible = true;
										if (this._packagesView.visible == false) {
											this.hdiv01.removeChildAt(2);
											this.hdiv01.removeChildAt(1);
											this.hdiv01.addChildAt(this._packageContentsView,1);
											this.hdiv01.addChildAt(this._packagesView,2);
										}
										break;
									default:
										this._current_target.list.dataProvider = event.data;
										this._current_target.grid.dataProvider = event.data;
										break;
								}
							}
						} else if (this.viewStack1.selectedIndex == 1) {
							function onClickOKButton(event:MouseEvent):void {
								PopUpManager.removePopUp(Alert(event.currentTarget));
								this.cancelFolderBrowserState();
							}
							// +++ doing an export !
							ac = this.makeContentsIntoCollectionOfObjects(event.data,isCSV);
							fname = String(ac.getItemAt(ac.length-1)[0]);
							var toks:Array = fname.split('/');
							if (toks.length == 1) {
								toks = String(ac.getItemAt(ac.length-1)).split(File.separator)
							}
							toks.pop();
							this.fileList1.directory = new File(toks.join(File.separator));
	
	 						popup = AlertPopUp.info("The package '" + fname + "' has been successfully exported.\nPress the OK button to continue.","INFO");
							PopUpManager.centerPopUp(popup);
							popup.styleName = 'InfoAlert';
							popup.buttonFlags = Alert.OK;
							popup.addEventListener(MouseEvent.CLICK, onClickOKButton);
						}
					} catch (err:Error) {
						popup = AlertPopUp.error(err.message,"Processing Error");
						PopUpManager.centerPopUp(popup);
						popup.styleName = 'ErrorAlert';
					}
					this._current_target = null;
					break;
	 
				case 'number':
					isNumber = true;
				case 'boolean':
					ac = this.makeContentsIntoCollectionOfObjects(event.data,isCSV);
					obj = this.collapseCollectionOfObjectsIntoSingleObject(ac);
					obj.source = ArrayUtils.pruneEmptyItems(obj.source.split(File.separator)).join(File.separator);
					var oTarget:Object = this.findCachedCallbackForItem(obj.source);
					try {
						var oFunc:Function = oTarget.obj[oTarget.methodName];
						obj.item = ((isNumber) ? Number(obj.item) : ((obj.item.toLowerCase() == 'true') ? true : false));
						obj.currentTarget = oTarget;
						oFunc(obj);
					} catch (err:Error) {
						popup = AlertPopUp.error(err.message,"CallBack ERROR in 'boolean' case for onDataReceived()");
						PopUpManager.centerPopUp(popup);
						popup.styleName = 'ErrorAlert';
					}
					break;
	
				case 'license':
					LicenseUtils.licenseLevel = event.data['value'];
					break;
					
				case 'LicenseLevels':
					ac = this.makeContentsIntoCollectionOfObjects(event.data,isCSV);
					obj = this.collapseCollectionOfObjectsIntoSingleObject(ac);
					LicenseUtils.licenseLevels = obj;
					break;
	
				case 'null':
					break;
					
				case 'error':
					var errorTitle:String = 'APPLICATION ERROR';
					XMLObjectUtils.flattenChildrenIntoNodeValue(event.data);
					if (event.data['value'] is Array) {
						var _ar:Array = event.data['value'];
						errorTitle = StringUtils.replaceAll(_ar[0],'<br>', '\n');
						nodeValue = StringUtils.replaceAll(_ar[_ar.length-1],'<br>', '\n');
					} else {
						nodeValue = event.data['value'];
						nodeValue = StringUtils.replaceAll(nodeValue,'<br>', '\n');
					}
					popup = AlertPopUp.error(nodeValue,errorTitle);
					PopUpManager.centerPopUp(popup);
					popup.styleName = 'ErrorAlert';
					break;
	
				default:
					popup = AlertPopUp.info(this.dataToString(event.data,true) + "\n\n(" + nodeType + ")","Unknown Response");
					PopUpManager.centerPopUp(popup);
					popup.styleName = 'InfoAlert';
					break;
			}
		} catch (err:Error) {
			popup = AlertPopUp.error("Report this error to the Technical Support folks at http://www.sexyblondessoftware.com.\n\n(" + nodeType + ")\n\n" + err.message,"Application Error");
			PopUpManager.centerPopUp(popup);
			popup.styleName = 'ErrorAlert';
		}
		this.onlineStatusIndicator.isOnline = true;
		this.enabled = true;	// handle the scenario where we disabled the GUI while the server is busy...
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
				
	private function makeThisListTheOneInFocus(list:*):void {
		this.list_Archives.styleName = '';
		try {
			this._packagesView.listGridCanvasPkgs.listWidget.styleName = '';
			this._packageContentsView.listGridCanvasPkgContents.listWidget.styleName = '';
		} catch (err:Error) { }
		if (list is List) {
			list.styleName = 'ListInFocus';
		} else if (list is ListGridCanvas) {
			try {
				list.list.styleName = 'ListInFocus';
			} catch (err:Error) { }
		}
	}
				
	private function clearContentWidgets():void {
		try {
			this._packagesView.listGridCanvasPkgs.list_dataProvider = new ArrayCollection();
			this._packagesView.listGridCanvasPkgs.grid_dataProvider = new ArrayCollection();
			this._packageContentsView.listGridCanvasPkgContents.list_dataProvider = new ArrayCollection();
			this._packageContentsView.listGridCanvasPkgContents.grid_dataProvider = new ArrayCollection();
		} catch (err:Error) {}
	}
				
	private function onClickListArchivesButton():void {
		this._current_target = this.list_Archives;
		this.current_archive_name = '';
		this.current_package_name = '';
		this.makeThisListTheOneInFocus(this._current_target);
		this.clearContentWidgets();
		this.socketsManager.sendCommandToSocket(this.commandNameID(this._const_list_archives_symbol));
	}
	
	private function onChangeArchiveList(event:ListEvent):void {
		var target:List = List(event.currentTarget);
		if (target.selectedIndex > -1) {
			var item:Object = ArrayCollection( target.dataProvider).getItemAt(target.selectedIndex);
			var _item:String = item[target.labelField] as String;
			this.currentState = 'ArchivesListClickedState';
			this.activateArchiveSelected();
			this._current_target = ((_item.toUpperCase().indexOf(PackageBuilderCanvas._packageFileExtension) > -1) ? this._packageContentsView.listGridCanvasPkgContents : this._packagesView.listGridCanvasPkgs);
			this.current_archive_name = _item;
			this.current_package_name = '';
			this.makeThisListTheOneInFocus(this._current_target);
			this.clearContentWidgets();
			this._packagesView.visible = true;
			this.showHideDividerAt(1,true);
			this.socketsManager.sendCommandToSocketWithArgs(this.commandNameID(this._const_open_archive_symbol),_item);
		} else {
			this._packagesView.visible = false;
			this.showHideDividerAt(1,false);
			this.currentState = this._baseState;
		}
	}
	
	private function isPackageNameValid(name:String):Boolean {
		return (name != 'NO PACKAGES');
	}
				
	private function onChangeArchiveContentsList(event:ListEvent):void {
		var target:List = List(event.currentTarget);
		if (target.selectedIndex > -1) {
			var item:String = Object(ArrayCollection( target.dataProvider).getItemAt(target.selectedIndex))[target.labelField] as String;
			this._current_target = this._packageContentsView.listGridCanvasPkgContents;
			this.current_package_name = item;
			if (this.isPackageNameValid(item)) {
				this.socketsManager.sendCommandToSocketWithArgs(this.commandNameID(this._const_open_package_symbol),this._current_archive_name+','+item);
			}
		}
	}
				
	private function onChangeArchivePkgContentsList(event:ListEvent):void {
		var target:List = List(event.currentTarget);
		var item:String = Object(ArrayCollection( target.dataProvider).getItemAt(target.selectedIndex))[target.labelField] as String;
	//	this._current_target = this._packagesView.listGridCanvasPkgs.list;
	//	this._current_package_name = item;
	//	this.socketsManager.sendCommandToSocketWithArgs(this.commandNameID(this._const_open_package_symbol),this._current_archive_name+','+item);
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
		} else if (dispObj is PackagesView) {
			var p:PackagesView = PackagesView(dispObj);
			return p.getChildren();
		} else if (dispObj is PackageContentsView) {
			var pv:PackageContentsView = PackageContentsView(dispObj);
			return pv.getChildren();
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
				
	private function isListGridCanvas(dispObj:*):Boolean {
		return (dispObj is ListGridCanvas);
	}
				
	private function isButton(dispObj:*):Boolean {
		return ( (dispObj is Button) && ( (Button(dispObj).id == 'btn_ArchiveContentsGridToggle') || (Button(dispObj).id == 'btn_ArchivePkgContentsGridToggle') ) );
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
				
	private function onClickGridToggleButton(event:MouseEvent):void {
		var ea:*;
		var _btn:Button;
		var btn:Button = Button(event.currentTarget);
		var collection:Array = [];
		var exclusions:Array = [];
		var _collection:Array = [];
		var _exclusions:Array = [];
		this.locateArbitraryDisplayObjectBasedOn(btn.parent,this.isListGridCanvas,collection,exclusions);
		var obj:ListGridCanvas = collection[0];
		if (obj) {
			collection = [];
			exclusions.push(obj);
			this.locateArbitraryDisplayObjectBasedOn(btn.parent,this.isListGridCanvas,collection,exclusions);
			_exclusions.push(btn);
			this.locateArbitraryDisplayObjectBasedOn(btn.parent,this.isButton,_collection,_exclusions);
			obj.flipToggle();
			if (btn.styleName == 'ToggleButtonGridState') {
				btn.styleName = 'ToggleButtonListState';
				obj.parent.parent.width += ((obj.id == 'listGridCanvasPkgContents') ? 350 : 250);
				this.viewStack1.width += ((obj.id == 'listGridCanvasPkgContents') ? 150 : 0);
				for (ea in collection) {
					ListGridCanvas(collection[ea]).parent.parent.width -= ((obj.id == 'listGridCanvasPkgContents') ? 150 : 100);
				}
				for (ea in _collection) {
					_btn = Button(_collection[ea]);
					_btn.enabled = false;
					if (_btn.styleName == 'ToggleButtonGridState') {
						_btn.styleName = 'ToggleButtonGridDisabledState';
					} else if (_btn.styleName == 'ToggleButtonListState') {
						_btn.styleName = 'ToggleButtonListDisabledState';
					}
				}
			} else {
				btn.styleName = 'ToggleButtonGridState';
				obj.parent.parent.width -= ((obj.id == 'listGridCanvasPkgContents') ? 350 : 250);
				this.viewStack1.width -= ((obj.id == 'listGridCanvasPkgContents') ? 150 : 0);
				for (ea in collection) {
					ListGridCanvas(collection[ea]).parent.parent.width += ((obj.id == 'listGridCanvasPkgContents') ? 150 : 100);
				}
				for (ea in _collection) {
					_btn = Button(_collection[ea]);
					_btn.enabled = true;
					if (_btn.styleName == 'ToggleButtonGridDisabledState') {
						_btn.styleName = 'ToggleButtonGridState';
					} else if (_btn.styleName == 'ToggleButtonListDisabledState') {
						_btn.styleName = 'ToggleButtonListState';
					}
				}
			}
		}
	}
				
	private function onListInFocus(event:ListInFocusEvent):void {
		this.makeThisListTheOneInFocus(event.event.currentTarget);
	}
				
	private function onMouseOverArchiveList(event:MouseEvent):void {
		this.makeThisListTheOneInFocus(event.currentTarget);
	}
				
	private function onPkgsListItemSelected(event:ListItemSelectedEvent):void {
		var target:List = List(event.event.currentTarget);
		this._packageContentsView.visible = (target.selectedIndex > -1);
		this.refreshMenuBarMenu();
	}
				
	private function onCreationCompleteListGridCanvas(event:FlexEvent):void {
	 	var obj:ListGridCanvas;
	 	if (event.currentTarget is ListGridCanvas) {
	 		obj = ListGridCanvas(event.currentTarget);
	 	} else if (event.currentTarget is PackagesView) {
	 		obj = PackagesView(event.currentTarget).listGridCanvasPkgs;
	 	} else {
	 		return;
	 	}
	 	switch (obj.id) {
	 		case this._packagesView.listGridCanvasPkgs.id:
			 	obj.listWidget.addEventListener(ListEvent.CHANGE, onChangeArchiveContentsList);
	 			break;
	 		case this._packageContentsView.listGridCanvasPkgContents.id:
			 	obj.listWidget.addEventListener(ListEvent.CHANGE, onChangeArchivePkgContentsList); 
	 			break;
	 	}
	 	obj.addEventListener(ListInFocusEvent.TYPE_LIST_IN_FOCUS, onListInFocus); 
	 	obj.listWidget.addEventListener(MouseEvent.CLICK, onClickListGridCanvas);
	 	this._packagesView.listGridCanvasPkgs.addEventListener(ListItemSelectedEvent.TYPE_LIST_ITEM_SELECTED, onPkgsListItemSelected);
	 }
				
	private function onDividerReleaseHDividedBox(event:DividerEvent):void {
		var div:HDividedBox = HDividedBox(event.target);
		var o:* = div.getDividerAt(event.dividerIndex);
	//	AlertPopUp.info(div.id + '\n' + event.dividerIndex + '\n' + event.toString());
	}
				
	private function get isCurrentArchiveValid():Boolean {
		return ( (this.current_archive_name.length > 0) && (this.current_archive_name.indexOf('.exe') > -1) );
	}
	
	private function onItemClickMenuBar(event:MenuEvent):void {
		var i:int;
		var j:int;
		var packageObj:Object;
		var archObj:Object;
		var popUp:Alert;
		var data:String = event.item.@data;
		this._current_action = '';
		this._current_action2 = '';
		if (data != "top") {
			var item:String = event.item.@data;
			switch (item) {
				case "exportPackage":
					if (this.isCurrentArchiveValid) {
						this.currentState = 'FolderBrowserState';
						this._expectedViewStackIndex = 1;
						this.viewStack1.selectedIndex = 1;
						this.tabBar1.enabled = false;
						this._current_action = 'Export Package "' + this.current_package_name + '"';
						this._current_action2 = 'from "' + this.current_archive_name + '"';
					} else {
						popUp = AlertPopUp.info("You must choose an Archive from the list of Archives.  Packages cannot be exported as they already exist on your local hard disk.  Archives have names that end with '.EXE'; packages have names that end with '{PackageBuilderCanvas._packageFileExtension}'.", "INFO");
						popUp.styleName = 'InfoAlert';
					}
					break;

				case "removePackage":
					i = this._packagesView.listGridCanvasPkgs.listWidget.selectedIndex;
					j = this.list_Archives.selectedIndex;
					if ( (i > -1) && (j > -1) ) {
						archObj = this.list_Archives.selectedItem;
						packageObj = this._packagesView.listGridCanvasPkgs.listWidget.selectedItem;
						var _cmd:int = commandNameID(_const_remove_package_from_symbol);
						popUp = AlertPopUp.confirm('Are you sure you want to remove "' + packageObj.name + '" from "' + archObj.fname + '" ?', "Confirm",
							function (event:CloseEvent):void {
								if (event.detail == Alert.YES) {
									popUp = AlertPopUp.info('Your License cannot perform this function.\n\nUpgrade your License to unlock this important feature.', "WARNING :: Time to Upgrade your License.");
									popUp.styleName = 'ErrorAlert';
					//				socketsManager.sendCommandToSocketWithArgs(_cmd,archObj.item,packageObj.name,packageObj.pos);
								}
							} 
						);
						popUp.styleName = 'ConfirmAlert';
					}
					break;
	
				case "addPackage":
					if (this.isCurrentArchiveValid) {
						if (this._building_package == null) {
							this.currentState = 'PackageBuildState';
						} else {
							popUp = AlertPopUp.info("Label: " + event.item.@label + "\n" + "Data: " + event.item.@data, "Clicked Add Package (Package Exists)");
							popUp.styleName = 'InfoAlert';
						}
					}
					break;
					
				case "createPackage":
					if (this._building_package == null) {
						this.currentState = 'PackageBuildState';
						this._expectedViewStackIndex = 1;
						this.viewStack1.selectedIndex = 1;
						this.tabBar1.enabled = false;
					} else {
						popUp = AlertPopUp.info("Label: " + event.item.@label + "\n" + "Data: " + event.item.@data, "Clicked Create Package (Package Exists)");
						popUp.styleName = 'InfoAlert';
					}
					break;
	
				case "findArchives":
					this.cancelFolderBrowserState();
					this.onClickListArchivesButton();
					this.initListStates();
					break;
					
				case "createArchive":
					if (this._building_archive == null) {
						this.currentState = 'ArchiveBuildState';
						this._expectedViewStackIndex = 1;
						this.viewStack1.selectedIndex = 1;
						this.tabBar1.enabled = false;
					} else {
						popUp = AlertPopUp.info("Label: " + event.item.@label + "\n" + "Data: " + event.item.@data, "Clicked Create Package (Archive Exists)");
						popUp.styleName = 'InfoAlert';
					}
					break;
					
				case "aboutInfo":
					popUp = AlertPopUp.info('EzPackager (aka. pyAIR) - Adobe AIR Packaging and Deployment System\n\npyAIR is the fusion of Python 2.5.1 and Adobe AIR using a unique mixture of technologies that makes it very E-Z to produce high-powered Adobe AIR Apps empowered with embedded Python.\n\nNow you too can embed Python 2.5.1 Scripts directly in your Adobe AIR apps to achieve performance levels unparallelled by Flex ActionScript 3 alone.\n\nGain access to the Win32 API.\n\nEmpower your Adobe AIR Apps to achieve what was previously thought to be impossible where Adobe AIR alone is being used.\n\npyAIR & EzPackager are published by Hierarchical Applications Limited, Inc. (c). Copyright 2007, Hierarchical Applications Limited, Inc, All Rights Reserved.', "Info :: EzPackager & pyAIR - {LicenseUtils.licenseLevel} License");
					popUp.styleName = 'InfoAlert';
					break;
					
				case "aboutLicense":
					switch (LicenseUtils.licenseLevel) {
						case LicenseUtils.LICENSE_TRIAL:
						break;
	
						case LicenseUtils.LICENSE_STANDARD:
						break;
	
						case LicenseUtils.LICENSE_PRO:
						break;
	
						case LicenseUtils.LICENSE_ENTERPRISE:
						break;
					}
					popUp = AlertPopUp.info('Not yet Implemented !', "Info :: {LicenseUtils.licenseLevel} License");
					popUp.styleName = 'InfoAlert';
					break;
					
				case "debugWindow":
					this.socketsManagerPanel.visible = ((this.socketsManagerPanel.visible) ? false : true);
					this.socketsManagerPanel.height = ((this.socketsManagerPanel.visible) ? 200 : 0);
					break;
			}
		}        
	}

	private function handleBuilderCancelled():void {
		this._expectedViewStackIndex = 0;
		this.currentState = '';
		this.tabBar1.enabled = true;
		this.viewStack1.selectedIndex = 0;
		this.refreshArchivesPackagesList(this._current_folder);
	}

	private function onArchiveBuilderCancelled(event:PackageBuilderCancelledEvent):void {
		this.handleBuilderCancelled();
	}
	
	private function onPackageBuilderCancelled(event:PackageBuilderCancelledEvent):void {
		this.handleBuilderCancelled();
	}
				
	private function onExecPython(event:ExecPythonEvent):void {
		this._cacheCallbacks[event.args[0]] = event;
		this.socketsManager.sendCommandToSocketWithArgs(event.pythonCommand,event.args);
	}

	private function callbackPackageBuilderAccepted(obj:Object):void {
		var popUp:Alert = AlertPopUp.info('The New Package "' + obj.source + '" has ' + ((obj.item) ? 'been successfully built' : 'not been built due to some kind of problem') + '.',((obj.item) ? 'INFO' : 'WARNING') + ' :: New Package ' + ((obj.item) ? 'Successfully' : 'NOT') + ' Built');
		popUp.styleName = ((obj.item) ? 'InfoMsgAlert' : 'ErrorAlert');
	}
	
	private function callbackArchiveBuilderAccepted(obj:Object):void {
		var popUp:Alert = AlertPopUp.info('The New Archive "' + obj.source + '" has ' + ((obj.item) ? 'been successfully built' : 'not been built due to some kind of problem') + '.',((obj.item) ? 'INFO' : 'WARNING') + ' :: New Archive ' + ((obj.item) ? 'Successfully' : 'NOT') + ' Built');
		popUp.styleName = ((obj.item) ? 'InfoMsgAlert' : 'ErrorAlert');
	}
	
	private function onPackageBuilderAccepted(event:PackageBuilderAcceptedEvent):void {
		var fileNames:Array = [];
		var i:int;
		for (i = 0; i < event.filesList.length; i++) {
			fileNames.push(File(event.filesList[i]).nativePath);
		}
		this.enabled = false;
		this._cacheCallbacks[event.fileName] = {'obj':{'callBackFunc':this.callbackPackageBuilderAccepted},'methodName':'callBackFunc'};

		var allowedNumPackages:int = LicenseUtils.allowedPackagesNumber;
				
		this.socketsManager.sendCommandToSocketWithArgs(this._const_build_package_symbol,event.fileName,allowedNumPackages,fileNames);
	}
	
	private function onArchiveBuilderAccepted(event:ArchiveBuilderAcceptedEvent):void {
		var fileNames:Array = [];
		var i:int;
		for (i = 0; i < event.filesList.length; i++) {
			fileNames.push(File(event.filesList[i]).nativePath);
		}
		this.enabled = false;
		this._cacheCallbacks[event.fileName] = {'obj':{'callBackFunc':this.callbackArchiveBuilderAccepted},'methodName':'callBackFunc'};

		var allowedNumArchives:int = LicenseUtils.allowedArchivesNumber;
				
		this.socketsManager.sendCommandToSocketWithArgs(this._const_build_archive_symbol,event.fileName,allowedNumArchives,fileNames);
	}
	
	private function checkPackageNameForArchive(obj:Object):void {
		var currentTarget:Object = obj.currentTarget;
		var oCallback:Function = currentTarget.callback;
		oCallback(obj);
	}
	
	private function onArchiveBuilderCheckPackageName(event:PackageBuilderCheckPackageNameEvent):void {
		this._cacheCallbacks[event.fileName] = {'obj':{'callBackFunc':this.checkPackageNameForArchive},'methodName':'callBackFunc','callback':event.callback};
		this.socketsManager.sendCommandToSocketWithArgs(this.commandNameID(this._const_check_package_name_symbol),event.fileName);
	}

	private function onCreationCompleteArchiveBuilderCanvas():void {
		// +++
		this.archiveBuilder.addEventListener(PackageBuilderCancelledEvent.TYPE_PACKAGE_BUILDER_CANCELLED, onArchiveBuilderCancelled);
		this.archiveBuilder.addEventListener(ExecPythonEvent.TYPE_EXEC_PYTHON, onExecPython);
		this.archiveBuilder.addEventListener(ArchiveBuilderAcceptedEvent.TYPE_ARCHIVE_BUILDER_ACCEPTED, onArchiveBuilderAccepted);
		this.archiveBuilder.addEventListener(ArchiveBuilderCheckArchiveNameEvent.TYPE_ARCHIVE_BUILDER_CHECK_ARCHIVE_NAME, onArchiveBuilderCheckArchiveName);
		this.archiveBuilder.addEventListener(PackageBuilderCheckPackageNameEvent.TYPE_PACKAGE_BUILDER_CHECK_PACKAGE_NAME, onArchiveBuilderCheckPackageName);
	}
	
	private function onCreationCompletePackageBuilderCanvas():void {
		this.packageBuilder.addEventListener(PackageBuilderCancelledEvent.TYPE_PACKAGE_BUILDER_CANCELLED, onPackageBuilderCancelled);
		this.packageBuilder.addEventListener(ExecPythonEvent.TYPE_EXEC_PYTHON, onExecPython);
		this.packageBuilder.addEventListener(PackageBuilderAcceptedEvent.TYPE_PACKAGE_BUILDER_ACCEPTED, onPackageBuilderAccepted);
		this.packageBuilder.addEventListener(PackageBuilderCheckPackageNameEvent.TYPE_PACKAGE_BUILDER_CHECK_PACKAGE_NAME, onPackageBuilderCheckPackageName);
	}
				
	private function onChangeViewStack1(event:IndexChangedEvent):void {
		if (this._expectedViewStackIndex != event.newIndex) {
			var popUp:Alert = AlertPopUp.error('You cannot switch from the view at ' + event.oldIndex + ' to the view at ' + event.newIndex + ' at this time.', "View Context Change Error");
			popUp.styleName = 'ErrorAlert';
			var vs:ViewStack = ViewStack(event.currentTarget);
			this._expectedViewStackIndex = event.oldIndex;
			vs.selectedIndex = event.oldIndex;
		}
	}
	
	private function initListStates():void {
		if (this._packagesView) {
			this._packagesView.visible = false;
		}
		if (this._packageContentsView) {
			this._packageContentsView.visible = false;
		}
		this.showHideDividerAt(1,false);
	}
				
	private function cancelFolderBrowserState():void {
		if (this.viewStack1.selectedIndex != 0) {
			this._expectedViewStackIndex = 0;
			this.viewStack1.selectedIndex = 0;
			this.currentState = this._baseState;
	
			this.viewStack1.width -= this._packagesView.width;
			this.viewStack1.width -= this._packageContentsView.width;
			this.hdiv01.removeChild(this._packagesView);
			this.hdiv01.removeChild(this._packageContentsView);
			this._packagesView = null;
			this._packageContentsView = null;
		}
	}
				
	private function onClickCancelFolderBrowserButton():void {
		this.cancelFolderBrowserState();
		this.refreshMenuBarMenu();
	}
				
	private function onClickAcceptFileButton():void {
		this._expectedViewStackIndex = 0;
		var item:* = this.fileList1.selectedItem;
		if (item == null) {
			item = unescape(this.fileList1.directory.url).replace('file:///','');
		}
		if (FileListUtils.isFileListAtRoot(this.fileList1) == false) {
			var archName:String = this.current_archive_name;
			var pkgName:String = this.current_package_name;
			var destName:String = item + '/' + pkgName;
			this.socketsManager.sendCommandToSocketWithArgs(this.commandNameID(this._const_export_package_from_archive_symbol),archName,pkgName,destName);
		}
	}
				
	private function refreshNavigationButtons():void {
		this.btn_acceptFile.enabled = this.btn_navigateUp.enabled = (FileListUtils.isFileListAtRoot(this.fileList1) == false);
		this.btn_navigateUp.styleName = ((this.btn_navigateUp.enabled) ? 'EnabledButton' : 'DisabledButton');
		this._toolTipCache[this.btn_navigateUp.id+'_'+((this.btn_navigateUp.enabled) ? 'EnabledButton' : 'DisabledButton')] = this.btn_navigateUp.toolTip; 
		this.btn_navigateUp.toolTip = ((this.btn_navigateUp.enabled) ? this._toolTipCache[this.btn_navigateUp.id+'_EnabledButton'] : 'This button has been disabled.  Navigate to a folder that is one level lower than the current folder to enable this button or Navigate to the HOME folder.');
	}
	
	private function makeFolder(folderPath:String):void {
		if (FileListUtils.makeFolder(folderPath)) {
			this.fileList1.directory = new File(FileUtils.correctFolderSpec(folderPath));
			var popUp:Alert = AlertPopUp.info("Successfully created the folder '" + folderPath + "'.", "INFO");
			popUp.styleName = 'InfoMsgAlert';
		}
	}
				
	private function onClickNavigateNewButton():void {
		if (this.fileList1.directory.isDirectory) {
			FileListUtils.showNewFolderDialog(this,this.fileList1.directory.nativePath,this.makeFolder,true);
		} else {
			var popUp:Alert = AlertPopUp.error("Cannot make a new folder in anything other than an existing folder.", "ERROR in onClickNavigateNewButton().");
			popUp.styleName = 'ErrorAlert';
		}
	}
				
	private function onCloseDialogConfirmDeletion(event:CloseEvent):void {
		var popUp:Alert;
		if (event.detail == Alert.YES) {
			var oFile:File = File(this.fileList1.selectedItem);
			if (oFile) {
				if (oFile.isDirectory == false) {
					oFile.deleteFile();
				} else if (oFile.getDirectoryListing().length == 0) {
					oFile.deleteDirectory();
				} else {
					popUp = AlertPopUp.error(oFile.name + ' cannot been deleted because it is a folder that is not empty.', "WARNING");
					popUp.styleName = 'ErrorAlert';
				}
				this.fileList1.directory = new File(this.fileList1.directory.nativePath);
			}
			popUp = AlertPopUp.info(oFile.name + ' has been deleted.', "INFO");
			popUp.styleName = 'InfoMsgAlert';
		}
	}
				
	private function onClickDeleteItemButton():void {
		var popUp:Alert;
		var oFile:File = File(this.fileList1.selectedItem);
		try {
			popUp = AlertPopUp.confirm('Are you sure you want to delete "' + oFile.name + '" ?', "CONFIRMATION", onCloseDialogConfirmDeletion);
			popUp.styleName = 'ConfirmAlert';
		} catch (err:Error) {
			popUp = AlertPopUp.error(err.message, "ERROR");
			popUp.styleName = 'ErrorAlert';
		}
	}
				
	private function isSelectedItemDeletable():Boolean {
		var isEmpty:Boolean = true;
		var files:Array = [];
		var oFile:File = File(this.fileList1.selectedItem);
		if (this.fileList1.selectedItem != null) {
			try { files = oFile.getDirectoryListing(); } catch (err:Error) { }
			isEmpty = (files.length == 0);
		}
		var isDeletable:Boolean = ( (this.fileList1.selectedItem != null) && ( (oFile.isDirectory == false) || ( (oFile.isDirectory) && (isEmpty) ) ) );
		var reason:String = ((oFile.isDirectory) ? ((isEmpty) ? 'it is empty and empty folders can be deleted' : 'is not empty and folders with contents cannot be deleted. Navigate into the folder and manually delete all contents before attempting to delete the folder') : 'files can always be deleted');
		this.btn_deleteFolder.toolTip = 'Click this button to delete the currently selected file or folder.<br>The selected item is a "' + ((oFile.isDirectory) ? 'Folder' : 'File') + '" and ' + ((isDeletable) ? 'can' : 'cannot') + ' be deleted because ' + reason + '.';
		return isDeletable;
	}
				
	private function onChangeFileSystemList(event:ListEvent):void {
		this.btn_deleteFolder.enabled = this.isSelectedItemDeletable();
		this.refreshNavigationButtons();
	}
				
	private function onClickNavigateUpButton():void {
		this.fileList1.navigateUp();
		this.refreshNavigationButtons();
	}
				
	private function initFileSystemList():void {
		var toks:Array = this.current_archive_name.split(File.separator);
		toks.pop();
		var pathName:String = toks.join(File.separator);
		if (pathName.length > 0) {
			this.fileList1.directory = new File(FileUtils.correctFolderSpec(pathName));
		}
	}
				
	private function onClickNavigateHomeButton():void {
		this.initFileSystemList();
		this.refreshNavigationButtons();
	}
				
	private function onCreationCompleteFileSystemList():void {
		this.initFileSystemList();
	}
	
	private function refreshMenuBarMenu():void {
		var menu:XMLListCollection = XMLListCollection(this.menuBar.dataProvider);
		menu[1].@enabled[0] = 'true';
		var nodes:XMLList = XML(menu[1]).children();
		var i:int;
		var node:XML;
		var isPackageSelected:String = 'false';
		if (this._packagesView) {
			try {
				isPackageSelected = ((this._packagesView.listGridCanvasPkgs.listWidget.selectedItem == null) ? 'false' : 'true');
			} catch (err:Error) { }
		} 
		var isArchiveSelected:String = ((this.isCurrentArchiveValid) ? 'true' : 'false');
		var canPackageBuilderBeOpened:String = ((this.currentState == 'PackageBuildState') ? 'false' : 'true');
		var data:String;
		for (i = 0; i < nodes.length(); i++) {
			node = XML(nodes[i]);
			data = String(node.@data);
			if ( (data == 'exportPackage') || (data == 'removePackage') ) {
				node.@enabled = isPackageSelected;
			} else if (data == 'addPackage') {
				node.@enabled = isArchiveSelected;
			} else if (data == 'createPackage') {
				node.@enabled = canPackageBuilderBeOpened;
			}
		}
	}
				
	private function onCreationCompleteAppMenuBar():void {
		this.refreshMenuBarMenu();
	}
				
	private function onClickArchiveList():void {
		this.currentState = 'ArchivesListClickedState';
		var menu:XMLListCollection = new XMLListCollection(this.menubarXML);
		var enabled:Boolean = (String(menu[1].@enabled[0]).toLowerCase() == 'true');
		this.refreshMenuBarMenu();
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
				
	private function onClickListGridCanvas(event:MouseEvent):void {
		var obj:* = this.getProperParentFrom(event.currentTarget.parent, this.isListGridCanvas);
		if (obj is ListGridCanvas) {
			var target:ListGridCanvas = ListGridCanvas(obj);
			var item:* = target.listWidget.selectedItem;
			if ( (target.id == this._packagesView.listGridCanvasPkgs.id) && (item) && (this.isPackageNameValid(item.name)) ) {
			} else if ( (target.id == this._packageContentsView.listGridCanvasPkgContents.id) && (this.isPackageNameValid(String(item.name)) == false) ) {
			}
		}
	}
				