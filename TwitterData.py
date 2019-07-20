import tweepy
import re
import requests_cache


class TwitterData(object):

    def __init__(self):
        # self.all_tweets = []
        self.tweet_data = []  # this is the new field you added.
        self.API = None
        self.positive = None
        self.negative = None

    def authorize(self):
        try:
            # keys deleted for privacy
            consumerKey =
            consumerSecret =

            accessKey =
            accessSecret = 


            authorized = tweepy.OAuthHandler(consumerKey, consumerSecret)
            authorized.set_access_token(accessKey, accessSecret)

            self.API = tweepy.API(authorized, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

        except:
            print("ERROR: AUTHENTICATION FOR API FAILED")

    def get_data(self, candidate, NUM_TWEETS):
        requests_cache.install_cache('twitter_cache', backend='sqlite', expire_after=1800)

        print("getting tweets")
        self.tweet_data.clear()

        # for each tweet returned, get rid of unwanted symbols and add it to all_tweets
        for tweet in tweepy.Cursor(self.API.search, q=candidate, lang='en').items(NUM_TWEETS):
            tweet.text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", tweet.text).split())
            self.tweet_data.append(tweet)

        print("done getting data")
