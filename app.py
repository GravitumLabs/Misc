import os
import sys
import json
from datetime import datetime
from gravitumUtils import *

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
	# when the endpoint is registered as a webhook, it must echo back
	# the 'hub.challenge' value it receives in the query arguments
	# if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
	#     if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
	#         return "Verification token mismatch", 403
	#     return request.args["hub.challenge"], 200
	data = request.data
	# dataDict = json.loads(data, encoding='utf-8')
	# logJsn(dataDict)
	print data

	return "GET Ok", 200


@app.route('/', methods=['POST'])
def webhook():

	# endpoint for processing incoming messaging events

	data = request.data
	# dataDict = json.loads ( data ,encoding = 'utf-8')
	# logJsn(dataDict)
	print data
	return "POST ok", 200

if __name__ == '__main__':
	app.run(debug=True)
