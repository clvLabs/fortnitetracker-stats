import json
import logging

logger = logging.getLogger('model/match')

class Match():
    def __init__(self, username):
        
        self.username = username
        self.id = 0
        self.date_collected = ""
        self.kills = 0
        self.matches = 0
        self.playlist = ""
        self.score = 0
        self.top1 = 0
        self.top10 = 0
        self.top12 = 0
        self.top25 = 0
        self.top3 = 0
        self.top5 = 0
        self.top6 = 0
        self.trn_Rating = 0


    @staticmethod
    def from_dict(dict_, username):
        new_match = Match(username)
        new_match._fill(dict_)
        return new_match


    @staticmethod
    def from_file(filename, username):
        matches = []
        try:
            with open(filename, 'r') as f:
                original_matches = json.loads(f.read())
            for m in original_matches:
                matches.append(Match.from_dict(m, username))
        except FileNotFoundError:
            logger.debug(f"username {username} not found")
        return matches
    
    @property
    def eskores(self):
        ret_val = 0
        ret_val += self.kills * 2
        ret_val += self.top1 * 15
        ret_val += self.top10 * 15
        ret_val += self.top12 * 15
        ret_val += self.top25 * 15
        ret_val += self.top3 * 15
        ret_val += self.top5 * 15
        ret_val += self.top6 * 15
        return ret_val
    
    @property
    def game_mode(self):
        if self.playlist == "p2":
            return "solo"
        elif self.playlist == "p9":
            return "trios"
        elif self.playlist == "p10":
            return "duos"
        elif self.playlist == "misc":
            return "misc"
        else:
            return f"UNKNOWN [{self.playlist}]"


    def _fill(self, data):
        self.id = data.get("id", 0)
        self.date_collected = data.get("dateCollected","")
        self.kills = data.get("kills",0)
        self.matches = data.get("matches",0)
        self.playlist = data.get("playlist","")
        self.score = data.get("score",0)
        self.top1 = data.get("top1",0)
        self.top10 = data.get("top10",0)
        self.top12 = data.get("top12",0)
        self.top25 = data.get("top25",0)
        self.top3 = data.get("top3",0)
        self.top5 = data.get("top5",0)
        self.top6 = data.get("top6",0)
        self.trn_Rating = data.get("trnRating", 0)


    def get_dict(self):
        new_dict = {
            "username": self.username,
            "id": self.id,
            "date_collected": self.date_collected,
            "kills": self.kills,
            "matches": self.matches,
            "playlist": self.playlist,
            "score": self.score,
            "top1": self.top1,
            "top10": self.top10,
            "top12": self.top12,
            "top25": self.top25,
            "top3": self.top3,
            "top5": self.top5,
            "top6": self.top6,
            "trn_Rating": self.trn_Rating,
            "eskores": self.eskores,
            "game_mode": self.game_mode,
        }
        return new_dict
    

