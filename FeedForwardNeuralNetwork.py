import sklearn
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.neural_network import MLPRegressor

import SQLconnection
import database
import numpy as np

data = database.getDataAndPriceFeaturesAndRealizedVarianceData ()


def formatting ():
    listOfDates = data['date_from_1996'].tolist ()
    distinctListOfDates = []
    for d in listOfDates:
        if d not in distinctListOfDates:
            distinctListOfDates.append (d)

    mapOfdatesAndOthers = {}
    for date in distinctListOfDates:
        mapOfdatesAndOthers[date] = (SQLconnection.something (date=date)['priceFeatures'].tolist (),
                                     SQLconnection.somethingelse (date=date)['futureRealizedVariance'].tolist ())

    return mapOfdatesAndOthers


def preprocess():
    sklearn.preprocessing.StandardScaler()

def additionalFormat ():
    my_map = formatting ()
    keys = my_map.keys ()
    X = []
    y = []
    for item in keys:
        print(item)
        print(len(my_map[item][0]))
        X.append (my_map[item][0])
        y.append (my_map[item][1])
    y = np.array (y)
    X = np.array (X)
    return X, y

def splittingDataAndTrain ():
    X, y = additionalFormat ()
    time_series_split = TimeSeriesSplit (n_splits=300)
    for train_index, test_index in time_series_split.split (X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        regression = MLPRegressor (hidden_layer_sizes=80).fit (X_train, y_train)
        regression.predict (X_test)
        print(regression.score (X_test, y_test))

splittingDataAndTrain()