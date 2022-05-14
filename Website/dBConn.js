(function () {

    var express = require('express');
    var router = express.Router();
    var app = express();
    var sql = require('mssql');
    
    //Middleware for process POST requests
    app.use(express.json());
    app.use(express.urlencoded({extended: true}));
    
    //DB Connection info
    const sqlConfig = {
        user: 'serverConTest',
        password: 'serverTest',
        database: 'testDB',
        server: '50.91.112.92',
        pool: {
            max: 10,
            min: 0,
            idleTimeoutMillis: 30000
        },
        options : {
            encrypt: false,
            trustServerCertifice: true
        }
    }
    
    //Early test
    async function runQuery() {
        console.log('running')
        var outPacket = {"set1" : "", "set2" : ""}
        try {
            console.log('test')
            await sql.connect(sqlConfig)
            var result = await sql.query`select * from userList FOR JSON AUTO`
            console.log(result)
            outPacket["set1"] = result.recordset
            result = await sql.query`select * from companyList FOR JSON AUTO`
            console.log(result)
            outPacket["set2"] = result.recordset
            console.log(outPacket.set2)
            return outPacket
        }
        catch (err) {
            console.log('testing')
            console.log(err)
        }
    
    }
    
    //Check if user name exists in DB
    async function checkUserName(userName) {
        console.log('Checking existence of Username')
    
        try {
            await sql.connect(sqlConfig)
            const result = await sql.query`SELECT * FROM userList WHERE userName = ${userName}`
            if (result.recordset[0]) return "exists"
            else return "clear"
        }
        catch(err) {
            console.log(err)
            return err
        }
    
    }
    
    //Insert user into database
    //uses checkUserName to ensure user name doesn't already exist.
    async function insertUser(userInfo) {
        console.log('Inserting User')
    
        var check = await checkUserName(userInfo.user)
    
        if (check == "clear") {
            try {
                console.log('connecting')
                await sql.connect(sqlConfig)
                const result = await sql.query`INSERT INTO userList (firstName, lastName, userName, passWrd) VALUES(${userInfo.first}, ${userInfo.last}, ${userInfo.user}, ${userInfo.pass})`
                console.log(result.recordset)
                return "Success"
            }
            catch(err) {
                console.log(err)
                return err
            }
        }
        else return "Username already exists"
    
    
    }
    //Grabbing user information for login verification
    //And session information
    async function grabUserInfo(userName) {
        var check = await checkUserName(userName)
    
        if (check == "exists") {
            try {
                console.log("Querying Pass")
                await sql.connect(sqlConfig)
                const result = await sql.query`SELECT * FROM userList WHERE userName = ${userName}`
                console.log(result)
                return result.recordset[0]
            }
            catch (err) {
                console.log(err)
                return err
            }
        }
    }
    
    async function grabChartData(companyID, startDate, endDate) {
        var check=false
    
        //Check company is in database
        try {
            console.log(companyID)
            console.log("checking if company in database")
            await sql.connect(sqlConfig)
            let q = `SELECT * FROM companyList WHERE companyID = '${companyID}'`
            //console.log(q)
            const result = await sql.query(q)
            //console.log(result)
            if (result.recordset[0]) check = true
            console.log(check)
        }
        catch (err) {
            console.log(err)
            return err
        }
    
        if (check) {

            var output = {"set1" : "", "set2" : ""}

            //Build queryString
            console.log('company in database')
            var sentString = `SELECT A.tweetContent, dateTweet, sentScore, keyword
                                FROM sentimentHistory as A RIGHT JOIN
                                (
                                    SELECT dateTweet, tweetContent, keyWord
                                    FROM arc_tweetTest join companyKeys
                                    ON CHARINDEX (keyWord, tweetContent) > 0
                                    WHERE companyID = '${companyID}'
                                ) AS B
                                ON A.tweetContent = B.tweetContent`
            var stockString = `SELECT * FROM stockInfo WHERE stockID = '${companyID}'`
            if (startDate) {
                sentString += ` WHERE dateTweet >= '${startDate}'`
                stockString += ` AND infoDate >= '${startDate}'`
                if (endDate) {
                    sentString += ` AND dateTweet <= '${endDate}'`
                    stockString += ` AND infoDate <= '${endDate}'`
                }
            }
            else if (endDate) {
                sentString += ` WHERE dateTweet < ${endDate}`
                stockString += ` AND infoDate < ${endDate}`
            }
            sentString += ` ORDER BY dateTweet`
            stockString += ` ORDER BY infoDate`

            //Query Database
            //console.log(sentString)
            try {
                const queryResult = await sql.query(sentString)
                //console.log(queryResult.recordset)
                output.set1 = queryResult.recordset
            }
            catch (err) {
                console.log(err)
                return err
            }


            try {
                console.log("Second query")
                console.log(stockString)
                const queryResult2 = await sql.query(stockString)
                console.log(queryResult2)
                output.set2 = queryResult2.recordset
            }
            catch (err) {
                console.log(err)
                return err
            }

            return output

            
        }
        else {
            return "Company not in Database"
        }
    }
    
    //Add stock to the tracking Table
    async function insertStockTrack(info) {
        console.log(`Adding ${stockSymbol} to ${userName}'s tracked stocks.`)

        try {
            await sql.connect(sqlConfig)
            const queryResult = await sql.query`INSERT INTO tracking (userNAme, stockID) VALUES (${info.user}, ${info.symbol})`
            return "Added"
        }
        catch (err) {
            console.log(err)
            return err
        }

    }
    //Grab tracked stock information
    async function getTrackedStock(userName) {
        console.log(`Pulling ${userName}'s tracked stocks`)

        try {
            await sql.connect(sqlConfig)
            const queryResult = await sql.query`SELECT stockID FROM tracking WHERE userName = ${userName}`
            console.log(queryResult.recordset)
            return queryResult.recordset 
        }
        catch (err) {
            console.log(err)
            return err
        }

    }

    //Handlers

    //Account Creation
    app.post('/create', async function(req, res) {
        var userInfo = {
            "first" : req.body.firstName,
            "last" : req.body.lastName,
            "user" : req.body.userName,
            "pass" : req.body.passWord
        }
        var queryResult = await insertUser(userInfo)
        res.send(queryResult)
    })

    //Login
    app.post('/verify', async function(req, res) {
        var user = req.body.userName

        var queryResult = await grabUserInfo(user)
        console.log(queryResult)
        if (queryResult) {
            res.send(queryResult.passWrd)
        }
        else {
            res.send("User does not exist")
        }

    })

    //Grab user infrmation for $_SESSION Values
    app.post('/grabInfo', async function(req,res) {
        var user = req.body.userName

        var queryResult = await grabUserInfo(user)
        console.log(queryResult)

        res.send(queryResult)
    })

    //Grab Chart Information
    app.post('/grabChartInfo', async function(req, res) {
        var stockInfo = {
            "companyId" : req.body.companyID,
            "startDate" : req.body.startDate,
            "endDate" : req.body.endDate
        }
        console.log(stockInfo)

        var queryResult = await grabChartData(stockInfo.companyId, stockInfo.startDate, stockInfo.endDate)
        //console.log(queryResult)
        console.log(queryResult.set2)
        res.json(queryResult)

    })
    //Insert user's tracked data into database
    app.post('/insertTrackInfo', async function(req, res) {
        var info = {
            "user": req.body.userName,
            "symbol": req.body.stockSymbol
        }

        var queryResult = await insertStockTrack(info)

        res.send(queryResult)
    })
    //Grab user's tracked stock data
    app.post('/grabTrackInfo', async function(req,res) {
        var user = req.body.userName
        var queryResult = await getTrackedStock(user)
        console.log(queryResult)
        res.send(queryResult)
    })


    app.listen(3680, function() {
        console.log("Server Running...")
    })

})();