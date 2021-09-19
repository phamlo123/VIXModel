from datetime import timedelta


class Option:
    def __init__ (self, date: timedelta.days, strike, exp_date: timedelta, quote, term_interest_rate):
        self.date = date
        self.strike = strike
        self.exp_date = exp_date
        self.quote = quote
        self.term_interest_rate = term_interest_rate

    def has_30_day_tenor (self):
        return self.exp_date - self.date == 30

    def get_time_to_maturity(self):
        return self.exp_date - self.date






