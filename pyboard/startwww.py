from microWebSrv import MicroWebSrv
from L298N import L298N
import machine
import ujson

websocketList = []
_pvr = L298N(2,15)
_pvr.delete()
del _pvr
pvr = L298N(12,13)
phr = L298N(14,27)
pvl = L298N(25,26)
phl = L298N(32,33)
pvr.speed = 0
phr.speed = 0
pvl.speed = 0
phl.speed = 0




def timerEvent():
    for i, webSocket in enumerate(websocketList):
        webSocket.SendText("" + ujson.dumps(dict))


# ----------------------------------------------------------------------------


@MicroWebSrv.route("/test")
def _httpHandlerTestGet(httpClient, httpResponse):
    content = (
        """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST GET</title>
        </head>
        <body>
            <h1>TEST GET</h1>
            Client IP address = %s
            <br />
			<form action="/test" method="post" accept-charset="ISO-8859-1">
				First name: <input type="text" name="firstname"><br />
				Last name: <input type="text" name="lastname"><br />
				<input type="submit" value="Submit">
			</form>
        </body>
    </html>
	"""
        % httpClient.GetIPAddr()
    )
    httpResponse.WriteResponseOk(
        headers=None, contentType="text/html", contentCharset="UTF-8", content=content
    )


@MicroWebSrv.route("/test", "POST")
def _httpHandlerTestPost(httpClient, httpResponse):
    formData = httpClient.ReadRequestPostedFormData()
    firstname = formData["firstname"]
    lastname = formData["lastname"]
    content = """\
	<!DOCTYPE html>
	<html lang=en>
		<head>
			<meta charset="UTF-8" />
            <title>TEST POST</title>
        </head>
        <body>
            <h1>TEST POST</h1>
            Firstname = %s<br />
            Lastname = %s<br />
        </body>
    </html>
	""" % (
        MicroWebSrv.HTMLEscape(firstname),
        MicroWebSrv.HTMLEscape(lastname),
    )
    httpResponse.WriteResponseOk(
        headers=None, contentType="text/html", contentCharset="UTF-8", content=content
    )


@MicroWebSrv.route("/edit/<index>")  # <IP>/edit/123           ->   args['index']=123
@MicroWebSrv.route(
    "/edit/<index>/abc/<foo>"
)  # <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
@MicroWebSrv.route("/edit")  # <IP>/edit               ->   args={}
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}):
    content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST EDIT</title>
        </head>
        <body>
	"""
    content += "<h1>EDIT item with {} variable arguments</h1>".format(len(args))

    if "index" in args:
        content += "<p>index = {}</p>".format(args["index"])

    if "foo" in args:
        content += "<p>foo = {}</p>".format(args["foo"])

    content += """
        </body>
    </html>
	"""
    httpResponse.WriteResponseOk(
        headers=None, contentType="text/html", contentCharset="UTF-8", content=content
    )


# ----------------------------------------------------------------------------


def _acceptWebSocketCallback(webSocket, httpClient):
    print("WS ACCEPT")
    webSocket.RecvTextCallback = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback = _closedCallback
    websocketList.append(webSocket)


def _recvTextCallback(webSocket, msg):
    print("WS RECV TEXT : %s" % msg)
    parse = ujson.loads(msg)
    vr = parse.get("vr")
    if not vr is None:
        pvr.speed = vr
    hr = parse.get("hr")
    if not hr is None:
        phr.speed = hr
    vl = parse.get("vl")
    if not vl is None:
        pvl.speed = vl
    hl = parse.get("hl")
    if not hl is None:
        phl.speed = hl
    brake = parse.get("brake")
    if not brake is None:
        pvr.brake()
        phr.brake()
        pvl.brake()
        phl.brake()
    stop = parse.get("stop")
    if not brake is None:
        pvr.stop()
        phr.stop()
        pvl.stop()
        phl.stop()
    
def _recvBinaryCallback(webSocket, data):
    print("WS RECV DATA : %s" % data)


def _closedCallback(webSocket):
    websocketList.remove(webSocket)
    print("WS CLOSED")



# ----------------------------------------------------------------------------

# routeHandlers = [
# 	( "/test",	"GET",	_httpHandlerTestGet ),
# 	( "/test",	"POST",	_httpHandlerTestPost )
# ]
srv = MicroWebSrv(webPath="www/")
srv.MaxWebSocketRecvLen = 256
srv.WebSocketThreaded = True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start(threaded=True)


# ----------------------------------------------------------------------------
