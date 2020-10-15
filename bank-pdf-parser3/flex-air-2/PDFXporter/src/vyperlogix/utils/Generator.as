package vyperlogix.utils {
	import mx.collections.ArrayCollection;

	public class Generator {
		public var parent:*;
		public var dataSource:*;
		public var children:Array = [];
		
		private var _callback:Function;
		
		public function Generator(datasource:*,callback:Function=null) {
			var _this:* = this;
			this.children = [];
			this.parent = parent;
			this.dataSource = datasource;
			this._callback = callback;
			
			var gen:Generator;
			
			function iterate_over_array(ar:Array):void {
				for (i in ar) {
					anItem = ar[i];
					if (_this._callback is Function) {
						try { _this._callback(_this,anItem) } catch (err:Error) {trace('Generator().ERROR.1 '+err.toString()+'\n'+err.getStackTrace());}
					}
					gen = new Generator(anItem,_this._callback);
					gen.parent = _this;
					_this.children.push(gen);
				}
			}
			
			var i:String;
			if (this.dataSource is Array) {
				iterate_over_array(this.dataSource);
			} else if (this.dataSource is ArrayCollection) {
				iterate_over_array(this.dataSource.source);
			} else if (this.dataSource is String) {
				// Do Nothing - this is a leaf node.
			} else {
				var keys:Array = [];
				try { keys = ObjectUtils.keys(this.dataSource); }
					catch (err:Error) {}
				if (keys.length > 0) {
					var anItem:*;
					for (i in this.dataSource) {
						anItem = this.dataSource[i];
						if (this._callback is Function) {
							try { this._callback(this,anItem) } catch (err:Error) {trace('Generator().ERROR.2 '+err.toString()+'\n'+err.getStackTrace());}
						}
						gen = new Generator(anItem,this._callback);
						gen.parent = this;
						this.children.push(gen);
					}
				}
			}
		}
	}
}