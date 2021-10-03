class Option:
    def __init__ (self, id, date, strike, cp, date_till_expiration, bid, ask):
        self.id = id
        self.date = date
        self.cp = cp
        self.strike = strike
        self.date_till_expiration = date_till_expiration
        self.quote = (bid + ask) / 2

    def has_30_day_tenor (self):
        return self.date_till_expiration == 30

    def get_time_to_maturity (self):
        return self.date_till_expiration
