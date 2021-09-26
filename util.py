import myOption
import math
# get price of an option for using in VIX calculation using interpolation when maturity of desired option does not
# coincides with forecast horizon (30days)
import myDate

forecastHorizon = 30


def get_price_using_interpolation (option1: myOption, option2: myOption):
    option1_price = option1.Option.quote
    option2_price = option2.Option.quote
    option1_time_to_mat = option1.Option.get_time_to_maturity ()
    option2_time_to_mat = option2.Option.get_time_to_maturity ()
    first_term = option1_price * (option2_time_to_mat - forecastHorizon) / (option2_time_to_mat - option1_time_to_mat)
    second_term = option2_price * (forecastHorizon - option1_time_to_mat) / (option2_time_to_mat - option1_time_to_mat)

    constructed_price = first_term + second_term

    return constructed_price


# This function calculates the value of VIX from the selected options price
def vix_calculation_30days (list_of_option, date: myDate):
    variance = variance_calculation (list_of_option, date)
    vix = (variance ** (1 / 2)) * 100

    return vix


# From the CBOE booklet
def variance_calculation (list_of_option, date: myDate):
    first_term = 0
    k_delta = 5
    e_term = date.interest_rate * 30
    e_term = e_term.exp ()

    for item in list_of_option:
        price = item.Option.quote
        strike = item.Option.strike
        portion = e_term * (2 * k_delta) / (strike ** 2) * price / 30
        first_term += portion

    last_term = ((date.index_forward_price / date.nearest_strike_below_index - 1) ** 2) / 30

    variance = first_term - last_term
    return variance


# Equation 2 and 3
def vix_calculation_not_30days (list_near_options, date1: myDate, list_far_options, date2: myDate):
    variance1 = variance_calculation (list_near_options, date1)
    variance2 = variance_calculation (list_far_options, date2)

    t1 = list_near_options[0].Option.get_time_to_maturity ()
    t2 = list_far_options[0].Option.get_time_to_maturity ()
    time_ratio1 = (t2 - 30) / (t2 - t1)
    time_ratio2 = (30 - t1) / (t2 - t1)
    first_term = t1 * variance1 * time_ratio1
    second_term = t2 * variance2 * time_ratio2

    vix = 100 * math.sqrt (first_term + second_term)
    return vix


def addToDatabase(connection, my_map):
    for item in my_map.keys():
        connection.updateVarianceTable(item.date, my_map.get(item))

def addToDatabase2(connection, my_map):
    for item in my_map.keys():
        connection.updateMainTable(item.Option.id, my_map.get(item))

