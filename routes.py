#!/usr/bin/wnv python3
from flask import Flask, request, send_from_directory, make_response, Blueprint, \
redirect, url_for, g, flash, render_template, jsonify
from http import HTTPStatus
import json
import logging
import requests
from config import config

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s, %(threadName)s, %(name)s, %(module)s, %(lineno)d: %(message)s')
console.setFormatter(formatter)
log.addHandler(console)

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