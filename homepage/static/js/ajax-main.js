function initAJAX(xhttprArray, count) {
  var i;
  for (i = 0; i < count; i++) {
    var xhttpr;
    if (window.XMLHttpRequest) {
      xhttpr = new XMLHttpRequest();
      if (xhttpr.overrideMimeType) {
        xhttpr.overrideMimeType('text/xml');
      }
    } else if (window.ActiveXObject) { // IE
    try {
      xhttpr = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e) {
        try {
          xhttpr = new ActiveXObject("Microsoft.XMLHTTP");
        } catch (e) {
          alert('Ваш браузер не поддерживает AJAX');
          return false;
        }
      }
    }
    if (!xhttpr) {
      alert('Ваш браузер не поддерживает AJAX');
      return false;
    }
    xhttprArray.push(xhttpr);
  }
}