function init() {
  // output = setValue("output");
  startWebSocket();
}

function startWebSocket() {
  var wsUri = "ws://" + window.location.hostname;
 //var wsUri = "ws://espressif.lan";
  //var wsUri = "ws://192.168.4.1";
  console.log("Connection to " + wsUri + "...");
  websocket = new WebSocket(wsUri);
  websocket.onopen = function (evt) {
    onOpen(evt);
  };
  websocket.onclose = function (evt) {
    onClose(evt);
  };
  websocket.onmessage = function (evt) {
    onMessage(evt);
  };
  websocket.onerror = function (evt) {
    onError(evt);
  };
}

function onOpen(evt) {
  console.log("<strong>-- CONNECTED --</strong>");
  //SendMsg("Hello world :)");
  //SendMsg("This is a WebSocket test");
  //SendMsg("(with a text frame encoded in UTF-8)");
  //setTimeout( function() { websocket.close() }, 5000 )
}

function onClose(evt) {
  console.log("<strong>-- DISCONNECTED --</strong>");
}

function onMessage(evt) {
  try {
    //console.log('MSG FROM SERVER' , evt.data  );
    var data = JSON.parse(evt.data);


  } catch (e) { }
}
function setValue(id, value) {
  if (value == null || value.length == 0) {
    value = "&nbsp;";
  }
  var element = document.getElementById(id);
  if (element != null) {
    element.innerHTML = value;
  } else {
    console.log(id, element);
  }
}

function onError(evt) {
  console.log('ERROR : <span style="color: red;">' + evt.data + "</span>");
}

function SendMsg(msg) {
  console.log('MSG TO SERVER : <span style="color: green;">' + msg + "</span>");
  websocket.send(msg);
}
window.addEventListener("load", init, false);
// Create JoyStick object into the DIV 'joy1Div'
var joy1Param = { "title": "joystick1", "autoReturnToCenter": true };
var Joy1 = new JoyStick('joy1Div', joy1Param);

// Create JoyStick object into the DIV 'joy2Div'
var joy2Param = { "title": "joystick2", "autoReturnToCenter": true };
var Joy2 = new JoyStick('joy2Div', joy2Param);


setInterval(function () {
  //https://seamonsters-2605.github.io/archive/mecanum/
  var x = Number(Joy1.GetX());
  //var rot = Number(Joy2.GetX());
  var y = Number(Joy1.GetY());
  var r = Math.hypot(x, y);
  var robotAngle = Math.atan2(y, x) ;
  var _sin_vrhl = Math.sin(robotAngle + Math.PI / 4); 
  var _sin_vlhr = Math.sin(robotAngle - Math.PI / 4);
  vlhr = (r * _sin_vrhl).toFixed();
  vrhl = (r * _sin_vlhr).toFixed();
  var vl = vlhr;
  var vr = vrhl;
  var hl = vrhl;
  var hr = vlhr;
  websocket.send('{ "vr": ' +  vr + ',"vl":' + vl + ',"hr":' + hr +',"hl":'+ hl + '}');
}, 100);


