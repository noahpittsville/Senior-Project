# Twitter Scraper

# Import libraries

# Our main API to grab twitter information
# pip install tweepy
import tweepy

# Tokens, Keys, Secrets
# pip install config
# pip install configparser

import config
import configparser
import ast

# save data into a csv
# pip install pandas
import pandas as pd

# for menu
#pip install numpy
import numpy as np
import re
import shlex


# settings & search info
def getSettings():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    grab_limit = config['settings']['limit']
    time_start = config['settings']['start']
    time_end = config['settings']['end']
    config.read('searchSettings.txt')
    keywords = config['search']['key']
    hashtags = config['search']['hash']
    usernames = config['search']['user']
    timeline = config['search']['timeline']
    return grab_limit, time_start, time_end, keywords, hashtags, usernames, timeline

def setSettings(section, element, value, update):
    grab_limit, time_start, time_end, keywords, hashtags, usernames, timeline = getSettings()
    config = configparser.ConfigParser()
    interval = []
    config.read('settings.ini')
    if update is 'set':
        grab_limit = str(value)
        config.set(section, element, grab_limit)
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
    config.read('searchSettings.txt')
    if update is 'add':
        if element is 'key':
            interval = keywords
        elif element is 'hash':
            interval = hashtags
        elif element is 'user':
            interval = usernames
        elif element is 'user_timeline':
            interval = timeline
        interval = interval.replace("[", '')
        interval = interval.replace("]", '')
        interval = interval.replace("',", "'")
        #interval = interval.split(',')
        #interval = schlex.split(interval)
        interval = shlex.split(interval)
        if value not in interval:
            interval.append(value)
            interval = str(interval)
            config.set(section, element, interval)
        else:
            print('Already exists as a search term.\n')
    if update is 'delete':
        if element is 'key':
            interval = keywords
        elif element is 'hash':
            interval = hashtags
        elif element is 'user':
            interval = usernames
        elif element is 'usertimeline':
            interval = timeline
        interval = interval.replace("[", '')
        interval = interval.replace("]", '')
        interval = interval.replace("',", "'")
        interval = shlex.split(interval)
        if value in interval:
            #interval = [x for x in interval if x != value]
            interval.remove(value)
            interval = str(interval)
            config.set(section, element, interval)
        else:
            print('Does not exist, failed to delete anything.\n')
    with open('searchSettings.txt', 'w') as configfile:
        config.write(configfile)



# set up the secrets, keys, and tokens  in the config.ini
def getConfig():
    config = configparser.ConfigParser()
    config.read("config.ini")
    consumer_key = config['twitter']['API_KEY']
    consumer_secret = config['twitter']['API_KEY_SECRET']
    access_token = config['twitter']['ACCESS_TOKEN']
    access_token_secret = config['twitter']['ACCESS_TOKEN_SECRET']
    return consumer_key, consumer_secret, access_token, access_token_secret

def getOAuthHandler(): # OAuthHandler deprecated, use OAuth1UserHandler instead
    consumer_key, consumer_secret, access_token, access_token_secret = getConfig()
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

def getAPI():
    auth = getOAuthHandler()
    api = tweepy.API(auth)
    columns = ['Time', 'User', 'Tweet']
    data = []
    return api, data, columns

# SPECIFIC SEARCHES
def homeTimeline():
    api, data, columns = getAPI()
    home_timeline = api.home_timeline()
    for tweet in home_timeline:
        data.append([tweet.created_at, tweet.user.screen_name, tweet.text])
    return data, columns

def userTimeline():
    api, data, columns = getAPI()
    grab_limit, time_start, time_end, keywords, hashtags, usernames, timeline = getSettings()
    grab_limit = int(grab_limit)
    #user_timeline = api.user_timeline()
#    keywords, hashtags, usernames, usernames_timeline, grab_limit = getSearchInfo()
    # user_timeline max grab is 200
    #user_timeline_tweets = api.user_timeline(screen_name=username, count=grab_limit, tweet_mode='extended')
    timeline = timeline.replace("[", '')
    timeline = timeline.replace("]", '')
    timeline = timeline.replace("',", "'")
    timeline = shlex.split(timeline)
    for user in timeline:
        timeline = tweepy.Cursor(api.user_timeline,
                                 screen_name=user,
                                 count=200,
                                 tweet_mode='extended').items(grab_limit)
        for tweet in timeline:
            data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])
    return data, columns


