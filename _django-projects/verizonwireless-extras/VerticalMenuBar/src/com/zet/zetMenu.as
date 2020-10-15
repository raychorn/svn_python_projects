package com.zet {

import flash.display.DisplayObject;
import flash.display.DisplayObjectContainer;
import flash.display.Graphics;
import flash.display.Sprite;
import flash.events.MouseEvent;
import flash.geom.Point;
import flash.geom.Rectangle;

import mx.controls.Menu;
import mx.controls.listClasses.IListItemRenderer;
import mx.controls.menuClasses.IMenuItemRenderer;
import mx.core.Application;
import mx.core.ClassFactory;
import mx.core.EventPriority;
import mx.core.FlexSprite;
import mx.core.UIComponent;
import mx.core.UIComponentGlobals;
import mx.core.mx_internal;
import mx.effects.Tween;
import mx.events.MenuEvent;
import mx.managers.PopUpManager;

use namespace mx_internal;

/**
 *  Custom Menu class that reallocates menu items when they are about to
 *  move beyond the screen bounds.
 */
public class ZetMenu extends mx.controls.Menu {
    include "../core/Version.as";

    //------------------------------------------------------------
    //
    //  Constructor
    //
    //------------------------------------------------------------

    /**
     *  Constructor
     */
    public function ZetMenu() {
        itemRenderer = new ClassFactory(MenuItemRenderer);
        setRowHeight(19);
        iconField = "icon";

        visible = false;
    }

    //------------------------------------------------------------
    //
    //  Variables
    //
    //------------------------------------------------------------

    /**
     *  @private
     */
    private var direction:String = "right";

    /**
     *  @private
     */
    private var verticalDirection:String = "bottom";

    /**
     *  @private
     */
    private var subMenu:ZetMenu;

    /**
     *  Creates and returns an instance of the Menu class. The Menu control's
     *  content is determined by the method's <code>mdp</code> argument. The
     *  Menu control is placed in the parent container specified by the
     *  method's <code>parent</code> argument.
     *
     *  This method does not show the Menu control. Instead,
     *  this method just creates the Menu control and allows for modifications
     *  to be made to the Menu instance before the Menu is shown. To show the
     *  Menu, call the <code>Menu.show()</code> method.
     *
     *  @param parent A container that the PopUpManager uses to place the Menu
     *  control in. The Menu control may not actually be parented by this object.
     *
     *  @param mdp The data provider for the Menu control.
     *  @see mx.controls.Menu@dataProvider
     *
     *  @param showRoot A Boolean flag that specifies whether to display the
     *  root node of the data provider.
     *  @see mx.controls.Menu@showRoot
     *
     *  @return An instance of the Menu class.
     *
     *  @see mx.controls.Menu#popUpMenu()
     */
    public static function createMenu(parent:DisplayObjectContainer, mdp:Object, showRoot:Boolean = true):ZetMenu {
        var menu:ZetMenu = new ZetMenu();
        menu.tabEnabled = false;
        menu.owner = DisplayObjectContainer(Application.application);
        menu.showRoot = showRoot;
        popUpMenu(menu, parent, mdp);

        return menu;
    }

    /**
     *  Sets the dataProvider of an existing Menu control and places the Menu
     *  control in the specified parent container.
     *
     *  This method does not show the Menu control; you must use the
     *  <code>Menu.show()</code> method to display the Menu control.
     *
     *  The <code>Menu.createMenu()</code> method uses this method.
     *
     *  @param menu Menu control to popup.
     *
     *  @param parent A container that the PopUpManager uses to place the Menu
     *  control in. The Menu control may not actually be parented by this object.
     *  If you omit this property, the method sets the Menu control's parent to
     *  the application.
     *
     *  @param mdp dataProvider object set on the popped up Menu. If you omit this
     *  property, the method sets the Menu data provider to a new, empty XML object.
     */
    public static function popUpMenu(menu:ZetMenu, parent:DisplayObjectContainer, mdp:Object):void
    {
        menu.parentDisplayObject = parent ?
                                   parent :
                                   DisplayObject(Application.application);
        if(!mdp)
            mdp = new XML();

        menu.supposedToLoseFocus = true;
        menu.isPressed = true;
        menu.dataProvider = mdp;
    }

    /**
     *  @private
     */
    override mx_internal function getRootMenu():mx.controls.Menu
    {
        var target:ZetMenu = this;

        while (target.parentMenu)
            target = ZetMenu(target.parentMenu);

        return target;
    }

    /**
     *  @private
     */
    private static function menuHideHandler(event:MenuEvent):void
    {
        var menu:ZetMenu = ZetMenu(event.target);
        if (!event.isDefaultPrevented() && event.menu == menu)
        {
            PopUpManager.removePopUp(menu);
            menu.removeEventListener(MenuEvent.MENU_HIDE, menuHideHandler);
        }
    }

    /**
     *  Shows the Menu control. If the Menu control is not visible, this method
     *  places the Menu in the upper-left corner of the parent application at
     *  the given coordinates, resizes the Menu control as needed, and makes
     *  the Menu control visible.
     *
     *  The x and y arguments of the <code>show()</code> method specify the
     *  coordinates of the upper-left corner of the Menu control relative to the
     *  parent application, which is not necessarily the direct parent of the
     *  Menu control.
     *
     *  For example, if the Menu control is in an HBox container which is
     *  nested within a Panel container, the x and y coordinates are
     *  relative to the Application container, not to the HBox container.
     *
     *  @param x Horizontal location of the Menu control's upper-left
     *  corner (optional).
     *  @param y Vertical location of the Menu control's upper-left
     *  corner (optional).
     */
    override public function show(xShow:Object = null, yShow:Object = null):void
    {
        //this could be an empty menu so we'll return if it is
        if (collection && collection.length == 0)
            return;

        // If parent is closed, then don't show this submenu
        if (parentMenu && !parentMenu.visible)
            return;

        // If I'm already visible, then do nothing
        if (visible)
            return;

        if (parentDisplayObject && parent != parentDisplayObject)
        {
            PopUpManager.addPopUp(this, parentDisplayObject, false);
            addEventListener(MenuEvent.MENU_HIDE, menuHideHandler, false, EventPriority.DEFAULT_HANDLER);
        }

        // Fire an event
        var menuEvent:MenuEvent = new MenuEvent(MenuEvent.MENU_SHOW);
        menuEvent.menu = this;
        menuEvent.menuBar = sourceMenuBar;
        getRootMenu().dispatchEvent(menuEvent);

        // Activate the focus manager for that menu
        systemManager.activate(this);

        // Position it
        if (xShow !== null && !isNaN(Number(xShow)))
            x = Number(xShow);
        if (yShow !== null && !isNaN(Number(yShow)))
            y = Number(yShow);


        // Prevents menuItems to go beyond the screen bounds.
        if (this != getRootMenu())
        {
            // if it's in the right direction
            // checks whether it's about to go out of bounds.
            if (direction == "right")
            {
                var shift:Number = x + width - screen.width;
                direction = "right";
                x = parentMenu.x + parentMenu.width;
                if (shift > 0)
                {
                    direction = "left";
                    x = parentMenu.x - width;
                }
            }
            // if it's in the left direction
            // checks whether it's about to go out of bounds.
            else if(direction == "left")
            {
                direction = "left";
                x = parentMenu.x - width;
                if (x < 0)
                {
                    direction = "right";
                    x = parentMenu.x + parentMenu.width;
                }
            }

            if (verticalDirection == "bottom")
            {
                var verticalShift:Number = y + height - screen.height;


                verticalDirection = "bottom";
                y = parentMenu.y + parentMenu.height - explicitRowHeight;
                if (verticalShift > 0)
                {
                    verticalDirection = "top";
                    y = parentMenu.y - height + explicitRowHeight;
                }
            }
            else if (verticalDirection == "top")
            {
                verticalDirection = "top";
                y = parentMenu.y - height + explicitRowHeight;
                if (y < 0)
                {
                    verticalDirection = "bottom";
                    y = parentMenu.y + parentMenu.height - explicitRowHeight;
                }
            }

        }

        // Make sure the Menu's width and height has been determined
        // before we try to set the size for its mask
        UIComponentGlobals.layoutManager.validateClient(this, true);
        setActualSize(getExplicitOrMeasuredWidth(), getExplicitOrMeasuredHeight());

        cacheAsBitmap = true;
        scrollRect = new Rectangle(0, 0, unscaledWidth, 0);

        // Make it visible
        visible = true;

        UIComponentGlobals.layoutManager.validateNow();

        // Block all layout, responses from web service, and other background
        // processing until the tween finishes executing.
        UIComponent.suspendBackgroundProcessing();

        var duration:Number = getStyle("openDuration");
        popupTween = new Tween(this, [0,0], [unscaledWidth,unscaledHeight], duration);

        focusManager.setFocus(this);
        supposedToLoseFocus = true;

        // If the user clicks outside the menu, then hide the menu
        systemManager.addEventListener(MouseEvent.MOUSE_DOWN, mouseDownOutsideHandler, false, 0, true);
    }

    /**
     *  @private
     */
    private function mouseDownOutsideHandler(event:MouseEvent):void
    {
        if (!isMouseOverMenu(event) && !isMouseOverMenuBarItem(event))
            hideAllMenus();
    }

    /**
     *  @private
     */
    private function isMouseOverMenu(event:MouseEvent):Boolean
    {
        var target:DisplayObject = DisplayObject(event.target);
        while (target)
        {
            if (target is ZetMenu)
                return true;
            target = target.parent;
        }

        return false;
    }

    /**
     *  @private
     */
    private function isMouseOverMenuBarItem(event:MouseEvent):Boolean
    {
        if (!sourceMenuBarItem)
            return false;

        var target:DisplayObject = DisplayObject(event.target);
        while (target)
        {
            if (target == sourceMenuBarItem)
                return true;
            target = target.parent;
        }

        return false;
    }

    /**
     *  @private
     */
    override mx_internal function openSubMenu(row:IListItemRenderer):void
    {
        supposedToLoseFocus = true;

        var r:mx.controls.Menu = getRootMenu();
        var menu:ZetMenu;

        // check to see if the menu exists, if not create it
        if (!IMenuItemRenderer(row).menu)
        {
            menu = new ZetMenu();
            menu.parentMenu = this;
            menu.owner = this;
            menu.showRoot = showRoot;
            menu.dataDescriptor = r.dataDescriptor;
            menu.styleName = r;
            menu.labelField = r.labelField;
            menu.labelFunction = r.labelFunction;
            menu.iconField = r.iconField;
            menu.iconFunction = r.iconFunction;
            menu.itemRenderer = r.itemRenderer;
            menu.rowHeight = r.rowHeight;
            menu.scaleY = r.scaleY;
            menu.scaleX = r.scaleX;

            // if there's data and it has children then add the items
            if (row.data &&
                _dataDescriptor.isBranch(row.data) &&
                _dataDescriptor.hasChildren(row.data))
            {
                menu.dataProvider = _dataDescriptor.getChildren(row.data);
            }
            menu.sourceMenuBar = sourceMenuBar;
            menu.sourceMenuBarItem = sourceMenuBarItem;

            IMenuItemRenderer(row).menu = menu;
            PopUpManager.addPopUp(menu, r, false);
        }
        else
        {
            menu = ZetMenu(IMenuItemRenderer(row).menu);
        }

        var _do:DisplayObject = DisplayObject(row);
        var pt:Point = new Point(0,0);
        pt = _do.localToGlobal(pt);

        // when loadMovied, you may not be in global coordinates
        if (_do.root)   //verify this is sufficient
        {
            pt = _do.root.globalToLocal(pt);
        }

        // sets the direction of menu items.
        menu.direction = direction;
        menu.verticalDirection = verticalDirection;

        // if it's in the right direction,
        // resets its x position as current menu's x + width.
        if (direction == "right")
        {
            menu.show(pt.x + row.width, pt.y);
        }
          // if it's in the left direction,
        // resets its x position as current menu's x - width.
        else
        {
            menu.show(pt.x - row.width, pt.y);
        }

        if (verticalDirection == "bottom")
        {
            menu.show(pt.y, pt.y - row.height);
        }

        else
        {
            menu.show(pt.y, pt.y + row.height);
        }

        subMenu = ZetMenu(menu);
        openSubMenuTimer = 0;

        var s:Sprite = new FlexSprite();
        s.mouseEnabled = false;
        selectionLayer.addChild(s);

        drawTraceIndicator(s, row.x, row.y, row.width, row.height, getStyle("rollOverColor"));
    }

    private function drawTraceIndicator(indicator:Sprite, x:Number, y:Number, width:Number, height:Number, color:uint):void
    {
    	var g:Graphics = indicator.graphics;
    	g.clear();
    	g.beginFill(color);
    	g.drawRect(0, 0, width, height);
    	g.endFill();
    	indicator.x = x;
    	indicator.y = y;
    }
}
}