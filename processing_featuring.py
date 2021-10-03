import myDate
import util
import numpy

strikeDelta = 5


# this class is responsible for doing the processing needed before feeding the data into our machine learning model
class ProcessingAndFeaturing:

    def __init__ (self, list_of_dates):
        self.price_features = {}
        self.list_of_dates = list_of_dates
        self.map_of_synthetic_vix = {}

    def feature_engineering (self):
        for each_day in self.list_of_dates:
            selected_strike = each_day.selectStrike ()
            option_day_list = []
            # this date has option maturing in exactly 30 dates from this date
            if each_day.has_options_maturing_in_30_days ():
                list_price_features_t = []
                for option_t in myDate.get_options_in_strike_range (selected_strike,
                                                                    each_day.list_of_options, 30):
                    # assuming all options have quotes for now, will come back to add strike interpolation for options that
                    # dont have a price
                    option_day_list.append (option_t)
                    list_price_features_t.append (option_t.quote)
                vix_t = util.vix_calculation_30days (date=each_day, list_of_option=option_day_list)
                self.map_of_synthetic_vix[each_day] = vix_t
                list_price_features_t_bar = make_stationary (date=each_day,
                                                             list_of_price_features=list_price_features_t)
                self.price_features[each_day] = list_price_features_t_bar

            # this date does not have option maturing in exactly 30 dates from this date
            else:
                lower_term = self.findLowerTermOnGivenDate (each_day)
                higher_term = self.findHigherTermOnGivenDate (each_day)

                # assuming all options have quotes for now, will come back to add strike interpolation for options that
                # dont have a price
                list_options_near = myDate.get_options_in_strike_range (selected_strike,
                                                                        each_day.list_of_options, lower_term)
                list_options_far = myDate.get_options_in_strike_range (selected_strike,
                                                                       each_day.list_of_options, higher_term)

                vix_interpolated_t = util.vix_calculation_not_30days (list_near_options=list_options_near,
                                                                      list_far_options=list_options_far,
                                                                      term1=lower_term,
                                                                      term2=higher_term, date=each_day)

                self.map_of_synthetic_vix[each_day] = vix_interpolated_t
                list_price_features_t = calculate_price_features_helper (t_lower=lower_term, t_higher=higher_term,
                                                                         list_options_near=list_options_near,
                                                                         list_options_far=list_options_far)

                list_price_features_t_bar = make_stationary (date=each_day,
                                                             list_of_price_features=list_price_features_t)

                self.price_features[each_day] = list_price_features_t_bar

    # This method help find the nearest lower maturity that some options have on this date
    def findLowerTermOnGivenDate (self, date: myDate) -> myDate:
        n = 29
        while True:
            if n == 0:
                print ("no options posted on this date has maturity less than 30 days (impossible)")
                return
            for option in date.list_of_options:
                if option.date_till_expiration == n:
                    return n
            else:
                n = n - 1

    # This method help find the higher date that has options maturing in exactly 30 days
    def findHigherTermOnGivenDate (self, date: myDate) -> myDate:
        n = 31
        while True:
            if n == 90:
                print ("no options posted on this date has maturity more than 30 days (impossible)")
                return
            if n == 0:
                print ("no lower options posted on this date has maturity less than 30 days (impossible)")
            for option in date.list_of_options:
                if option.date_till_expiration == n:
                    return n
                else:
                    n = n + 1


# Equation 5
def calculate_price_features_helper (t_lower, list_options_near, t_higher, list_options_far) -> list:
    list_near = []
    list_far = []
    for option1 in list_options_near:
        list_near.append (option1.quote)
    for option2 in list_options_far:
        list_far.append (option2.quote)

    list_interpolated_feature_price = []
    for i in range (len (list_near)):
        term_1 = (t_higher - 30) / (t_higher - t_lower) * list_near[i]
        term_2 = (30 - t_lower) / (t_higher - t_lower) * list_far[i]

        price = term_1 + term_2
        list_interpolated_feature_price.append (price)
    return list_interpolated_feature_price


# Equation  (to be applied before ML normalization). This is to add extra step in normalizing time-series data before
# a standard ML technique to normalize data
def make_stationary (date: myDate, list_of_price_features):
    K = date.nearest_strike_below_index
    list_of_price_features_bar = []
    for item in list_of_price_features:
        price_feature_bar = item / (K ** 2)
        list_of_price_features_bar.append (price_feature_bar)
    return date, list_of_price_features_bar


# Before feeding into the model, all features are normalized by subtracting from the sample mean and divide them by
# the standard deviation. This could be done by Sklearn so will not use it for now
def machine_learning_normalization (map_of_date_and_features) -> {}:
    listOfDates = map_of_date_and_features.keys ()
    listOfFeatures = map_of_date_and_features.values ()

    mean = numpy.mean (listOfFeatures)
    standard_deviation = numpy.std (listOfFeatures)

    normalized_map = {}
    for item in listOfDates:
        feature = map_of_date_and_features[item]
        normalized_map[item] = (feature - mean) / standard_deviation

    return normalized_map
