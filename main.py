import pandas as pd
from textblob import TextBlob
from geopy import geocoders
import matplotlib.pyplot as plt
import tweepy
import re
import requests_cache
import folium


# added this class to this file because moving objects from file to file is taking up too much times
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




NUM_TWEETS = 130
# chose 0.3 as the cut-off becuase "I love <candidate>" got this polarity
POL_POS = 0.3
POL_NEG = -0.3


def geo(location):
    g = geocoders.Nominatim(user_agent="my_application")
    loc = g.geocode(location)
    return loc.latitude, loc.longitude


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

    candidates = ['Donald Trump', 'Bernie Sanders', 'Elizabeth Warren', 'Kamala Harris',
                  'Pete Buttigieg', 'Joe Biden', 'Beto O’Rourke']

    pos_arr = []
    neg_arr = []

    TD = TwitterData()
    TD.authorize()

    for candidate in candidates:
        print("current candidate: ", candidate)
        TD.get_data(candidate, NUM_TWEETS)

        print("calculating polarity")
        TD.negative = 0
        TD.positive = 0

        map = folium.Map(prefer_canvas=True)

        for tweet in TD.tweet_data:

            loc = tweet.user.location
            try:
                (lat, long) = geo(loc)
                pol = get_polarity(tweet.text)

                if pol <= 0:
                    TD.negative += 1

                    folium.CircleMarker(
                        radius=5,
                        location=[lat, long],
                        # popup='The Waterfront',
                        opacity=0.4,
                        color='red',
                        fill=True,
                    ).add_to(map)

                elif pol > 0:
                    TD.positive += 1

                    folium.CircleMarker(
                        radius=5,
                        location=[lat, long],
                        opacity=0.4,
                        # popup='The Waterfront',
                        color='green',
                        fill=True,
                    ).add_to(map)

            except:
                pass

        pos_arr.append(TD.positive)
        neg_arr.append(TD.negative)

        map.save(outfile='' + candidate + '.html')

    df = pd.DataFrame({
        "candidates": candidates,
        "positive": pos_arr,
        "negative": neg_arr})

    plot_bar_graph_data(df)
