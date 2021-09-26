

class Option:
    def __init__ (self, id,  date , strike, exp_date , bid, ask, term_interest_rate):
        self.id = id
        self.date = date
        self.strike = strike
        self.exp_date = exp_date
        self.quote = (bid + ask) / 2
        self.term_interest_rate = term_interest_rate

    def has_30_day_tenor (self):
        return self.exp_date - self.date == 30

    def get_time_to_maturity (self):
        return self.exp_date - self.date


