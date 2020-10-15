package com.HAL.utils {
	import flash.text.AntiAliasType;
	import flash.text.GridFitType;
	import flash.text.TextLineMetrics;
	
	import mx.core.UITextFormat;
	import mx.managers.ISystemManager;
	
	public class Misc {
		public static var systemManager:ISystemManager;

		public static function computeTextMetricsForString(str:String):TextLineMetrics {
			var ut:UITextFormat = new UITextFormat(Misc.systemManager, str);
			ut.antiAliasType = AntiAliasType.NORMAL;
			ut.gridFitType = GridFitType.PIXEL;
			var lineMetrics:TextLineMetrics = ut.measureText(str);
			return lineMetrics;
		}
		
		public static function computeTextWidthForString(str:String):Number {
			var m:TextLineMetrics = computeTextMetricsForString(str);
			return m.width + m.leading;
		}
	}
}