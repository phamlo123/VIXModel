from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import pandas as pd




X, x = make_regression (n_samples=200, random_state=1)
X_train, X_test, y_train, y_test = train_test_split (X, x, random_state=1)
regression = MLPRegressor (500).fit (X_train, y_train)
regression.predict (X_test[:2])
regression.score (X_test, y_test)
