package vyperlogix.controls.Alert {
	import flash.display.Sprite;
	
	import mx.controls.Alert;
	import mx.core.Application;
	import mx.core.UIComponent;
	import mx.events.CloseEvent;
	import mx.managers.PopUpManager;

	public class ButtonlessAlert extends Alert {
		public function ButtonlessAlert() {
			super();
		}
		
	    private var alertForm:ButtonlessAlertForm;

		public static function show(text:String = "", title:String = "",
		                            parent:Sprite = null, 
		                            closeHandler:Function = null, 
		                            iconClass:Class = null):ButtonlessAlert
		{
		    var modal:Boolean = true;
		
		    if (!parent) {
		        parent = Sprite(Application.application);   
		    }
		    
		    var alert:ButtonlessAlert = new ButtonlessAlert();
		
		    alert.text = text;
		    alert.title = title;
		    alert.iconClass = iconClass;
		        
		    if (closeHandler != null) {
		        alert.addEventListener(CloseEvent.CLOSE, closeHandler);
		    }
		
			// Setting a module factory allows the correct embedded font to be found.
		    if (parent is UIComponent) {
		    	alert.moduleFactory = UIComponent(parent).moduleFactory;
		    }
		    	
		    PopUpManager.addPopUp(alert, parent, modal);
		
		    alert.setActualSize(alert.getExplicitOrMeasuredWidth(), alert.getExplicitOrMeasuredHeight());
		    
		    return alert;
		}

		protected override function createChildren():void {
	        var messageStyleName:String = getStyle("messageStyleName");
	        if (messageStyleName) {
	            styleName = messageStyleName;
	        }
	
	        if (!alertForm) {   
	            alertForm = new ButtonlessAlertForm();
	            alertForm.styleName = this;
	            addChild(alertForm);
	        }
		}
	}
}