import paho.mqtt.client as mqtt
import logging
import json
import time

#to catch socket conection errors
import errno
from socket import error as socket_error


# local imports
import logger

# logger for this module
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class MQTT(mqtt.Client):
    def __init__(self, broker, name, menu):
        super().__init__(name)
        self.broker = broker
        self.name = name
        self.execute = menu
        self.message_callback_add(self.name+"/command", self.__on_command)
        self.setupConnection
        self.loop_start()  
        
    def setupConnection(self):
        connected = False
        while not connected:
            try:
                self.connect(self.broker)
                connected = True
            except socket_error as serr:
                if serr.errno != errno.ECONNREFUSED:
                    # Not the error we are looking for, re-raise
                    raise serr
                # connection refused
                log.debug("the connection to MQTT was refused")
                time.sleep(10)


    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            log.debug("connected OK Returned code= {}".format(rc))
            log.debug("subscribe {}/command".format(self.name))
            self.subscribe(self.name+'/command')
        else:
            log.debug("Bad connection Returned code= {}".format(rc))        

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
        r = self.execute(command,__respond(recipientId=senderId, sender=bot))
        return (r)


    def on_message(self, client, userdata, message):
        log.debug("message received; {} ".format(str(message.payload.decode("utf-8").replace("'", '"'))))
        log.debug("message topic= {}".format(message.topic))
        log.debug("message qos= {}".format(message.qos))
        log.debug("message retain flag= {}".format(message.retain))
        pass


        