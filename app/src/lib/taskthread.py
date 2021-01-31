#!/usr/bin/env python3
import logging
import time
import threading


class TaskThread():

    def __init__(self, cfg):
        self.log = logging.getLogger('TaskThread')

        self.updateConfig(cfg)

        self.thread = None          # Thread object
        self.threadrunning = False  # Is the thread running?
        self.stopRequested = False


    def updateConfig(self, cfg):
        self.cfg = cfg


    def start(self):
        if self.threadrunning:
            self.log.warning("Task already started")
            return

        try:
            self.log.info("Starting task")
            self.threadrunning = True
            self.stopRequested = False
            self.thread = threading.Thread(target=self._threadhandler, args=())
            self.thread.start()
        except:
            self.log.exception("Exception in start()")


    def stop(self):
        if not self.threadrunning:
            self.log.warning("Task not started")
            return

        self.log.info("Stopping task")
        self.stopRequested = True
        self.thread.join()


    def _threadsleep(self, seconds):
        endtime = time.time() + seconds

        while time.time() < endtime:
            time.sleep(1)
            if self.stopRequested:
                return False  # Wait cancelled, please exit

        return True  # Wait finished, continue working


    def _threadhandler(self):
        self.taskSetup()

        while not self.stopRequested:
            self.taskLoop()

        self.threadrunning = False


    def taskSetup(self):
        ''' Override this method in subclasses '''

        # Do nothing for the base class
        pass


    def taskLoop(self):
        ''' Override this method in subclasses '''

        # Do nothing for the base class
        self._threadsleep(1)
