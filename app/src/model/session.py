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
            total += m.matches
        return total

    @property 
    def total_kills(self):
        total = 0
        for m in self.entries:
            total += m.kills
        return total
    
    @property 
    def total_eskores(self):
        total = 0
        for m in self.entries:
            total += m.eskores
        return total
    
    @property
    def kill_ratio(self):
        return self.total_kills / self.total_matches
    
    @property
    def eskores_ratio(self):
        return self.total_eskores / self.total_matches
    
    def add_match(self, entry):
        self.entries.append(entry)
        self.entries = sorted(self.entries, key=lambda item: item.date_collected, reverse=True)
        
    def get_dict(self):
        new_dict = {
            "username": self.username,
            "first_date": self.first_date,
            "last_date": self.last_date,
            "total_entries": self.total_entries,
            "total_matches": self.total_matches,
            "total_kills": self.total_kills,
            "total_eskores": self.total_eskores,
            "kill_ratio": self.kill_ratio,
            "eskores_ratio": self.eskores_ratio,
            "entries": {}
        }

        new_dict["entries"] = [m.get_dict() for m in self.entries]
        return new_dict
