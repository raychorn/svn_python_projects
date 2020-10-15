package vyperlogix.controls.Alert {
	import mx.controls.alertClasses.AlertForm;
	import mx.core.IUITextField;
	import mx.core.UITextField;
	import flash.display.DisplayObject;

	public class ButtonlessAlertForm extends AlertForm {
		public function ButtonlessAlertForm() {
			super();
		}
		
		private var icon:DisplayObject;
		private var textField:IUITextField;

		private function createTextField(childIndex:int):void {
		    if (!textField) {
				textField = IUITextField(createInFontContext(UITextField));
		
				textField.styleName = this;
				textField.text = ButtonlessAlert(parent).text;
				textField.multiline = true;
				textField.wordWrap = true;
				textField.selectable = true;
		
		        if (childIndex == -1) {
		            addChild(DisplayObject(textField));
		        } else { 
		            addChildAt(DisplayObject(textField), childIndex);
		        }
		    }
		}

		override protected function createChildren():void {
			// Create the UITextField to display the message.
			this.createTextField(-1);
	
			// Create the icon object, if any.
			var iconClass:Class = ButtonlessAlert(parent).iconClass;
			if (iconClass && !icon) {
				icon = new iconClass();
				addChild(icon);
			}
		}
	}
}