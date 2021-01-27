#!/usr/bin/env python3
import logging
import time
import requests
import threading

class APIStatsGetter():

  def __init__(self, cfg):
    self.log = logging.getLogger('APIStatsGetter')
    self.log.info("Initializing")

    self.updateConfig(cfg, initialUpdate=True)

    self.thread = None          # Thread object
    self.threadrunning = False  # Is the thread running?


  # [ Public methods ] #################################################################

  def start(self):
    self.log.info("Starting")

    if self.threadrunning:
      return

    try:
      self.threadrunning = True
      self.thread = threading.Thread(target=self._threadhandler, args=())
      self.thread.start()
    except:
      self.log.exception("Exception in start()")


  def stop(self):
    self.log.info("Stopping")

    if not self.threadrunning:
      return

    self.threadrunning = False
    self.thread.join()


  def updateConfig(self, cfg, initialUpdate=False):
    self.cfg = cfg
    if initialUpdate:
      self.log.info("Configuration:")
    else:
      self.log.info("Configuration UPDATED:")

    self.log.info(f" - Request delay : {self.cfg['apiStatsGetter']['requestDelay']}s")


  # [ Private methods ] #################################################################

  def _threadsleep(self, seconds):
    elapsed = 0

    while elapsed < seconds:
      time.sleep(0.1)
      elapsed += 0.1
      if not self.threadrunning:
        return False  # Wait cancelled, please exit

    return True # Wait finished, continue working


  def _threadhandler(self):
    while self.threadrunning:
      self.log.info("New api stats update --------------------------------")

      # Fill this with beautiful code   :-p

      self._threadsleep(self.cfg['apiStatsGetter']['requestDelay'])
