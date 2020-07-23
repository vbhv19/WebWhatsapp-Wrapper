from flask import Flask, json, Response, request
import os, sys, time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message, MediaMessage

app = Flask(__name__, static_url_path='')
driver = None
msg = None
pwd ="hps@123";
defContacts = ["8109583706"];

@app.route('/sendMsg')
def sendMessage():
	try:
		mob = request.args.get('mob')
		msg = request.args.get('msg')
		img = request.args.get('img')
		print("mobile numbers", mob);
		print("message", msg);
		print("image", img);
		# imagePath = "images/" + img
		if(img != None):
			print("image", img)
			imagePath = os.path.join("images", img)
			if(os.path.exists(imagePath) == False):
				resp = getResponse('{"status": 400, "message": "Image not found"}', 501)
				return resp

		contacts = [x.strip() for x in mob.split(',')] + defContacts;
		print(contacts)

		if(msg == None):
			print("message not set")
			resp = getResponse('{"status": 501, "message": "message not set"}', 501)
			return resp

		for i in range(len(contacts)):
				wappId = "91" + contacts[i] + "@c.us"
				print(wappId)
				if (img == None):
					driver.send_message_to_id(wappId, msg)
				else:
					driver.send_media(imagePath, wappId, msg)

		resp = getResponse('{"status": 200, "message": "message sent"}', 200)
		return resp

	except Exception as e:
		print(e)
		resp = getResponse('{"status": 501, "message": "message not sent"}', 501)
		return resp


@app.route('/setMsg')
def setMsg():
	try:
		global msg
		msg = request.args.get('msg')
		print(msg)
		resp = getResponse('{"status": 200, "message": "msg set successfully"}', 200)
		return resp;
	except Exception as e:
		print(e)


@app.route('/authorize')
def auth():
	try:

		auth = request.args.get('auth')
		print("got authorize", auth)
		

		if(auth == pwd):
			resp = getResponse('{"status": 200, "message": "authorized"}', 200)
		else:
			resp = getResponse('{"status": 401, "message": "unauthorized"}', 401)

		return resp;

	except Exception as e:
		print(e)
		resp = getResponse('{"status": 401, "message": "error in authorize"}', 401)
		return resp;


def getResponse(strJsonData, status):
	return Response(json.dumps(json.loads(strJsonData), indent=2), status=status, mimetype='application/json')

@app.route('/driverLoaded')
def driverLoaded():
	try:
		global driver
		json = ""
		if(driver != None and driver.is_logged_in):
			json = '{"status": 200, "message": "driver available"}'
		else:
			json = '{"status": 200, "message": "driverLoaded: driver not available"}'

		resp = getResponse(json, 200)
		return resp;
	except Exception as e:
		print(e)
		driver = None
		resp = getResponse('{"status": 200, "message": "driver not available"}', 200)
		return resp;


@app.route('/loadDriver')
def loadDriver():
	try:
		global driver
		profiledir=os.path.join(".","chrome_cache")
		if not os.path.exists(profiledir): os.makedirs(profiledir)
		driver = WhatsAPIDriver(profile=profiledir)
		driver.wait_for_login()
		resp = getResponse('{"status": 200, "message": "driver available"}', 200)
		return resp;
	except Exception as e:
		print(e)
		driver = None
		resp = getResponse('{"status": 200, "message": "driver not available"}', 200)
		return resp;

@app.route('/')
def root():
	html = open('indexHPS.html').read()
	return html

@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status': 404,
		'message': 'Not Found: ' + request.url,
	}
	resp = json.dumps(message)
	return resp

@app.errorhandler(500)
def not_found(error=None):
	message = {
		'status': 500,
		'message': 'Internal Server Error'
	}
	resp = json.dumps(message)
	return resp


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3003)
