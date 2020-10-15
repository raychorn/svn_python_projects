String.prototype.isNumeric = function (iLoc) {
    iLoc = ((!!iLoc) ? iLoc : 0);
    iLoc = ((iLoc < 0) ? 0 : iLoc);
    iLoc = ((iLoc > (this.length - 1)) ? this.length : iLoc);
    var _ch = this.substr(iLoc, 1);
    var b = ( (_ch >= '0') && (_ch <= '9') );
    return b;
}
String.prototype.numeric = function () {
    var t = '';
    for (var i = 0; i < this.length; i++) {
	if (this.isNumeric(i)) {
	    t += this.substr(i, 1);
	}
    }
    return t;
}
