package vyperlogix.utils {
	public class ObjectExplainer {
		public var source:Object;
		public var explanation:String = "";

		public function ObjectExplainer(o:Object) {
			super();
			this.source = o;
			this.explanation = "";
		}

		public function pushAllIntoArrayFromArray(destArray:Array, sourceArray:Array):void {
			for (var v:Object in sourceArray) {
				if (v is Number) {
					destArray.push(sourceArray[v]);
				} else {
					destArray.push(v);
				}
			}
		}
		
		public function stringValuesInObject(o:Object):Array {
			var ar:Array = new Array;
			for (var v:Object in o) {
				if (v is String) {
					ar.push(v.toString());
				}
			}
			return ar;
		}
		
		public function explainThisWay(sep:String = ", ", pre:String = "(", post:String = ")"):String {
			var ar:Array = new Array;
			var ex:ObjectExplainer;
			var anObj:*;
			var keys:Array;
			for (var v:String in this.source) {
				anObj = this.source[v];
				keys = ObjectUtils.keys(anObj);
				if (anObj is Array) {
					for (var i:int = 0; i < anObj.length; i++) {
						if ( (anObj[i] is String) || (anObj[i] is Number) ) {
							ar.push(pre + v + "[" + i + "]" + "=" + anObj[i] + post);
						} else {
				    		ex = new ObjectExplainer(anObj[i]);
				    		ar.push(pre + v + "[" + i + "]" + "=" + ex.explainThisWay(pre,sep,post) + post);
						}
					}
				} else if (keys.length > 0) {
		    		ex = new ObjectExplainer(anObj);
		    		ar.push(pre + v + "=" + ex.explainThisWay(pre,sep,post) + post);
				} else {
					ar.push(pre + v + "=" + anObj + post);
				}
			}
			this.explanation = "[" + ar.join(sep) + "]";
			return this.explanation;
		}
	}
}