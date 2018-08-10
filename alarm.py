import serial
from time import sleep
import time
import os
from datetime import datetime
import sys
import threading
from threading import Thread
import logging

#local imports
from mqtt import MQTT

# logger for this module
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class Alarm(object):
    def __init__(self, name, device, passcode, speed=115200, **kwargs):
        log.debug(kwargs)
        self.name = name
        self.passcode = passcode
        self.port = serial.serial_for_url(device, baudrate=speed, timeout=0)
        self.dcs1500state = 'unknown'
        self.status = 'unknown'
        self.lastStatus = 'unknown'
        self.mqtt = MQTT(broker="192.168.0.4", name=self.name, menu=self.command)

    def start(self):
        self.thread = Thread(name="alarm_monitor", target=self.__monitor)
        self.event = threading.Event()
        self.thread.start()
        self.__monitor()

    def stop(self):
        self.mqtt.loop_stop()
        self.mqtt.disconnect()
        self.event.set()

    def __readSerial(self):
        buffer_string = ''
        while not self.event.is_set():
            self.event.wait(timeout=1.0)
            buffer_string = buffer_string + self.port.read(self.port.inWaiting()).decode(('utf-8'))
            if '\n' in buffer_string:
                timestamp = datetime.today().isoformat()
                lines = buffer_string.split('\n')
                last_received = lines[-2] # Last full line.
                buffer_string = lines[-1] # First part of next line.
                self.dcs1500state = last_received
                self.alarmTime = timestamp
                break

            
    def __get_status(self):
        """
        Monitors serial port until there is a full update from the arduino.Monitors
        """
        self.__readSerial()
        if self.dcs1500state[21:26] == 'Armed':
            self.status = 'ARMED'
            if self.dcs1500state[39] == 'A':
                self.status = 'TRIPPED'
        elif self.dcs1500state[1:3] == 'RA':
            self.status = 'ARMING'
        else:
            self.status = 'DISARMED'
        pass
    
    def __monitor(self):
        log.debug("started Monitor")
        while not self.event.is_set():
            self.event.wait(timeout=1.0)
            self.__get_status()
            if  self.status != self.lastStatus:
                self.sendEventNotification("alarm is {}, previously {}".
                        format(self.status, self.lastStatus.lower()))
                log.info("alarm status change to: {}  previous status: {}".format(self.status, self.lastStatus))
                self.lastStatus = self.status

        
    def __on(self):
        self.port.write(self.passcode.encode())

        
    def __off(self):
        self.port.write(self.passcode.encode())

        
    def get_status(self):
        return self.status
        

    def sendEventNotification(self, msg):
        message = {"recipientId":"admins", "sender":self.name, "message":msg}
        try:
            log.debug("publish {}/event msg: {}".format(self.name, str(message)))
            self.mqtt.publish(self.name+"/event", str(message))
        except requests.exceptions.ConnectionError as e:
            log.warning("Connection Error: {}".format(e))
            pass
            

    def command(self, cmd, respond):
        command = cmd.lower()

        if self.status == 'unknown':
            self.get_status()
            respond('connot process command at this time')
        elif command == 'off':
            if self.status != 'DISARMED':
                self.__off()
                respond('alarm turning off')
            else:
                respond('alarm already off')
        elif command == 'on':
            if self.status == 'DISARMED':
                self.__on()
                respond('alarm turning on')
            else:
                respond('alarm aLready on')
        elif command == 'hi':
            respond (self.get_status())
        else:
            respond('invalid command')
