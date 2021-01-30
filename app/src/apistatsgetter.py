#!/usr/bin/env python3
import logging
from typing import List
import requests
import json

from src.lib.taskthread import TaskThread

DATA_FOLDER = "/fortnitetracker-stats/data"

class APIStatsGetter(TaskThread):

  def __init__(self, cfg):
    super().__init__()

    self.log = logging.getLogger('APIStatsGetter')
    self.log.info("Initializing")

    self.updateConfig(cfg, initialUpdate=True)

    # We grab the users_ids and retain until next start
    self.fill_users_id()


  def updateConfig(self, cfg, initialUpdate=False):
    self.cfg = cfg
    if initialUpdate:
      self.log.info("Configuration:")
    else:
      self.log.info("Configuration UPDATED:")

    self.log.info(f" - Request delay : {self.cfg['apiStatsGetter']['requestDelay']}s")


  def fill_users_id(self):
    for user in self.cfg['profiles']:
      self.log.info(f"[{user['username']}] Requesting profile data")
      user_id = self.get_user_id(user['trn_username'], user['platform'])
      if user_id:
        user['user_id'] = user_id


  def get_user_id(self, trn_user, platform):
    profile_response_dict = self.get_user_profile(trn_user, platform)

    if profile_response_dict:
      return profile_response_dict['accountId']
    else:
      return None


  def get_user_profile(self, trn_user, platform):
    url = self.cfg['apiStatsGetter']['profileURL'].format(platform=platform, trn_username=trn_user)
    profile_response = requests.get(url, headers = self.cfg['apiHeaders'])
    try:
      profile_response_dict = json.loads(profile_response.text)
    except:
      self.log.exception(f"EXCEPTION getting profile info for {trn_user} - platform {platform}")
      return None

    if 'accountId' in profile_response_dict:
      return profile_response_dict
    else:
      self.log.error(f"Can't get profile info for {trn_user} - platform {platform}")
      self.log.error(f"Response: {profile_response_dict}")
      self.log.error(f"User {trn_user} will be IGNORED")
      return None


  def mainLoop(self):
    self.log.info("New api stats update --------------------------------")

    # Recorremos el array de profiles de los que tenemos que recopilar datos
    for user in self.cfg['profiles']:

      # Avoid checking users with no user_id (possible errors getting profile)
      if not 'user_id' in user:
        continue

      # path to data file
      filename = f"{DATA_FOLDER}/{user['username']}_matches.json"
      self.log.info(f"Requesting matches for {user['username']}")

      # hacemos el request
      url = self.cfg['apiStatsGetter']['matchesURL'].format(user_id=user['user_id'])
      matches_response = requests.get(url, headers=self.cfg['apiHeaders'])
      matches_actual_dict = json.loads(matches_response.text)

      # Make sure we have a valid response
      if type(matches_actual_dict) is not list:
        self.log.error(f"Can't get matches for {user['username']}")
        self.log.error(f"Response: {matches_actual_dict}")
        self.log.error(f"SKIPPING {user['username']}")
        continue

      try:
        # cargamos la historia de partidas, si peta, el try lo llevará
        # a la parte de código que crea el nuevo data file
        with open(filename, 'r') as f:
          matches_history_dict = json.loads(f.read())

        new_matches = 0
        # recorremos el array de partidas que hemos recibido con el request
        for match in matches_actual_dict:
          gotit = False
          # recorremos las partidas del history para comparar con las que hemos recibido
          for history_match in matches_history_dict:
            if match['id'] == history_match['id']:
              gotit = True
              break
          # si no la hemos encontrado en la historia, la añadimos
          if not gotit:
            new_matches += 1
            matches_history_dict.insert(0,match)

        if new_matches > 0:
          self.log.info(f"Added {str(new_matches)} new matches")
          with open(filename, 'w') as f:
            json.dump(matches_history_dict, f)
        else:
          self.log.info("No new matches")
      except FileNotFoundError:
        # No se ha encontrado el fichero, asi que lo creamos con los datos recibidos
        self.log.info("History not found. Creating new file")
        with open(filename, 'w') as f:
          json.dump(matches_actual_dict, f)
    # # #

    self.log.info("Api stats update FINISHED --------------------------------")

    self._threadsleep(self.cfg['apiStatsGetter']['requestDelay'])
