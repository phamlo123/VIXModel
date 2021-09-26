from collections import Set
from typing import List

import Option


def get_options_in_strike_range (strike_range: dict, list_options):
    result = []
    for option in list_options:
        if option.strike >= strike_range[0] or option.strike <= strike_range[1]:
            result.append (option)

    return result


# this class represents a trading day, which has a unique time stamp starting from 1, being the earliest day we include in
# our analysis; a list of options posted on that day; and a date in datetime format for referencing purposes

class Date:
    def __init__ (self, timeInDaysFrom0: int, date : int, time_stamp, list_of_options, index_spot_price,
                  index_forward_price,
                  interest_rate,
                  nearest_strike_below_index):
        self.timeInDaysFrom0 = timeInDaysFrom0
        self.date = date
        self.time_stamp = time_stamp
        self.list_of_options = list_of_options
        self.nearest_strike_below_index = nearest_strike_below_index
        self.interest_rate = interest_rate
        self.index_forward_price = index_forward_price
        self.index_spot_price = index_spot_price

    # this method returns whether or not there is an option contract maturing 30 days from this day.
    def has_options_maturing_in_30_days (self) -> bool:
        for option in self.list_of_options:
            if option.exp_date == self.date + 30:
                return True
            else:
                continue
        return False

    # this method returns a list of Options that will mature exactly 30 days from this day, according to this day records.
    def get_options_maturing_in_30 (self) -> List[Option]:
        result = []
        for option in self.list_of_options:
            if option.exp_date == self.date + 30:
                result.append (option)

        return result
