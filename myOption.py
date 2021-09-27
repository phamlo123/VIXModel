class Option:
    def __init__ (self, id, date, strike, cp, exp_date, bid, ask):
        self.id = id
        self.date = date
        self.cp = cp
        self.strike = strike
        self.exp_date = exp_date
        self.quote = 0

    def has_30_day_tenor (self):
        return self.exp_date - self.date == 30

    def get_time_to_maturity (self):
        return self.exp_date - self.date




