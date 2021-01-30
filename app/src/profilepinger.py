#!/usr/bin/env python3
import logging
import requests

from src.lib.taskthread import TaskThread

class ProfilePinger(TaskThread):

  def __init__(self, cfg):
    super().__init__()

    self.log = logging.getLogger('ProfilePinger')
    self.log.info("Initializing")

    self.updateConfig(cfg, initialUpdate=True)

    self.log.info(f"Getting public IP")
    self.publicIP = requests.get("https://api.ipify.org/?format=json").json()['ip']
    self.log.info(f"Public IP: {self.publicIP}")


  def updateConfig(self, cfg, initialUpdate=False):
    self.cfg = cfg
    if initialUpdate:
      self.log.info("Configuration:")
    else:
      self.log.info("Configuration UPDATED:")

    self.log.info(f" - Tracker       : {self.cfg['profilePinger']['trackerURL']}")
    self.log.info(f" - Notifications : {self.cfg['profilePinger']['notificationsURL']}")
    self.log.info(f" - Request delay : {self.cfg['profilePinger']['requestDelay']}s")
    self.log.info(f" - Profile delay : {self.cfg['profilePinger']['profileUpdateDelay']}s")


  def mainLoop(self):
    self.log.info("New profile update --------------------------------")

    for user in self.cfg['profiles']:

        self.log.info(f"[{user['username']}] Requesting tracker page")
        response = requests.get(self.cfg['profilePinger']['trackerURL'].format(user=user['trn_username']))
        if response.status_code != 200:
          self.log.warning(f"HTTP status {response.status_code}")
        if not self._threadsleep(self.cfg['profilePinger']['requestDelay']):
          return

        self.log.info(f"[{user['username']}] Requesting notification page")
        response = requests.get(self.cfg['profilePinger']['notificationsURL'].format(ip=self.publicIP))
        if response.status_code != 200:
          self.log.warning(f"HTTP status {response.status_code}")
        if not self._threadsleep(self.cfg['profilePinger']['requestDelay']):
          return

    self._threadsleep(self.cfg['profilePinger']['profileUpdateDelay'])
