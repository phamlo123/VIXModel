import mysql.connector
import pandas as pd
#establish Connection to workbench database
connection = mysql.connector.connect (user='root', password='0909963566',
                               host='127.0.0.1', port='3306',
                               database='vix_schema')

cursor = connection.cursor ()




def createPredictedVixTable ():
    query = 'CREATE TABLE prediction_variance (date INT NOT NULL PRIMARY KEY, realized_variance FLOAT, predicted_vix FLOAT )'
    res = cursor.execute (query)
    df = pd.DataFrame(res.fetchall())
    df.columns = res.keys()

query = 'SELECT ID, date FROM Main'
cursor.execute(query)

df=pd.DataFrame(cursor.fetchall(),columns=['ID','date'])
for ind, row in df.iterrows():
    print(row.values)



