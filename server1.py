from flask import Flask, json, Response, request
import os, sys, time, shutil, random
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message, MediaMessage

app = Flask(__name__, static_url_path='')
driversMap = {}
defaultContacts = ["8109583706"]; #send every msg to these numbers too


def getResponse(strJsonData, status):
  return Response(json.dumps(json.loads(strJsonData), indent=2), status=status, mimetype='application/json')


@app.route('/loadWhatsapp', methods = ['POST'])
def loadWhatsapp():
  try:
    req_data = request.get_json()
    uid = str(req_data['uid'])

    if not uid: 
      return getResponse('{"status": 400, "message": "uid not found in request form"}', 400)

    print("driver requested for uid " + uid)

    profiledir = os.path.join(".", str(uid) + "_cache")

    if not os.path.exists(profiledir): os.makedirs(profiledir)

    driversUids = list(driversMap.keys())

    print("Existing drivers uids ", driversUids)

    if len(driversUids) > 0:
      respData = {}
      respData["status"] = 403
      respData["message"] = "Already logged in user found, Please unload existing account before loading new"
      respData["data"] = {}
      respData["data"]["uid"] = driversUids
      return getResponse(json.dumps(respData), 403)

    userDriver = WhatsAPIDriver(headless=True, profile=profiledir)
    driversMap[str(uid)] = userDriver

    return getResponse('{"status": 200, "message": "user driver ready"}', 200)

  except Exception as e:
    print(e)
    return getResponse('{"status": 500, "message": "Internal Server Error"}', 500)


@app.route('/unloadWhatsapp', methods = ['POST'])
def unloadWhatsapp():
  try:
    req_data = request.get_json()
    uid = str(req_data['uid'])

    if not uid:
      return getResponse('{"status": 400, "message": "uid not found in request form"}', 400)

    if uid not in driversMap:
      return getResponse('{"status": 403, "message": "driver not loaded for this uid, Please load Whatsapp for this uid first "}', 403)

    print("unloading driver for uid " + uid)

    userDriver = driversMap[uid]
    userDriver.quit()
    driversMap.pop(str(uid), None)

    return getResponse('{"status": 200, "message": "Whatsapp unloaded successfully"}', 200)

  except Exception as e:
    print(e)
    return getResponse('{"status": 500, "message": "Internal Server Error"}', 500)



@app.route('/checkLogin', methods = ['POST'])
def checkLogin():
  try:
    req_data = request.get_json()
    uid = str(req_data['uid'])

    if not uid:
      return getResponse('{"status": 400, "message": "uid not found in request form"}', 400)

    if uid not in driversMap:
      return getResponse('{"status": 403, "message": "driver not loaded, Please load Whatsapp for this uid first "}', 403)

    userDriver = driversMap[uid]
    is_logged_in = userDriver.is_logged_in()

    respData = {}
    respData["status"] = 200
    respData["data"] = {}
    respData["data"]["is_logged_in"] = is_logged_in

    return getResponse(json.dumps(respData), 200)

  except Exception as e:
    print(e)
    return getResponse('{"status": 500, "message": "Internal Server Error"}', 500)



@app.route('/reloadQr', methods = ['GET'])
def reloadQr():
  try:
    uid = request.args.get('uid')

    if uid == None:
      return getResponse('{"status": 400, "message": "uid not found in args"}', 400)

    if str(uid) not in driversMap:
      return getResponse('{"status": 403, "message": "driver not loaded for this uid, Please load Whatsapp for this uid first "}', 403)

    userDriver = driversMap[str(uid)]
    is_logged_in = userDriver.is_logged_in()

    if is_logged_in:
      return getResponse('{"status": 403, "message": "Cannot reload Qr as user is already logged in"}', 403)

    userDriver.reload_qr()

    return getResponse('{"status": 200, "message": "qr reload complete"}', 200)

  except Exception as e:
    print(e)
    return getResponse('{"status": 500, "message": "Internal Server Error"}', 500)




