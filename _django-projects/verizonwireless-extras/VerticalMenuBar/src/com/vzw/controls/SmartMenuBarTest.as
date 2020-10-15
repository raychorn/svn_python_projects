package com.vzw.controls
{
	import com.vzw.controls.menuClasses.SmartMenuItemRenderer;
	
	import flash.display.DisplayObject;
	import flash.geom.Point;
	import flash.geom.Rectangle;
	
	import mx.controls.Label;
	import mx.controls.Menu;
	import mx.controls.MenuBar;
	import mx.controls.TextArea;
	import mx.controls.menuClasses.IMenuBarItemRenderer;
	import mx.controls.menuClasses.MenuBarItem;
	import mx.controls.menuClasses.MenuItemRenderer;
	import mx.core.ClassFactory;
	import mx.core.IFlexDisplayObject;
	import mx.core.UITextField;
	import mx.events.MenuEvent;
	import mx.managers.ISystemManager;
	
	import vyperlogix.utils.EzObjectExplainer;
	import vyperlogix.utils.XMLUtils;

	public class SmartMenuBarTest extends MenuBar {
   		private static const MARGIN_HEIGHT:int = 0;		
	    
	    /**
	    * There are two possiblities for direction: left or right. Here we define
	    * these two constants that you should use in your AS code to change the
	    * direction of the SmartMenuBarTest. So to change the direction the code would
	    * be something like: 
	    * menubar.direction = SmartMenuBarTest.LEFT;
	    */
	    public static const LEFT:String = "left";
	    public static const RIGHT:String = "right";
	    
	    public static const VERTICAL:String = "vertical";
	    public static const HORIZONTAL:String = "horizontal";

	    /**
	    * We're storing a variable to specify direction. This can be set via MXML
	    * or Actionscript. The direction will take effect the next time a menu item
	    * is clicked.
	    */
	    private var _orientation:String = SmartMenuBarTest.HORIZONTAL;
	    private var _direction:String = SmartMenuBarTest.RIGHT;

	    private var _debugger:TextArea;

	    private var _alignField:String = 'align';
		
		public function get debugger():TextArea {
			return this._debugger;
		}
		
		public function set debugger(value:TextArea):void {
			if (this._debugger != value) {
				this._debugger = value;
			}		
		}
		
		public function get direction():String {
			return this._direction;
		}
		
		public function set direction(value:String):void {
			if ( (this._direction != value) && ( (value == SmartMenuBarTest.LEFT) || (value == SmartMenuBarTest.RIGHT) ) ) {
				this._direction = value;
			}		
		}
		
		public function get orientation():String {
			return this._orientation;
		}
		
		public function set orientation(value:String):void {
			if ( (this._orientation != value) && ( (value == SmartMenuBarTest.HORIZONTAL) || (value == SmartMenuBarTest.VERTICAL) ) ) {
				this._orientation = value;
			}		
		}
		
		public function get is_orientation_horizontal():Boolean {
			return this.orientation == SmartMenuBarTest.HORIZONTAL;
		}
		
		public function get is_orientation_vertical():Boolean {
			return this.orientation == SmartMenuBarTest.VERTICAL;
		}
		
		public function get alignField():String {
			return this._alignField;
		}
		
		public function set alignField(value:String):void {
			if (this._alignField != value) {
				this._alignField = value;
			}		
		}
		
		public function SmartMenuBarTest() {
			super();
		}
		
	    override public function set dataProvider(value:Object):void {
	        super.dataProvider = value;
	    }
	    
	    /**
	     *  @private
	     */
	    private var background:IFlexDisplayObject;

		/**
	     *  Changed to calculate based on vertical layout. Pretty much
	     *  the same code as in MenuBar, but instad of using the X and width
	     *  properties, now we're using Y and height.
	     */
		override protected function updateDisplayList(unscaledWidth:Number, unscaledHeight:Number):void {
	        super.updateDisplayList(unscaledWidth, unscaledHeight);
	
			if (this.is_orientation_vertical) {
				var lastY:Number = 0;
				var lastH:Number = 0;
				
		        var len: int = menuBarItems.length;
		
		        var clipContent:Boolean = false;
		        var hideItems:Boolean = (unscaledWidth == 0 || unscaledHeight == 0);
		
		        for (var i:int = 0; i < len; i++) {
		            var item:IMenuBarItemRenderer = menuBarItems[i];
		
		            item.setActualSize(unscaledWidth, item.getExplicitOrMeasuredHeight());
		            item.visible = !hideItems;
		
					item.move(0, lastY + lastH);
					
		            lastY = item.y = lastY+lastH;
		            lastH = item.height;
		            
		            if (!hideItems &&
		                (item.getExplicitOrMeasuredWidth() > unscaledWidth ||
		                 (lastY + lastH) > unscaledHeight)) {
		                clipContent = true;
		            }
		            
		        }
		        
		        if (background) {
		            background.setActualSize(unscaledWidth, unscaledHeight);
		            background.visible = !hideItems;
		        }
				
		        // Set a scroll rect to handle clipping.
		        scrollRect = clipContent ? new Rectangle(0, 0, unscaledWidth, unscaledHeight) : null;
			}
	    }
	    
	    /**
	     *  Changed to calculate based on vertical layout. Pretty much
	     *  the same code as in MenuBar, but instad of using the X and width
	     *  properties, now we're using Y and height.
	     */
	    override protected function measure():void
	    {
	        super.measure();
	
			if (this.is_orientation_vertical) {
		        var len:int = menuBarItems.length;
		
		        measuredHeight = 0;
		
		        measuredWidth = DEFAULT_MEASURED_MIN_WIDTH; 
		        for (var i:int = 0; i < len; i++) {
		            measuredHeight += menuBarItems[i].getExplicitOrMeasuredHeight();
		            measuredWidth = Math.max(measuredWidth, menuBarItems[i].getExplicitOrMeasuredWidth());
		        }
		
		        if (len > 0) {
		            measuredHeight += 2 * MARGIN_HEIGHT;
		        } else { 
		            measuredHeight = DEFAULT_MEASURED_MIN_HEIGHT;
		        } 
		
		        measuredMinWidth = measuredWidth;
		        measuredMinHeight = measuredHeight;
			}
	    }
	   
    	/**
    	 * We're overriding getMenuAt for two reasons. First, we set a custom itemRenderer for 
    	 * the menu if we're supposed to be facing left. Second, we add a listener that gets 
    	 * executed when the menu is shown. The secret to what we're doing is we're repositiong
    	 * the menu only after it has been positioned originally by the mx.controls.MenuBar class.
    	 * This allows us to not have to override a ton of private methods of the MenuBar class.
    	 * The fundamental problem with extending MenuBar for our purposes is that the showMenu 
    	 * method is private. If showMenu was protected we might be able to just override that
    	 * and specify our own coordinates for where to place the menu. But instead, we do it
    	 * a sneaky way and try to move the Menu the instant it gets shown.
    	 */
	    override public function getMenuAt(index:int):Menu
	    {
	    	var menu:Menu = menus[index];
	    	
	    	var wasNull:Boolean = (menu == null);
	    	
	    	menu = super.getMenuAt(index);
	    	
			var is_directon_reversed:Boolean = false;
	    	try {
	    		var ez:EzObjectExplainer;
		    	var xml:XML = menu.dataProvider[0];
		    	var oXML:Object = XMLUtils.convertXmlToObject(xml);
		    	var labelField:String = menu.labelField.replace('@','');
		    	var aLabel:String = oXML.menuitem[labelField];
		    	var alignField:String = this.alignField.replace('@','');
		    	var align:String = oXML.menuitem[alignField];
		    	
		    	ez = new EzObjectExplainer(oXML);

				this.debugger.text = this.className + ' :: ' + '(getMenuAt).1 ' + ', aLabel=' + aLabel + '\n' + this.debugger.text; 
				this.debugger.text = this.className + ' :: ' + '(getMenuAt).2 ' + ', labelField=' + labelField + '\n' + this.debugger.text; 
				this.debugger.text = this.className + ' :: ' + '(getMenuAt).3 ' + ', align=' + align + '\n' + this.debugger.text; 
				this.debugger.text = this.className + ' :: ' + '(getMenuAt).4 ' + ', alignField=' + alignField + '\n' + this.debugger.text; 

				this.debugger.text = this.className + ' :: ' + '(getMenuAt).5.1 ' + ez.explainThisWay() + '\n' + this.debugger.text; 
		    	
		    	is_directon_reversed = (align == 'left');
				this.debugger.text = this.className + ' :: ' + '(getMenuAt).5.2 ' + ((is_directon_reversed) ? '<<' : '>>') + '\n' + this.debugger.text; 

		    	var num_kids:int = this.numChildren;
		    	var aMenuBarItem:*;
		    	var aMenuBarItem_numChildren:Number;
		    	var anObj:*;
		    	var aMenuBarItem_label:*;
				var x:Number;
				var w:Number;
				var xP:Number;
				var wP:Number;
				var now:Date = new Date();
				var width_total:Number = 0;
				var type:String;
		    	for (var i:int = 0; i < num_kids; i++) {
		    		aMenuBarItem = this.getChildAt(i);
		    		if (aMenuBarItem is MenuBarItem) {
    					x = aMenuBarItem.x;
    					w = aMenuBarItem.width;
			    		aMenuBarItem_numChildren = aMenuBarItem.numChildren;
			    		for (var j:int = 0; j < aMenuBarItem_numChildren; j++) {
			    			anObj = aMenuBarItem.getChildAt(j);
			    			if ( (anObj is UITextField) || (anObj is Label) ) {
			    				aMenuBarItem_label = anObj;
			    				if (aMenuBarItem_label.text == aLabel) {
			    					xP = aMenuBarItem.parent.x;
			    					wP = aMenuBarItem.parent.width;
			    					this.debugger.text = this.className + ' :: ' + '(getMenuAt).6.1 ' + ((is_directon_reversed) ? '<<' : '>>') + ' (' + aLabel + ') ' + '[' + index + '] ' + 'x=' + x.toString() + ',w=' + w.toString() + ',xP=' + xP.toString() + ',wP=' + wP.toString() + ', width_total=' + width_total.toString() + '\n' + this.debugger.text; 
			    					if (w+w >= width_total) {
			    						is_directon_reversed = true;
			    					} 
			    					this.debugger.text = this.className + ' :: ' + '(getMenuAt).6.2 ' + ((is_directon_reversed) ? '<<' : '>>') + ' (' + aLabel + ') ' + '[' + index + '] ' + 'x=' + x.toString() + ',w=' + w.toString() + ',xP=' + xP.toString() + ',wP=' + wP.toString() + ', width_total=' + width_total.toString() + '\n' + this.debugger.text; 
			    				} 
			    			}
			    		}
			    		width_total += w;
		    		}
		    	}
				this.debugger.text = this.className + ' (getMenuAt).7 ' + '================================================================================' + '\n' + this.debugger.text; 
	    	} catch (e:Error) { }
	       	
	       	//is_directon_reversed = true;
			this.debugger.text = this.className + ' :: ' + '(getMenuAt).8 ' + 'is_directon_reversed=(' + is_directon_reversed + ') ' + ', this.is_orientation_vertical=(' + this.is_orientation_vertical + ') ' + '\n' + this.debugger.text; 
			if (this.is_orientation_vertical) {
		       	if (is_directon_reversed) {
		        	menu.itemRenderer = new ClassFactory(SmartMenuItemRenderer);
					this.debugger.text = this.className + ' :: ' + '(getMenuAt).9 ' + 'SmartMenuItemRenderer! ' + '\n' + this.debugger.text; 
		        } else {
		        	menu.itemRenderer = new ClassFactory(MenuItemRenderer);
					this.debugger.text = this.className + ' :: ' + '(getMenuAt).10 ' + 'MenuItemRenderer! ' + '\n' + this.debugger.text; 
		        }
		        /* Now here's a sneaky part. First, we elminate the openDuration
		         * because that screws the whole thing up. If openDuration is not 1, then
		         * menu shows the opening tween prior to shifting the menu to the
		         * left or right, so we see the menu visibly jump. That's no good.
		         * And if we set the openDuration to 0 I've noticed unexplained behavior
		         * that messes up showing an Alert box. I have no idea why.
		         */
		        if (wasNull) {
		        	menu.setStyle("openDuration", 1);
		       		
		       		/* This is the listener that gets executed when the menu is shown.
		       		 * Basically we're going to wait until the menu is shown, and then
		       		 * quickly move it over to the right or left.
		       		 */
		       		menu.addEventListener("menuShow", this.moveMenuOnShow);
		        }
			} else {
	        	menu.itemRenderer = new ClassFactory(SmartMenuItemRenderer);
				this.debugger.text = this.className + ' :: ' + '(getMenuAt).11 ' + 'SmartMenuItemRenderer! ' + '\n' + this.debugger.text; 
			}
	        return menu;
	    }
    	
	    private function moveMenuOnShow(event:MenuEvent):void {
	    	var menu:Menu = event.menu;
	    	var menuBar:MenuBar = event.menuBar;
	    	var parentMenu:Menu = menu.parentMenu;

	    	/* OK, cool, we're going to shift the Menu. But we need to use callLater
	    	 * because we need to first update the Menu's x and y position so we can
	    	 * use that to shift the menu over 
	    	 */
	    	if(parentMenu == null) {
	    		var item:IMenuBarItemRenderer = menuBar.menuBarItems[menuBar.selectedIndex];
	
	    		callLater(this.shiftRootMenu, [menu, menuBar, item]);
	    	}
	    	else {
	    		callLater(this.shiftSubMenu, [menu, parentMenu]);
	    	}
	    }
	    
	    /** 
	     * If we're showing the menu to the left, then we need to shift the submenus
	     * to the left as well. Normal functionality is to show the submenu
	     * to the right of the parent menu. So if we're facing right then
	     * we don't need to shift the submenu at all.
	     */
	    private function shiftSubMenu(menu:Menu, parentMenu:Menu):void {    	
			this.debugger.text = this.className + ' (shiftSubMenu) ' + 'this._direction=' + this._direction + ', SmartMenuBarTest.LEFT=' + SmartMenuBarTest.LEFT + ', SmartMenuBarTest.RIGHT=' + SmartMenuBarTest.RIGHT + '\n' + this.debugger.text; 
	    	if (this._direction == SmartMenuBarTest.LEFT) {
	    		menu.move(parentMenu.x - menu.width, menu.y);
	    	}
	    }
	    
	    /** 
	     * The root menus always need to be shifted, either to the right or to the left.
	     * The default Menu functionality is to show the menu directly below the MenuItem.
	     * So we just shift the Menu from where the default places it, and move it to the
	     * right or the left. We also move it up higher, to be at the same y position as 
	     * the MenuItem.
	     */
	    private function shiftRootMenu(menu:Menu, menuBar:MenuBar, item:IMenuBarItemRenderer):void {    	
	    	
	    	/* Here's some code taken from the MenuBar class from the showMenu method
	    	 * that's used to calculcate the position that we need to place the menu.
	    	 * It's only been modified to adjust the menu to the right or the left of 
	    	 * the current item.
	    	 */
	    	var pt:Point = new Point(0, 0);
	        pt = DisplayObject(item).localToGlobal(pt);
	        
			this.debugger.text = this.className + ' (shiftRootMenu) ' + 'this._direction=' + this._direction + ', SmartMenuBarTest.LEFT=' + SmartMenuBarTest.LEFT + ', SmartMenuBarTest.RIGHT=' + SmartMenuBarTest.RIGHT + '\n' + this.debugger.text; 
	        if (this._direction == SmartMenuBarTest.LEFT) {
	        	pt.x -= menu.width;
	        } else {
	        	pt.x += item.width;
	        }
	        
	        pt.y -= item.height;
	        
	        var sm:ISystemManager = systemManager;
	        
	        // check to see if we'll go offscreen
	        if (pt.y + item.height + 1 + menu.getExplicitOrMeasuredHeight() > screen.height + screen.y) {
	            pt.y -= menu.getExplicitOrMeasuredHeight();
	        } else {
	            pt.y += item.height + 1;
	        }
	        if (pt.x + menu.getExplicitOrMeasuredWidth() > screen.width + screen.x) {
	            pt.x = screen.x + screen.width - menu.getExplicitOrMeasuredWidth();
	        }
	        pt = DisplayObject(sm.topLevelSystemManager).globalToLocal(pt);
	    	
			this.debugger.text = this.className + ' (shiftRootMenu) ' + 'pt=' + pt.toString() + '\n' + this.debugger.text; 
	    	menu.move(pt.x, pt.y);
	    }
	    
	}
}