class Match():
    def __init__(self, username):
        self.username = username
        self.id = ""
        self.date_collected = ""
        self.kills = ""
        self.matches = ""
        self.playlist = ""
        self.score = ""
        self.top1 = ""
        self.top10 = ""
        self.top12 = ""
        self.top25 = ""
        self.top3 = ""
        self.top5 = ""
        self.top6 = ""
        #self.trn_rating = data["trnRating"]
        
        self.game_mode = ""
        self.eskores = ""

    def fill(self, data):
        self.id = data["id"]
        self.date_collected = data["dateCollected"]
        self.kills = data["kills"]
        self.matches = data["matches"]
        self.playlist = data["playlist"]
        self.score = data["score"]
        self.top1 = data["top1"]
        self.top10 = data["top10"]
        self.top12 = data["top12"]
        self.top25 = data["top25"]
        self.top3 = data["top3"]
        self.top5 = data["top5"]
        self.top6 = data["top6"]
        #self.trn_rating = data["trnRating"]
        
        self.game_mode = self.get_game_mode()
        self.eskores = self.get_eskores()
    def get_game_mode(self):
        if self.playlist == "p1":
            return "solo"
        elif self.playlist == "p9":
            return "trios"
        elif self.playlist == "p10":
            return "duos"
        elif self.playlist == "misc":
            return "creative"
        else:
            return self.playlist
    
    def get_eskores(self):
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
