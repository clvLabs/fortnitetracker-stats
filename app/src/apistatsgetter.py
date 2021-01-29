#!/usr/bin/env python3
import logging
import time
import requests
import threading

class APIStatsGetter():

  def __init__(self, cfg):
    self.log = logging.getLogger('APIStatsGetter')
    self.log.info("Initializing")

    self.updateConfig(cfg, initialUpdate=True)

    self.thread = None          # Thread object
    self.threadrunning = False  # Is the thread running?


  # [ Public methods ] #################################################################

  def start(self):
    self.log.info("Starting")

    if self.threadrunning:
      return
    
    # We grab the users_ids and retain until next start
    self.fill_users_id()

    try:
      self.threadrunning = True
      self.thread = threading.Thread(target=self._threadhandler, args=())
      self.thread.start()
    except:
      self.log.exception("Exception in start()")


  def stop(self):
    self.log.info("Stopping")

    if not self.threadrunning:
      return

    self.threadrunning = False
    self.thread.join()


  def updateConfig(self, cfg, initialUpdate=False):
    self.cfg = cfg
    if initialUpdate:
      self.log.info("Configuration:")
    else:
      self.log.info("Configuration UPDATED:")

    self.log.info(f" - Request delay : {self.cfg['apiStatsGetter']['requestDelay']}s")

  def fill_users_id(self):
    for user in self.cfg['profiles']:
      self.log.info(f"[{user['trn_username']}] Requesting profile data")
      user['user_id'] = self.get_user_id(user['trn_username'], user['platform'])

  def get_user_id(self, trn_user, platform):
    profile_response_dict = self.get_user_profile(trn_user, platform)
    return profile_response_dict['accountId']

  def get_user_profile(self, trn_user, platform):
    profile_response = requests.get(self.cfg['apiStatsGetter']['profileURL'].format(platform=platform, trn_username=trn_username), headers = self.cfg['apiHeaders'])
    profile_response_dict = json.loads(profile_response.text)
    return profile_response_dict
  
  # [ Private methods ] #################################################################

  def _threadsleep(self, seconds):
    elapsed = 0

    while elapsed < seconds:
      time.sleep(0.1)
      elapsed += 0.1
      if not self.threadrunning:
        return False  # Wait cancelled, please exit

    return True # Wait finished, continue working


  def _threadhandler(self):
    while self.threadrunning:
      self.log.info("New api stats update --------------------------------")

      # Fill this with beautiful code   :-p

      # Recorremos el array de profiles de los que tenemos que recopilar datos
      for user in self.cfg['profiles']:
        # path to data file
        filename = f"/data/{user['username']}_matches.json"
        self.log.info(f"Requesting matches for {user['username']}")
        # hacemos el request
        matches_response = requests.get(
                            self.cfg['apiStatsGetter']['matchesURL'].format(user_id=user['user_id']), 
                            headers=self.cfg['apiHeaders'])
        matches_actual_dict = json.loads(matches_response.text)

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

      self._threadsleep(self.cfg['apiStatsGetter']['requestDelay'])
