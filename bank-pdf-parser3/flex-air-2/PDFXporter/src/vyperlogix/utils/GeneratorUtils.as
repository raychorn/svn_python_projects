package vyperlogix.utils {
	import vyperlogix.menu.builder.MenuController;
	
	public class GeneratorUtils {
		public static function isHomeNode(aGenerator:Generator):Boolean {
			var bool:Boolean = false;
			try {
				var aSource:Object = aGenerator.dataSource;
				if (aSource != null) {
					var aHeaderItem:Object = aSource[MenuController._currentTargetMenuBarDataProvider.headerData.name];
					if (aHeaderItem != null) {
						var anId:String = aHeaderItem[MenuController._currentTargetMenuBarDataProvider.metaData.hash.id];
						bool = (anId == 'home');
					}
				}
			} catch (err:Error) {}
			return bool;
		}

		public static function isTitleNode(aGenerator:Generator):Boolean {
			var i:String;
			var bool:Boolean = false;
			try {
				var sources:Array = aGenerator.dataSource;
				var aSource:Object;
				var aHeaderItem:Object;
				if (sources is Array) {
					for (i in sources) {
						aSource = sources[i];
						if (aSource != null) {
							var anId:String = aSource[MenuController._currentTargetMenuBarDataProvider.metaData.hash.id];
							bool = (anId == 'title');
						}
					}
				}
			} catch (err:Error) {}
			return bool;
		}

		public static function isProfileNode(aGenerator:Generator):Boolean {
			var i:String;
			var bool:Boolean = false;
			try {
				var sources:Array = aGenerator.dataSource;
				var aSource:Object;
				var aHeaderItem:Object;
				if (sources is Array) {
					for (i in sources) {
						aSource = sources[i];
						if (aSource != null) {
							var anId:String = aSource[MenuController._currentTargetMenuBarDataProvider.metaData.hash.id];
							bool = (anId == 'profile');
						}
					}
				}
			} catch (err:Error) {}
			return bool;
		}
	}
}