// Functions
function detectResize(_element) {
  let promise = {};
  let _listener = [];
  promise.addResizeListener = function (listener) {
    if (typeof (listener) != "function") { return; }
    if (_listener.includes(listener)) { return; };
    _listener.push(listener);
  };
  promise.removeResizeListener = function (listener) {
    let index = _listener.indexOf(listener);
    if (index >= 0) { _listener.splice(index, 1); }
  };
  let _size = { width: _element.clientWidth, height: _element.clientHeight };
  function checkDimensionChanged() {
    let _currentSize = { width: _element.clientWidth, height: _element.clientHeight };
    if (_currentSize.width != _size.width || _currentSize.height != _size.height) {
      let previousSize = _size;
      _size = _currentSize;
      let diff = { width: _size.width - previousSize.width, height: _size.height - previousSize.height };
      fire({ width: _size.width, height: _size.height, previousWidth: previousSize.width, previousHeight: previousSize.height, _element: _element, diff: diff });
    }
    _size = _currentSize;
  }
  function fire(info) {
    if (!_element.parentNode) { return; }
    _listener.forEach(listener => { listener(info); });
  }
  let mouseDownListener = event => {
    let mouseUpListener = event => {
      window.removeEventListener("mouseup", mouseUpListener);
      window.removeEventListener("mousemove", mouseMoveListener);
    };
    let mouseMoveListener = event => {
      checkDimensionChanged();
    };
    window.addEventListener("mouseup", mouseUpListener);
    window.addEventListener("mousemove", mouseMoveListener);
  };
  _element.addEventListener("mousedown", mouseDownListener);
  window.addEventListener("resize",
    event => {
      checkDimensionChanged();
    });
  return promise;
  // textarea = $("#dMain")[0];
  // let detector = detectResize(textarea);
  // let listener = info =>
  // {
  //   $("#dMain")[0].textContent = info.width;
  // };
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
function rgb2hex(rgb) {
  if (/^#[0-9A-F]{6}$/i.test(rgb)) return rgb;
  rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
  function hex(x) {
    return ("0" + parseInt(x).toString(16)).slice(-2);
  }
  return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
}
function hex2rgb(str) { 
  if ( /^#([0-9a-f]{3}|[0-9a-f]{6})$/ig.test(str) ) { 
      var hex = str.substr(1);
      hex = hex.length == 3 ? hex.replace(/(.)/g, '$1$1') : hex;
      var rgb = parseInt(hex, 16);               
      return 'rgb(' + [(rgb >> 16) & 255, (rgb >> 8) & 255, rgb & 255].join(',') + ')';
  } 
  return 'rgb(0,0,0)'; 
}

function addJS(url) {
  var script = document.createElement("script");
  script.src = url;
  document.head.appendChild(script);
}

function addCSS(selector, rules) {
  head = document.head || document.getElementsByTagName('head')[0];
  style = document.createElement('style');
  head.appendChild(style);
  if (style.styleSheet) {
    style.styleSheet.cssText = "{0} {{1}}".format(selector, rules);
  } else {
    style.appendChild(document.createTextNode("{0} {{1}}".format(selector, rules)));
  }
  // if (typeof document.styleSheets[0].insertRule === 'function') {
  //   document.styleSheets[0].insertRule("{0} {{1}}".format(selector, rules), 0);
  // } else if (typeof style.sheet.addRule === 'function') {
  //   document.styleSheets[0].addRule(selctor, rules, 0);
  // }
}
function openWindowWithPost(url, data) {
  var form = document.createElement("form");
  form.target = "_blank";
  form.method = "POST";
  form.action = url;
  form.style.display = "none";
  for (var key in data) {
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = key;
    input.value = data[key];
    form.appendChild(input);
  }
  document.body.appendChild(form);
  form.submit();
  document.body.removeChild(form);
}

