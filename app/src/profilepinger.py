#!/usr/bin/env python3
import logging
import requests

from src.lib.taskthread import TaskThread
from src.lib.fortnitetracker import FortniteTracker


class ProfilePinger(TaskThread):

    def __init__(self, cfg):
        super().__init__(cfg)

        self.log = logging.getLogger('ProfilePinger')
        self.log.info("Initializing")

        self.tracker = FortniteTracker(self.cfg, 'ProfilePinger')

        self.log.info(f"Getting public IP")
        self.public_ip = requests.get("https://api.ipify.org/?format=json").json()['ip']
        self.log.info(f"Public IP: {self.public_ip}")


    def start(self):
        if self.cfg['profilePinger']['active']:
            super().start()
        else:
            self.log.warning("Skipping start (deactivated)")


    def mainLoop(self):
        self.log.info("New profile update --------------------------------")

        for user in self.cfg['profiles']:
            username = user['username']
            trn_username = user['trn_username']

            self.log.info(f"[{username}] Requesting tracker page")
            self.tracker.getTrackerPage(trn_username)

            self.log.info(f"[{username}] Requesting notification page")
            self.tracker.getNotificationsPage(self.public_ip)

        self.log.info("Profile update FINISHED --------------------------------")

        self._threadsleep(self.cfg['profilePinger']['profilePingInterval'])
