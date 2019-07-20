import pandas as pd
from textblob import TextBlob
# from TwitterData import TwitterData
import matplotlib.pyplot as plt
import tweepy
import re
import requests_cache


# added this class to this file because moving objects from file to file is taking up too much times
class TwitterData(object):

    def __init__(self, candidates):
        # self.all_tweets = []
        self.tweet_data = []  # this is the new field you added.
        self.API = None
        self.positive = None
        self.negative = None

    def authorize(self):
        try:
            # keys deleted for privacy
            consumerKey = 'coJsIbWW7o1WN0Caiihc6quOQ'
            consumerSecret = 'TA4ZNUbSu3u9PfeWqmKZtClNRF4Y0ZXIDxiVuKdgZFGPmsq9iO'

            accessKey = '1150145735259807745-o2TymPP1JJyuFJPIOvR2BmitOVWKjd'
            accessSecret = 'XnvutgN0NdPzcuoHX9mzcRL6WNriLaGY40b5hsgCldPyb'


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


NUM_TWEETS = 100

# I chose 0.2 and -0.2 as the cut-offs because "I love <candidate>" got a polarity of 0.2
POL_POS = 0.2
POL_NEG = -0.2


def plot_bar_graph_data(df):
    print("plotting data")

    df.set_index("candidates", drop=True, inplace=True)
    df.plot.bar(color=['green', 'red'])
    plt.ylabel("number of tweets")
    plt.title("number of positive and negative tweets regarding presidential candidates")
    plt.tight_layout()
    plt.show()


# returns -1 if polarity is negative, 1 if positive and 0 otherwise
def get_polarity(text):

    blob = TextBlob(text)

    if blob.sentiment.polarity >= POL_POS:
        # print(tweet)
        return 1
    elif blob.sentiment.polarity <= POL_NEG:
        # print(tweet)
        return -1
    else:
        return 0


if __name__ == "__main__":

    candidates = ['Bernie Sanders', 'Donald Trump', 'Joe Biden', 'Elizabeth Warren',
                  'Kamala Harris', 'Pete Buttigieg','Cory Booker', 'Beto O’Rourke',
                  'Julián Castro', 'Amy Klobuchar']

    pos_arr = []
    neg_arr = []

    TD = TwitterData(candidates)
    TD.authorize()
    for candidate in candidates:
        print("current candidate: ", candidate)
        TD.get_data(candidate, NUM_TWEETS)

        print("calculating polarity")
        TD.negative = 0
        TD.positive = 0

        for tweet in TD.tweet_data:
            # TODO: get location of tweet

            pol = get_polarity(tweet.text)
            if pol < 0:
                TD.negative += 1
            elif pol > 0:
                TD.positive += 1

        pos_arr.append(TD.positive)
        neg_arr.append(TD.negative)

    df = pd.DataFrame({
        "candidates": candidates,
        "positive": pos_arr,
        "negative": neg_arr})

    plot_bar_graph_data(df)

