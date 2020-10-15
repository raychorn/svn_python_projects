var vs_im = new Image();
function _hbOnPostPV(a){
var i0 = a.indexOf('cd=');
var i1 = i0-1;
var i2 = a.indexOf('c1=')
var i3= i2-1
var x = a.substring(i0,i3);
var j0 = a.indexOf('c4=');
var j1 = a.indexOf('&',j0);
var y = a.substring(j1);
//var k0 = a.indexOf('cv.c5=');
//var k1 = a.indexOf('&',k0);
//var z = a.substring(k1);
b = x;
b = b.split(y).join("");
//b = b.split(z).join("");
b = b.replace('vcon=','vcon=/vzw');
var x = location.protocol + '//ehg-verizon.hitbox.com/HG?' + b + '&hb=DM550928B8DM;DM561021P9DE';
vs_im.src = x;
}
