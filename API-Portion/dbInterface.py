
#Functions for interacting with Database
#Nick Jackson

#GRABBING AND MANIPULATING CSV
#manipulat
#pip install shlex
import shlex

#pip install pandas
import pandas as pd
#pip install configparser
import configparser

#DATABASE HANDLING
#pip install pyodbc
import pyodbc 
#For Archiving
import time

#location: can be ignored if running remote, only used for local testing
def archiveTweets(location = 'remote'):
    if (location == 'local'):
        server = "localhost\SENIORPROJTEST"
    else:
        server = "50.91.112.92"
    database = "testDB"
    username = "serverConTest"
    password = "serverTest"
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    cursor.execute("""INSERT INTO arc_tweetTest SELECT * from tweetTest""")
    cursor.execute("""DELETE FROM tweetTest""")
    cnxn.commit()
    print('Tweets Archived')

#filename: Name of input csv file
#location: can be ignored if running remote, only used for local testing
def pushTweets(filename, location = 'remote'):
    if (location == 'local'):
        server = "localhost\SENIORPROJTEST"
    else:
        server = "50.91.112.92"
    database = "testDB"
    username = "serverConTest"
    password = "serverTest"
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    file_input = filename
    count = 0

    df = pd.read_csv(file_input)

    for index, col in df.iterrows():
        print(col['Time'], col['User'], col['Tweet'])
        cursor.execute("""INSERT INTO tweetTest (dateTweet, userName, tweetContent) VALUES (?,?,?)""",col['Time'], col['User'], col['Tweet'])
        count+=1
    cnxn.commit()
    print('Rows Inserted: ', str(count))
    currentTime = time.strftime("%Y,%m,%d",time.localtime())
    df.to_csv(str(currentTime) + filename)

#location: can be ignored if running remote, only used for local testing
def pullTweets(location = 'remote'):
    if (location == 'local'):
        server = "localhost\SENIORPROJTEST"
    else:
        server = "50.91.112.92"
    database = "testDB"
    username = "serverConTest"
    password = "serverTest"
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    outputString = ""
    cursor.execute("SELECT * FROM tweetTest")

    row = cursor.fetchone()
    while row:
        print(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]))
        outputString += str(row[0]) + ',' + str(row[1]) + ',' + str(row[3]) + '\n'
        row = cursor.fetchone()
    
    return outputString

#filename: input csv file
#stockSymbol: Stock identifier added to DB entries
#location: can be ignored if running remote, only used for local testing
def pushStockInfo(filename, stockSymbol, location = 'remote'):
    if (location == 'local'):
        server = "localhost\SENIORPROJTEST"
    else:
        server = "50.91.112.92"
    database = "testDB"
    username = "serverConTest"
    password = "serverTest"
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    file_input = filename
    count = 0

    df = pd.read_csv(file_input)

    for index, col in df.iterrows():
        print(col['Date'], col['Open'], col['High'], col['Low'], col['Close'], col['Adj Close'], col['Volume'])
        cursor.execute("""INSERT INTO stockInfo (stockID, infoDate, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume) VALUES (?,?,?,?,?,?,?,?b)""",
        stockSymbol, col['Date'], col['Open'], col['High'], col['Low'], col['Close'], col['Adj Close'], col['Volume'])
        count+=1
    cnxn.commit()
    print('Rows Inserted: ', str(count))
    #currentTime = time.strftime("%Y,%m,%d",time.localtime())
    #df.to_csv(str(currentTime) + filename)
    

    

#TESTING

#Use the argument local for testing with the same machine.
#Remove the local argument when connecting from a remote machine.

#pushTweets('StaticHomeTimeline.csv', 'local')
#print(pullTweets('local'))
#archiveTweets('local')
#pushStockInfo('stock_prices.csv', 'AAPL', 'local')
