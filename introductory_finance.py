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
from tkinter import Tk
from tkinter.filedialog import askopenfilename




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

option = st.sidebar.selectbox("which dashboard", ("yfinance introductory", "backtest", "stock screener", "twitter", "wallstreetbets", "stocktwits", "chart", "pattern"   ),2)
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

    emasUsed=[3,5,8,10,12,15,30,35,40,45,50,60]

    for x in emasUsed:
        ema = x
        emaString = "Ema_" + str(ema)
        df[emaString] = df.iloc[:,4].ewm(span = ema, adjust = False).mean()
    st.write(df.tail())




    df_min = df.iloc[:,6:12]
    df_max = df.iloc[:,13:]
    df["cmin"] = np.min(df_min, axis = 1)
    df["cmax"] = np.max(df_max, axis = 1)

    cmin = np.array(df["cmin"])
    cmax = np.array(df["cmax"])

    df["indicator"] = np.where( cmin > cmax, "red white blue", "blue white red" )

    st.write(df)


    # SIMULATION
    # POS := Position variable -> enter 1 else not enter 0
    pos = 0
    # Num := keep track row we are in
    num = 0
    # percentchange := emptylist that we are gonna add results of our trade in.
    percentchange = []


    for i in df.index:
        close = df["Adj Close"][i]
        if (df["indicator"][i] == "red white blue"):
            st.write(i)
            st.write(df["indicator"][i])
            if(pos == 0):
                bp = close
                pos = 1
                st.write("Buy now at " + str(bp))
        else:
            st.write(i)
            st.write(df["indicator"][i])
            if(pos == 1):
                sp = close
                pos = 0
                st.write("Sell now at " + str(sp))
                pc = (sp/bp - 1)*100
                percentchange.append(pc)
        if(num == df["Adj Close"].count()-1 and pos == 1):
            pos = 0
            st.write("Sell now at " + str(sp))
            pc = (sp/bp - 1)*100
            percentchange.append(pc)
        num+=1

    st.write(num)
    st.write(pos)
    st.write(percentchange)

    cumProd_Return = np.cumprod(1 + (np.divide(percentchange,100)))
    st.write(cumProd_Return)
    st.write("total return of trade " + str(round(100*(cumProd_Return[-1]-1),2)) + "%")

    y = np.array(percentchange)
    x = 0

    pos_ret = sum((y > 0).astype(int))
    neg_ret = sum((y < 0).astype(int))


    st.write("Results for " + symbol + " going back to " + str(df.index[0])  + ", Sample Size: " + str(pos_ret + neg_ret) + " trades.")
    st.write("Input parameters are as follows:")
    st.write("EMAs used:" + str(emasUsed))


    st.write("Output from trade are as follows:")

    st.write("Number of postive trade: " + str(pos_ret))
    st.write("Number of negative trade: " + str(neg_ret))

    neg_ind = (y < 0).astype(int)
    pos_ind = (y > 0).astype(int)

    gains = pos_ind*percentchange
    losses = neg_ind*percentchange

    ## Finding average gains
    avgGains = sum(gains)/pos_ret
    maxGains = max(gains)
    st.write("Average gains from trade: " + str(round(avgGains,2)) + "%")
    st.write("Max gains from trade: " + str(round(maxGains,2)) + "%")

    ## Finding average losses
    avgLosses = sum(losses)/neg_ret
    maxLosses = min(losses)
    st.write("Average losses from trade: " + str(round(avgLosses,2)) + "%")
    st.write("Max losses from trade: " + str(round(maxLosses,2)) + "%")

    # risk ratio
    Risk_ratio = (-avgGains/avgLosses)*100
    batting_avg = (pos_ret / (pos_ret + neg_ret))*100
    st.write("Gain/Loss Ratio from trade: " + str(round(Risk_ratio,2)) + "%")
    st.write("Batting Average from trade strategy: " + str(round(batting_avg,2)) + "%")




        # cmin = min(df["Ema_3"][i], df["Ema_5"][i], df["Ema_8"][i], df["Ema_10"][i], df["Ema_12"][i], df["Ema_15"][i])
        # cmax = max(df["Ema_30"][i], df["Ema_35"][i], df["Ema_40"][i], df["Ema_45"][i], df["Ema_50"][i], df["Ema_60"][i])
        #
        # if(cmin > cmax):
        #     df["flag"][i] = "Red White Blue"
        # else:
        #     df["flag"][i] = "Blue White Red"
