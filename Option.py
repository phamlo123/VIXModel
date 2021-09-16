import datetime


class Option:
    def __init__ (self, date: datetime, strike, expDate: datetime, quote):
        self.date = date
        self.strike = strike
        self.expDate = expDate
        self.quote = quote

    def has30dayTenor (self):
        return self.expDate - self.date == 30
