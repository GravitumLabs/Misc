from serverConfiguration import *
import requests
import logging
from gravitumUtils import *


# FB Functions:
def getFBUserProfile(playerID):
    # Otherwise make a fresh call to FB
    params = {
        "access_token": getServerConfig(key="PAGE_ACCESS_TOKEN")
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.get(
        "https://graph.facebook.com/v2.6/" + playerID + "?fields=first_name,last_name,profile_pic,locale,timezone,gender",
        params=params, headers=headers)
    if r.status_code != 200:
        # print ( r.status_code )
        # print ( r.text )
        logging.error("getFBUserProfile: ERROR Code {}, Text={}".format(str(r.status_code), str(r.text)))
        return None
    else:
        return json.loads(r.text, encoding='utf-8')


def getFbUserInfo(psfid):
    first_name = last_name = None
    doc = getFBUserProfile(psfid)
    if doc:
        first_name = doc["first_name"]
        last_name = doc["last_name"]
        profile_pic = doc["profile_pic"]
    return [first_name, last_name, profile_pic]


def send_text_message(sendto_id, message_text, type=None, payload=None):
    if payload is None:
        msg = {
            "text": message_text
        }
    else:
        msg = {
            "text": message_text,
            "metadata": json.dumps(payload)
        }
    data = json.dumps({
        "recipient": {
            "id": sendto_id
        },
        "message": msg
    })
    sendTo_FBMsgAPI(sendto_id, data, type)
    return


def sendTo_FBMsgAPI(sendto_id, data, type=None):
    params = {
        "access_token": getServerConfig(key="PAGE_ACCESS_TOKEN")
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v2.10/me/messages", params=params, headers=headers,
                      data=data)
    if r.status_code != 200:
        logging.error("sendTo_FBMsgAPI- FAIL Code:" + str(r.status_code) + " Response: " + str(r.text))
    return r


def sendCustomShare(sharerID, gameID, liveMatchID, sharer_title, sharer_image_url, sharer_subtitle, receiver_title,
                    receiver_image_url, receiver_subtitle, destURL):
    # refJson={
    # 	"type":inviteType,
    # 	"data":{
    # 		"gameID":str(gameID),
    # 		"inviterId":str(inviter_ID),
    # 		"pageID":pageID
    # 	}
    # }
    # refStr=json.dumps(refJson)
    # url="https://polar-lake-43722.herokuapp.com/templates/?"+"gameID="+gameID+"&"+"liveMatchID="+liveMatchID
    # print "Share URL is: "+str(url)

    data = json.dumps({
        "recipient": {
            "id": sharerID
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": sharer_title,
                            "image_url": sharer_image_url,
                            "subtitle": sharer_subtitle,
                            # "default_action" : {
                            # 	"type" : "web_url" ,
                            # 	"url" : "https://m.me/778273462325745?ref="+refStr ,
                            #
                            # } ,
                            "buttons": [
                                # {
                                # 	"type" : "web_url" ,
                                # 	"url" : "https://m.me/778273462325745?ref="+refStr ,
                                # 	"title" : "I accept"
                                # } ,
                                # {
                                # 	"type" : "element_share"
                                # },
                                getElementShare(destURL, receiver_title, receiver_image_url, receiver_subtitle)
                            ]
                        }
                    ]
                }
            }
        }
    })
    code = sendTo_FBMsgAPI(sharerID, data)
    return code


def getElementShare(url, receiver_title, receiver_image_url, receiver_subtitle):
    el = {
        "type": "element_share",
        "share_contents": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": receiver_title,
                            "subtitle": receiver_subtitle,
                            "image_url": receiver_image_url,
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": url,
                                    "webview_height_ratio": "full",
                                    "title": "Count me in!",
                                    "messenger_extensions": True
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    return el


def sendListImages(sendto_id, imgElementArray=[]):
    # elements=[]
    # for el in imgElementArray:
    # 	temp={"title": el["title"],
    # 	      "subtitle" : el [ "subtitle" ],
    #          "image_url": el["image_url"]
    #          }
    # 	elements.append((temp))

    data = json.dumps({
        "recipient": {
            "id": sendto_id
        }, "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "elements": imgElementArray,

                }
            }
        }
    })
    sendTo_FBMsgAPI(sendto_id, data)


def sendImageURL(playerID, url):
    data = json.dumps({
        "recipient": {
            "id": playerID
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": url
                }
            }
        }
    })
    sendTo_FBMsgAPI(playerID, data, type)
    return


def sendAttachment(playerID, fileURL, type):
    data = {
        "recipient": {
            "id": playerID
        },
        "message": {
            "attachment": {
                "type": type,
                "payload": {
                    "url": fileURL
                }
            }
        }
    }
    dataStr = json.dumps(data)
    sendTo_FBMsgAPI(playerID, data=dataStr)
    return


def sendUserMessage(psUserID, text=None, fileURL=None, imageURL=None, audioURL=None, videoURL=None):
    POSTResult = 'Error'
    POSTError = True

    if (not psUserID) or not (text or fileURL or imageURL or audioURL or videoURL):
        POSTResult = "None of the inputs were found"
        return [POSTResult, POSTError]

    if text:
        send_text_message(psUserID, text)
    elif fileURL:
        type = "file"
        sendAttachment(psUserID, fileURL, type)
    elif imageURL:
        type = "image"
        sendAttachment(psUserID, imageURL, type)
    elif audioURL:
        type = "audio"
        sendAttachment(psUserID, audioURL, type)
    elif videoURL:
        type = "video"
        sendAttachment(psUserID, videoURL, type)

    POSTResult = 'Success'
    POSTError = False
    return [POSTResult, POSTError]

