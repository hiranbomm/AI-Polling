import pandas as pd
from textblob import TextBlob
from geopy import geocoders
import matplotlib.pyplot as plt
import folium
from TwitterData import TwitterData


NUM_TWEETS = 200
# chose 0.3 as the cut-off because "I like <candidate>" got this rating
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

                if pol < 0:
                    TD.negative += 1

                    folium.CircleMarker(
                        radius=5,
                        location=[lat, long],
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


