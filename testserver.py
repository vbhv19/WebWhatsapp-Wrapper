from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response


app = Flask(__name__)
# app.run(debug=True)

import logging
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


@app.route('/allevents', methods = ['GET'])
def api_all_events():
	import requests
	import json

	token = request.args.get('token')
	url="https://api.betfair.com/exchange/betting/json-rpc/v1"
	header = { 'X-Application' : 'tNAFQ8J6b6ioo5qJ', 'X-Authentication' : token ,'content-type' : 'application/json' }
	jsonrpc_req= '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": { "filter": {} }, "id": 1 }'
	response = requests.post(url, data=jsonrpc_req, headers=header)
	resp = Response(json.dumps(json.loads(response.text), indent=3), status=200, mimetype='application/json')
	return resp




@app.route('/events/<eventId>', methods = ['GET'])
def api_events(eventId):
	import requests
	import json

	token = request.args.get('token')
	url="https://api.betfair.com/exchange/betting/json-rpc/v1"
	header = { 'X-Application' : 'tNAFQ8J6b6ioo5qJ', 'X-Authentication' : token ,'content-type' : 'application/json' }
	jsonrpc_req= '{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listEvents","params": {"filter": {"eventTypeIds": ['+eventId+'],"marketStartTime": {}}},"id": 1}'
	response = requests.post(url, data=jsonrpc_req, headers=header)
	resp = Response(json.dumps(json.loads(response.text), indent=3), status=200, mimetype='application/json')
	return resp


@app.route('/listEventCatalogue/<eventIds>', methods = ['GET'])
def api_listEventCatlog(eventIds):
	import requests
	import json

	token = request.args.get('token')
	url="https://api.betfair.com/exchange/betting/json-rpc/v1"
	header = { 'X-Application' : 'tNAFQ8J6b6ioo5qJ', 'X-Authentication' : token ,'content-type' : 'application/json' }
	jsonrpc_req_list_events= '{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listMarketCatalogue","params": {"filter": {"eventTypeIds": ['+eventIds+'],"inPlayOnly":true,"marketTypeCodes":["MATCH_ODDS"]},"maxResults": "200", "sort":"FIRST_TO_START" ,"marketProjection": ["COMPETITION","EVENT","EVENT_TYPE","RUNNER_DESCRIPTION","RUNNER_METADATA","MARKET_START_TIME"]},"id": 1}'
	response = requests.post(url, data=jsonrpc_req_list_events, headers=header)
	resp = Response(json.dumps(json.loads(response.text), indent=3), status=200, mimetype='application/json')
	return resp


@app.route('/listMarketCatalogue/<eventIds>', methods = ['GET'])
def api_listMarketCatlog(eventIds):
	import requests
	import json

	token = request.args.get('token')
	url="https://api.betfair.com/exchange/betting/json-rpc/v1"
	header = { 'X-Application' : 'tNAFQ8J6b6ioo5qJ', 'X-Authentication' : token ,'content-type' : 'application/json' }
	jsonrpc_req_list_events= '{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listMarketCatalogue","params": {"filter": {"eventIds": ['+eventIds+'],"inPlayOnly":true},"maxResults": "200", "sort":"FIRST_TO_START" ,"marketProjection": ["COMPETITION","EVENT","EVENT_TYPE","RUNNER_DESCRIPTION","RUNNER_METADATA","MARKET_START_TIME"]},"id": 1}'
	response = requests.post(url, data=jsonrpc_req_list_events, headers=header)
	resp = Response(json.dumps(json.loads(response.text), indent=3), status=200, mimetype='application/json')
	return resp


@app.route('/listMarketBook/<marketIds>', methods = ['GET'])
def api_listMarketRates(marketIds):
	import requests
	import json

	token = request.args.get('token')
	url="https://api.betfair.com/exchange/betting/json-rpc/v1"
	header = { 'X-Application' : 'tNAFQ8J6b6ioo5qJ', 'X-Authentication' : token ,'content-type' : 'application/json' }
	market_book_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params": {"marketIds":['+marketIds+'],"priceProjection":{"priceData":["EX_BEST_OFFERS"]}}, "id": 1}'
	response = requests.post(url, data=market_book_req, headers=header)
	resp = Response(json.dumps(json.loads(response.text), indent=3), status=200, mimetype='application/json')
	return resp


@app.route('/listMarketBookAlternate/<marketIds>', methods = ['GET'])
def api_listMarketRatesAlternate(marketIds):
	import requests
	import json

	token = request.args.get('token')
	url="https://api.betfair.com/exchange/betting/json-rpc/v1"
	header = { 'X-Application' : 'tNAFQ8J6b6ioo5qJ', 'X-Authentication' : token ,'content-type' : 'application/json' }
	market_book_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params": {"marketIds":["'+marketIds+'"],"priceProjection":{"priceData":["SP_AVAILABLE","SP_TRADED","EX_BEST_OFFERS","EX_ALL_OFFERS","EX_TRADED"]}}, "id": 1}'
	response = requests.post(url, data=market_book_req, headers=header)
	resp = Response(json.dumps(json.loads(response.text), indent=7), status=200, mimetype='application/json')
	return resp


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



@app.route('/')
def api_root():
	message = {
		'status': 200,
		'message': 'The Server is Running file'
	}
	resp = json.dumps(message)
	return resp

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3003)