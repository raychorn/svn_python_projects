package com.HAL.utils {
	import flash.display.BitmapData;
	import flash.display.DisplayObjectContainer;

    import flash.geom.*;
    import flash.display.*;
    import flash.utils.*;
	
	public class BitmapUtils {
		public static const const_JPG_image_type:String = "jpg";
		public static const const_PNG_image_type:String = "png";
		public static const const_UNDEFINED_image_type:String = "undefined-image-type";
		
		public static function getBitmapFrom(canvas:DisplayObjectContainer):BitmapData {
			var bitmap:BitmapData = new BitmapData(canvas.width, canvas.height, false, 0xffffff);
			bitmap.draw(canvas);
			return bitmap;
		}
	}
}