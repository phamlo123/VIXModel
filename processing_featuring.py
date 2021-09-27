import myDate
import util

strikeDelta = 5


class ProcessingAndFeaturing:

    def __init__ (self, num_strikes_selected, list_of_dates):
        self.price_features = dict
        self.num_strikes_selected = num_strikes_selected
        self.list_of_dates = list_of_dates
        self.map_of_synthetic_vix = dict

    def feature_engineering (self):
        for each_day in self.list_of_dates:
            option_day_list = []
            if each_day.has_options_maturing_in_30_days ():
                list_price_features_t = []
                for option_t in myDate.get_options_in_strike_range (each_day.Date.selectStrike (),
                                                                    each_day.Date.get_options_maturing_in_30 ()):
                    # assuming all options have quotes for now, will come back to add strike interpolation for options that
                    # dont have a price
                    option_day_list.append (option_t)
                    list_price_features_t.append (option_t.quote)
                vix_t = util.vix_calculation_30days (option_day_list, each_day)
                self.map_of_synthetic_vix.update (each_day, vix_t)
                list_price_features_t_bar = make_stationary (each_day, list_price_features_t)
                self.price_features.update (each_day, list_price_features_t_bar)

            else:
                lower_date = self.findLowerTermFromGivenDate (each_day)
                higher_date = self.findHigherTermFromGivenDate (each_day)
                if(not isinstance(lower_date, myDate.Date) or not isinstance(higher_date, myDate.Date)):
                    continue
                # assuming all options have quotes for now, will come back to add strike interpolation for options that
                # dont have a price
                list_options_near = myDate.get_options_in_strike_range (lower_date.selectStrike (),
                                                                        lower_date.get_options_maturing_in_30 ())
                list_options_far = myDate.get_options_in_strike_range (higher_date.selectStrike (),
                                                                       higher_date.get_options_maturing_in_30 ())

                vix_interpolated = util.vix_calculation_not_30days (list_options_near, lower_date, list_options_far,
                                                                    higher_date)

                self.map_of_synthetic_vix.update (each_day, vix_interpolated)
                list_price_features_t = calculate_price_features_helper (lower_date, list_options_near,
                                                                         higher_date,
                                                                         list_options_far)

                list_price_features_t_bar = make_stationary (each_day, list_price_features_t)

                self.price_features.update (each_day, list_price_features_t_bar)

    # This method help find the nearest lower date that has options maturing in exactly 30 days
    def findLowerTermFromGivenDate (self, date: myDate) -> myDate:
        index = self.list_of_dates.index (date) - 1
        try:
            while True:
                if self.list_of_dates[index].has_options_maturing_in_30_days ():
                    return self.list_of_dates[index]
                index = index - 1
        except IndexError:
            print("no lower date has desired maturity for date {t}".format(t=date.date))

    def findHigherTermFromGivenDate (self, date: myDate) -> myDate:
        index = self.list_of_dates.index (date) - 1
        try:
            while True:
                if self.list_of_dates[index].has_options_maturing_in_30_days ():
                    return self.list_of_dates[index]
                index = index + 1
        except IndexError:
            print("no higher date has desired maturity for date {t}".format(t=date.date))


# Equation 5
def calculate_price_features_helper (t_near: myDate, list_options_near, t_far: myDate, list_options_far) -> list:
    list_price_near = []
    list_price_far = []
    for option1 in list_options_near:
        list_price_near.append (option1.quote)
    for option2 in list_options_far:
        list_price_far.append (option2.quote)

    list_interpolated_feature_price = []
    for i in range (len (list_price_near)):
        term_1 = (t_far.date - 30) / (t_far.date - t_near.date) * list_price_near[i]
        term_2 = (30 - t_near.date) / (t_far.date - t_near.date) * list_price_far[i]

        price = term_1 + term_2
        list_interpolated_feature_price.append (price)
    return list_interpolated_feature_price


# Equation 7
def make_stationary (date: myDate, list_of_price_features):
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

