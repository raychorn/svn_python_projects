package vyperlogix.controls.renderers {
	import vyperlogix.utils.ObjectExplainer;
	import vyperlogix.utils.StringUtils;
	
	import flash.events.Event;
	
	import mx.controls.CheckBox;

	public class CheckBoxRenderer extends CheckBox {
		public function CheckBoxRenderer() {
			super();
			this.addEventListener(Event.CHANGE, onChangeHandler); // => Add listener to detect change in selected
		}

		override public function set data(value:Object):void {  // Override the set method for the data property.
			super.data = value;                                 // => Make sure there is data
			if (value != null) {
				if (value is String) {
					this.label = new String(value);
				} else if (value is Object) {
					try {
						this.label = value.label;                       // => Set the label
						this.selected = value.isSelected;               // => Set the selected property             
					} catch (e:Error) {this.label = new String(value);}
				}
			}
			                                                    // => Invalidate display list,
			super.invalidateDisplayList();                      // => If checkbox is now selected, we need to redraw         
		}

		private function onChangeHandler(event:Event):void { // => Handle selection change
			super.data.isSelected = !super.data.isSelected;
			trace(this.className + '::onChangeHandler().1 --> super.data.isSelected=' + super.data.isSelected);
			trace(this.className + '::onChangeHandler().2 --> super.data=' + (new ObjectExplainer(super.data)).explainThisWay());
			trace(StringUtils.repeatedChars('=',30) + '\n\n');
		}
	}
}
