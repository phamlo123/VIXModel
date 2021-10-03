import mysql.connector
import pandas as pd

# establish Connection to workbench database
connection = mysql.connector.connect (user='root', password='0909963566',
                                      host='127.0.0.1', port='3306',
                                      database='vix_schema')

cursor = connection.cursor ()


def createPredictedVixTable ():
    query = 'CREATE TABLE prediction_variance (date INT NOT NULL PRIMARY KEY, realized_variance FLOAT, predicted_vix FLOAT )'
    res = cursor.execute (query)
    df = pd.DataFrame (res.fetchall ())
    df.columns = res.keys ()


def getListOfDates () -> pd.DataFrame:
    query = 'SELECT date_from_1996, spot, rate, nearestStrikeBelowSpot, realized_variance, vix FROM my_date LIMIT 100'
    cursor.execute (query)
    df = pd.DataFrame (cursor.fetchall (),
                       columns=['date_from_1996', 'spot', 'rate', 'nearestStrikeBelowSpot', 'realized_variance',
                                'vix'])
    return df


def update_my_date_table_vix (date: int, synthetic_vix: float):
    statement = 'UPDATE my_date SET synthetic_vix = {vix} WHERE date_from_1996 = {date}'.format (date=date,
                                                                                                 vix=synthetic_vix)
    cursor.execute (statement)
    connection.commit ()


def updateMainTable (optionID: int, price_features: float):
    statement = 'UPDATE mine SET priceFeatures = {fname} WHERE id = {id}'.format (fname=price_features, id=optionID)
    cursor.execute (statement)
    connection.commit ()


def getListOfOptionForDate (date: int):
    query = 'SELECT id, real_strike, cp_flag, bid, ask, days FROM mine WHERE date_from_1996 = {mydate}'.format (
        mydate=date)
    cursor.execute (query)
    df = pd.DataFrame (cursor.fetchall (), columns=['id', 'real_strike', 'cp_flag', 'bid', 'ask', 'days'])
    return df


def updateDateTableRealizedVariance (date, variance):
    statement = 'UPDATE my_date SET futureRealizedVariance = {sth} WHERE date_from_1996 = {d}'.format (sth=variance,
                                                                                                       d=date)
    cursor.execute (statement)
    connection.commit ()


# Pull the spot prices of the underlying SPX for all dates
def getListOfSpotPrices ():
    statement = 'SELECT * FROM my_date'
    cursor.execute (statement)
    df = pd.DataFrame (cursor.fetchall (), columns=['date', 'forward', 'spot', 'rate', 'nearestStrikeBelowSpot'])
    return df


def update_nearest_strike_below_index_for_date_table (date, strike):
    statement = 'UPDATE my_date SET nearestStrikeBelowSpot = {s} WHERE date_from_1996 = {d}'.format (s=strike,
                                                                                                     d=date)
    cursor.execute (statement)
    connection.commit ()


def update_price_features (date, price):
    statement = 'UPDATE dateAndPriceFeatures SET date_from_1996 = {d}, priceFeatures = {f}'.format (d=date, f=price)
    cursor.execute (statement)
    connection.commit ()
