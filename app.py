from flask import Flask, request,render_template, url_for,jsonify,make_response
from flask_api import status
import os
from gravitumUtils import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_webhook():
	# when the endpoint is registered as a webhook, it must echo back
	# the 'hub.challenge' value it receives in the query arguments
	# if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
	# 	if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
	# 		return "Verification token mismatch", 403
	# 	return request.args["hub.challenge"], 200
	data = request.get_json()
	logJsn(data)
	return "Hello world. I am alive and well.", 200

# @app.route('/api/',methods=['GET'])
# def apiGetProcessor():
#
# 	log("--------- API GET Request Received : {function} --------- ".format(function=request.args.get ( "function" )))
# 	user_agent = request.user_agent
# 	result = jsonify ( '' ) , status.HTTP_400_BAD_REQUEST
# 	fnctName=fnctArgs =fnctResult= None
# 	if 'function' in request.args:
# 		#Call the wrapper function
# 		fnctResult=apiProcessor(request.args,user_agent)
# 		#Jsonify the result from Python to send to the webview
# 		if fnctResult is not None:
# 			result = jsonify(fnctResult)
# 			log ( "Successful GET....(200)" )
# 			try :
# 				result = gzipper ( response = result )
# 			except Exception as e :
# 				log ( "GZIPPER FAILED" )
# 				log ( str ( e ) )
# 		else:
# 			log ( "ERROR IN GET....(400)" )
# 			result = jsonify ( '' ) , status.HTTP_400_BAD_REQUEST
#
#
# 	return result
#
#
# @app.route ( '/api/' , methods = [ 'POST' ] )
# def apiPostComms ( ) :
# 	result = None
#
# 	data = request.data
# 	dataDict = json.loads ( data ,encoding = 'utf-8')
# 	user_agent=request.user_agent
#
#
# 	if (data is not None) or (data != ''):
# 		#Insert user_agent into data
# 		dataDict["user_agent"]=user_agent
#
#
# 		log("--------- API POST Request Received : {post_type}--------- ".format(post_type=safeGetFromDict(dataDict,["postType"])))
# 		s="POST Data: "+str(data)[:1024]
# 		log(s)
# 		[ POSTResult , POSTError ]=apiPOSTProcessor(dataDict)
#
# 		if not POSTError:
# 			result = jsonify ( str(POSTResult)) , status.HTTP_200_OK
# 			log("Successful POST....(200)")
# 		else :
# 			result=jsonify(str(POSTResult)) , status.HTTP_400_BAD_REQUEST
# 			log ( "ERROR IN POST....(400)" )
#
# 	return result





@app.route('/', methods=['POST'])
def post_webhook():
	data = request.get_json()
	logJsn(data)
	result = jsonify("Post Received ok", status.HTTP_200_OK)
	return result







