String.prototype.alphaNumeric = function () {
    var t = '';
    for (var i = 0; i < this.length; i++) {
		if ( (this.isAlpha(i)) || (this.isNumeric(i)) ) {
			t += this.substr(i, 1);
		}
    }
    return t;
}
