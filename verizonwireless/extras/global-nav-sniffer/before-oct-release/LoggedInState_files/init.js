// This initialization function handles loading functionality 
// after the DOM is loaded, but before the entire page 
// including images and/or flash have completed loading.
// This means the user can interact with the functionality 
// earlier than if we simply used an onload. This is useful
// now, but it will be even more important when the main
// navigation is in place.

/* for Mozilla/Opera9 */

if (document.addEventListener) {

    document.addEventListener("DOMContentLoaded", init, false);

}

/* for Safari */

if (/WebKit/i.test(navigator.userAgent)) { // sniff

    var _timer = setInterval(function() {

        if (/loaded|complete/.test(document.readyState)) {

            init(); // call the onload handler

        }

    }, 10);

}

if(document.addLoadEvent){
	addLoadEvent(init); 
}
