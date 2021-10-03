num_strike_selected = 40
strike_Delta = 5
forecast_horizon = 30


# get nearest strike price below spot among the list of options on this date
def getNearestStrikeBelowSpot (index_spot_price, list_of_options):
    list_of_strikes = []
    for item in list_of_options:
        if item.strike <= index_spot_price:
            list_of_strikes.append (item.strike)
    nearest = list_of_strikes[0]
    for k in list_of_strikes:
        if abs (k - index_spot_price) < abs (nearest - index_spot_price):
            nearest = k
    return nearest


# This function returns a list of of options that have strikes within the given list of selected strikes and has the given maturity (number of days counted from this date)
def get_options_in_strike_range (strike_range, list_options, maturity: int):
    put = []
    call = []
    for option in list_options:
        if strike_range[0] <= option.strike < strike_range[1] and option.date_till_expiration == maturity and option.cp == 'P':
            put.append (option)
        if strike_range[1] < option.strike <= strike_range[2] and option.date_till_expiration == maturity and option.cp == 'C':
            call.append (option)

    result = []
    for item in list_options:
        if item.strike == strike_range[1] and item.date_till_expiration == maturity:
            result.append (item)

    result = put + call + result
    return result


# this class represents a trading day, which has a unique time stamp starting from 1, being the earliest day we include in
# our analysis; a list of options posted on that day; and a date in datetime format for referencing purposes

class Date:
    def __init__ (self, date: int, list_of_options: list, index_spot_price: float,
                  index_forward_price: float, nearestStrikeBelowSpot,
                  interest_rate: float, realized_variance, synthetic_vix):
        # date represented as the number of dates since 01/01/1996
        self.date = date
        # the list of options that are posted on the option chains for this date
        self.list_of_options = list_of_options
        # the lowest option strike below the index spot price eod
        self.nearest_strike_below_index = nearestStrikeBelowSpot
        # interest rate on this date
        self.interest_rate = interest_rate
        # forward price of index
        self.index_forward_price = index_forward_price
        # spot price of index
        self.index_spot_price = index_spot_price
        # list of selected strikes for our analysis
        self.selectedStrikes = []

        self.realized_variance = realized_variance

        self.synthetic_vix = synthetic_vix

    # this method returns whether or not there is an option contract maturing 30 days from this day.
    def has_options_maturing_in_30_days (self):
        for option in self.list_of_options:
            if option.date_till_expiration == 30:
                return True
            else:
                continue
        return False

    # This method returns a list of strike that are selected based on the number of strikes included in the analysis,
    # and the SPX spot price for that date
    def selectStrike (self):
        upper_bound = self.nearest_strike_below_index + (num_strike_selected * strike_Delta)

        lower_bound = self.nearest_strike_below_index - (num_strike_selected * strike_Delta)
        return lower_bound, self.nearest_strike_below_index, upper_bound
