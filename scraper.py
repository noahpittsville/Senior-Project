# pip install bs4
# pip install requests
# pip install lxml
# pip install datetime
# pip install tweepy

import bs4
import requests
import sys
import tweepy
import csv
import re
import time
from io import StringIO
from bs4 import BeautifulSoup
from datetime import datetime
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import Stream

# Twitter ------------
consumer_key = "XkYHMkPTvLRZCPLFM1xnKjrZX"  # API Key?
consumer_secret = "TwMnw4NUK6JWJqaO4KLSwvCE9CaaA5GIMgt16AUVSe6jSNrH6G" # API Key Secret?
access_token = "1469036989429153794-6NmkD3LWPUFRN8Ny65S7J816xFaHB0"
access_token_secret = "LrPl8TX3gApFzWNkW7TQJGe7kQufbBMz7a3mGITuA15r7"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class listener(Stream):
    def on_data(selfself, data):
        try:
            print(data)

            tweet = data.split(',"text":"')[1].split('","source')[0]
            print(tweet)

            saveThis = str(time.time())+'::'+tweet

            saveFile = open('twitDB.csv','a')
            saveFile.write(saveThis)
            saveFile.write('\n')
            saveFile.close()
            return True
        except BaseException as e:
            print('failed ondata, '),str(e)
            time.sleep(5)
    def on_error(self, status):
        print(status)

#twitterStream = Stream(auth, listener())
#twitterStream.filter(track=["stocks", "stock"])
Scraper = Stream(auth, listener())
Scraper.filter(track=["stocks", "stock"])

# Yahoos Finance --------------------
url_stats = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'
url_profile = 'https://finance.yahoo.com/quote/{}/profile?p={}'
url_financials = 'https://finance.yahoo.com/quote/{}/financials?p={}'

stock = 'F'

response = requests.get(url_financials.format(stock, stock))
soup = BeautifulSoup(response.text, 'html.parser')
pattern = re.compile(r'\s--\dSata\s--\s')
soup.find('script', text=pattern).contents[0]
##TO DO MORE

def getDate():
    r=requests.get("https://finance.yahoo.com/quote/INTC?p=INTC")
    soup=bs4.BeautifulSoup(r.text, "html.parser")
    date=soup.find_all('div', {'id':'quote-market-notice'}, {'class': 'C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm'})[0].find('span').text
    #date=date+date.today()
    return datetime.today().strftime("%m--%d")

def Tesla_parse():
    url = requests.get("https://finance.yahoo.com/quote/TSLA?p=TSLA&.tsrc=fin-srch")
    bs = bs4.BeautifulSoup(url.text, "html.parser")
    bs
    price = bs.find_all('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    return price

#


