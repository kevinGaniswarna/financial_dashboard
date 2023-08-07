## ACTIVATE VIRTUAL ENVIRONMENT
## PAUSED AS API ACCESS IS BLOACKER


## Run in CMD
## .\myvenv\Scripts\activate

## Run in CMD
## deactivate
#pip install -r requirement.txt

import streamlit as st;
import os;
import pandas as pd;
import yfinance as yf;
import datetime as dt;
import numpy as np;
import plotly.graph_objects as go;
#from pandas_datareader import data as wb;
import wbdata as wbank
import requests
import tweepy
import config
import psycopg2, psycopg2.extras
from pandas_datareader import data as pdr


#import snscrape.modules.twitter as sntwitter

#scraper = sntwitter.TwitterSearchScrape("#python")



# Twitter API Authenticator ACCESS
#
# auth = tweepy.OAuth1UserHandler(
#     config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET, config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET
# )
# api = tweepy.API(auth)

## connect to wallstreetbets
## connection = psycopg2.connect(host = config.DB_HOST, database = config.DB_NAME, user = config.DB_USER, password = config.DB_PASS)
## cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
##
##



st.sidebar.header("Options")

option = st.sidebar.selectbox("which dashboard", ("yfinance introductory", "backtest", "twitter", "wallstreetbets", "stocktwits", "chart", "pattern"   ),0)
# header
# Subheader

st.header(option)

if option == "yfinance introductory":
    st.subheader("this is the yfinance dashboard")
    yf.pdr_override()
    symbol = st.sidebar.text_input("Symbol", value = ' ', max_chars = 10)
    st.write(symbol)

    startyear = 2020
    startmonth = 1
    startdate = 1

    start = dt.datetime(startyear,startmonth, startdate)

    now = dt.datetime.now()

    df = pdr.get_data_yahoo(symbol, start, now)
    st.write(df)

## Moving Average calculations

    ma =  st.sidebar.number_input("MA period", min_value = 1, max_value = 365)
    smaString = "Sma_"+ str(ma)
    df[smaString] = df.iloc[:,4].rolling(window=ma).mean()
    df = df.iloc[ma:]
    st.write(df)
## iterate your database
    df['Flag'] = df.iloc[:,4] > df.iloc[:,6]

    numH = 0
    numC = 0
    for i in df.index:
         # st.write(df["Adj Close"][i])
         # st.write(df.iloc[:,4][i])
         # st.write(df["smaString"][i])
       if( df.iloc[:,4][i] > df.iloc[:,6][i] ):
          numH += 1
       else:
          numC +=1

    st.write("number of times higher =" + str(numH))
    st.write("number of times Lower =" + str(numC))

if option == "backtest":
    st.subheader("this is the yfinance backtest")
    yf.pdr_override()
    symbol = st.sidebar.text_input("Symbol", value = ' ', max_chars = 10)
    st.write(symbol)

    startyear = 2020
    startmonth = 1
    startdate = 1

    start = dt.datetime(startyear,startmonth, startdate)

    now = dt.datetime.now()

    df = pdr.get_data_yahoo(symbol, start, now)
    st.write(df)

    emasUsed[3,5,8,10,12,15,30,35,40,45,50,60]

    for x in emasUsed:
        ema = x
        df["Ema_" + str(ema)] = round(df.iloc[:4].ewm(span = ema, adjust = False).mean(),2)

    st.write(df.tail())
# SENTIMENTAL ANALYSIS DASHBOARD VIA TWITTER

if option == "twitter":
    st.subheader("this is the twitter dashboard")
    # for username in config.TWITTER_USERNAMES:
    #     user = api.get_user(username)
    #     tweets = api.user_timeline(username)
    #     st.write(user.id)
    # # get user avatar
    #     st.image(user.profle_image_url)
    # # st.write(tweets)
    #     for tweet in tweets:
    #         if '$' in tweet.text:
    #             words = tweet.text.split(' ')
    #             for word in words:
    #                 if word.startswith('$') and word[1:].isalpha():
    #                     symbol = word[1:]
    #                     st.write(symbol)
    #                     st.write(tweet.text)
    #                     st.image(f"https://finviz.com/quote.ashx?t={symbol}&p=d")

if option == "wallstreetbets":
    st.subheader("this is the wallstreetbets dashboard")

if option == "chart":
    st.subheader("this is the chart dashboard")

if option == "pattern":
    st.subheader("this is the pattern dashboard")


if option == "stocktwits":
    symbol = st.sidebar.text_input("Symbol", value = ' ', max_chars = 10)

    st.subheader("this is the stocktwits dashboard")
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")
    data = r.json()

    for message in data["messages"]:
        st.image(message['user']["avatar_url"])
        st.write(message['user']["username"])
        st.write(message['created_at'])
        st.write(message['body'])



## TUTORIAL for Streamlit
# st.write("text")
#
# """
# # Header
# ## Subheader
#
# """
#
# some_dictionary = {
#    "key1": "Value",
#    "key2": "Value2"
#
# };
# some_list = [1,2,3];
# st.write(some_dictionary)
# st.write(some_list)
#
# # Create Sidebar
#
# st.sidebar.write("write this to the sidebar")
#
#
# # show dataframe
# df = pd.DataFrame(np.random.randn(50,20), columns = ('col %d' % i for i in range(20)))
# st.dataframe(df)
#
# # input image
#
# #st.image()


