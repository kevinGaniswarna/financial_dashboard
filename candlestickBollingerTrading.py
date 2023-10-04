import os;
import pandas as pd;
import yfinance as yf;
import datetime as dt;
from pandas_datareader import data as pdr
import pandas as pd;
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np
from mpl_finance import candlestick_ohlc

yf.pdr_override # activate yahoo finance workaround

smasUsed= [10,30,50] # Choose SMAs

start = dt.datetime(2023,1,1)  - dt.timedelta(days = max(smasUsed)) # Sets start point of dataframe
now = dt.datetime.now() # sets initial end point of DataFrame
stock = input("Enter the stock symbol: ")  # Asks for new stock

while stock != "quit" :
    prices = pdr.get_data_yahoo(stock, start, now)

    fig, ax1 = plt.subplots() # create Plots
    # Calculate Moving averages

    for x in smasUsed: # this for loop calculate SMAs for the stated period and appends to DataFrame
        sma = x
        prices['SMA_' + str(sma)]= prices.iloc[:,4].rolling(window = sma).mean() #calculates sma and creates col

    # Calculate Bollinger bands
    BBperiod = 15
    stdev = 2
    prices["SMA" + str(BBperiod)] = prices.iloc[:,4].rolling(window = BBperiod).mean()
    prices["STDEV"] = prices.iloc[:,4].rolling(window = BBperiod).std()
    prices["LowerBand"]  = prices["SMA" + str(BBperiod)] - (stdev*prices['STDEV'])
    prices["UpperBand"]  = prices["SMA" + str(BBperiod)] + (stdev*prices['STDEV'])
    prices["Date"] = mdates.date2num(prices.index)

    # Calculate 10.4.4 Stochastics

    Period = 10
    K = 4
    D = 4
    prices["RolHigh"] = prices["High"].rolling(window= period).max()
    prices["RolLow"] = prices["Low"].rolling(window= period).min()
    prices["Stok"] = ((prices["Adj Close"] - prices["RolLow"])/(prices["RolHigh"] - prices["RolLow"])) * 100
    prices["K"] = prices["Stok"].rolling(window= K).mean()
    prices["D"] = prices["K"].rolling(window= D).mean()
    prices["GD"] = prices["High"]
    ohlc = []


# De;ete Extra dates
    prices = prices.iloc[max(smasUsed):]

    greenDotDate = [] # Stores dates of GreenDots
    greenDot = []  # stpres Values of Green dotSize
    lastK = 0 # Will store yesterday fast stoch
    lastD = 0 # Will store yesterday slow stoch
    lastLow = 0 # Will store yesterday lower
    lastClose = 0 # Will store yesterday close
    lastLowBB = 0 # Will store yesterday lower BBand

for i in prices.index:
    # append OHLC to make the candlestick_ohlc
    append_me = prices["Date"][i], prices["Open"][i], prices["High"][i], prices["Low"][i], prices["Adj Close"][i], prices["Volume"][i]
    ohlc.append(append_me)

    # Check for Green dot
    if prices["K"][i] > prices['D'][i] and lastK < lastD and lastK < 60:
        # make the marker of green dot
        plt.plot(prices["Date"][i], prices["High"][i] + 1, marker = "o", ms = 4, ls = "", color = "b") # plot blue dot
        greenDotDate.append(i) # store green dot dataExtent
        greenDot.append(prices["High"][i])

    # Check for lower Bollinger Band Volume
    if ((lastLow < lastLowBB) or (prices['Low'][i] < prices['LowerBand'][i])) and (prices["Adj Close"][i] > lastClose) and (prices["Adj Close"][i] > prices["LowerBand"][i]) and (lastK < 60):
        plt.plot(prices["Date"][i], prices["Low"][i]-1, marker = 'o', ms = 4, ls = "", color = 'b') # plot blue dot

    # store values
    lastK = prices['K'][i]
    lastD = prices['D'][i]
    lastLow = prices['Low'][i]
    lastClose = prices['Adj Close'][i]
    lastLowBB = prices["LowerBand"][i]

    # Plot Moving Averages and BBands

    for x in smasUsed: # This for loop calculates the EMAs for the stated periods and appends to datestamps
        sma = x
        prices['SMA_'+ str(sma)].plot(label = 'close')
    prices['UpperBand'].plot(label = 'close', color = 'lightgray')
    prices['LowerBand'].plot(label = 'close', color = 'lightgray')

    # olot candlesticks

    candlestick_ohlc(ax1, ohlc, width = .5, colorup = 'k', colordown = 'r', alpha = 0.75)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) # change x axis back to datestamps
    ax1.xaxis.set_major_locator(mticker.MaxNlocator(8)) # add more x axis labels
    plt.tick_params(axis = 'x', rotation = 45) #rotate dates for readability

    # Pivot points
    pivots = [] # Store Pivot Values
    dates = [] # Stpres Dates cprresponding to choose pivot Values
    counter = 0 # will keep track pf whether a certain value is a pivot
    lastPivot = 0 # will store the last Pivot values

    Range = [0,0,0,0,0,0,0,0,0,0] # Array used to iterate through stock prices
    dateRange = [0,0,0,0,0,0,0,0,0,0] # Array used to iterate through corresponding dates


    for i in df.index: # Iterates through the price history
        currentMax = max(Range, default = 0) # Determines the Maximum value of 10 item array
        # Identify a potential pivot points
        value = round(df["High"][i],2) # recieves next high value from dataframe
        Range = Range[1:9] # Cuts range array to only the most recent 9 values
        Range.append(value) # adds newest high value to array
        dateRange = dateRange[1:9] # Cuts date array to only the most recent 9 values
        dateRange.append(i) # Adds newest date to the array

        if currentMax == max(Range, default = 0): # If statement to check if the max stays the same
            counter += 1; # if yes add 1 to counter
        else:
            counter = 0 # otherwise new potential pivot to reset the counter
        if counter == 5: # check if we have identified a pivot
            lastPivot = currentMax # assign last pivot to current max value
            dateloc = Range.index(lastPivot) # finds index of the range array that is that pivot value
            lastDate = dateRange[dateloc] # Gets date corresponding to the index
            pivots.append(lastPivot) # Adds pivot to pivot array
            dates.append(lastDate) # Adds pivot date to date array
        print()

        timeD = dt.timedelta(days = 30) # Sets length of dotted line on chart

        for index in range(len(pivots)) : # iterate through pivot array
            plt.plot_date([dates[index] - (timeD*0.075), dates[index]+timeD], # plots the horizontal line of the pivot value
                         [pivots[index], pivots[index]], linestyle = "--", linewidth = 1, marker = ',')
            plt.annotate(str(pivot[index]), (mdates.date2num(dates[index]), pivots[index]), xytext = (-10, 7),
                    textcoords = 'offset points', fontsize = 7, arrowprops = dict(arrowstyle = '-|>'))

        plt.xLabel('Date')
        plt.yLabel('Price')
        plt.title(Stock + " - Daily")
        plt.ylim(prices["Low"].min(), prices["High"].max()*1.05) # add margins


        plt.show()

        stock = input("Enter the stock symbol: ")  # Asks for new stock
