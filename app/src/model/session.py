class Session():
    def __init__(self, username):
        self.username = username
        self.entries = []
    
    @property
    def first_date(self):
        return self.entries[-1].date_collected

    @property
    def last_date(self):
        return self.entries[0].date_collected

    @property
    def total_entries(self):
        return len(self.entries)

    @property 
    def total_matches(self):
        total = 0
        for m in self.entries:
            if m.game_mode == "solo" or m.game_mode == "duos" or m.game_mode == "trios":
                total += m.matches
        return total

    @property 
    def total_kills(self):
        total = 0
        for m in self.entries:
            if m.game_mode == "solo" or m.game_mode == "duos" or m.game_mode == "trios":
                total += m.kills
        return total
    
    @property 
    def total_eskores(self):
        total = 0
        for m in self.entries:
            if m.game_mode == "solo" or m.game_mode == "duos" or m.game_mode == "trios":
                total += m.eskores
        return total
    
    @property
    def kill_ratio(self):
        return self.total_kills / self.total_matches
    
    @property
    def eskores_ratio(self):
        return self.total_eskores / self.total_matches
    
    @property
    def best_match(self):
        best_tmp =  0
        for m in self.entries:
            if m.kills > best_tmp:
                if m.game_mode == "solo" or m.game_mode == "duos" or m.game_mode == "trios":
                    best_tmp = m.kills
        return best_tmp
    @property
    def last_trn_rating_solo(self):
        for m in self.entries:
            if m.game_mode == "solo":
                return m.trn_Rating
    
    @property
    def last_trn_rating_duos(self):
        for m in self.entries:
            if m.game_mode == "duos":
                return m.trn_Rating
    
    @property
    def last_trn_rating_trios(self):
        for m in self.entries:
            if m.game_mode == "trios":
                return m.trn_Rating
    
    @property
    def first_trn_rating_solo(self):
        inv_entries = self.entries[::-1]
        for m in inv_entries:
            if m.game_mode == "solo":
                return m.trn_Rating
    
    @property
    def first_trn_rating_duos(self):
        inv_entries = self.entries[::-1]
        for m in inv_entries:
            if m.game_mode == "duos":
                return m.trn_Rating
    
    @property
    def first_trn_rating_trios(self):
        inv_entries = self.entries[::-1]
        for m in inv_entries:
            if m.game_mode == "trios":
                return m.trn_Rating

    def add_match(self, entry):
        self.entries.append(entry)
        self.entries = sorted(self.entries, key=lambda item: item.date_collected, reverse=True)
        
    def get_dict(self):
        new_dict = {
            "username": self.username,
            "first_date": self.first_date,
            "last_date": self.last_date,
            "last_trn_rating_solo": self.last_trn_rating_solo,
            "last_trn_rating_duos": self.last_trn_rating_duos,
            "last_trn_rating_trios": self.last_trn_rating_trios,
            "first_trn_rating_solo": self.first_trn_rating_solo,
            "first_trn_rating_duos": self.first_trn_rating_duos,
            "first_trn_rating_trios": self.first_trn_rating_trios,
            "total_entries": self.total_entries,
            "total_matches": self.total_matches,
            "total_kills": self.total_kills,
            "total_eskores": self.total_eskores,
            "kill_ratio": self.kill_ratio,
            "eskores_ratio": self.eskores_ratio,
            "best_match": self.best_match,
            "entries": {}
        }

        new_dict["entries"] = [m.get_dict() for m in self.entries]
        return new_dict
