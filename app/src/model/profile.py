import json
import logging

logger = logging.getLogger('model/profile')

class Profile():
    def __init__(self):
        self.id = ""
        self.name = ""
        self.country = ""
        self.stats_image = ""
        self.battle_pass_level = -1
        self.battle_pass_progress = -1


    @staticmethod
    def from_files(trn_filename, fapi_filename):
        new_profile = Profile()
        new_profile.add_trn_from_file(trn_filename)
        new_profile.add_fapi_from_file(fapi_filename)
        return new_profile
        

    def add_trn_from_file(self, trn_filename):
        try:
            with open(trn_filename, 'r') as f:
                dict_profile = json.loads(f.read())
            if dict_profile:
                self.add_trn_data_from_dict(dict_profile)
        except FileNotFoundError:
            logger.debug(f"{self.name} trn profile file not found")


    def add_trn_data_from_dict(self, trn_dict):
        self.id = trn_dict["accountId"]
        if 'country' in trn_dict.keys():
            self.country = trn_dict["country"]


    def add_fapi_from_file(self, fapi_filename):
        try:
            with open(fapi_filename, 'r') as f:
                dict_profile = json.loads(f.read())
            if dict_profile:
                self.add_fapi_data_from_dict(dict_profile)
        except FileNotFoundError:
            logger.debug(f"{self.name} fortnite-api profile file not found")


    def add_fapi_data_from_dict(self, fapi_dict):
        self.name = fapi_dict["data"]["account"]["name"]
        self.stats_image = fapi_dict["data"]["image"]
        self.battle_pass_level = fapi_dict["data"]["battlePass"]["level"]
        self.battle_pass_progress = fapi_dict["data"]["battlePass"]["progress"]


    def get_dict(self):
        new_dict = {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "stats_image": self.stats_image,
            "battle_pass_level": self.battle_pass_level,
            "battle_pass_progress": self.battle_pass_progress,
        }

        return new_dict