class Session():
    def __init__(self, username):
        self.username = username
        self.first_date = "3021-02-10T16:58:00.0000000"
        self.last_date = "1978-03-10T00:00:00.0000000"
        self.total_matches = 0
        self.matches = []
    
    def get_killdeath_ratio(self):
        data = 0
        return data
    
    def add_match(self, match):
        self.matches.append(match)
        self.total_matches = len(self.matches)
        if match["dateCollected"] > self.last_date:
            self.last_date = match["dateCollected"]
        if match["dateCollected"] < self.first_date:
            self.first_date = match["dateCollected"]
        

