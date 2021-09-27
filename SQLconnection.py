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
    query = 'SELECT * FROM Date'
    cursor.execute (query)
    df = pd.DataFrame (cursor.fetchall (), columns=['date', 'forward', 'spot', 'rate', 'nearestStrikeBelowSpot'])
    return df


def updateVarianceTable (date: int, synthetic_vix: float):
    statement = 'INSERT INTO prediction_variance (date, predicted_vix)  VALUES ({date} {vix})'.format (date=date,
                                                                                                       vix=synthetic_vix)
    cursor.execute (statement)
    connection.commit ()


def updateMainTable (optionID: int, price_features: float):
    statement = 'UPDATE Main SET priceFeatures = {fname} WHERE ID = {id}'.format (fname=price_features, id=optionID)
    cursor.execute (statement)
    connection.commit ()


def getListOfOptionForDate (date: int):
    query = 'SELECT ID, date, expiry, days, k, cp, bid, ask FROM Main WHERE date = {mydate}'.format (mydate=date)
    cursor.execute (query)
    df = pd.DataFrame (cursor.fetchall (), columns=['ID', 'date', 'expiry', 'days', 'k', 'cp', 'bid', 'ask'])
    return df


def updateDateTableRealizedVariance (date, variance):
    statement = 'UPDATE Date SET futureRealizedVariance = {sth} WHERE date = {d}'.format (sth=variance, d=date)
    cursor.execute (statement)
    connection.commit ()


# Pull the spot prices of the underlying SPX for all dates
def getListOfSpotPrices ():
    statement = 'SELECT * FROM Date'
    cursor.execute(statement)
    df = pd.DataFrame(cursor.fetchall(), columns=['date', 'forward', 'spot', 'rate', 'nearestStrikeBelowSpot'])
    return df

