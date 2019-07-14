import tweepy
import csv, re, sys
import pandas as pd
from textblob import TextBlob
from TwitterData import TwitterData


def init():
    candidates = ['Bernie Sanders']

    TD = TwitterData(candidates)
    TD.authorize()
    for candidate in candidates:
        TD.getData(candidate)

    print(TD.all_tweets)

if __name__ == "__main__":
    init()
