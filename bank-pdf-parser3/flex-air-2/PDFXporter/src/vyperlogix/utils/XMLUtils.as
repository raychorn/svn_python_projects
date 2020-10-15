package vyperlogix.utils {
	import flash.xml.XMLDocument;
	
	import mx.collections.ArrayCollection;
	import mx.rpc.xml.SimpleXMLDecoder;
	import mx.utils.ArrayUtil;

	public class XMLUtils {
		public function XMLUtils() {
		}

		public static function convertXmlToObject(file:String):Object {
			var xml:XMLDocument = new XMLDocument(file);
		
			var decoder:SimpleXMLDecoder = new SimpleXMLDecoder();
			var data:Object = decoder.decodeXML(xml);
			return data;
		}
		
		public static function convertXmlToArrayCollection(file:String):ArrayCollection {
			var data:Object = convertXmlToObject(file);
			var array:Array = [];
			try {
				array = ArrayUtil.toArray(data.rows.row);
			} catch (e:Error) {
				try {
					array = ArrayUtil.toArray(data);
				} catch (e:Error) {
				}
			}
		
			return new ArrayCollection(array);
		}
	}
}