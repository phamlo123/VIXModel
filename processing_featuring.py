import pandas as pd
import numpy as np
from typing import List
import Date
import util

strikeDelta = 5
forecast_horizon = 30


# Equation 5
def calculate_price_features_helper (t_near: Date, list_options_near, t_far: Date, list_options_far) -> list:
    list_price_near = []
    list_price_far = []
    for option1 in list_options_near:
        list_price_near.append (option1.quote)
    for option2 in list_options_far:
        list_price_far.append (option2.quote)

    list_interpolated_feature_price = []
    for i in range (len (list_price_near)):
        term_1 = (t_far.Date.date - 30) / (t_far.Date.date - t_near.Date.date) * list_price_near[i]
        term_2 = (30 - t_near.Date.date) / (t_far.Date.date - t_near.Date.date) * list_price_far[i]

        price = term_1 + term_2
        list_interpolated_feature_price.append (price)
    return list_interpolated_feature_price


# Equation 7
def make_stationary (date: Date, list_of_price_features):
    K = date.nearest_strike_below_index
    list_of_price_features_bar = []
    for item in list_of_price_features:
        price_feature_bar = item / (K ** 2)
        list_of_price_features_bar.append (price_feature_bar)
    return list_of_price_features_bar


# Before feeding into the model, all features are normalized by subtracting from the sample mean and divide them by
# the standard deviation
def machine_learning_normalization ():
    return 0


class ProcessingAndFeaturing:

    def __init__ (self, num_strikes_selected, list_of_dates: List[Date], list_of_options: list,
                  list_of_strike_range: List[dict]):
        self.price_features = None
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
                list_price_features_t = []
                for option_t in Date.get_options_in_strike_range (selected_strike[i],
                                                                  each_day.Date.get_options_maturing_in_30 ()):
                    # assuming all options have quotes for now, will come back to add strike interpolation for options that
                    # dont have a price
                    option_day_list.append (option_t)
                    list_price_features_t.append (option_t.quote)
                vix_t = util.vix_calculation_30days (option_day_list, each_day)
                self.list_of_synthetic_vix.append (vix_t)
                list_price_features_t_bar = make_stationary (each_day, list_price_features_t)
                self.price_features.dict.update (each_day, list_price_features_t_bar)

            else:
                lower_date = self.findLowerTermFromGivenDate (each_day)
                higher_date = self.findHigherTermFromGivenDate (each_day)
                lower_date_time_stamp = lower_date.Date.time_stamp
                higher_date_time_stamp = higher_date.Date.time_stamp
                # assuming all options have quotes for now, will come back to add strike interpolation for options that
                # dont have a price
                list_options_near = Date.get_options_in_strike_range (selected_strike[lower_date_time_stamp],
                                                                      lower_date.Date.get_options_maturing_in_30 ())
                list_options_far = Date.get_options_in_strike_range (selected_strike[higher_date_time_stamp],
                                                                     higher_date.Date.get_options_maturing_in_30 ())

                vix_interpolated = util.vix_calculation_not_30days (list_options_near, lower_date, list_options_far,
                                                                    higher_date)

                self.list_of_synthetic_vix.append (vix_interpolated)
                list_price_features_t = calculate_price_features_helper (lower_date, list_options_near,
                                                                         higher_date,
                                                                         list_options_far)
                list_price_features_t_bar = make_stationary (each_day, list_price_features_t)

                self.price_features.dict.update (each_day, list_price_features_t_bar)



    def findLowerTermFromGivenDate (self, date: Date) -> Date:
        index = self.list_of_dates.index (date) - 1
        try:
            while True:
                if self.list_of_dates[index].Date.has_options_maturing_in_30_days ():
                    return self.list_of_dates[index]
                index = index - 1
        except IndexError:
            return None

    def findHigherTermFromGivenDate (self, date: Date) -> Date:
        index = self.list_of_dates.index (date) - 1
        try:
            while True:
                if self.list_of_dates[index].Date.has_options_maturing_in_30_days ():
                    return self.list_of_dates[index]
                index = index + 1
        except IndexError:
            return None


