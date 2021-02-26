import logging
import json
from datetime import datetime
from .stats_item import StatsItem

DATA_FOLDER = "/fortnitetracker-stats/data"

class Stats():
    def __init__(self, _cfg):
        self.log = logging.getLogger('model_stats')
        self.cfg = _cfg
        self.overall = []
        self.solo = []
        self.duos = []
        self.squad = []


    def fill_for_user(self, username):
        filename = f"{DATA_FOLDER}/{username}_stats.json"
        self.fill_from_file(filename)


    def fill_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                dict_stats = json.loads(f.read())
            if dict_stats:
                for s in dict_stats["overall"]:
                    self.overall.append(StatsItem.from_dict(s))
                #self.overall = [s.from_trn_dict() for s in dict_stats["overall"]]
                for s in dict_stats["solo"]:
                    self.solo.append(StatsItem.from_dict(s))
                for s in dict_stats["duos"]:
                    self.duos.append(StatsItem.from_dict(s))
                for s in dict_stats["squad"]:
                    self.squad.append(StatsItem.from_dict(s))
        except FileNotFoundError:
            #Not found, pues nada, pasamos del tema
            return
    

    def add_stats(self, game_mode, trn_data):
        if game_mode == "solo":
            self.solo.append(StatsItem.from_trn_dict("solo", trn_data))
        elif game_mode == "duos":
            self.duos.append(StatsItem.from_trn_dict("duos", trn_data))
        elif game_mode == "squad":
            self.squad.append(StatsItem.from_trn_dict("squad", trn_data))

    
    def add_stats_from_trn_dict(self, username, trn_data):
        try:
            gap = self.cfg["sessions"]["gapBetweenSessions"] # gap en segundos
            last_match_date = datetime.strptime(trn_data["recentMatches"][0]["dateCollected"], "%Y-%m-%dT%H:%M:%S")
            now = datetime.now()
            interval = abs(now - last_match_date).seconds

            self.fill_for_user(username)
            # solo actualizamos stats si hemos cambiado de sesion y hay datos nuevos
            if interval > gap or not self.overall:
                new_data = False
                if self.solo:
                    if trn_data["stats"]["p2"]["matches"]["valueInt"] > self.solo[-1].matches:
                        self.solo.append(StatsItem.from_trn_dict("solo", trn_data))
                        new_data = True
                else:
                    self.solo.append(StatsItem.from_trn_dict("solo", trn_data))
                    new_data = True
                
                if self.duos:
                    if trn_data["stats"]["p10"]["matches"]["valueInt"] > self.duos[-1].matches:
                        self.duos.append(StatsItem.from_trn_dict("duos", trn_data))
                        new_data = True
                else:
                    self.duos.append(StatsItem.from_trn_dict("duos", trn_data))
                    new_data = True

                if self.squad:
                    if trn_data["stats"]["p9"]["matches"]["valueInt"] > self.squad[-1].matches:
                        self.squad.append(StatsItem.from_trn_dict("squad", trn_data))
                        new_data = True
                else:
                    self.squad.append(StatsItem.from_trn_dict("squad", trn_data))
                    new_data = True
                
                if new_data:
                    self.overall.append(self.get_new_overall())
        except:
            self.log.error("add_stats_from_trn_dict() Cant add stats, possible empty matches dict")


    def get_new_overall(self):
        new_stats_item = StatsItem()
        #self.overall.trn_rating = 
        new_stats_item.score = self.solo[-1].score + self.duos[-1].score + self.squad[-1].score
        new_stats_item.top1 = self.solo[-1].top1 + self.duos[-1].top1 + self.squad[-1].top1
        new_stats_item.top3 = self.solo[-1].top3 + self.duos[-1].top3 + self.squad[-1].top3
        new_stats_item.top5 = self.solo[-1].top5 + self.duos[-1].top5 + self.squad[-1].top5
        new_stats_item.top6 = self.solo[-1].top6 + self.duos[-1].top6 + self.squad[-1].top6
        new_stats_item.top10 = self.solo[-1].top10 + self.duos[-1].top10 + self.squad[-1].top10
        new_stats_item.top12 = self.solo[-1].top12 + self.duos[-1].top12 + self.squad[-1].top12
        new_stats_item.top25 = self.solo[-1].top25 + self.duos[-1].top25 + self.squad[-1].top25
        new_stats_item.kd = (self.solo[-1].kd + self.duos[-1].kd + self.squad[-1].kd) / 3
        new_stats_item.matches = self.solo[-1].matches + self.duos[-1].matches + self.squad[-1].matches
        new_stats_item.kills = self.solo[-1].kills + self.duos[-1].kills + self.squad[-1].kills
        new_stats_item.minutes_played = self.solo[-1].minutes_played + self.duos[-1].minutes_played + self.squad[-1].minutes_played
        now = datetime.now()
        new_stats_item.date = now.strftime("%Y-%m-%dT%H:%M:%S")
        return new_stats_item


    def get_dict(self):
        new_dict = {
            "overall": {},
            "solo": {},
            "duos": {},
            "squad": {}
        }
        new_dict["overall"] = [s.get_dict() for s in self.overall]
        new_dict["solo"] = [s.get_dict() for s in self.solo]
        new_dict["duos"] = [s.get_dict() for s in self.duos]
        new_dict["squad"] = [s.get_dict() for s in self.squad]
        return new_dict