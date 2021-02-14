#!/usr/bin/env python3
import logging
from typing import List
import requests
import json

from .lib.task import Task
from .lib.fortnitetracker import FortniteTracker

DATA_FOLDER = "/fortnitetracker-stats/data"


class APIStatsGetter(Task):

    def __init__(self, cfg):
        super().__init__(cfg)
        self.log = logging.getLogger('APIStatsGetter')
        self.log.info("Initializing")
        self.tracker = FortniteTracker(self.cfg, 'APIStatsGetter')


    def start(self):
        ''' Override of Task.start() '''
        if not self.cfg['apiStatsGetter']['enabled']:
            self.log.warning("Skipping start (disabled in config)")
            return

        super().start()


    def stop(self):
        ''' Override of Task.stop() '''
        self.tracker.stop()
        super().stop()


    def fill_users_id(self):
        for user in self.cfg['profiles']:
            username = user['username']
            user_id = self.get_user_id(username)

            if self.stopRequested:
                return

            if user_id:
                self.log.info(f"[{username}] Profile data received")
                user['user_id'] = user_id
            else:
                self.log.warning(f"[{username}] User will be IGNORED")


    def get_user_id(self, username):
        filename = f"{DATA_FOLDER}/{username}_trn_profile.json"

        try:
            with open(filename, 'r') as f:
                profile = json.loads(f.read())
            return profile['accountId']
        except FileNotFoundError:
            self.log.info(f"[{username}] Profile file not found.")

    def taskSetup(self):
        ''' Override of Task.taskSetup() '''
        self.log.info("Task setup")
        # Grab the users_ids and retain until next start
        self.log.info(f"Getting user IDs")
        self.fill_users_id()
        self.log.info("Task setup FINISHED")


    def taskLoop(self):
        ''' Override of Task.taskLoop() '''
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

            if self.stopRequested:
                return

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
