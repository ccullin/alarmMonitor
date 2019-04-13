# Note
This code is provided as an example of how to implement webhooks for home alarm control.  The concept can be extended to
any IoT device running the home.

# Overview
Twitter is retiring the streaming interface in faviour of webhooks through the new Account Activity API.  I use Twitter to control
the house alarm and the alarm sends notifications via Twitter.  So I need to move off the streaming API.

The solution comprises two components 1) a Bot Contoller that interfaces into Twitter via the new Account Activity API
and webhooks (see [Git Twitter_webhook](https://github.com/ccullin/twitter-webhook), and 2) this alarm Bot.

The Alarm Bot and Bot Controller interface over MQTT.  The Bot Controller provides the Web interface via an abstracted API,
with current support for Twitter. the Alarm Bot receives commands, send responses, and send notification events over MQTT, 
and the Bot Controller maps to the web interface.

It is now also possible to replace or supliment Twitter with another communications medium for command and notification,
for example, discord or SMS.

# Installation & setup

1. clone to '/usr/local/src/alarmMonitor'
2. execute './setup.sh'
- moves files to correct directories
- sets the file permissions and
- configures 'alarmMonitor' to run on boot
3. pip3 install -r requirements.txt
4. run 'sudo service alarmMonitor start'

A Docker image is also available on [dockerhub](https://hub.docker.com/u/homebots/dashboard/).
to run this docker image.
1. sudo docker pull homebots/alarm
2. docker run --name=alarm --device=/dev/ttyUSB0 -it -d homebots/alarm:latest


Other requirements include:

-  Configure 'config.py'. a config-sample.py is provided, which must be renamed to config.py.
Sample config:
```
config = {
    "name": "e.g. alarmBot, this needs to match to name in Bot Controller",
    "device": "e.g. /dev/ttUSB0, this is the serial interface the DSC alarm is connect to"
    "passcode": "passcode for the DSC alarm",
    "mqtt_host": "hostname or ip address of mqtt broker",
}
```

# API Reference

The alarm bot subscribes to 'alarm name'/commands and publishes to 'alarm name'/response and 'alarm name'/event MQTT topics.


# Acknowledgements

developed in collaboration with [Sam Cullin](https://samcullin.github.io/)
