import datetime


class Date:
    def __init__ (self, date):
        self.date = date

    def has30DayOptionTenures (self, listOfOptions: list) -> bool:
        for option in listOfOptions:
            if option.expDate == self.date + 30:
                return True
            else:
                continue

