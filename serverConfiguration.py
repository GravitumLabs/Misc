import json


#Flip the environment from "prod" to "dev"
environment="nissan" #or
# environment="production"
def getServerConfig(key):
	# Get the config file
	fn = "devServerConfig.json"
	with open ( fn ) as data_file :
		serverConfig = json.load ( data_file , encoding = 'utf-8' )

	serverConfig=serverConfig[environment]

	value=None
	if key in serverConfig:
		value=serverConfig[key]

	return value
def getEnvironment():
	return environment
#Notes:
# */2 * * * * /home/ec2-user/playAlongGame/restartGameServer.sh
