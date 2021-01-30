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
    self.public_ip = requests.get("https://api.ipify.org/?format=json").json()['ip']
    self.log.info(f"Public IP: {self.public_ip}")


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


  def waitBetweenRequests(self):
    return self._threadsleep(self.cfg['profilePinger']['requestDelay'])


  def requestPage(self, url):
    response = requests.get(url)
    if response.status_code != 200:
      self.log.warning(f"HTTP status {response.status_code}")

    return self.waitBetweenRequests()


  def mainLoop(self):
    self.log.info("New profile update --------------------------------")

    for user in self.cfg['profiles']:
      username = user['username']
      trn_username = user['trn_username']
      trackerUrl = self.cfg['profilePinger']['trackerURL']
      notificationsUrl = self.cfg['profilePinger']['notificationsURL']

      self.log.info(f"[{username}] Requesting tracker page")
      url = trackerUrl.format(trn_username=trn_username)
      if not self.requestPage(url):
        return

      self.log.info(f"[{username}] Requesting notification page")
      url = notificationsUrl.format(public_ip=self.public_ip)
      if not self.requestPage(url):
        return

    self._threadsleep(self.cfg['profilePinger']['profileUpdateDelay'])
