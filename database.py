import pandas
import SQLconnection as con
from myOption import Option
from myDate import Date

list_of_date_id = con.getListOfDates ()["date"].tolist ()
list_of_forwards = con.getListOfDates ()["forward"].tolist ()
list_of_spot = con.getListOfDates ()["spot"].tolist ()
list_of_rate = con.getListOfDates ()["rate"].tolist ()
list_of_nearestStrike = con.getListOfDates ()["nearestStrikeBelowSpot"].tolist ()


def constructOptions (date: int):
    df = con.getListOfOptionForDate (date)
    list_of_option_id = df['ID'].tolist ()
    list_of_expiry = df['expiry'].tolist ()
    list_of_strikes = df['k'].tolist ()
    list_of_days = df['days'].tolist ()
    list_of_cp = df['cp'].tolist ()
    list_of_bid = df['bid'].tolist ()
    list_of_ask = df['ask'].tolist ()
    list_of_options = list ()
    for i in range (len (list_of_option_id)):
        option = Option (list_of_option_id[i], date, list_of_strikes[i], list_of_cp[i], list_of_expiry[i],
                         list_of_bid[i],
                         list_of_ask[i])
        list_of_options.append (option)
    return list_of_options


def getListOfDates () -> list:
    list_of_dates = list ()
    for i in range (len (list_of_date_id)):
        list_of_options = constructOptions (list_of_date_id[i])
        this_date = Date (list_of_date_id[i], list_of_options, list_of_spot[i], list_of_forwards[i], list_of_rate[i],
                          list_of_nearestStrike[i])
        list_of_dates.append (this_date)
    return list_of_dates




list_of_dates = getListOfDates ()
