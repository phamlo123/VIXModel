import myOption
import math
# get price of an option for using in VIX calculation using interpolation when maturity of desired option does not
# coincides with forecast horizon (30days)
import myDate

forecastHorizon = 30


def get_price_using_interpolation (option1, option2):
    option1_price = option1.quote
    option2_price = option2.quote
    option1_time_to_mat = option1.get_time_to_maturity ()
    option2_time_to_mat = option2.get_time_to_maturity ()
    first_term = option1_price * (option2_time_to_mat - forecastHorizon) / (option2_time_to_mat - option1_time_to_mat)
    second_term = option2_price * (forecastHorizon - option1_time_to_mat) / (option2_time_to_mat - option1_time_to_mat)

    constructed_price = first_term + second_term

    return constructed_price


# This function calculates the value of VIX from the selected options price
def vix_calculation_30days (list_of_option, date: myDate):
    variance = variance_calculation (list_of_option, date)
    vix = (variance ** (1 / 2)) * 100
    print (vix)
    return vix


# From the CBOE booklet
def variance_calculation (list_of_option, date, term=30):
    first_term = 0
    k_delta = 5
    e_term = date.interest_rate / 100 * 30
    e_term = math.exp (e_term)

    for item in list_of_option:
        price = item.quote
        strike = item.strike
        portion = e_term * (2 * k_delta) / (strike ** 2) * price / term
        first_term = first_term + portion
    return first_term


# Equation 2 and 3
def vix_calculation_not_30days (list_near_options, term1, list_far_options, term2, date):
    variance1 = variance_calculation (list_of_option=list_near_options, date=date, term=term1)
    variance2 = variance_calculation (list_of_option=list_far_options, date=date, term=term2)

    time_ratio1 = (term2 - forecastHorizon) / (term2 - term1)
    time_ratio2 = (forecastHorizon - term1) / (term2 - term1)

    first = term1 * variance1 * time_ratio1
    second = term2 * variance2 * time_ratio2

    vix = 100 * math.sqrt (first + second)
    return vix


def realizedVarianceCalculationByInterval (mapOfDateAndReturn):
    dates = list (mapOfDateAndReturn.keys ())
    mapOfDatesAndRealizedVariance = {}
    for dateIndex in range (len (dates) - 30):
        list_of_daily_returns_next30 = []
        for i in range (1, 30):
            d = dates[dateIndex + i]
            list_of_daily_returns_next30.append (mapOfDateAndReturn[d])
        realizedVariance = realizedVarianceCal (list_of_daily_returns_next30)

        mapOfDatesAndRealizedVariance[dates[dateIndex]] = realizedVariance
    return mapOfDatesAndRealizedVariance


def realizedVarianceCal (list_of_daily_returns):
    variance = 0
    for retu in list_of_daily_returns:
        variance = variance + retu ** 2
    return variance


def calculateListOfReturns (list_of_date):
    mapOfDateAndReturn = {}
    for i in range (1, len (list_of_date)):
        returnRate = calculateReturn (price1=list_of_date[i - 1].index_spot_price,
                                      price2=list_of_date[i].index_spot_price)
        mapOfDateAndReturn[list_of_date[i]] = returnRate
    return mapOfDateAndReturn


def calculateReturn (price1, price2):
    returnRate = math.log (price2) - math.log (price1)
    return returnRate


def addPriceFeaturesToDatabase (connection, my_map):
    try:
        for item in my_map.keys ():
            connection.updateVarianceTable (item.date, my_map.get (item))
    except TypeError:
        print ('Map of dates and corresponding lists of price features is empty')


def addCalculatedVixToDatabase (connection, my_map):
    try:
        for item in my_map.keys ():
            connection.updateMainTable (item.id, my_map.get (item))
    except TypeError:
        print ('Map of date and corresponding synthetic vix is empty')