# Define functions for data collection from Twitter Scrapes

#
# #A for loop is used to iterate over and store the tweet data (username, date,
# # and tweet content) returned by the get_items method of
# # sntwitter.TwitterSearchScraper.
#
# # We use lang:en (English language) and exclude:retweets as the search filters.
# # The tweet data is finally returned as a dataframe.
# def scrape_tweet(search_term, start_date, end_date, num_tweets):
#     start_date = start_date.strftime("%Y-%m-%d")
#     end_date = end_date.strftime("%Y-%m-%d")
#     tweet_data = []
#     for i, tweet in enumerate(
#         sntwitter.TwitterSearchScraper(
#             "{} since:{} until:{} lang:en exclude:retweets".format(
#                 search_term, start_date, end_date
#             )
#         ).get_items()
#     ):
#         if i >= num_tweets:
#             break
#         tweet_data.append([tweet.user.username, tweet.date, tweet.content])
#     tweet_df = pd.DataFrame(tweet_data, columns=["username", "date", "tweet"])
#     return tweet_df
#
#
# # For this project, we want to retrieve tweets
# # from 2022-01-01 to 2022-12-31.
# # So we make another function, daily_scrape_2022 which utilizes
# # the scrape_tweet function to retrieve tweets for each day in 2022.
# # We can specify the number of tweets we want to retrieve for each day
# # using num_daily.
# def daily_scrape_2022(search_term, num_daily):
#     start_date = dt.datetime(2022, 1, 1)
#     end_date = dt.datetime(2022, 1, 2)
#     delta = dt.timedelta(days=1)
#     df = pd.DataFrame()
#     for n in range(365):
#         temp_df = scrape_tweet(search_term, start_date, end_date, num_daily)
#         df = pd.concat([df, temp_df])
#         start_date += delta
#         end_date += delta
#     return df
#
#
# # Now we will use the daily_scrape_2022 function to retrieve 1000 tweets
# # for each day in 2022. Tweets with negative sentiment
# # will be searched with the term ":("
# # while tweets with positive sentiment will be searched with the term ":)".
#
# ori_neg_df = daily_scrape_2022(":(", 1000)
# ori_pos_df = daily_scrape_2022(":)", 1000)
#
# #
# # The retrieved tweets do not always contain the specified search term,
# # so we need to do some filtering.
# # We create two functions, filter_include to include tweets containing a
# # specific term and filter_exclude to exclude tweets containing a specific term.
# # Note that both functions take a list of terms as the second argument,
# # so we can filter multiple terms at once.
#
# def filter_include(df, term_list):
#     temp_df = pd.DataFrame()
#     for term in term_list:
#         add_df = df[df["tweet"].str.contains(term, regex=False) == True]
#         temp_df = pd.concat([temp_df, add_df]).drop_duplicates(ignore_index=True)
#     return
#
# def filter_exclude(df, term_list):
#     temp_df = df.copy()
#     for term in term_list:
#         temp_df = temp_df[temp_df["tweet"].str.contains(term, regex=False) == False]
#     return temp_df
#
#
# # For the negative tweets, first we will include tweets containing the term ":("
# # or ":-(", then exclude tweets containing the term ":)", ":D", or ":-)".
# # Note that filter_exclude is done on neg_df, not ori_neg_df. Tweets with smiley
# # face emoticon are excluded because we do not want to label tweets containing
# # both frowning face and smiley face emoticons as negative. After filtering,
# # we have 358624 tweets with negative sentiment.
#
# neg_df = filter_include(ori_neg_df, [":(", ":-("])
# neg_df = filter_exclude(neg_df, [":)", ":D", ":-)"])
# st.write(neg_df.shape)
#
# #Similar filtering is done for the positive tweets. After filtering,
# #we have 343477 tweets with positive sentiment.
# pos_df = filter_include(ori_pos_df, [":)", ":D", ":-)"])
# pos_df = filter_exclude(pos_df, [":(", ":-("])
# st.write(pos_df.shape)
#
# #
# # Next, we will remove all the emoticons used for filter_include from the tweets.
# # This is required because we want our model to classify the sentiment based on
# # the words instead of the emoticons. If we include the emoticons in the training
# # data, the model will have poor generalization performance because the emoticons
# #  may not be present in real-world data
#
# def remove_term(df, term_list):
#     temp_df = df.copy()
#     for term in term_list:
#         temp_df["tweet"] = temp_df["tweet"].str.replace(term, " ", regex=False)
#     return temp_df
#
# neg_df = remove_term(neg_df, [":(", ":-("])
# pos_df = remove_term(pos_df, [":)", ":D", ":-)"])
#
# # Last we will label the sentiment of the tweets and combine them into
# # one dataframe.
#
# neg_df["sentiment"] = "Negative"
# pos_df["sentiment"] = "Positive"
# df = pd.concat([neg_df, pos_df]).reset_index(drop=True)
# current_wd = Path.cwd()
# df.to_csv(current_wd, index=False)

# So now we have collected our training data through distant supervision.
