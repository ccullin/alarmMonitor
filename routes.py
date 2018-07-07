from flask import Flask, request,url_for, jsonify
from http import HTTPStatus
import json
import requests

#local imports
from config import config
from logger import log

app = Flask(__name__)


#The POST for the Twitter Bot Controller to send commands to
@app.route("/webhook/alarm", methods=["POST"])
def twitterEventReceived():
    requestJson = request.get_json()
    alarm = app.config['Alarm']

    bot = requestJson.get('recipient', None)
    sender = requestJson.get('sender', None)
    senderId = requestJson.get('senderId', None)
    command = requestJson.get('command', None)

    if bot == alarm.name and sender in alarm.admins:
        log.debug("sending command to alarm")
        alarm.command(command, __respond(recipientId=senderId, sender=bot))
        return ('', HTTPStatus.OK)
    else:
        log.warning("invalid Twitter command '{}' for '{}' from '{}'".
            format(command, bot, sender))
        return ('', HTTPStatus.FORBIDDEN)
    
# Callback function to send 'msg' to the twitter user that send command    
def __respond(recipientId, sender):
    def respond(msg):
        url = config.get('WEBHOOK_ALARM_URL')
        message = {"recipientId":recipientId, "sender":sender, "message":msg}
        r = requests.post(url, json=message)
        log.debug("response {}:{}".format(r.status_code, r.text))
    return respond