btnsX=[
    {
        "content_type":"text",
        "title":u'\U0001F600'+"Very Happy",
        "payload":"<POSTBACK_PAYLOAD>"
    },
{
        "content_type":"text",
        "title":u'\U0001F642'+"Fine",
        "payload":"<POSTBACK_PAYLOAD>"
    },
{
        "content_type":"text",
        "title":u'\U0001F620'+"Angry",
        "payload":"<POSTBACK_PAYLOAD>"
    },

]
def sendQuickReplyButtons(psUserID, headline, btns):
    data = {
        "recipient": {
            "id": psUserID
        },
        "message": {
            "text": headline,
            "quick_replies": btns
        }
    }
    dataStr = json.dumps(data)
    sendTo_FBMsgAPI(sendto_id=psUserID, data=dataStr)
    return


def sendPhoneToCall(psUserID, headline, phoneNumber, buttonTitle="Call Representative"):
    data = {
        "recipient": {
            "id": psUserID
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": headline,
                    "buttons": [
                        {
                            "type": "phone_number",
                            "title": buttonTitle,
                            "payload": str(phoneNumber)
                        }
                    ]
                }
            }
        }
    }
    dataStr = json.dumps(data)
    sendTo_FBMsgAPI(sendto_id=psUserID, data=dataStr)
    return


def send_userRef_message(user_ref, message_text):
    msg = {
        "text": message_text
    }
    data = json.dumps({
        "recipient": {
            "user_ref": str(user_ref)
        },
        "message": msg
    })
    r = sendTo_FBMsgAPI(user_ref, data, type)
    psUserID = None
    if r.status_code == 200:
        data = json.loads(r.text)
        psUserID = data["recipient_id"]
        log(data)

    return psUserID


def sendWebURL(psFbId, imgURL, title, subtitle,buttons):
    data = {
        "recipient": {
            "id": psFbId
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": title,
                            "image_url": imgURL,
                            "subtitle": subtitle,
                            # "default_action": {
                            # 	"type": "web_url",
                            # 	"url": destURL,
                            # 	"messenger_extensions": False,
                            # 	"webview_height_ratio": "tall",
                            # 	"fallback_url": destURL
                            # },
                            "buttons": buttons
                        }
                    ]
                }
            }
        }
    }
    dataStr = json.dumps(data)
    r = sendTo_FBMsgAPI(sendto_id=psFbId, data=dataStr)
    if r.status_code == 200:
        print "All OK"

    return


def persistentMenuSetup():
    params = {
        "access_token": getServerConfig(key="PAGE_ACCESS_TOKEN")
    }
    headers = {
        "Content-Type": "application/json"
    }


    subMenu2 = [{
        "type": "postback",
        "title": "UAE Leaders Summit",
        "payload": '{"buttonPressID": "checkVault"}',
        }
    ]
    subMenu = [
        {
            "type": "postback",
            "title": "Event Check In",
            "type": "nested",
            "payload": '{"buttonPressID": "checkVault"}',
            "call_to_actions":subMenu2
        },
        {
            "type": "postback",
            "title": "Meeting Check In",
            "payload": '{"buttonPressID": "checkVault"}',

        }
    ]


    dataJsn = {
        "persistent_menu": [
            {
                "locale": "default",
                "call_to_actions":subMenu
                # "call_to_actions": [
                #     {
                #         "title": u'\U00002630' + "Menu",
                #         "type": "nested",
                #         "call_to_actions": subMenu
                #     }
                # ]
            }
        ]
    }
    data = json.dumps(dataJsn)
    r = requests.post("https://graph.facebook.com/v2.10/me/messenger_profile?", params=params, headers=headers,
                      data=data)
    if r.status_code != 200:
        logging.error("FB_INIT-PersistMenu FAIL Code:" + str(r.status_code) + " Response: " + str(r.text))
    else:
        logging.info("FB_INIT-PersistMenu Success:" + str(r.text))

    return


def setGetStartedButton():
    params = {
        "access_token": getServerConfig(key="PAGE_ACCESS_TOKEN")
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "new_thread",
        "call_to_actions": [
            {
                "payload": '{"buttonPressID": "GetStarted"}'
            }
        ]
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings?", params=params, headers=headers, data=data)
    if r.status_code != 200:
        logging.error("FB_INIT-GetStarted FAIL Code:" + str(r.status_code) + " Response: " + str(r.text))
    else:
        logging.info("FB_INIT-GetStarted Success:" + str(r.text))
    return


def sendGenerictemplate(sendto_id, title=None, image_url=None, subtitle=None, buttons=None):
    data = json.dumps({
        "recipient": {
            "id": sendto_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": title,
                            "image_url": image_url,
                            "subtitle": subtitle,
                            "buttons": buttons
                        }
                    ]
                }
            }
        }
    })
    sendTo_FBMsgAPI(sendto_id, data)
    return

