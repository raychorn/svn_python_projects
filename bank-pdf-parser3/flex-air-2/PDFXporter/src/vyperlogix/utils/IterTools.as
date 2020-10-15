package vyperlogix.utils {
	import mx.collections.ArrayCollection;
	
	public class IterTools {
		public static function all(iter:*,criteria:Function=null):Boolean {
			var iterable:ArrayCollection;
			if (iter is Array) {
				iterable = new ArrayCollection(iter);
			} else {
				try {
					iterable = iter as ArrayCollection;
				} catch (e:Error) { iterable = new ArrayCollection(); }
			}
			if ( (iterable is ArrayCollection) && (criteria) && (criteria is Function) ) {
				for (var i:int = 0; i < iterable.length-1; i++) {
					try {
						if (criteria(iterable.getItemAt(i)) == false) {
							return false;
						}
					} catch (e:Error) { return false; }
				}
				return true;
			}
			return false;
		}
	}
}