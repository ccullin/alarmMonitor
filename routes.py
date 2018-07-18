from flask import Flask, request,url_for, jsonify
from http import HTTPStatus
import json
import requests
import logging

#local imports
from config import config

# logger for this module
log = logging.getLogger(__name__)

app = Flask(__name__)


#The POST for the Twitter Bot Controller to send commands to
@app.route("/alarm/webhook", methods=["POST"])
def twitterEventReceived():
    requestJson = request.get_json()
    alarm = app.config['Alarm']

    bot = requestJson.get('recipient', None)
    sender = requestJson.get('sender', None)
    senderId = requestJson.get('senderId', None)
    command = requestJson.get('command', None)

    log.debug("sending command to alarm")
    r = alarm.command(command, __respond(recipientId=senderId, sender=bot))
    return (r)


# Callback function to send 'msg' to the twitter user that send command    
def __respond(recipientId, sender):
    def respond(msg):
        alarm = app.config['Alarm']
        # url = config.get('WEBHOOK_ALARM_URL')
        message = {"recipientId":recipientId, "sender":sender, "message":msg}
        r = requests.post(alarm.url, json=message)
        log.debug("response {}:{}".format(r.status_code, r.text))
    return respond