from datetime import datetime
import json,sys






def utcTsNow():
	return int(dateTimeToEpoch(datetime.utcnow()))



def epochToDateTime(epoch):
	return datetime.fromtimestamp(int(epoch))
def dateTimeToEpoch(dt):
	return int ( (dt - datetime ( 1970 , 1 , 1 )).total_seconds ( ) )

def printMongoResults(results):
	import pprint
	print len(results)
	for r in results:
		pprint.pprint (r)
		print
	return

def log(message):  # simple wrapper for logging to stdout on heroku
	print str(message)
	sys.stdout.flush()

def logJsn(jsn): #Simple json printer
	print json.dumps ( jsn , indent = 4 )
	sys.stdout.flush ( )

def saveJSonFile(fn,data):
	with open(fn, 'w') as outfile:
		json.dump(data, outfile,encoding = 'utf-8',indent=4, sort_keys=True)
	return
def jsnPrint(jsn):
	str=json.dumps ( jsn , encoding = 'utf-8' , indent = 4 , sort_keys = True )
	print str
	return
def loadJsn(jsnFile):
	with open ( jsnFile ) as data_file :
		dict = json.load ( data_file , encoding = 'utf-8' )
	return dict

def safeGetFromDict(dct,keyList):

	if (dct is None) or (keyList is None):
		return None

	# Save function to return None if one of the Keys does not exist
	# or return the value if it exists
	safe=False
	for n,k in enumerate(keyList):
		if dct:
			if (k in dct):
				dct=dct[k]
				if n==len(keyList)-1:
					safe=True
	if safe:
		return dct
	else:
		return None

def convertDTimeZoneToUTC(dt,currentTZString=None):
	import pytz
	tz_utc = pytz.timezone ( 'UTC' )
	if currentTZString:
		tz_curr = pytz.timezone ( currentTZString )
		# Convert first to current TZ
		dt = tz_curr.localize ( dt )
		# Convert to UTC next
		dt = dt.astimezone ( tz_utc )
	else:
		dt=tz_utc.localize(dt)

	return dt