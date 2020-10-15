package com.HAL.utils {
	import com.HAL.Alert.AlertPopUp;
	import com.HAL.sockets.views.dialogs.NewFolderDialog;
	
	import flash.filesystem.File;
	
	import mx.controls.Alert;
	import mx.controls.FileSystemList;
	import mx.events.CloseEvent;
	import mx.managers.PopUpManager;
	
	public class FileListUtils {
		private static var _currentFile:File;
		private static var _currentCallback:Function;
		
		public static function isRoot(name:String):Boolean {
			return (name.indexOf('root$:/') > -1);
		}

		public static function isFileListAtRoot(fList:FileSystemList):Boolean {
			return (fList.canNavigateUp == false);
		}

		public static function makeFolder(folderPath:String):Boolean {
			var dir:File = File.userDirectory.resolvePath(folderPath);
			dir.createDirectory();
			if (dir.exists) {
				return true;
			} else {
				var popUp:Alert = AlertPopUp.error("Unable to create the folder ''" + folderPath + "'.", "ERROR");
				popUp.styleName = 'ErrorAlert';
			}
			return false;
		}

        public static function showNewFolderDialog(parent:*, pathName:String, callback:Function, isModal:Boolean):NewFolderDialog {
            var dialog:NewFolderDialog = NewFolderDialog(PopUpManager.createPopUp(parent, NewFolderDialog, isModal));
            dialog.callback = callback;
            dialog.pathName = pathName;
            dialog.title = 'New Folder Dialog - Type the name of a new folder.';
            dialog.width = parent.width-20;
            PopUpManager.centerPopUp(dialog);
            return dialog;
        }

		private static function dummyFileDeletionCallback(file:File,isDeleted:Boolean):void {
			// This is a do-nothing dummy callback just to show how to handle this in the future...
		}
		
		private static function onCloseDialogConfirmDeletion(event:CloseEvent):void {
			var popUp:Alert;
			var isDeleted:Boolean = true;
			if (event.detail == Alert.YES) {
				var oFile:File = _currentFile;
				if (oFile) {
					if (oFile.isDirectory == false) {
						oFile.deleteFile();
					} else if (oFile.getDirectoryListing().length == 0) {
						oFile.deleteDirectory();
					} else {
						isDeleted = false;
						popUp = AlertPopUp.error(oFile.name + ' cannot been deleted because it is a folder that is not empty.', "WARNING");
						popUp.styleName = 'ErrorAlert';
					}
					try { _currentCallback(_currentFile,isDeleted); } catch (err:Error) { }
				}
				popUp = AlertPopUp.info(oFile.name + ' has been deleted.', "INFO");
				popUp.styleName = 'InfoMsgAlert';
			}
		}
		
		public static function confirmFileOrDirectoryDeletion(file:File,callback:Function=null):void {
			var popUp:Alert;
			_currentFile = file;
			_currentCallback = ((callback == null) ? dummyFileDeletionCallback : callback);
			try {
				var msg:String = 'Are you sure you want to delete "' + file.name + '" ?';
				popUp = AlertPopUp.confirm(msg, "CONFIRMATION", onCloseDialogConfirmDeletion);
				popUp.styleName = 'ConfirmAlert';
			} catch (err:Error) {
				popUp = AlertPopUp.error(err.message, "ERROR");
				popUp.styleName = 'ErrorAlert';
			}
		}
	}
}