def keywordsUser():
    api, data, columns = getAPI()
    grab_limit, time_start, time_end, keywords, hashtags, usernames, timeline = getSettings()
    grab_limit = int(grab_limit)
    usernames = usernames.replace("[", '')
    usernames = usernames.replace("]", '')
    usernames = usernames.replace("',", "'")
    usernames = shlex.split(usernames)
    for key in usernames:
        keyword_search = tweepy.Cursor(api.search_tweets,
                                       q=key,
                                       count=100,
                                       tweet_mode='extended').items(grab_limit)
        for tweet in keyword_search:
            if not tweet.truncated:
                data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])
            else:
                data.append([tweet.created_at, tweet.user.screen_name, tweet.extended_tweet['full_text']])
    return data, columns

def keywordsHashtag():
    api, data, columns = getAPI()
    grab_limit, time_start, time_end, keywords, hashtags, usernames, timeline = getSettings()
    grab_limit = int(grab_limit)
    hashtags = hashtags.replace("[", '')
    hashtags = hashtags.replace("]", '')
    hashtags = hashtags.replace("',", "'")
    hashtags = shlex.split(hashtags)
    for hash in hashtags:
        keyword_search = tweepy.Cursor(api.search_tweets, q=hash, count=100, tweet_mode='extended').items(grab_limit)
        for tweet in keyword_search:
            if not tweet.truncated:
                data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])
            else:
                data.append([tweet.created_at, tweet.user.screen_name, tweet.extended_tweet['full_text']])
    return data, columns

def keywordsSearch():
    api, data, columns = getAPI()
    grab_limit, time_start, time_end, keywords, hashtags, usernames, timeline = getSettings()
    grab_limit = int(grab_limit)
    keywords = keywords.replace("[", '')
    keywords = keywords.replace("]", '')
    keywords = keywords.replace("',", "'")
    keywords = shlex.split(keywords)
    for keyword in keywords:
        keyword_search = tweepy.Cursor(api.search_tweets, q=keyword, count=100, tweet_mode='extended').items(grab_limit)
        for tweet in keyword_search:
            if not tweet.truncated:
                data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])
            else:
                data.append([tweet.created_at, tweet.user.screen_name, tweet.extended_tweet['full_text']])
    return data, columns

def TwitterLiveStream(search_type):
    api, data, columns = getAPI()
    grab_limit, time_start, time_end, keywords, hashtags, usernames, timeline = getSettings()
    grab_limit = int(grab_limit)
    if search_type is 'keywords':
        search_type = keywords
    if search_type is 'hashtags':
        search_type = hashtags
    if search_type is 'usernames':
        search_type = usernames



    class Listener(tweepy.Stream):
        def on_status(self, status):
            self.tweets.append(status)
            print(status.created_at + ": " + status.user.screen_name + ": " + status.text)

            if len(self.tweets) == self.grab_limit:
                self.disconnect()

    consumer_key, consumer_secret, access_token, access_token_secret = getConfig()
    stream_tweet = Listener(consumer_key, consumer_secret, access_token, access_token_secret)

    stream_tweet.filter(track=search_type)

    for tweet in stream_tweet.tweets:
        data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

    makeDataTable('LiveStream {}'.format(search_type))
    print(df)


def makeDataTable(element):
    # SPECIFIC SEARCHES
    if element is 'HomeTimeline':
        data, columns = homeTimeline()
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('StaticHomeTimeline.csv')
    if element is 'UserTimeline':
        data, columns = userTimeline()
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('StaticUserTimeline.csv')
    if element is 'UserKeywords':
        data, columns = keywordsUser()
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('StaticUserKeywords.csv')
    if element is 'HashtagKeywords':
        data, columns = keywordsHashtag()
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('StaticHashtagKeywords.csv')
    if element is 'SearchKeywords':
        data, columns = keywordsSearch()
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('StaticSearchKeywords.csv')

    #LIVESTREAM
    if element is 'LivestreamHomeTimeline':
        data, columns = homeTimeline()
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('HomeTimeline.csv')
    if element is 'UserTimeline':
        data, columns = userTimeline()
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('UserTimeline.csv')
    if element is 'UserKeywords':
        data, columns = keywordsUser()
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('UserKeywords.csv')
    if element is 'HashtagKeywords':
        data, columns = keywordsHashtag()
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('HashtagKeywords.csv')
    if element is 'SearchKeywords':
        data, columns = keywordsSearch()
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('SearchKeywords.csv')





