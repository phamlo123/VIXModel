import SQLconnection
import SQLconnection as con
import util
from myOption import Option
from myDate import Date
from processing_featuring import ProcessingAndFeaturing


# construct our internal representation of an option using data fetched from the database
def constructOptions (date: int):
    my_df = con.getListOfOptionForDate (date)
    list_of_option_id = my_df['id'].tolist ()
    list_of_expiry = my_df['days'].tolist ()
    list_of_strikes = my_df['real_strike'].tolist ()
    list_of_cp = my_df['cp_flag'].tolist ()
    list_of_bid = my_df['bid'].tolist ()
    list_of_ask = my_df['ask'].tolist ()

    list_of_options = list ()
    for i in range (len (list_of_option_id)):
        option = Option (id=list_of_option_id[i], date=date, cp=list_of_cp[i], bid=list_of_bid[i], ask=list_of_ask[i],
                         strike=list_of_strikes[i],
                         date_till_expiration=list_of_expiry[i])
        list_of_options.append (option)
    return list_of_options


# construct the list of dates with the internal representation of a Day with data fetched from the database
def getListOfDates () -> list:
    list_of_date_from_con = con.getListOfDates ()
    list_of_date_id = list_of_date_from_con["date_from_1996"].tolist ()
    list_of_spot = list_of_date_from_con["spot"].tolist ()
    list_of_rate = list_of_date_from_con["rate"].tolist ()
    list_of_nearest_strike = list_of_date_from_con['nearestStrikeBelowSpot'].tolist ()
    list_of_variance = list_of_date_from_con["realized_variance"].tolist ()
    list_of_vix = list_of_date_from_con["vix"].tolist ()
    list_of_dates = []
    for i in range (len (list_of_date_id)):
        list_of_options = constructOptions (list_of_date_id[i])
        this_date = Date (date=list_of_date_id[i], list_of_options=list_of_options, index_spot_price=list_of_spot[i],
                          interest_rate=list_of_rate[i],
                          index_forward_price=0, realized_variance=list_of_variance[i], synthetic_vix=list_of_vix[i],
                          nearestStrikeBelowSpot=list_of_nearest_strike[i])
        list_of_dates.append (this_date)
    return list_of_dates


# self-explanatory
def get_map_of_date_and_nearest_strike (listOfDates):
    my_map = {}
    for each in listOfDates:
        my_map[each] = each.nearest_strike_below_index
    return my_map


# This is just to download all dates and use my own script to find the nearest strike below spot price because apparently
# the data did not give that
def fillingDateTableCauseThedataSucks ():
    list_of_dates = getListOfDates ()
    mymap = get_map_of_date_and_nearest_strike (listOfDates=list_of_dates)
    for item in mymap.keys ():
        SQLconnection.update_nearest_strike_below_index_for_date_table (date=item.date, strike=mymap.get (item))


def addRealizedVarianceToDatabase (connection, my_map):
    try:
        for item in my_map.keys ():
            connection.updateDateTableRealizedVariance (item.date, my_map.get (item))
    except TypeError:
        print ('Map of date and corresponding future realized variance is empty')


addRealizedVarianceToDatabase (connection=SQLconnection,
                               my_map=util.calculateListOfReturns (list_of_date=getListOfDates ()))




# this is the final step in processing and featuring: fetching all options given a list of dates and perform calculation
# on them (including calculating synthetic vix and price features used later for machine learning step)
def updateVixAndStuffPriceFeatures ():
    list_of_dates = getListOfDates ()
    proAndFea = ProcessingAndFeaturing (list_of_dates=list_of_dates)
    proAndFea.feature_engineering ()
    date_and_vix_map = proAndFea.map_of_synthetic_vix
    option_and_price_feature_map = proAndFea.price_features

    for item in date_and_vix_map.keys ():
        SQLconnection.update_my_date_table_vix (date=item.date, synthetic_vix=date_and_vix_map[item])
        for feature in option_and_price_feature_map[item]:
            SQLconnection.update_price_features (inte=item.date, price=feature)


