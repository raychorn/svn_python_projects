package com.vzw.controls.menuClasses
{
	import flash.display.DisplayObject;
	
	import mx.controls.Label;
	import mx.controls.menuClasses.MenuItemRenderer;

	public class SmartMenuItemRenderer extends MenuItemRenderer {
		//Space on the left before the branch icon (if there is one)
		private var leftMargin:int = 5;
		
		private var _label:Label;

		/**
		 * This class is used as the menuItemRenderer for vertical menus 
		 * that need to go to the left. It's nothing more than a simple
		 * extension of MenuItemRenderer that flips and repositions the 
		 * branch icon.
		 * */
		public function SmartMenuItemRenderer() {
			super();
		}
		
		/**
		 *  @private
		 */
		override protected function createChildren():void {
	        super.createChildren();
	
			this.createLabel(-1);
		}

	    /**
	     *  @private
	     *  Creates the title text field and adds it as a child of this component.
	     * 
	     *  @param childIndex The index of where to add the child.
		 *  If -1, the text field is appended to the end of the list.
	     */
	    private function createLabel(childIndex:int):void {
	        if (!this._label) {
	            this._label = new Label();
	            
				this._label.styleName = "SmartMenuItemLabel";

	            if (childIndex == -1)
	                this.addChild(DisplayObject(this._label));
	            else 
	                this.addChildAt(DisplayObject(this._label), childIndex);
	        }
	    }

		override protected function updateDisplayList(unscaledWidth:Number,	unscaledHeight:Number):void {
			super.updateDisplayList(unscaledWidth, unscaledHeight);

			/* We're going to flip the branchIcon by setting scaleX to -1. 
			 * This means we have to move it a bit to the right of where you
			 * might think it would go, since now the x,y position of 0,0 is the
			 * top-right corner, not the top-left.
			 */
			if (branchIcon) {
				branchIcon.scaleX = -1;
				branchIcon.x = leftMargin + branchIcon.width;
			}
		}
	}
}