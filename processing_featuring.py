import pandas as pd
import numpy as np
from typing import List

import VIXComp

strikeDelta = 5
forecast_horizon = 30


class ProcessingAndFeaturing:

    def __init__ (self, num_strikes_selected, time_stamp: list, list_of_options: list):
        self.forecast_horizon = forecast_horizon
        self.num_strikes_selected = num_strikes_selected
        self.time_stamp = time_stamp
        self.list_of_options = list_of_options
        self.list_of_options_price = {}

    def strike_selection (self, atm_strike: list) -> list:
        selected_strikes = []
        for i in range (len (self.time_stamp)):
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
