#!/usr/bin/env python3
import logging
from typing import List
import requests
import json

from .lib.task import Task
from .lib.fortnitetracker import FortniteTracker
from .lib.fortniteapi import FortniteApi

DATA_FOLDER = "/fortnitetracker-stats/data"

class APIProfilesGetter(Task):

    def __init__(self, cfg):
        super().__init__(cfg)
        self.log = logging.getLogger('APIProfilesGetter')
        self.log.info("Initializing")
        self.tracker = FortniteTracker(self.cfg, 'APIProfilesGetter')
        self.fortniteapi = FortniteApi(self.cfg, 'APIProfilesGetter')

    
    def start(self):
        ''' Override of Task.start() '''
        if not self.cfg['apiProfilesGetter']['enabled']:
            self.log.warning("Skipping start (disabled in config)")
            return

        super().start()


    def stop(self):
        ''' Override of Task.stop() '''
        self.tracker.stop()
        self.fortniteapi.stop()
        super().stop()


    # def taskSetup(self):
    #     ''' Override of Task.taskSetup() '''
    #     self.log.info("Task setup")
    #     # Grab the users_ids and retain until next start
    #     self.log.info(f"Getting user IDs")
    #     self.fill_users_id()
    #     self.log.info("Task setup FINISHED")


    def taskLoop(self):
        ''' Override of Task.taskLoop() '''
        self.log.info("New api profiles update --------------------------------")

        # loop through the profiles array
        for user in self.cfg['profiles']:

            username = user['username']
            trn_username = user['trn_username']
            platform = user['platform']
            account_type = user['account_type']

            self.getProfileFromTrn(username, trn_username, platform)
            self.getProfileFromFortniteApi(username, account_type)

        # # 

        self.log.info("Api stats update FINISHED --------------------------------")

        self._threadsleep(self.cfg['apiStatsGetter']['statusGetInterval'])

    def getProfileFromTrn(self, username, trn_username, platform):
        filename = f"{DATA_FOLDER}/{username}_trn_profile.json"
        self.log.info(f"[{username}] Requesting profile from tracking network")
        trn_profile_actual_dict = self.tracker.getUserProfile(trn_username, platform)

        if self.stopRequested:
            return
        
        if not trn_profile_actual_dict:
            self.log.warning(f"[{username}] Can't get profile from tracking network api")
            return
        
        self.log.info(f"[{username}] Writing profile from tracking network")
        with open(filename, 'w') as f:
            json.dump(trn_profile_actual_dict, f)


    def getProfileFromFortniteApi(self, username, account_type):
        filename = f"{DATA_FOLDER}/{username}_fortnite-api_profile.json"
        self.log.info(f"[{username}] Requesting profile from Fortnite-Api")
        fapi_profile_actual_dict = self.fortniteapi.getUserProfile(username, account_type)

        if self.stopRequested:
            return
        
        if not fapi_profile_actual_dict:
            self.log.warning(f"[{username}] Can't get profile from fortnite api")
            return
        
        self.log.info(f"[{username}] Writing profile from fortnite api")
        with open(filename, 'w') as f:
            json.dump(fapi_profile_actual_dict, f)