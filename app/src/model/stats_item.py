from datetime import datetime

class StatsItem():
    def __init__(self):
        self.game_mode = ""
        self.trn_rating = 0
        self.score = 0
        self.top1 = 0
        self.top3 = 0
        self.top5 = 0
        self.top6 = 0
        self.top10 = 0
        self.top12 = 0
        self.top25 = 0
        self.kd = 0
        self.matches = 0
        self.kills = 0
        self.minutes_played = 0
        self.date = ""


    @staticmethod
    def from_dict(dict):
        new_item = StatsItem()
        new_item.game_mode = dict["game_mode"]
        new_item.trn_rating = dict["trn_rating"]
        new_item.score = dict["score"]
        new_item.top1 = dict["top1"]
        new_item.top3 = dict["top3"]
        new_item.top5 = dict["top5"]
        new_item.top6 = dict["top6"]
        new_item.top1 = dict["top1"]
        new_item.top12 = dict["top12"]
        new_item.top25 = dict["top25"]
        new_item.kd = dict["kd"]
        new_item.matches = dict["matches"]
        new_item.kills = dict["kills"]
        new_item.minutes_played = dict["minutes_played"]
        new_item.date = dict["date"]
        return new_item

    @staticmethod 
    def from_trn_dict(game_mode, trn_stats):
        new_item = StatsItem()
        new_item.game_mode = game_mode

        if game_mode == "solo":
            trn_playlist = "p2"
        elif game_mode == "duos":
            trn_playlist = "p10"
        elif game_mode == "squad":
            trn_playlist = "p9"
        else:
            return new_item

        new_item.trn_rating = trn_stats["stats"][trn_playlist]["trnRating"]["valueInt"]
        new_item.score = trn_stats["stats"][trn_playlist]["score"]["valueInt"]
        new_item.top1 = trn_stats["stats"][trn_playlist]["top1"]["valueInt"]
        new_item.top3 = trn_stats["stats"][trn_playlist]["top3"]["valueInt"]
        new_item.top5 = trn_stats["stats"][trn_playlist]["top5"]["valueInt"]
        new_item.top6 = trn_stats["stats"][trn_playlist]["top6"]["valueInt"]
        new_item.top10 = trn_stats["stats"][trn_playlist]["top10"]["valueInt"]
        new_item.top12 = trn_stats["stats"][trn_playlist]["top12"]["valueInt"]
        new_item.top25 = trn_stats["stats"][trn_playlist]["top25"]["valueInt"]
        new_item.kd = trn_stats["stats"][trn_playlist]["kd"]["valueDec"]
        new_item.matches = trn_stats["stats"][trn_playlist]["matches"]["valueInt"]
        new_item.kills = trn_stats["stats"][trn_playlist]["kills"]["valueInt"]
        new_item.minutes_played = trn_stats["stats"][trn_playlist]["minutesPlayed"]["valueInt"]
        now = datetime.now()
        new_item.date = now.strftime("%Y-%m-%dT%H:%M:%S")

        return new_item


    def get_dict(self):
        new_dict = {
            "game_mode": self.game_mode,
            "trn_rating": self.trn_rating,
            "score": self.score,
            "top1": self.top1,
            "top3": self.top3,
            "top5": self.top5,
            "top6": self.top6,
            "top10": self.top10,
            "top12": self.top12,
            "top25": self.top25,
            "kd": self.kd,
            "matches": self.matches,
            "kills": self.kills,
            "minutes_played": self.minutes_played,
            "date": self.date
        }
        return new_dict



        