# SENTIMENTAL ANALYSIS DASHBOARD VIA TWITTER

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

    emasUsed=[3,5,8,10,12,15,30,35,40,45,50,60]

    for x in emasUsed:
        ema = x
        emaString = "Ema_" + str(ema)
        df[emaString] = df.iloc[:,4].ewm(span = ema, adjust = False).mean()
    st.write(df.tail())




    df_min = df.iloc[:,6:12]
    df_max = df.iloc[:,13:]
    df["cmin"] = np.min(df_min, axis = 1)
    df["cmax"] = np.max(df_max, axis = 1)

    cmin = np.array(df["cmin"])
    cmax = np.array(df["cmax"])

    df["indicator"] = np.where( cmin > cmax, "red white blue", "blue white red" )

    st.write(df)


    # SIMULATION
    # POS := Position variable -> enter 1 else not enter 0
    pos = 0
    # Num := keep track row we are in
    num = 0
    # percentchange := emptylist that we are gonna add results of our trade in.
    percentchange = []


    for i in df.index:
        close = df["Adj Close"][i]
        if (df["indicator"][i] == "red white blue"):
            st.write(i)
            st.write(df["indicator"][i])
            if(pos == 0):
                bp = close
                pos = 1
                st.write("Buy now at " + str(bp))
        else:
            st.write(i)
            st.write(df["indicator"][i])
            if(pos == 1):
                sp = close
                pos = 0
                st.write("Sell now at " + str(sp))
                pc = (sp/bp - 1)*100
                percentchange.append(pc)
        if(num == df["Adj Close"].count()-1 and pos == 1):
            pos = 0
            st.write("Sell now at " + str(sp))
            pc = (sp/bp - 1)*100
            percentchange.append(pc)
        num+=1

    st.write(num)
    st.write(pos)
    st.write(percentchange)

    cumProd_Return = np.cumprod(1 + (np.divide(percentchange,100)))
    st.write(cumProd_Return)
    st.write("total return of trade " + str(round(100*(cumProd_Return[-1]-1),2)) + "%")

    y = np.array(percentchange)
    x = 0

    pos_ret = sum((y > 0).astype(int))
    neg_ret = sum((y < 0).astype(int))


    st.write("Results for " + symbol + " going back to " + str(df.index[0])  + ", Sample Size: " + str(pos_ret + neg_ret) + " trades.")
    st.write("Input parameters are as follows:")
    st.write("EMAs used:" + str(emasUsed))


    st.write("Output from trade are as follows:")

    st.write("Number of postive trade: " + str(pos_ret))
    st.write("Number of negative trade: " + str(neg_ret))

    neg_ind = (y < 0).astype(int)
    pos_ind = (y > 0).astype(int)

    gains = pos_ind*percentchange
    losses = neg_ind*percentchange

    ## Finding average gains
    avgGains = sum(gains)/pos_ret
    maxGains = max(gains)
    st.write("Average gains from trade: " + str(round(avgGains,2)) + "%")
    st.write("Max gains from trade: " + str(round(maxGains,2)) + "%")

    ## Finding average losses
    avgLosses = sum(losses)/neg_ret
    maxLosses = min(losses)
    st.write("Average losses from trade: " + str(round(avgLosses,2)) + "%")
    st.write("Max losses from trade: " + str(round(maxLosses,2)) + "%")

    # risk ratio
    Risk_ratio = (-avgGains/avgLosses)*100
    batting_avg = (pos_ret / (pos_ret + neg_ret))*100
    st.write("Gain/Loss Ratio from trade: " + str(round(Risk_ratio,2)) + "%")
    st.write("Batting Average from trade strategy: " + str(round(batting_avg,2)) + "%")

