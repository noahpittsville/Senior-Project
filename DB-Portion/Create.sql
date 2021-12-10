--Used to reset database for example.
DROP TABLE tracking
DROP TABLE sentimentHistory
DROP TABLE userList
DROP TABLE stockInfo
DROP TABLE companyList

--Keep track of users & their data, will see expansion as website is developed.
CREATE TABLE userList (
    userID int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL
)
--Keep track of basic company information
CREATE TABLE companyList (
    companyID VARCHAR(10) NOT NULL PRIMARY KEY,
    companyName VARCHAR(255) NOT NULL,
    founded DATE NULL,
    worth DECIMAL(9,2) NULL,
    sentiment VARCHAR(255) NULL

)
--List of daily stock transaction information
CREATE TABLE stockInfo (
    dailyID int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    inputDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    stockID VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES companyList,
    openPrice DECIMAL(9,2) NULL,
    closePrice DECIMAL(9,2) NULL,
    highPrice DECIMAL(9,2) NULL,
    lowPrice DECIMAL(9,2) NULL,
    volume INT NULL
)
--Relational table connecting users and their tracked stock.
CREATE TABLE tracking (
    userID int NOT NULL FOREIGN KEY REFERENCES userList,
    stockID VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES companyList
)
--Table to contain recorded sentiments, used to aggregate score and double check our analyzer.
CREATE TABLE sentimentHistory (
    transID int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    transDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    companyID VARCHAR(10) NOT NULL FOREIGN KEY REFERENCES companyList,
    sentScore VARCHAR(255) NOT NULL
)

--Example inserts.

INSERT INTO userList (firstName, lastName) VALUES 
('Jim', 'Everyman'),
('Joe', 'Mama'),
('Johny', 'Test')

INSERT INTO companyList (companyID, companyName, founded, worth, sentiment) VALUES
('AAPL', 'Apple', '1976-4-1', 3650, 'Neutral'),
('MSFT', 'Microsoft', '1975-4-1', 1610, 'Positive')

INSERT INTO stockInfo (stockID, openPrice, closePrice, highPrice, lowPrice, volume) VALUES
('AAPL', 174.91, 175.08, 176.75, 173.92, 108.73),
('MSFT', 334.41, 334.97, 336.49, 332.12, 21.95)

INSERT INTO tracking (userID, stockID) VALUES
(1, 'AAPL'),
(1, 'MSFT'),
(2, 'AAPL'),
(3, 'MSFT')

INSERT INTO sentimentHistory(companyID, sentScore) VALUES
('AAPL', 'Positive'),
('AAPL', 'Neutral'),
('MSFT', 'Neutral'),
('AAPL', 'Negative'),
('MSFT', 'Positive'),
('MSFT', 'Positive')


SELECT * from userList
SELECT * from tracking
SELECT * from companyList
SELECT * from StockInfo
select * from sentimentHistory
SELECT * from sys.tables
GO