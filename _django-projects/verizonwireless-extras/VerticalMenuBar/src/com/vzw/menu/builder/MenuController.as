package com.vzw.menu.builder
{
	import adobe.serialization.json.JSONEncoder;
	
	import com.vzw.controls.MenuNamePopUp;
	import com.vzw.controls.MenuNameRenamePopUp;
	import com.vzw.controls.SmartMenuFlyoutItemAdmin;
	import com.vzw.menu.builder.events.MenuChangedEvent;
	import com.vzw.menu.builder.events.MenuDataChangedEvent;
	
	import flash.events.Event;
	import flash.events.MouseEvent;
	
	import mx.collections.ArrayCollection;
	import mx.controls.Alert;
	import mx.controls.Menu;
	import mx.events.CloseEvent;
	import mx.events.FlexEvent;
	import mx.events.MenuEvent;
	import mx.managers.PopUpManager;
	import mx.messaging.messages.HTTPRequestMessage;
	import mx.rpc.events.ResultEvent;
	
	import vyperlogix.controls.Alert.AlertPopUp;
	import vyperlogix.utils.ArrayCollectionUtils;
	import vyperlogix.utils.EzHTTPService;
	import vyperlogix.utils.ObjectUtils;
	import vyperlogix.utils.StringUtils;
	import vyperlogix.utils.URLUtils;
	
	public class MenuController {
        [Bindable]
		public static var AdminMode:Boolean = true;

        [Bindable]
		public static var domains:ArrayCollection = new ArrayCollection();
		
		public static var urlPrefix:String = 'http://127.0.0.1:8888';
		
        [Bindable]
		public static var _isAdminMode:Boolean = true;

        [Bindable]
		public static var _isAdminEnabled:Boolean = false;

        [Bindable]
		public static var _numMenus:int = -1;

        public static var ezREST:EzHTTPService = new EzHTTPService(false,false);

        public static var _currentTargetMenuBar:*;

        [Bindable]
        public static var _currentSelectedMenuId:int;
            
        [Bindable]
        public static var _currentSelectedMenu:Object = null;
        
        [Bindable]
        public static var reloadMenus_callback:Function; // +++ ?

        private static var _registered_categories:ArrayCollection;

        private static var _registered_menuitems:ArrayCollection;

		[Embed(source="assets/icons/admin/delete.gif")]
		[Bindable]
		public static var adminDeleteIcon:Class;
		
		[Embed(source="assets/icons/admin/edit-script.gif")]
		[Bindable]
		public static var adminEditIcon:Class;
		
		[Embed(source="assets/icons/admin/add.gif")]
		[Bindable]
		public static var adminAddIcon:Class;

        public static var parent:*;

        [Bindable]
        public static var controlPanel:ControlPanel;
        
        [Bindable]
		public static var metaProvider:Object = {};

        [Bindable]
		public static var metafield:String = 'meta';

        [Bindable]
		public static var datafield:String = 'menuitem';

        private static var _admin_editor_popup:*;
        
        public static var dummy:Function = function ():void {};
        public static var callback:Function = dummy;
        
		MenuController._registered_categories = new ArrayCollection();
		MenuController._registered_menuitems = new ArrayCollection();

		// ===============================================================================================

		public static function initialize(container:*):void {
            var ezREST:EzHTTPService = new EzHTTPService(false,false);
            
            function onResultMenuEnvJSON(event:ResultEvent):void {
				var response:*;
				try {
					response = event.result.getItemAt(0);
					response = (response is ObjectProxy) ? response.valueOf() : response;
					var ac:ArrayCollection = new ArrayCollection(response as Array);
					ac.addItemAt('Choose...',0);
					domains.removeAll();
					for (var i:int = 0; i < ac.length; i++) {
						domains.addItem(ac.getItemAt(i));
					}
				} catch (e:Error) {
					var stackTrace:String = e.getStackTrace();
					AlertPopUp.errorNoOkay('Constants :: 1.0\n' + e.message.toString() + '\n' + StringUtils.ellipsis(stackTrace,1024),'ERROR');
				} finally {
	            	container.enabled = true;
				}
            }
            
			function getDomains():void {
            	container.enabled = false;
				var url:String = urlPrefix + '/rest/get/menu/environments/json/';
            	ezREST.send(url, onResultMenuEnvJSON, ezREST.jsonResultType);
			}
			
			getDomains();
		}

		public static function initialize_control_panel(container:*):void {
			function after_controlPanel():void {
				//MenuController.controlPanel.btn_menuChoice.addEventListener("dataChanged",MenuController.controlPanel.menu_changed);
			}
			
			MenuController.controlPanel = new ControlPanel();
			MenuController.controlPanel.id = MenuController.controlPanel.name = 'control_panel';
        	MenuController.controlPanel.addEventListener(MenuChangedEvent.TYPE_MENU_CHANGED_EVENT,MenuController.controlPanel.menu_changed);
        	MenuController.controlPanel.callLater(after_controlPanel);
			container.addChild(MenuController.controlPanel);
		}
		
		private static function onClick_admin_editor_popup(event:MouseEvent):void {
			PopUpManager.removePopUp(MenuController._admin_editor_popup);
			MenuController._admin_editor_popup = null;
		}
		
		private static function onClick_PopUpMenu_ActionBtn(event:*):void {
			var item:* = event.item;
			var aCategory:* = item.category;
			var aDP:* = aCategory.dataProvider;
			var keys:Array = ObjectUtils.keys(aDP,ObjectUtils.criteria_isSomeKindOfObject);
			aDP = aDP[keys[keys.length-1]];
			var name:String = item.name;
			var menuitem:* = item.menuitem;
			menuitem = (menuitem == null) ? {} : menuitem;
			var aLabel:* = aCategory.dataProvider[MenuController.metaProvider.label];
			if (aCategory) {
				if (name == 'delete_menuitem') {
					var uuid:String = menuitem.uuid;
					
					function handle_confirmation(event:CloseEvent):void { 
						if (event.detail == Alert.YES) {
							for (var i:int = 0; i < aDP.length; i++) {
								if ( (uuid != null) && (aDP[i]['uuid'] == uuid) ) {
									aDP.splice(i,1);
									var menu:* = MenuController._currentSelectedMenu;
									MenuController.handle_menuitem_update(menu.uuid);
									break;
								}
							}
						} 
					}
					var label:* = item._label;
					AlertPopUp.confirm('Are you sure you want to delete the menuitem named "' + label.text + '" from "' + aLabel + '" ?','Confirm',handle_confirmation);
				} else {
					MenuController._admin_editor_popup = PopUpManager.createPopUp(MenuController.parent, SmartMenuFlyoutItemAdmin, true) as SmartMenuFlyoutItemAdmin;
					MenuController._admin_editor_popup.width = MenuController.parent.width - 150;
					PopUpManager.centerPopUp(MenuController._admin_editor_popup);
					MenuController._admin_editor_popup.btn_save.addEventListener(MouseEvent.CLICK,MenuController.onClick_save_admin_editor_popup);
					MenuController._admin_editor_popup.btn_dismiss.addEventListener(MouseEvent.CLICK,MenuController.onClick_admin_editor_popup);
					MenuController._admin_editor_popup.combo_domain.dataProvider = MenuController.domains;
					MenuController._admin_editor_popup.combo_domain.labelField = 'name';
					MenuController._admin_editor_popup.label_category.text = aLabel;
					MenuController._admin_editor_popup.source = aCategory;
					MenuController._admin_editor_popup.dataProvider = menuitem;
				}
			} else {
				AlertPopUp.errorNoOkay('Cannot edit a Menu unless the Category is known at runtime and now the Category is not known.\nThis is a programming error. Kindly perform the required maintenance to resolve this issue before proceeding.','ERROR MenuController.101');
			}
		}
		
		private static function handle_registered_category(aContainer:*,aCategory:*,category_label:*):void {
			var aChild:* = aContainer;
			var popup:MenuItemActions;
			var popup_id:String = 'btn_admin_add';
			var items:Array = [];
			try {
	            items = [{'label':'Add Menu Item to Category "' + category_label.text + '"...','name':'add_menu_item','icon':MenuController.adminAddIcon,'category':aCategory,'_label':category_label}];
			} catch (e:Error) {
				var stackTrace:String = e.getStackTrace();
				AlertPopUp.errorNoOkay(StringUtils.ellipsis(stackTrace,1000),'ERROR');
			}

			popup = new MenuItemActions();
			popup.x = 0;
			popup.y = 0;
			popup.height = 16;
			popup.width = 14;
			popup.styleName = 'AdminButton';
			popup.id = popup_id;
			aChild.parent.addChild(popup);
			category_label.text = ' ' + category_label.text;
			popup.addEventListener(FlexEvent.CREATION_COMPLETE, 
				function(event:FlexEvent):void { 
					var target:MenuItemActions = event.currentTarget as MenuItemActions;
					var child:* = target.getChildByName('popup');
					if (child) {
						child.labelField = 'label';
						child.dataProvider = items;
						child.addEventListener("itemClick", MenuController.onClick_PopUpMenu_ActionBtn); 
					} else {
						AlertPopUp.errorNoOkay('Programming Error - you should never see this message but you have so there is a problem and your menu cannot be edited at this time until this error has been resolved. Sorry...','ERROR MenuController.201');
					}
				});
			MenuController._registered_categories.addItem(aCategory);
		}
		
		public static function registerCategory(aContainer:*,aCategoryObject:*,category_label:*):void {
			MenuController.handle_registered_category(aContainer,aCategoryObject,category_label);
		}
		
		private static function handle_registered_menuitem(aMenuItemObject:*,parentSelector:String,parentClassName:String):void {
			var aChild:* = aMenuItemObject;
			var aParent:* = aChild;
			var aLabel:* = ObjectUtils.getChildUntilFoundByName('label',aChild);
			var label_text:String = (aLabel) ? aLabel.text : '*UNKNOWN*';
			var popup:MenuItemActions;
			var popup_id:String = 'btn_admin_add_menuitem';
			var parentDp:* = MenuController._currentTargetMenuBar.dataProvider;
			var aCategory:* = aMenuItemObject[parentSelector];
			while (aCategory) {
				if (aCategory[parentSelector].className == parentClassName) {
					aCategory = aCategory[parentSelector];
					break;
				}
				aCategory = aCategory[parentSelector];
			}
            var items:Array = [
            					{'label':'Add/Edit/Delete the slected menuitem named "' + label_text + '"...','name':''},
            					{'label':'Delete MenuItem "' + label_text + '"...','name':'delete_menuitem','icon':MenuController.adminDeleteIcon,'menuitem':aMenuItemObject.dataProvider,'category':aCategory,'_label':aLabel},
            					{'label':'Edit MenuItem "' + label_text + '"...','name':'edit_menuitem','icon':MenuController.adminEditIcon,'menuitem':aMenuItemObject.dataProvider,'category':aCategory,'_label':aLabel},
            					{'label':'Add Sub-MenuItem "' + label_text + '"...','name':'add_submenuitem','icon':MenuController.adminAddIcon,'menuitem':aMenuItemObject.dataProvider,'category':aCategory,'_label':aLabel},
            				];

			popup = new MenuItemActions();
			popup.height = 16;
			popup.width = 14;
			popup.x = 0;
			popup.y = (aParent.height/2)-(popup.height/2);
			popup.styleName = 'AdminButton';
			popup.id = popup_id;
			popup.parentSelector = parentSelector;
			aParent.addChild(popup);
			if (aLabel) {
				aLabel.text = '  ' + aLabel.text;
			}
			popup.addEventListener(FlexEvent.CREATION_COMPLETE, 
				function(event:FlexEvent):void { 
					var target:MenuItemActions = event.currentTarget as MenuItemActions;
					var child:* = target.getChildByName('popup');
					if (child) {
						child.labelField = 'label';
						child.dataProvider = items;
						child.addEventListener("itemClick", MenuController.onClick_PopUpMenu_ActionBtn); 
					} else {
						AlertPopUp.errorNoOkay('Programming Error - you should never see this message but you have so there is a problem and your menu cannot be edited at this time until this error has been resolved. Sorry...','ERROR MenuController.301');
					}
				});
			MenuController._registered_menuitems.addItem(aMenuItemObject);
		}
		
		public static function registerMenuItem(aMenuItemObject:*,parentSelector:String,parentClassName:String):void {
			MenuController.handle_registered_menuitem(aMenuItemObject,parentSelector,parentClassName);
		}
		
		public static function getMenuCount(parent:*):void {
            function onResultMenuCountJSON(event:ResultEvent):void {
				var response:*;
				try {
					response = event.result.getItemAt(0);
					response = (response is ObjectProxy) ? response.valueOf() : response;
					MenuController._numMenus = response.count;
				} catch (e:Error) {
					var stackTrace2:String = e.getStackTrace();
					AlertPopUp.errorNoOkay('<MenuController> :: 2.3\n' + e.message.toString() + '\n' + StringUtils.ellipsis(stackTrace2,1024),'ERROR MenuController.401');
				} finally {
	            	parent.enabled = true;
				}
            }
            
        	parent.enabled = false;
			var url:String = WmsAPI.api_Get_Menu_Count();
        	MenuController.ezREST.send(url, onResultMenuCountJSON, MenuController.ezREST.jsonResultType);
		}

		public static function getMenus():void {
			function onClickMenuChoiceBtn(event:MenuEvent):void {
				var menu:Menu = event.currentTarget as Menu;
				MenuController._currentSelectedMenuId = menu.selectedIndex;
				MenuController._currentSelectedMenu = event.item;
				menu.callLater(MenuController.getMenu);
			}
			
            function onResultMenusJSON(event:ResultEvent):void {
				var response:*;
				try {
					response = event.result.getItemAt(0);
					response = (response is ObjectProxy) ? response.valueOf() : response;

					MenuController._numMenus = 0;
	                var aMenu:Menu = new Menu();
	                var dp:Array = [{label: "Choose Menu..."}];
	                var node:Object;
	                for (var i:String in response) {
	                	node = response[i];
	                	node['label'] = node.name;
	                	dp.push(node);
	                	trace('getMenus::onResultMenusJSON --> ' + node.name);
	                	MenuController._numMenus++;
	                }
	                aMenu.dataProvider = dp;
	                aMenu.selectedIndex = 0;
	                aMenu.addEventListener("itemClick", onClickMenuChoiceBtn);
	                MenuController.controlPanel.dispatchEvent(new MenuChangedEvent(MenuChangedEvent.TYPE_MENU_CHANGED_EVENT,aMenu));
	                MenuController.controlPanel.dispatchEvent(new MenuDataChangedEvent(MenuDataChangedEvent.TYPE_MENU_DATA_CHANGED_EVENT));
	                trace('getMenus::onResultMenusJSON --> ' + MenuController.controlPanel.className + ', ' + 'MenuChangedEvent.TYPE_MENU_CHANGED_EVENT!');
	                if (MenuController._currentSelectedMenuId > 0) {
		            	MenuController._currentSelectedMenu = dp[MenuController._currentSelectedMenuId];
	                } else {
		            	MenuController._currentSelectedMenu = {};
		            	MenuController._currentSelectedMenuId = -1;
	                }
				} catch (e:Error) {
					var stackTrace2:String = e.getStackTrace();
					AlertPopUp.errorNoOkay('<MenuController> :: 2.6\n' + e.message.toString() + '\n' + StringUtils.ellipsis(stackTrace2,1024),'ERROR MenuController.501');
				} finally {
	            	parent.enabled = true;
	            	if (MenuController.callback is Function) {
	            		MenuController.callback();
	            	}
				}
            }
            
        	parent.enabled = false;
			var url:String = WmsAPI.api_Get_Menus();
        	MenuController.ezREST.send(url, onResultMenusJSON, MenuController.ezREST.jsonResultType);
		}

		public static function performMenuDelete(event:CloseEvent):void {
			var parent:* = MenuController._currentTargetMenuBar;
            function onResultMenuDeleteJSON(event:ResultEvent):void {
				var response:*;
				try {
					response = event.result.getItemAt(0);
					response = (response is ObjectProxy) ? response.valueOf() : response;
				} catch (e:Error) {
					var stackTrace2:String = e.getStackTrace();
					AlertPopUp.errorNoOkay('<MenuController> :: 2.4\n' + e.message.toString() + '\n' + StringUtils.ellipsis(stackTrace2,1024),'ERROR MenuController.601');
				} finally {
	            	parent.enabled = true;
	            	MenuController._currentTargetMenuBar.dataProvider = [];
	            	try { MenuController.reloadMenus_callback() } catch (e:Error) { }
	            	MenuController.getMenus();
				}
            }

        	if (event.detail == Alert.YES) {
            	parent.enabled = false;
				var url:String = WmsAPI.api_Delete_Menu_By_UUID(MenuController._currentSelectedMenu.uuid);
            	MenuController.ezREST.send(url, onResultMenuDeleteJSON, MenuController.ezREST.jsonResultType);
        	}
		}
						
        public static function onResultMenuJSON(event:ResultEvent):void {
			var response:*;
			var metafield:String = '';
			var datafield:String = '';
			var metadata:Object = {};
			var keys:Array = [];
			try {
				response = event.result.getItemAt(0);
				response = (response is ObjectProxy) ? response.valueOf() : response;
				response = ObjectUtils.locate_root(response);
				metafield = response.metafield;
				datafield = response.datafield;
				metadata = ObjectUtils.collector(response[metafield]);
				response = ObjectUtils.processor(response[datafield],ObjectUtils.urlDecode);
			} catch (err:Error) {
				var stackTrace1:String = err.getStackTrace();
				AlertPopUp.errorNoOkay('<MenuController> :: 2.8\n' + err.message + '\n' + StringUtils.ellipsis(stackTrace1,1024),'ERROR MenuController.701');
			}
			try {
            	MenuController.metaProvider = metadata;
            	MenuController.metafield = metafield;
            	MenuController.datafield = datafield;
            	MenuController._currentTargetMenuBar.dataProvider = response;

            	var aMessage:HTTPRequestMessage = event.token.message as HTTPRequestMessage;
            	var url:String = aMessage.url;
            	var protocol:String = URLUtils.protocol(url);
            	var domain:String = URLUtils.domain_with_port(url);
            	MenuController._currentTargetMenuBar.urlPrefix = protocol + "//" + domain;
            	
            	try { MenuController.reloadMenus_callback() } catch (e:Error) { }
 			} catch (e:Error) {
				var stackTrace2:String = e.getStackTrace();
				AlertPopUp.errorNoOkay('<MenuController> :: 2.9\n' + e.message.toString() + '\n' + StringUtils.ellipsis(stackTrace2,1024),'ERROR MenuController.801');
			} finally {
            	MenuController.parent.enabled = true;
				MenuController._isAdminEnabled = true;
            	MenuController.getMenus();
			}
        }
            
		public static function getMenu():void {
        	MenuController.parent.enabled = false;
			var url:String = WmsAPI.api_Get_Menu_By_UUID(MenuController._currentSelectedMenu.uuid);
        	MenuController.ezREST.send(url, MenuController.onResultMenuJSON, MenuController.ezREST.jsonResultType);
		}
						
		public static function handleMenuNameRenamePopUp(parent:*,popup:MenuNameRenamePopUp):void {
            function onResultMenuRenameJSON(event:ResultEvent):void {
				var response:*;
				var uuid:String;
				try {
					response = event.result.getItemAt(0);
					response = (response is ObjectProxy) ? response.valueOf() : response;
					uuid = response.uuid;
				} catch (e:Error) {
					var stackTrace2:String = e.getStackTrace();
					AlertPopUp.errorNoOkay('<MenuController> :: 2.2\n' + e.message.toString() + '\n' + StringUtils.ellipsis(stackTrace2,1024),'ERROR MenuController.1001');
				} finally {
	            	parent.enabled = true;
	            	MenuController.getMenus();
				}
            }

        	parent.enabled = false;
        	var menuName:String = popup.txt_new_menu_name.text;
			var url:String = WmsAPI.api_Rename_Menu_by_UUID(MenuController._currentSelectedMenu.uuid,menuName);
        	MenuController.ezREST.send(url, onResultMenuRenameJSON, MenuController.ezREST.jsonResultType);
		}
			
		public static function onClick_btnRenameSelectedMenu(event:Event):void {
			function popuUpRenameMenuNameEditor(menuName:String):void {
				var parent:* = MenuController.parent;
				parent.enabled = false;
				var popup:MenuNameRenamePopUp = PopUpManager.createPopUp(parent, MenuNameRenamePopUp, true) as MenuNameRenamePopUp;
				popup.width = 500;
				PopUpManager.centerPopUp(popup);
				popup.txt_current_menu_name.text = menuName;
				popup.btn_save.addEventListener(MouseEvent.CLICK, function (event:MouseEvent):void { parent.enabled = true; PopUpManager.removePopUp(popup); MenuController.handleMenuNameRenamePopUp(parent,popup); });
				popup.btn_dismiss.addEventListener(MouseEvent.CLICK, function (event:MouseEvent):void { parent.enabled = true; PopUpManager.removePopUp(popup); });
			}

			popuUpRenameMenuNameEditor(MenuController._currentSelectedMenu.name);
		}

		public static function popuUpNewMenuNameEditor(menuName:String,loggedIn:Boolean,loggedOut:Boolean):void {
			var parent:* = MenuController.parent;

			function handleMenuNamePopUp(popup:MenuNamePopUp):void {
            	parent.enabled = false;
            	var menuName:String = popup.txt_menu_name.text;
            	var bLoggedIn:Boolean = popup.isStateLoggedIn;
            	var bLoggedOut:Boolean = popup.isStateLoggedOut;
            	
            	function handle_menu_names_loaded(event:MenuDataChangedEvent):void {
            		MenuController.controlPanel.removeEventListener(MenuDataChangedEvent.TYPE_MENU_DATA_CHANGED_EVENT,handle_menu_names_loaded);
            		var aMenu:Menu = MenuController.controlPanel.btn_menuChoice.popUp as Menu;
            		var ac:ArrayCollection = aMenu.dataProvider as ArrayCollection;
            		var i:int = ArrayCollectionUtils.findIndexOfItem(ac,'label',menuName);
            		if (i > -1) {
	            		aMenu.selectedIndex = i;
	            		aMenu.dispatchEvent(new MenuEvent(MenuEvent.ITEM_CLICK));
            		}
            	}
            	
            	bLoggedIn = false;
            	bLoggedOut = true; // this is the default.
            	if (bLoggedIn == bLoggedOut) {
            		AlertPopUp.errorNoOkay('Cannot create a New Menu unless the menu state has been selected.','ERROR MenuController.1201',function ():void { parent.enabled = true; popuUpNewMenuNameEditor(menuName,bLoggedIn,bLoggedOut); });
            	} else {
            		MenuController.controlPanel.addEventListener(MenuDataChangedEvent.TYPE_MENU_DATA_CHANGED_EVENT, handle_menu_names_loaded);
	            	var state:String = (bLoggedIn) ? popup.symbol_logged_in : popup.symbol_logged_out;
					var url:String = MenuController.urlPrefix + '/rest/new/menu/' + StringUtils.urlEncode(menuName) + '/' + state + '/json/';
	            	MenuController.ezREST.send(url, MenuController.onResultMenuJSON, MenuController.ezREST.jsonResultType);
            	}
			}

			parent.enabled = false;
			var popup:MenuNamePopUp = PopUpManager.createPopUp(parent, MenuNamePopUp, true) as MenuNamePopUp;
			popup.width = 500;
			PopUpManager.centerPopUp(popup);
			popup.txt_menu_name.text = menuName;
			popup.rbLoggedIn.selected = loggedIn;
			popup.rbLoggedOut.selected = loggedOut;
			popup.btn_save.addEventListener(MouseEvent.CLICK, function (event:MouseEvent):void { parent.enabled = true; PopUpManager.removePopUp(popup); handleMenuNamePopUp(popup); });
			popup.btn_dismiss.addEventListener(MouseEvent.CLICK, function (event:MouseEvent):void { parent.enabled = true; PopUpManager.removePopUp(popup); });
		}
			
		public static function onClick_btnNewMenu(event:MouseEvent):void {
			MenuController.popuUpNewMenuNameEditor('',false,false);
		}
			
		public static function setMenuJSON(json:String):void {
	        function onResultSetMenuJSON(event:ResultEvent):void {
				var response:*;
				try {
					response = event.result.getItemAt(0);
					response = (response is ObjectProxy) ? response.valueOf() : response;
				} catch (e:Error) {
					var stackTrace2:String = e.getStackTrace();
					AlertPopUp.errorNoOkay('<MenuController> :: 2.3\n' + e.message.toString() + '\n' + StringUtils.ellipsis(stackTrace2,1024),'ERROR MenuController.1301');
				} finally {
	            	MenuController.parent.enabled = true;
	            	MenuController.getMenu();
				}
	        }

        	MenuController.parent.enabled = false;
			var url:String = WmsAPI.api_Set_Menu_by_UIUD(MenuController._currentSelectedMenu.uuid);
        	MenuController.ezREST.post(url, json, onResultSetMenuJSON, MenuController.ezREST.jsonResultType);
		}

        public static function onClick_save_admin_editor_popup(event:MouseEvent):void {
        	var popup:SmartMenuFlyoutItemAdmin = event.currentTarget.parentDocument as SmartMenuFlyoutItemAdmin;
        	var dataSelectors:* = popup.dataSelectors;

        	var label:String = popup.label_edit.text;
        	var url:String = popup.url_edit.text;
        	var new_window:Boolean = popup.cb_newWindow.selected;
        	var domain:* = popup.combo_domain.selectedItem;
        	var env_keys:Array = ObjectUtils.keys(domain);
        	var env_i:int = env_keys.indexOf('mx_internal_uid');
        	if (env_i > -1) {
        		env_keys.splice(env_i,1);
        		var new_env:Object = {};
        		for (var i:String in env_keys) {
        			new_env[env_keys[i]] = domain[env_keys[i]];
        		}
        		domain = new_env;
        	}

        	var menuitem:* = popup.dataProvider;
        	var metaData:Object = MenuController.metaProvider;

        	var source_dp:Object = popup.source.dataProvider;
			var aMenuItem:* = ObjectUtils.unpack(source_dp,ObjectUtils.criteria_unpack_isSomeKindOfObject);
			var isMenuItem:Boolean;
			try { isMenuItem = ( (aMenuItem is ArrayCollection) || (aMenuItem is Array) ) && (aMenuItem.length > 0) } catch (e:Error) { isMenuItem = false; }
        	var ar:Array = [];
        	var obj:Object = {};
        	var isEditing:Boolean = false;
			if (isMenuItem) {
				ar = (aMenuItem is ArrayCollection) ? aMenuItem.source : (aMenuItem is Array) ? aMenuItem : [];
				for (var j:String in ar) {
					if (ar[j].uuid == menuitem.uuid) {
						isEditing = true;
						obj = ar[j];
					}
				}
			}
        	obj[metaData.label] = label;
        	obj[metaData.url] = url;
        	obj[metaData.target] = (new_window) ? '_blank' : '_top';
        	obj[metaData.domain] = domain.name;
        	
        	if (isEditing == false) {
	        	obj['uuid'] = UIDUtil.createUID();
	        	ar.push(obj);
        	}

			if (isMenuItem == false) {
            	source_dp[MenuController.datafield] = ar;
			}
        	var src:Object = {};
        	src[MenuController.datafield] = MenuController._currentTargetMenuBar.dataProvider.source;
        	src[MenuController.metafield] = metaData;
        	src['metafield'] = MenuController.metafield;
        	src['datafield'] = MenuController.datafield;
        	var json:JSONEncoder = new JSONEncoder(src);
        	var s_json:String = json.getString();
        	PopUpManager.removePopUp(popup);
        	MenuController.setMenuJSON(s_json);
        }

		public static function handle_menuitem_update(uuid:String):void {
        	var metaData:Object = MenuController.metaProvider;
        	var dp:* = MenuController._currentTargetMenuBar.dataProvider;
        	var src:Object = {};
        	src[MenuController.datafield] = dp.source;
        	src[MenuController.metafield] = metaData;
        	src['metafield'] = MenuController.metafield;
        	src['datafield'] = MenuController.datafield;
        	var json:JSONEncoder = new JSONEncoder(src);
        	var s_json:String = json.getString();
        	MenuController.setMenuJSON(s_json);
		}
	}
}