if option == "stock screener":
    st.subheader("this is the stock screener dashboard")
    yf.pdr_override()

    startyear = 2020
    startmonth = 1
    startdate = 1

    start = dt.datetime(startyear,startmonth, startdate)

    now = dt.datetime.now()

    filePath = r"C:\Users\Kevin Ganis\Documents\kevin personal doc\financial_Dashboard\RichardStocks.xlsx"
    stocklist = pd.read_excel(filePath)
    stocklist = stocklist.head()
    exportList = pd.DataFrame(columns = ["Stock","RS_Rating", "50 Day MA", "150 Day MA", "200 Day MA", "52 Week Low", "52 week High"])
    st.write("initial export list are as follows:")
    st.write(exportList)

    for i in stocklist.index :
        stock = str(stocklist["Symbol"][i])
        st.write(stock)
        RS_rating = stocklist["RS Rating"][i]
        try:
            df = pdr.get_data_yahoo(stock, start, now)
            st.write(df)
            smaUsed = [50,150, 200]

            for x in smaUsed:
                sma=x
                df["SMA_"+str(sma)]=round(df.iloc[:,4].rolling(window=sma).mean(),2)


            currentClose = df["Adj Close"][-1]
            moving_average_50 = df["SMA_50"][-1]
            moving_average_150 = df["SMA_150"][-1]
            moving_average_200 = df["SMA_200"][-1]
            low_of_52_week = min(df["Adj Close"][-260:])
            high_of_52_week = max(df["Adj Close"][-260:])

            try:
                moving_average_200_20past = df["SMA_200"][-20]
            except Exception:
                moving_average_200_20past = 0

            # condition 1 current price ? 150 SMA and > 200 SMA
            if(currentClose > moving_average_150 and currentClose > moving_average_200):
                cond_1 = True
            else:
                cond_1 = False

            # condition 2 150 SMA >200 SMA
            if( moving_average_150 > moving_average_200):
                cond_2 = True
            else:
                cond_2 = False


                # Condition 3 200 SMA trending up for at least 1 month (ideally 4-5 months)
            if( moving_average_200 > moving_average_200_20past):
                cond_3 = True
            else:
                cond_3 = False

            # Condition 4 50 SMA > 150 SMA and 50 SMA > 200 SMA
            if(moving_average_50 > moving_average_150 and moving_average_50 > moving_average_200):
                cond_4 = True
            else:
                cond_4 = False
            # condition 5 Current Price > 50 SMA
            if(currentClose > moving_average_50):
                cond_5 = True
            else:
                cond_5 = False

                # condition 6 Current price at least 30% above 52 week low ( Many of teh best are up 100 - )
            if(currentClose >= (1.3*low_of_52_week) ):
                cond_6 = True
            else:
                cond_6 = False
            # Condition 7 Current price is within 25% of 52 week high
            if(currentClose >= 0.75*high_of_52_week):
                cond_7 = True
            else:
                cond_7 = False
                # Condition 8 IBD RS rating > 70 and higher the better
            if(RS_rating > 70):
                cond_8 = True
            else:
                cond_8 = False


            ## DEBUG AROUND HERE REQUIRED
            st.write([cond_1, cond_2, cond_3, cond_4, cond_5, cond_6, cond_7, cond_8])
            st.write(cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6 and cond_7 and cond_8)
            row =  {'Stock': stock, "RS_Rating": RS_Rating, "50 Day MA": moving_average_50, "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200, "52 Week Low": low_of_52week, "52 week High": high_of_52week}
            st.write(row)

            if (cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6 and cond_7 and cond_8):
                row = {'Stock': stock, "RS_Rating": RS_Rating, "50 Day MA": moving_average_50, "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200, "52 Week Low": low_of_52week, "52 week High": high_of_52week}
                exportList = exportList.append(row, ignore_index=True)
            else:
                exportList = exportList

        except Exception:
            st.write("No data on " + stock)

    st.write("final export list are as follows: ")
    st.write(exportList)
    # write output exportlist into excel
    newFile=os.path.dirname(filePath)+"\ScreenOutput.xlsx"
    writer= pd.ExcelWriter(newFile)
    exportList.to_excel(writer,"Sheet1")
    #writer.save()

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
