
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

    

#TESTING

#Use the argument local for testing with the same machine.
#Remove the local argument when connecting from a remote machine.

#pushTweets('StaticHomeTimeline.csv', 'local')
#print(pullTweets('local'))
#archiveTweets('local')
