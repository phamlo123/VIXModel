import pandas as pd
import numpy as np
from typing import List
import Date
import util

strikeDelta = 5
forecast_horizon = 30


class ProcessingAndFeaturing:

    def __init__ (self, num_strikes_selected, list_of_dates: List[Date], list_of_options: list,
                  list_of_strike_range: List[dict]):
        self.forecast_horizon = forecast_horizon
        self.num_strikes_selected = num_strikes_selected
        self.list_of_dates = list_of_dates
        self.list_of_strike_range = list_of_strike_range
        self.list_of_options = list_of_options
        self.list_of_options_price = []
        self.list_of_synthetic_vix = []

    def strike_selection (self, atm_strike: list) -> list:
        selected_strikes = []
        for i in range (len (self.list_of_dates)):
            selected_strike_call = []
            selected_strike_put = []
            for i in range (self.num_strikes_selected):
                selected_strike_call.append (atm_strike[i] + strikeDelta)
                selected_strike_put.append (atm_strike[i] - strikeDelta)

            selected_strikes.append (selected_strike_put)
            selected_strikes.append (selected_strike_call)

        selected_strikes.append (atm_strike)
        return selected_strikes

    def feature_engineering (self, atm_strikes_list: List[int]):
        selected_strike = self.strike_selection (atm_strikes_list)
        for each_day in self.list_of_dates:
            option_day_list = []
            if each_day.Date.has_options_maturing_in_30_days ():
                i = each_day.Date.time_stamp
                for option in Date.get_options_in_strike_range (selected_strike[i],
                                                                each_day.Date.get_options_maturing_in_30 ()):
                    # assuming all options have quotes for now, will come back to add strike interpolation for options that
                    # dont have a price
                    option_day_list.append (option)
                vix_t = util.vix_calculation (option_day_list)
                self.list_of_synthetic_vix.append (vix_t)
            else:
                lower_date = self.findLowerTermFromGivenDate (each_day)
                higher_date = self.findHigherTermFromGivenDate (each_day)
                for t in {lower_date, higher_date}:
                    # assuming all options have quotes for now, will come back to add strike interpolation for options that
                    # dont have a price







    def findLowerTermFromGivenDate (self, date: Date):
        index = self.list_of_dates.index (date) - 1
        try:
            while True:
                if self.list_of_dates[index].Date.has_options_maturing_in_30_days ():
                    return self.list_of_dates[index]
                index = index - 1
        except IndexError:
            return None

    def findHigherTermFromGivenDate (self, date: Date):
        index = self.list_of_dates.index (date) - 1
        try:
            while True:
                if self.list_of_dates[index].Date.has_options_maturing_in_30_days ():
                    return self.list_of_dates[index]
                index = index + 1
        except IndexError:
            return None
