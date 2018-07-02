# Note
This code is provided as an example of how to implement webhooks for home alarm control.  The concept can be extended to
any IoT device running the home.

# Overview
Twitter is retiring the streaming interface in faviour of webhooks through the new Account Activity API.  I use Twitter to control
the house alarm and the alarm sends notifications via Twitter.  So I need to move off the streaming API.

The solution comprises two components 1) a Bot Contoller that interfaces into Twitter via the new Account Activity API
and webhooks (see [Git Twitter_webhook](https://github.com/ccullin/twitter-webhook), and 2) this alarm Bot.

The Alarm Bot has a webhook for the Bot Controller to post commmands to, and will post requests (events) of its own to the
Bot Controller, which the Bot Controller then sends out via Twitter Direct Message.  All the Twitter interfacing is in the
Bot Controller and the alarm bot is much simpler

It is now also possible to replace or supliment Twitter with another communications medium for command and notification,
for example, discord or SMS.

# Installation & setup

python requirements are defined in requirements.txt
Other requirements include:


1.  Configure 'config.py' with your Twitter user and alarm details. a config-sample.py is provided, which must be renamed
2.  to config.py.  Sample config:
```
config = {
    "screen_name": "e.g. Twitter screen_name of your alarm",
    "admins": {
        "screen_name of admin 1": "twitter id",
        "screen_name of admin 2": "twitter id",
        },
    "WEBHOOK_ALARM_URL": "Webhook of Bot controller, e.g. https://mydomain.com/webhook/alarm",
    "passcode": "passcode for alarm",
}
```

# API Reference

The alarm bot implements a single webhook at 192.168.1.10/webhook/alarm.  Commands to control the alarm are POSTed to this
url, which is implemented using Flask.  

For Notifcations the alarm bot sends a HTTP Post request to the Bot Controller.


# Acknowledgements

developed in collaboration with [Sam Cullin](https://samcullin.github.io/)
