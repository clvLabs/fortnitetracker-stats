#!/usr/bin/env python3
import logging
import time
import threading


class TaskThread():

    def __init__(self):
        self.log = logging.getLogger('TaskThread')

        self.thread = None          # Thread object
        self.threadrunning = False  # Is the thread running?


    def start(self):
        self.log.info("Starting thread")

        if self.threadrunning:
            return

        try:
            self.threadrunning = True
            self.thread = threading.Thread(target=self._threadhandler, args=())
            self.thread.start()
        except:
            self.log.exception("Exception in start()")


    def stop(self):
        self.log.info("Stopping thread")

        if not self.threadrunning:
            return

        self.threadrunning = False
        self.thread.join()


    def _threadsleep(self, seconds):
        endtime = time.time() + seconds

        while time.time() < endtime:
            time.sleep(1)
            if not self.threadrunning:
                return False  # Wait cancelled, please exit

        return True  # Wait finished, continue working


    def _threadhandler(self):
        while self.threadrunning:
            self.mainLoop()


    def mainLoop(self):
        ''' Override this method in subclasses '''

        # Do nothing for the base class
        self._threadsleep(1)
