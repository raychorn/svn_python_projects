package com.HAL.utils {
	import com.HAL.Alert.AlertPopUp;
	
	import mx.controls.Alert;
	
	public class LicenseUtils {
		public static const LICENSE_TRIAL:String = 'TRIAL';
		public static const LICENSE_STANDARD:String = 'STANDARD';
		public static const LICENSE_PRO:String = 'PRO';
		public static const LICENSE_ENTERPRISE:String = 'ENTERPRISE';
		
		private static var _isLicensed:Boolean = false;
		private static var _licenseLevel:String = LICENSE_TRIAL;
		
		private static var _licenseLevels:Object = {};
		
		private static var __licenseLevels:Array = [LicenseUtils.LICENSE_TRIAL, LicenseUtils.LICENSE_STANDARD, LicenseUtils.LICENSE_PRO, LicenseUtils.LICENSE_ENTERPRISE];
		
		public static function get allowedPackagesNumber():Number {
			if (LicenseUtils.isLicenseLevelTrial) {
				return 1;
			}
			return -1;
		}
		
		public static function get allowedArchivesNumber():Number {
			if (LicenseUtils.isLicenseLevelTrial) {
				return 1;
			}
			return -1;
		}
		
		public static function set licenseLevels(licenseLevels:Object):void {
			var i:int;
			var isValid:Boolean = true;
			var isFailure:Boolean = false;
			for (i = 0; i < LicenseUtils.__licenseLevels.length; i++) {
				if (licenseLevels[LicenseUtils.__licenseLevels[i]] == null) {
					isFailure = true;
					isValid = false;
					break;
				}
			}
			if ( (isFailure == false) && (isValid == true) ) {
				LicenseUtils._licenseLevels = licenseLevels;
			} else {
				var popUp:Alert = AlertPopUp.error('Unable to determine your License based on the information given, you may not be allowed to access all the features other than the TRIAL mode.','ERROR');
				popUp.styleName = 'ErrorAlert';
			}
		}
		
		public static function get licenseLevels():Object {
			return LicenseUtils._licenseLevels;
		}
		
		public static function set isLicensed(bool:Boolean):void {
			LicenseUtils._isLicensed = bool;
		}
		
		public static function get isLicensed():Boolean {
			return LicenseUtils._isLicensed;
		}

		public static function set licenseLevel(level:String):void {
			var isValid:Boolean = (LicenseUtils._licenseLevels[level] != null);
			if (isValid) {
				LicenseUtils._isLicensed = true;
				LicenseUtils._licenseLevel = level;
			}
		}
		
		public static function get licenseLevel():String {
			return LicenseUtils._licenseLevel;
		}

		public static function get isLicenseLevelTrial():Boolean {
			return (LicenseUtils._licenseLevel == LicenseUtils.LICENSE_TRIAL);
		}

		public static function get isLicenseLevelStandard():Boolean {
			return (LicenseUtils._licenseLevel == LicenseUtils.LICENSE_STANDARD);
		}

		public static function get isLicenseLevelPro():Boolean {
			return (LicenseUtils._licenseLevel == LicenseUtils.LICENSE_PRO);
		}

		public static function get isLicenseLevelEnterprise():Boolean {
			return (LicenseUtils._licenseLevel == LicenseUtils.LICENSE_ENTERPRISE);
		}
	}
}