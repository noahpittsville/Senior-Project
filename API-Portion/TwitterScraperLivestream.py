from TwitterScraper import *

api, data, columns = getAPI()
grab_limit, time_start, time_end, keywords, hashtags, usernames, timeline = getSettings()

# LIVESTREAM
class Listener(tweepy.Stream):

    tweets = []
    limit = 100

    def on_status(self, status):
        self.tweets.append(status)
        print(status.created_at + ": " + status.user.screen_name + ": " + status.text)

        if len(self.tweets) == self.limit:
            self.disconnect()

consumer_key, consumer_secret, access_token, access_token_secret = getConfig()
stream_tweet = Listener(consumer_key, consumer_secret, access_token, access_token_secret)

# Stream by keyword
stream_tweet.filter(track=keywords)

for tweet in stream_tweet.tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

df = pd.DataFrame(data, columns=columns)
print(df)

print("Scraping in the background")
