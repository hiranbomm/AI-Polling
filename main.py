import csv, re, sys
import pandas as pd
from textblob import TextBlob
from TwitterData import TwitterData

# TODO: cache the data into a file and read it from there. If file doesnt exist, then call the API for fresh data
# TODO:     OR: set a flag for newData. if it is true, then rewrite the file. else, use the existing file

NUM_TWEETS = 100
POS_POL = 0.2   # "I love ___ " got polarity of 0.5, so aiming a bit lower to consider a tweet positive
NEG_POL = -0.5  # "I hate ___ " got polarity of -0.8, so aiming a bit higher to consider a tweet negative

def init():
    candidates = ['Bernie Sanders', 'Donald Trump']
    pol_dict = {}

    TD = TwitterData(candidates)
    TD.authorize()
    for candidate in candidates:
        print("current candidate: ", candidate)
        TD.getData(candidate, NUM_TWEETS)

        print("calculating polarity")
        TD.negative = 0
        TD.positive = 0

        for tweet in TD.all_tweets:
            pol = getPolarity(tweet)
            if pol < 0: TD.negative += 1
            elif pol > 0: TD.positive += 1

        pol_dict[candidate] = (TD.positive, TD.negative, len(TD.all_tweets)) # TODO: make sure this tuple goes into the dictionary well

    print(pol_dict)


# returns -1 if polarity is negative, 1 if positive and 0 otherwise
def getPolarity(tweet):

    blob = TextBlob(tweet)
    if blob.sentiment.polarity >= POS_POL:
        return 1
    elif blob.sentiment.polarity <= NEG_POL:
        return -1
    else:
        return 0



if __name__ == "__main__":
    init()
