--Used to reset database for example.
DROP TABLE tracking
DROP TABLE sentimentHistory
DROP TABLE userList
DROP TABLE stockInfo
DROP TABLE companyList
DROP TABLE tweetTest
DROP TABLE arc_tweetTest

--Keep track of users & their data, will see expansion as website is developed.
CREATE TABLE userList (
    userID int IDENTITY(1,1) NOT NULL,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    userName VARCHAR(255) NOT NULL PRIMARY KEY,
    passWrd VARCHAR(255) NOT NULL
)
--Keep track of basic company information
CREATE TABLE companyList (
    companyID VARCHAR(10) NOT NULL PRIMARY KEY,
    companyName VARCHAR(255) NOT NULL,
    founded DATE NULL,
    worth DECIMAL(9,2) NULL,
    sentiment VARCHAR(255) NULL

)
--List of key words used for sorting
CREATE TABLE companyKeys (
    companyID VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES companyList,
    keyWord VARCHAR(128) NOT NULL
)
--List of daily stock transaction information
CREATE TABLE stockInfo (
    dailyID int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    inputDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    infoDate DATE NOT NULL,
    stockID VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES companyList,
    openPrice DECIMAL(9,2) NULL,
    highPrice DECIMAL(9,2) NULL,
    lowPrice DECIMAL(9,2) NULL,
    closePrice DECIMAL(9,2) NULL,
    adjClosePrice DECIMAL(9,2) NULL,
    volume INT NULL
)
--Relational table connecting users and their tracked stock.
CREATE TABLE tracking (
    userName VARCHAR(255) NOT NULL FOREIGN KEY REFERENCES userList,
    stockID VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES companyList
)
--Table to contain recorded sentiments, used to aggregate score and double check our analyzer.
CREATE TABLE sentimentHistory (
    transID int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    transDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    tweetContent VARCHAR(1200) NOT NULL,
    sentScore VARCHAR(255) NOT NULL
)
CREATE TABLE tweetTest (
    tweetID int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    dateTweet DATE NOT NULL,
    userName VARCHAR(32) NOT NULL,
    tweetContent VARCHAR(1200) NOT NULL
)
CREATE TABLE arc_tweetTest (
    tweetID int NOT NULL PRIMARY KEY,
    dateTweet DATE NOT NULL,
    userName VARCHAR(32) NOT NULL,
    tweetContent VARCHAR(1200) NOT NULL
)
GO

--Triggers--
CREATE TRIGGER cleanDuplicates
ON tweetTest
AFTER INSERT AS
DELETE T
FROM
(
Select *, dupRank = ROW_NUMBER() OVER (PARTITION BY tweetContent ORDER BY (SELECT NULL)) FROM tweetTest) AS T
WHERE dupRank > 1

GO

CREATE TRIGGER cleanDuplicatesSentiment
ON sentimentHistory
AFTER INSERT AS
DELETE T
FROM
(
Select *, dupRank = ROW_NUMBER() OVER (PARTITION BY tweetContent ORDER BY (SELECT NULL)) FROM sentimentHistory) AS T
WHERE dupRank > 1

GO
--Example inserts.

INSERT INTO userList (firstName, lastName, userName, passWrd) VALUES 
('Jim', 'Everyman', 'JimmyTheMan', 'SomeHash'),
('Joe', 'Mama', 'HaGotEm', 'SomeHash'),
('Johny', 'Test', 'GottaTest', 'SomeHash')

INSERT INTO companyList (companyID, companyName, founded, worth, sentiment) VALUES
('AAPL', 'Apple', '1976-4-1', 3650, 'Neutral'),
('MSFT', 'Microsoft', '1975-4-1', 1610, 'Positive')

INSERT INTO stockInfo (stockID, infoDate, openPrice, closePrice, highPrice, lowPrice, volume) VALUES
('AAPL', '2020-10-20', 174.91, 175.08, 176.75, 173.92, 108.73),
('MSFT', '2020-10-20', 334.41, 334.97, 336.49, 332.12, 21.95)

INSERT INTO tracking (userID, stockID) VALUES
(1, 'AAPL'),
(1, 'MSFT'),
(2, 'AAPL'),
(3, 'MSFT')


INSERT INTO tweetTest(dateTweet, userName, tweetContent) VALUES
('2022-03-09 16:51:08+00:00', 'Tesla', '???? at Giga Berlin https://t.co/ojIvG9cg4F')

INSERT INTO arc_tweetTest SELECT * FROM tweetTest


SELECT * from userList
SELECT * from tracking
SELECT * from companyList
SELECT * from StockInfo
select * from sentimentHistory
SELECT * from tweetTest
SELECT * from arc_tweetTest
SELECT * from sys.tables
GO