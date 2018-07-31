
import logging
import json

# local imports
import paho.mqtt.client as mqtt
import logger

# logger for this module
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class MQTT(mqtt.Client):
    def __init__(self, broker, name, alarm):
        super().__init__(name)
        self.name = name
        self.alarm = alarm
        self.message_callback_add(self.name+"/command", self.__on_command)
        self.connect(broker)
        self.loop_start()        
        

    def __on_command(self, client, userdata, message):
        # Callback function to reply back to commadn sender    
        def __respond(recipientId, sender):
            def respond(msg):
                message = {"recipientId":recipientId, "sender":sender, "message":msg}
                log.debug("publish {}/response msg: {}".format(self.name, str(message)))
                self.publish(self.name+'/response', str(message))
            return respond

        log.debug("message received: {} ".format(str(message.payload.decode("utf-8"))))
        jsonMsg = json.loads(message.payload.decode("utf-8").replace("'", '"'))
        bot = jsonMsg.get('recipient', None)
        sender = jsonMsg.get('sender', None)
        senderId = jsonMsg.get('senderId', None)
        command = jsonMsg.get('command', None)
        
        log.debug("sending command '{}' to bot '{}'".format(command, bot))
        r = self.alarm.command(command,__respond(recipientId=senderId, sender=bot))
        return (r)


    def on_message(self, client, userdata, message):
        log.debug("message received; {} ".format(str(message.payload.decode("utf-8").replace("'", '"'))))
        log.debug("message topic= {}".format(message.topic))
        log.debug("message qos= {}".format(message.qos))
        log.debug("message retain flag= {}".format(message.retain))
        pass


        