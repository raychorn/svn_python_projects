// ActionScript file
	import com.HAL.Alert.AlertPopUp;
	
	import mx.collections.XMLListCollection;
	import mx.controls.Alert;
	import mx.events.MenuEvent;

	[Bindable]
	private var menubarXML:XMLList =
	    <>
	        <menuitem label="Help" data="top">
	            <menuitem label="About" data="aboutInfo"/>
	        </menuitem>
	    </>;

	private var _menuBarCollection:XMLListCollection;

	private function onInitialize():void {
	}
	
	private function initMenuBar():void {
		this._menuBarCollection = new XMLListCollection(this.menubarXML);
	}
	
	public function get menuBarCollection():XMLListCollection {
		if (this._menuBarCollection == null) {
			this.initMenuBar(); 
		}
		return this._menuBarCollection;
	}
				
	private function handleMenuBar(item:String):void {
		var popUp:Alert;
		switch (item) {
			case "aboutInfo":
				popUp = AlertPopUp.info('Put some info here.', "Info :: " + this.appBar_title.text);
				popUp.styleName = 'InfoAlert';
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
	
	private function _refreshMenuBarMenu():void {
		var menu:XMLListCollection = XMLListCollection(this.menuBar.dataProvider);
		var i:int;
		for (i = 0; i < menu.length; i++) {
			this.refreshMenuBarMenu(XML(menu[i]).children());
		}
	}
				
	private function onItemClickMenuBar(event:MenuEvent):void {
		var i:int;
		var j:int;
		var popUp:Alert;
		var data:String = event.item.@data;
		if (data != "top") {
			this.handleMenuBar(event.item.@data);
		}        
	}

	private function onCreationCompleteSocketsManager():void {
	}
				
	private function onCreationCompleteAppMenuBar():void {
		this._refreshMenuBarMenu();
	}
				
	private function onClickGetPythonVersionButton():void {
	}
	
	private function onCreationCompletePythonCode():void {
	}

	