@app.route('/getQr', methods = ['GET'])
def getQr():
  try:
    uid = request.args.get('uid')

    if uid == None:
      return getResponse('{"status": 400, "message": "uid not found in args"}', 400)

    if str(uid) not in driversMap:
      return getResponse('{"status": 401, "message": "driver not loaded for this uid, Please load Whatsapp for this uid first "}', 403)

    userDriver = driversMap[str(uid)]
    is_logged_in = userDriver.is_logged_in()

    if is_logged_in:
      return getResponse('{"status": 403, "message": "Cannot get Qr as user is already logged in"}', 403)

    respData = {}
    respData["status"] = 200
    respData["data"] = {}
    respData["data"]["qrBase64"] = userDriver.get_qr_base64()

    return getResponse(json.dumps(respData), 200)

  except Exception as e:
    print(e)
    return getResponse('{"status": 500, "message": "Internal Server Error"}', 500)



@app.route('/sendMsg', methods = ['POST'])
def sendMsg():
  try:

    req_data = request.get_json()

    if not req_data['uid']:
      return getResponse('{"status": 400, "message": "uid not found in request form"}', 400)

    uid = str(req_data['uid'])

    if str(uid) not in driversMap:
      return getResponse('{"status": 403, "message": "driver not loaded for this uid, Please load Whatsapp for this uid first "}', 403)

    userDriver = driversMap[str(uid)]
    is_logged_in = userDriver.is_logged_in()

    if not is_logged_in:
      return getResponse('{"status": 403, "message": "Please login before sending any message"}', 403)

    mob = req_data['mob']
    msg = req_data['msg']

    print("message", msg);

    contacts = [x.strip() for x in mob.split(',')] + defaultContacts;

    print("mobile numbers", contacts);

    if(msg == None):
      print("message not set")
      resp = getResponse('{"status": 501, "message": "message not set"}', 501)
      return resp

    for i in range(len(contacts)):
        wappId = "91" + contacts[i] + "@c.us"
        userDriver.send_message_to_id(wappId, msg)
        seconds = random.randint(0, 3)
        print("sending message to ", wappId, "next delay", seconds, "seconds");
        time.sleep(seconds)

    resp = getResponse('{"status": 200, "message": "message sent"}', 200)
    return resp

  except Exception as e:
    print(e)
    resp = getResponse('{"status": 501, "message": "message not sent"}', 501)
    return resp


@app.route('/saveProfile', methods = ['POST'])
def saveProfile():
  try:
    req_data = request.get_json()
    
    if not req_data['uid']:
      return getResponse('{"status": 400, "message": "uid not found in request form"}', 400)

    uid = req_data['uid']

    if str(uid) not in driversMap:
      return getResponse('{"status": 403, "message": "driver not loaded for this uid, Please load Whatsapp for this uid first"}', 403)

    userDriver = driversMap[str(uid)]
    is_logged_in = userDriver.is_logged_in()

    if not is_logged_in:
      return getResponse('{"status": 403, "message": "Please login before saving profile"}', 403)

    profiledir = os.path.join(".", str(uid) + "_cache")

    if not os.path.exists(profiledir): os.makedirs(profiledir)

    userDriver.save_firefox_profile()

    return getResponse('{"status": 200, "message": "Whatsapp profile saved successfully"}', 200)

  except Exception as e:
    print(e)
    return getResponse('{"status": 500, "message": "Internal Server Error"}', 500)



@app.route('/deleteProfile', methods = ['DELETE'])
def deleteProfile():
  try:
    req_data = request.get_json()

    if not req_data['uid']:
      return getResponse('{"status": 400, "message": "uid not found in request form"}', 400)

    uid = req_data['uid']

    profiledir = os.path.join(".", str(uid) + "_cache")

    if os.path.exists(profiledir):
      shutil.rmtree(profiledir)

    userDriver = driversMap[str(uid)]
    userDriver.quit()
    driversMap.pop(str(uid), None)

    return getResponse('{"status": 200, "message": "Whatsapp profile deleted successfully"}', 200)

  except Exception as e:
    print(e)
    return getResponse('{"status": 500, "message": "Internal Server Error"}', 500)



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



