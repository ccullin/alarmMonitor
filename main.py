#!/usr/bin/env python3
from alarm import Alarm
import traceback
import sys
import signal
import time
import os
from threading import Thread
import logging
from config import config


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s, %(threadName)s, %(name)s, %(module)s, %(lineno)d: %(message)s')
console.setFormatter(formatter)
log.addHandler(console)

alarm = Alarm(passcode=config.get('passcode'), port='/dev/ttyUSB0', speed=115200)


def start_app(alarm):
    from routes import app
    app.config['SECRET_KEY'] = 'thisissupposedtobeasecret'
    app.config['Alarm'] = alarm
    
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False, processes=5)


def main():
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    
    try:
        log.info('start API')
        app_thread = Thread(target=start_app, args=(alarm,), name='alarm-api', daemon=True)
        app_thread.start()
        
        log.info('start alarm monitor')
        alarm.start()

        while True:
            time.sleep(5)

    except ServiceExit:
        log.info("Shutting Down")
        alarm.event.set()
        alarm.thread.join()
        log.info("Alarm Monitor shutdown")
        sys.exit(0)


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    log.info('Caught signal %d' % signum)
    raise ServiceExit



if __name__ == '__main__':
    main()
    
