import tweepy
import csv, re, sys
import pandas as pd
from textblob import TextBlob

class TwitterData(object):

    def __init__(self, candidates):
        self.all_tweets = []
        self.API = None
        # self.candidates = candidates

    def authorize(self):
        try:
            # keys deleted for privacy

            authorized = tweepy.OAuthHandler(consumerKey, consumerSecret)
            authorized.set_access_token(accessKey, accessSecret)

            self.API = tweepy.API(authorized)

        except:
            print("ERROR: AUTHENTICATION FOR API FAILED")



    def getData(self, candidate):
        print("getting data")
        self.all_tweets.clear()

        for tweet in tweepy.Cursor(self.API.search, q=candidate, lang='en').items(100):
            self.all_tweets.append(tweet)

        print("done getting data")



