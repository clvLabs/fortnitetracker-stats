#!/usr/bin/env python3
import logging
import requests

from src.lib.task import Task
from src.lib.fortnitetracker import FortniteTracker


class ProfilePinger(Task):

    def __init__(self, cfg):
        super().__init__(cfg)
        self.log = logging.getLogger('ProfilePinger')
        self.log.info("Initializing")
        self.tracker = FortniteTracker(self.cfg, 'ProfilePinger')


    def start(self):
        ''' Override of Task.start() '''
        if not self.cfg['profilePinger']['enabled']:
            self.log.warning("Skipping start (disabled in config)")
            return

        super().start()


    def stop(self):
        ''' Override of Task.stop() '''
        self.tracker.stop()
        super().stop()


    def taskSetup(self):
        ''' Override of Task.taskSetup() '''
        self.log.info("Task setup")
        self.log.info(f"Getting public IP")
        self.public_ip = requests.get("https://api.ipify.org/?format=json").json()['ip']
        self.log.info(f"Public IP: {self.public_ip}")
        self.log.info("Task setup FINISHED")


    def taskLoop(self):
        ''' Override of Task.taskLoop() '''
        self.log.info("New profile update --------------------------------")

        for user in self.cfg['profiles']:

            if self.stopRequested:
                return

            username = user['username']
            trn_username = user['trn_username']

            self.log.info(f"[{username}] Requesting tracker page")
            self.tracker.getTrackerPage(trn_username)

            self.log.info(f"[{username}] Requesting notification page")
            self.tracker.getNotificationsPage(self.public_ip)

        self.log.info("Profile update FINISHED --------------------------------")

        self._threadsleep(self.cfg['profilePinger']['profilePingInterval'])
