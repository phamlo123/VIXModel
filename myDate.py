
num_strike_selected = 40
strike_Delta = 5
forecast_horizon = 30


def get_options_in_strike_range (strike_range: list, list_options):
    result = list ()
    for option in list_options:
        if option.strike >= strike_range[0] or option.strike <= strike_range[len (strike_range) - 1]:
            result.append (option)
    return result


# this class represents a trading day, which has a unique time stamp starting from 1, being the earliest day we include in
# our analysis; a list of options posted on that day; and a date in datetime format for referencing purposes

class Date:
    def __init__ (self, date: int, list_of_options: list, index_spot_price: float,
                  index_forward_price: float,
                  interest_rate: float,
                  nearest_strike_below_index: float):
        self.date = date
        self.list_of_options = list_of_options
        self.nearest_strike_below_index = nearest_strike_below_index
        self.interest_rate = interest_rate
        self.index_forward_price = index_forward_price
        self.index_spot_price = index_spot_price
        self.selectedStrikes = list

    # this method returns whether or not there is an option contract maturing 30 days from this day.
    def has_options_maturing_in_30_days (self) -> bool:
        for option in self.list_of_options:
            if option.exp_date == self.date + 30:
                return True
            else:
                continue
        return False

    # this method returns a list of Options that will mature exactly 30 days from this day, according to this day records.
    def get_options_maturing_in_30 (self) -> list:
        result = []
        for option in self.list_of_options:
            if option.exp_date == self.date + 30:
                result.append (option)

        return result

    def selectStrike (self) -> list:
        selected_strikes = list ()
        for i in range (num_strike_selected):
            selected_strikes.append (self.nearest_strike_below_index + (i + 1) * strike_Delta)

        for i in range (num_strike_selected):
            selected_strikes.insert (0, self.nearest_strike_below_index - (i + 1) * strike_Delta)

        self.selectedStrikes = selected_strikes
        return selected_strikes
