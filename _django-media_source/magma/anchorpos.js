function getPageOffsetLeft(el) {
  var ol = 0;
  try {
      ol = el.offsetLeft;
      while ((el = el.offsetParent) != null) {
              ol += el.offsetLeft; 
      }
  } catch(e) {
  } finally {
  }
  return ol;
}

function getPageOffsetTop(el) {
  var ot = 0;
  try {
    ot = el.offsetTop;
    while ((el = el.offsetParent) != null) {
            ot += el.offsetTop; 
    }
  } catch(e) {
  } finally {
  }
  return ot;
}

function getAnchorPosition(anchorname) {
  anchorname = anchorname;
  x = 0, y = 0;
  use_gebi = ((!!document.getElementById) ? true : false);
  use_css = ((!use_gebi) ? ((!!document.all) ? true : false) : false);
  use_layers = (((!use_gebi) && (!!use_css)) ? ((!!document.layers) ? true : false) : false);

  if (use_gebi && document.all) {
    x = getPageOffsetLeft(document.all[anchorname]);
    y = getPageOffsetTop(document.all[anchorname]);
  } else if (use_gebi) {
    var o = document.getElementById(anchorname);
    x = getPageOffsetLeft(o);
    y = getPageOffsetTop(o);
  } else if (use_css) {
    x = getPageOffsetLeft(document.all[anchorname]);
    y = getPageOffsetTop(document.all[anchorname]);
  } else if (use_layers) {
    var found = 0;
    for (var i = 0; i < document.anchors.length; i++) {
      if (document.anchors[i].name == anchorname) { found = 1; break; }
    }
    if (found == 0) {
      x=0; y=0;
    }
    x = document.anchors[i].x;
    y = document.anchors[i].y;
  } else {
    x = 0; y = 0;
  }
  return [x,y];
}
    