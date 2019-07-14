import pandas as pd
from textblob import TextBlob
from TwitterData import TwitterData
import matplotlib.pyplot as plt



NUM_TWEETS = 100


def init():
    candidates = ['Bernie Sanders', 'Donald Trump', 'Joe Biden', 'Elizabeth Warren',
                  'Kamala Harris', 'Pete Buttigieg','Cory Booker', 'Beto O’Rourke',
                  'Julián Castro', 'Amy Klobuchar']

    pos_arr = []
    neg_arr = []

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

    plotData(df)


def plotData(df):
    print("plotting data")

    df.set_index("candidates", drop=True, inplace=True)
    df.plot.bar(color=['green', 'red'])
    plt.ylabel("number of tweets")
    plt.title("number of positive and negative tweets regarding presidential candidates")
    plt.tight_layout()
    plt.show()



## returns -1 if polarity is negative, 1 if positive and 0 otherwise
def getPolarity(tweet):

    blob = TextBlob(tweet)

    if blob.sentiment.polarity > 0:
        # print(tweet)
        return 1
    elif blob.sentiment.polarity < 0:
        # print(tweet)
        return -1
    else:
        return 0



if __name__ == "__main__":
    init()
