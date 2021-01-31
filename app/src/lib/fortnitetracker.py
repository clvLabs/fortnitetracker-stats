#!/usr/bin/env python3
import logging
import json
import time
import requests


class FortniteTracker():

    def __init__(self, cfg, loggerName):
        self.log = logging.getLogger(loggerName)
        self.cfg = cfg
        self.lastRequestTime = 0
        self.cancelRequest = False


    def cancelRequest(self):
        self.cancelRequest = True


    def getTrackerPage(self, trn_username):
        trackerUrl = self.cfg['fortniteTracker']['trackerURL']
        url = trackerUrl.format(trn_username=trn_username)
        return self._pageRequest(url)


    def getNotificationsPage(self, public_ip):
        notificationsUrl = self.cfg['fortniteTracker']['notificationsURL']
        url = notificationsUrl.format(public_ip=public_ip)
        return self._pageRequest(url)


    def getUserProfile(self, trn_username, platform):
        url = self._buildApiUrl('profile').format(platform=platform, trn_username=trn_username)

        profile = self._apiRequest(url)

        if profile and 'accountId' in profile:
            return profile
        else:
            self.log.debug(f"Response: {profile}")
            return None


    def getUserMatches(self, user_id):
        url = self._buildApiUrl('matches').format(user_id=user_id)

        matches = self._apiRequest(url)

        # Make sure we have a valid response
        if matches and type(matches) is not list:
            self.log.warning(f"Can't get matches for user {user_id}")
            self.log.debug(f"Response: {matches}")
            return None
        else:
            return matches


    def _buildApiUrl(self, pathType):
        baseUrl = self.cfg['fortniteTracker']['api']['baseUrl']
        path = self.cfg['fortniteTracker']['api']['paths'][pathType]
        return f"{baseUrl}/{path}"


    def _pageRequest(self, url, headers=None):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                self.log.warning(f"HTTP status {response.status_code}")
                return None
        except:
            self.log.exception("EXCEPTION requesting page")
            return None

        return response.text


    def _apiRequest(self, url):
        requestDelay = self.cfg['fortniteTracker']['api']['requestDelay']

        # Check if we have to wait until requestDelay
        if time.time() < self.lastRequestTime + requestDelay:
            if self.cancelRequest:
                return None
            time.sleep(0.1)

        requestHeaders = { "TRN-Api-Key": self.cfg['fortniteTracker']['api']['key'] }
        apiResponse = self._pageRequest(url, headers=requestHeaders)

        self.lastRequestTime = time.time()

        if not apiResponse:
            return None

        try:
            apiResponseObj = json.loads(apiResponse)
        except:
            self.log.exception(f"EXCEPTION getting api json response")
            self.log.debug(f"Api response:\n{apiResponse}")
            return None

        return apiResponseObj
