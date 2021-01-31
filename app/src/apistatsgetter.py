#!/usr/bin/env python3
import logging
from typing import List
import requests
import json

from src.lib.taskthread import TaskThread
from src.lib.fortnitetracker import FortniteTracker

DATA_FOLDER = "/fortnitetracker-stats/data"


class APIStatsGetter(TaskThread):

    def __init__(self, cfg):
        super().__init__(cfg)

        self.log = logging.getLogger('APIStatsGetter')
        self.log.info("Initializing")

        self.tracker = FortniteTracker(self.cfg, 'APIStatsGetter')

        # Grab the users_ids and retain until next start
        self.fill_users_id()


    def fill_users_id(self):
        for user in self.cfg['profiles']:
            username = user['username']
            self.log.info(f"[{username}] Requesting profile data")
            user_id = self.get_user_id(user)
            if user_id:
                self.log.info(f"[{username}] Profile data received")
                user['user_id'] = user_id
            else:
                self.log.warning(f"[{username}] User will be IGNORED")


    def get_user_id(self, user):
        profile = self.get_user_profile(user)
        if profile:
            return profile['accountId']
        else:
            return None


    def get_user_profile(self, user):
        username = user['username']
        trn_username = user['trn_username']
        platform = user['platform']

        profile = self.tracker.getUserProfile(trn_username, platform)
        if profile:
            return profile
        else:
            self.log.warning(f"[{username}] Can't get profile info for {trn_username} - platform {platform}")
            return None


    def mainLoop(self):
        self.log.info("New api stats update --------------------------------")

        # loop through the profiles array
        for user in self.cfg['profiles']:

            # Avoid checking users with no user_id (possible errors getting profile)
            if not 'user_id' in user:
                continue

            username = user['username']
            user_id = user['user_id']

            # path to data file
            filename = f"{DATA_FOLDER}/{username}_matches.json"
            self.log.info(f"[{username}] Requesting matches")

            # requesting
            matches_actual_dict = self.tracker.getUserMatches(user_id)

            # Make sure we have a valid response
            if not matches_actual_dict:
                self.log.warning(f"[{username}] Can't get matches")
                continue

            try:
                # load matches history, if throw an exception,
                # make the new matches history file
                with open(filename, 'r') as f:
                    matches_history_dict = json.loads(f.read())

                new_matches = 0
                # loop through the received matches array
                for match in matches_actual_dict:
                    gotit = False
                    # loop through matches history array to compare with received ones
                    for history_match in matches_history_dict:
                        if match['id'] == history_match['id']:
                            gotit = True
                            break
                    # if we didn't find it, we add it to the list
                    if not gotit:
                        new_matches += 1
                        matches_history_dict.insert(0, match)

                if new_matches > 0:
                    self.log.info(f"[{username}] Added {str(new_matches)} new matches")
                    with open(filename, 'w') as f:
                        json.dump(matches_history_dict, f)
                else:
                    self.log.info(f"[{username}] No new matches")
            except FileNotFoundError:
                # File not found, so we create the new one
                self.log.info(f"[{username}] History not found. Creating new file")
                with open(filename, 'w') as f:
                    json.dump(matches_actual_dict, f)

        # # #

        self.log.info("Api stats update FINISHED --------------------------------")

        self._threadsleep(self.cfg['apiStatsGetter']['statusGetInterval'])
