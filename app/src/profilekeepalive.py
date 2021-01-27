#!/usr/bin/env python3
import logging
import time
import requests
import threading

class ProfileKeepAlive():

  def __init__(self, cfg):
    self.log = logging.getLogger('ProfileKeepAlive')
    self.log.info("Initializing")

    self.updateConfig(cfg, initialUpdate=True)

    self.thread = None          # Thread object
    self.threadrunning = False  # Is the thread running?


  # [ Public methods ] #################################################################

  def start(self):
    self.log.info("Starting")

    if self.threadrunning:
      return

    self.log.info(f"Getting public IP")
    self.publicIP = requests.get("https://api.ipify.org/?format=json").json()['ip']
    self.log.info(f"Public IP: {self.publicIP}")

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

    self.log.info(f" - Tracker       : {self.cfg['profileKeepAlive']['trackerURL']}")
    self.log.info(f" - Notifications : {self.cfg['profileKeepAlive']['notificationsURL']}")
    self.log.info(f" - Request delay : {self.cfg['profileKeepAlive']['requestDelay']}s")
    self.log.info(f" - Profile delay : {self.cfg['profileKeepAlive']['profileUpdateDelay']}s")


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
      self.log.info("New profile update --------------------------------")

      for user in self.cfg['profiles']:

          self.log.info(f"[{user}] Requesting tracker page")
          response = requests.get(self.cfg['profileKeepAlive']['trackerURL'].format(user=user))
          if response.status_code != 200:
            self.log.warning(f"HTTP status {response.status_code}")
          if not self._threadsleep(self.cfg['profileKeepAlive']['requestDelay']):
            return

          self.log.info(f"[{user}] Requesting notification page")
          response = requests.get(self.cfg['profileKeepAlive']['notificationsURL'].format(ip=self.publicIP))
          if response.status_code != 200:
            self.log.warning(f"HTTP status {response.status_code}")
          if not self._threadsleep(self.cfg['profileKeepAlive']['requestDelay']):
            return

      self._threadsleep(self.cfg['profileKeepAlive']['profileUpdateDelay'])
