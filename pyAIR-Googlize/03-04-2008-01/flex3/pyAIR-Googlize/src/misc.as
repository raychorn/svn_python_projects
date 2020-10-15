// ActionScript file
import com.HAL.controls.popups.ProgressBarPopUp;
import com.HAL.utils.ArrayUtils;

import mx.collections.ArrayCollection;
import mx.controls.Alert;
import mx.controls.ComboBox;
import mx.controls.List;
import mx.events.ListEvent;
import mx.managers.PopUpManager;

	[Bindable]
	private var menubarXML:XMLList =
	    <>
	        <menuitem label="Help" data="top">
	            <menuitem label="About" data="aboutInfo"/>
	        </menuitem>
	    </>;

	private const _acceptableMachineNames:Array = ['MURRE', 'UNDEFINED2'];
		    	    
	public const _const_shutdown_symbol:String = 'SHUTDOWN';
	
	private const _const_execute_code_symbol:String = 'execute_code';
	
	private var _list_of_expected_commands:Array = [_const_shutdown_symbol,_const_execute_code_symbol];
	
	private var _pb:ProgressBarPopUp;
	
	private var _progressBar_maximum:Number;
	
	private var _hasTotalProgressBeenReceived:Boolean = false;
	
	private function onInitialize():void {
	}
	
	private function handleMachineID():void {
		this._refreshMenuBarMenu();
	}
	
	private function handleMenuBar(item:String):void {
		var popUp:Alert;
		switch (item) {
			case "aboutInfo":
				popUp = AlertPopUp.info('PyAIR Proof of Concept/Demo.', "Info :: pyAIR Demo");
				popUp.styleName = 'InfoAlert';
				break;
				
			case "debugWindow":
				this.socketsManagerPanel.visible = ((this.socketsManagerPanel.visible) ? false : true);
				this.socketsManagerPanel.height = ((this.socketsManagerPanel.visible) ? 200 : 0);
				break;
		}
	}

	private function refreshMenuBarMenu(nodes:XMLList):void {
		var i:int;
		var node:XML;
		var data:String;
		for (i = 0; i < nodes.length(); i++) {
			node = XML(nodes[i]);
			data = String(node.@data);
			switch (data) {
				case 'createConcordance':
	//				node.@enabled = ((this._acceptableMachineNames.indexOf(this._machineID) > -1) && (this._hasConcordanceBeenCreated == false));
				break;

				case 'openConcordance':
	//				node.@enabled = this._hasConcordanceBeenCreated;
				break;
			}
		}
	}
	
	private function handleErrorFromSocket():void {
		this._pb.dismissPopUp();
		this._refreshMenuBarMenu();
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
	
