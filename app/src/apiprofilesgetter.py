#!/usr/bin/env python3
import logging
from typing import List
import requests
import json

from .lib.task import Task
from .lib.fortnitetracker import FortniteTracker
from .lib.fortniteapi import FortniteApi
from .model.profile import Profile
from .model.stats import Stats

DATA_FOLDER = "/fortnitetracker-stats/data"

class APIProfilesGetter(Task):

    def __init__(self, cfg):
        super().__init__(cfg)
        self.log = logging.getLogger('APIProfilesGetter')
        self.log.info("Initializing")
        self.tracker = FortniteTracker(self.cfg, 'APIProfilesGetter')
        self.fortniteapi = FortniteApi(self.cfg, 'APIProfilesGetter')
        self.profile = Profile()
        self.stats = Stats(cfg)

    
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


    def taskLoop(self):
        ''' Override of Task.taskLoop() '''
        self.log.info("New api profiles update --------------------------------")

        # loop through the profiles array
        for user in self.cfg['profiles']:

            username = user['username']
            trn_username = user['trn_username']
            platform = user['platform']
            account_type = user['account_type']

            # get data from sources
            self.getProfileFromTrn(username, trn_username, platform)
            self.getProfileFromFortniteApi(username, account_type)

            # save files
            self.save_profile_to_file(username)
            self.save_stats_to_file(username)

            # reiniciamos datos
            self.profile = Profile()
            self.stats = Stats(self.cfg)

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
        
        self.profile.add_trn_data_from_dict(trn_profile_actual_dict)
        self.stats.add_stats_from_trn_dict(trn_profile_actual_dict)

        # Activamos para debuggar la fuente de datos
        self.save_trn_profile_to_file(username, trn_profile_actual_dict)


    def getProfileFromFortniteApi(self, username, account_type):
        filename = f"{DATA_FOLDER}/{username}_fortnite-api_profile.json"
        self.log.info(f"[{username}] Requesting profile from Fortnite-Api")
        fapi_profile_actual_dict = self.fortniteapi.getUserProfile(username, account_type)

        if self.stopRequested:
            return
        
        if not fapi_profile_actual_dict:
            self.log.warning(f"[{username}] Can't get profile from fortnite api")
            return
        
        self.profile.add_fapi_data_from_dict(fapi_profile_actual_dict)


    def save_trn_profile_to_file(self, username, trn_data):
        filename = f"{DATA_FOLDER}/{username}_trn_profile.json"
        
        self.log.info(f"[{username}] Writing tracking network profile file")
        with open(filename, 'w') as f:
            json.dump(trn_data, f)


    def save_fapi_profile_to_file(self, username, fapi_data):
        filename = f"{DATA_FOLDER}/{username}_fortnite-api_profile.json"
        
        self.log.info(f"[{username}] Writing fortnite-api profile file")
        with open(filename, 'w') as f:
            json.dump(fapi_data, f)


    def save_profile_to_file(self, username):
        filename = f"{DATA_FOLDER}/{username}_profile.json"
        
        self.log.info(f"[{username}] Writing profile file")
        with open(filename, 'w') as f:
            json.dump(self.profile.get_dict(), f)


    def save_stats_to_file(self, username):
        filename = f"{DATA_FOLDER}/{username}_stats.json"
        
        self.log.info(f"[{username}] Writing stats file")
        with open(filename, 'w') as f:
            json.dump(self.stats.get_dict(), f)