package com.REST {
	public class EzObjectExplainer {
		public var source:Object;
		public var explanation:String = "";
		public function EzObjectExplainer(o:Object) {
			this.source = o;
			this.explanation = "";
		}
		
		public function explainThisWay(sep:String = ", ", pre:String = "(", post:String = ")"):String {
			var ar:Array = new Array;
			var ex:EzObjectExplainer;
			for (var v:String in this.source) {
				if ( (this.source[v] is String) || (this.source[v] is Number) ) {
					ar.push(pre + v + "=" + this.source[v] + post);
				} else if (this.source[v] is Array) {
					for (var i:int = 0; i < this.source[v].length; i++) {
						if ( (this.source[v][i] is String) || (this.source[v][i] is Number) ) {
							ar.push(pre + v + "[" + i + "]" + "=" + this.source[v][i] + post);
						} else {
				    		ex = new EzObjectExplainer(this.source[v][i]);
				    		ar.push(pre + v + "[" + i + "]" + "=" + ex.explainThisWay(pre,sep,post) + post);
						}
					}
				} else {
		    		ex = new EzObjectExplainer(this.source[v]);
		    		ar.push(pre + v + "=" + ex.explainThisWay(pre,sep,post) + post);
				}
			}
			this.explanation = "[" + ar.join(sep) + "]";
			return this.explanation;
		}
	}
}