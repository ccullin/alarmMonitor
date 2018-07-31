#!/usr/bin/env python3
from alarm import Alarm
import traceback
import sys
import signal
import time
import os
from threading import Thread
import logging

#local imports
from config import config
import logger

# logger for this module
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

log.debug(type(config))
log.debug(config)
alarm = Alarm(**config)


def main():
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    
    try:
        log.info('start alarm monitor')
        alarm.start()
        while True:
            time.sleep(5)
    except ServiceExit:
        log.info("Shutting Down")
        alarm.stop()
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
    
