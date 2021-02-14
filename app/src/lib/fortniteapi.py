#!/usr/bin/env python3
import logging
import json
import time
import requests


class FortniteApi():

    def __init__(self, cfg, loggerName):
        self.log = logging.getLogger(loggerName)
        self.cfg = cfg
        self.lastRequestTime = 0
        self.stopRequested = False


    def stop(self):
        self.stopRequested = True


    def getUserProfile(self, username, account_type):
        url = self._buildApiUrl('profile').format(username=username, account_type=account_type)

        profile = self._apiRequest(url)

        if self.stopRequested:
            return None

        if profile:
            return profile
        else:
            self.log.debug(f"Response: {profile}")
            return None


    def _buildApiUrl(self, pathType):
        baseUrl = self.cfg['fortnite-api']['api']['baseUrl']
        path = self.cfg['fortnite-api']['api']['paths'][pathType]
        return f"{baseUrl}/{path}"


    def _pageRequest(self, url, headers=None):
        if self.stopRequested:
            return None

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
        if self.stopRequested:
            return None

        requestDelay = self.cfg['fortnite-api']['api']['requestDelay']

        # Check if we have to wait until requestDelay
        nextRequestTime = self.lastRequestTime + requestDelay
        remaining = nextRequestTime - time.time()

        # if remaining > 0:
        #     self.log.debug(f"[API] Waiting {remaining:5.3f}s before next request")

        while remaining > 0:
            if self.stopRequested:
                self.log.warning(f"[API] Wait cancelled - stop requested")
                return None
            time.sleep(0.1)
            remaining = nextRequestTime - time.time()

        apiResponse = self._pageRequest(url)

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
