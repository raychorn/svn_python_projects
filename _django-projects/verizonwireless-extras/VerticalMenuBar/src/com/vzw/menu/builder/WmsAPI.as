package com.vzw.menu.builder {
	import vyperlogix.utils.URLUtils;
	
	public class WmsAPI {
		private static var accessMode:Boolean = false; // true for external otherwise false for internal.
		
		private static var _urlPrefix:String = '';

        private static var _api_Get_Menu_Count:String = '';
        private static var _api_Delete_Menu_By_UUID:String = '';
        private static var _api_Get_Menu_By_UUID:String = '';
        private static var _api_Rename_Menu_by_UUID:String = '';
        private static var _api_Get_Menus:String = '';
        private static var _api_Set_Menu_by_UIUD:String = '';
        private static var _api_New_Menu:String = '';

		private static var internal_urlPrefix:String = 'http://127.0.0.1:8888';

		private static var external_urlPrefix:String = '';
		
        private static var symbol_uuid_token:String = '%uuid%';
        private static var symbol_state_token:String = '%state%';
        private static var symbol_name_token:String = '%name%';

        private static var internal_api_Get_Menu_Count:String = '/rest/get/menu/count/json/';
        private static var internal_api_Delete_Menu_By_UUID:String = '/rest/delete/menu/' + WmsAPI.symbol_uuid_token + '/json/';
        private static var internal_api_Get_Menu_By_UUID:String = '/rest/get/menu/' + WmsAPI.symbol_uuid_token + '/json/';
        private static var internal_api_Rename_Menu_by_UUID:String = '/rest/rename/menu/' + WmsAPI.symbol_name_token + '/' + WmsAPI.symbol_uuid_token + '/json/';
        private static var internal_api_Get_Menus:String = '/rest/get/menus/json/';
        private static var internal_api_Set_Menu_by_UIUD:String = '/rest/set/menu/' + WmsAPI.symbol_uuid_token + '/json/';
        private static var internal_api_New_Menu:String = '/rest/new/menu/' + WmsAPI.symbol_uuid_token + '/json/';

        private static var external_api_Get_Menu_Count:String = '/WMSWeb/globalnav?action=getMenuCount';
        private static var external_api_Delete_Menu_By_UUID:String = '/WMSWeb/globalnav?action=deleteMenu&uuid=' + WmsAPI.symbol_uuid_token;
        private static var external_api_Get_Menu_By_UUID:String = '/WMSWeb/globalnav?action=getMenuByUuid&uuid=' + WmsAPI.symbol_uuid_token;
        private static var external_api_Rename_Menu_by_UUID:String = '/WMSWeb/globalnav?action=renameMenuByUuid&uuid=' + WmsAPI.symbol_uuid_token + '&name=' + WmsAPI.symbol_name_token;
        private static var external_api_Get_Menus:String = '/WMSWeb/globalnav?action=getMenus';
        private static var external_api_Set_Menu_by_UIUD:String = '/WMSWeb/globalnav?action=setMenuByUuid&uuid=' + WmsAPI.symbol_uuid_token;
        private static var external_api_New_Menu:String = '/WMSWeb/globalnav?action=newMenu';

        public static function api_Get_Menus():String {
        	return WmsAPI._api_Get_Menus;
        }

        public static function api_Get_Menu_Count():String {
        	return WmsAPI._api_Get_Menu_Count;
        }
        
        public static function api_Rename_Menu_by_UUID(uuid:String,menuName:String):String {
        	return WmsAPI._api_Rename_Menu_by_UUID.replace(WmsAPI.symbol_uuid_token,uuid).replace(WmsAPI.symbol_name_token,menuName);
        }
        
        public static function api_Get_Menu_By_UUID(uuid:String):String {
        	return WmsAPI._api_Get_Menu_By_UUID.replace(WmsAPI.symbol_uuid_token,uuid);
        }
        
        public static function api_Set_Menu_by_UIUD(uuid:String):String {
        	return WmsAPI._api_Set_Menu_by_UIUD.replace(WmsAPI.symbol_uuid_token,uuid);
        }

        public static function api_Delete_Menu_By_UUID(uuid:String):String {
        	return WmsAPI._api_Delete_Menu_By_UUID.replace(WmsAPI.symbol_uuid_token,uuid);
        }

        public static function set_access_mode(accessMode:Boolean):Boolean {
        	if (WmsAPI.external_urlPrefix.length == 0) {
        		accessMode = false;
        	}
        	WmsAPI.accessMode = accessMode;
        	WmsAPI._urlPrefix = (WmsAPI.accessMode) ? WmsAPI.external_urlPrefix : WmsAPI.internal_urlPrefix;

	        WmsAPI._api_Get_Menu_Count = (WmsAPI.accessMode) ? WmsAPI.external_urlPrefix + WmsAPI.external_api_Get_Menu_Count : WmsAPI.internal_urlPrefix + WmsAPI.internal_api_Get_Menu_Count;
	        WmsAPI._api_Delete_Menu_By_UUID = (WmsAPI.accessMode) ? WmsAPI.external_urlPrefix + WmsAPI.external_api_Delete_Menu_By_UUID : WmsAPI.internal_urlPrefix + WmsAPI.internal_api_Delete_Menu_By_UUID;
	        WmsAPI._api_Get_Menu_By_UUID = (WmsAPI.accessMode) ? WmsAPI.external_urlPrefix + WmsAPI.external_api_Get_Menu_By_UUID : WmsAPI.internal_urlPrefix + WmsAPI.internal_api_Get_Menu_By_UUID;
	        WmsAPI._api_Rename_Menu_by_UUID = (WmsAPI.accessMode) ? WmsAPI.external_urlPrefix + WmsAPI.external_api_Rename_Menu_by_UUID : WmsAPI.internal_urlPrefix + WmsAPI.internal_api_Rename_Menu_by_UUID;
	        WmsAPI._api_Get_Menus = (WmsAPI.accessMode) ? WmsAPI.external_urlPrefix + WmsAPI.external_api_Get_Menus : WmsAPI.internal_urlPrefix + WmsAPI.internal_api_Get_Menus;
	        WmsAPI._api_Set_Menu_by_UIUD = (WmsAPI.accessMode) ? WmsAPI.external_urlPrefix + WmsAPI.external_api_Set_Menu_by_UIUD : WmsAPI.internal_urlPrefix + WmsAPI.internal_api_Set_Menu_by_UIUD;
	        WmsAPI._api_New_Menu = (WmsAPI.accessMode) ? WmsAPI.external_urlPrefix + WmsAPI.external_api_New_Menu : WmsAPI.internal_urlPrefix + WmsAPI.internal_api_New_Menu;

        	return WmsAPI.accessMode;
        }

        public static function initialize(application:*):Boolean {
        	try {
        		// +++ Read the config file and determine if the domain name is specified or not.
        		// +++ If domain is not specified use the domain from the application.url.
        		// +++ Read-in all the API URLs and initialize them here.
        		var domain:String = URLUtils.domain(application.url);
        		WmsAPI.external_urlPrefix = (domain.length == 0) ? WmsAPI.internal_urlPrefix : domain;
        		WmsAPI.set_access_mode((domain.length == 0) ? false : true);
        	} catch (e:Error) { return false; }
        	return true;
        }

	}
}