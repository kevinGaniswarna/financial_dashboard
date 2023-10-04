
import pandas as pd;
import yfinance as yf;
import datetime as dt;
import pandas as pd;
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

yf.pdr_override()
start = dt.datetime(2022,6,1)
now = dt.datetime.now()

stock = input("Enter the stock symbol : ")
#
while stock != "quit":
    df = pdr.get_data_yahoo(stock, start, now)
    df["High"].plot(label = "high")

    pivots = []; # list of pivot prices
    dates = []; # list of pivot dates
    counter = 0; # number of pivots occured
    lastPivot = 0 # last observed pivot prices


    Range = [0,0,0,0,0,0,0,0,0,0]
    dateRange = [0,0,0,0,0,0,0,0,0,0]

    for i in df.index:
        currentMax = max(Range, default = 0)
        value = round(df["High"][i],2)
        Range = Range[1:9]
        Range.append(value)
        dateRange = dateRange[1:9]
        dateRange.append(i)

        if currentMax == max(Range, default = 0):
            counter += 1;
        else:
            counter = 0
        if counter == 5:
            lastPivot = currentMax
            dateloc = Range.index(lastPivot)
            lastDate = dateRange[dateloc]
            pivots.append(lastPivot)
            dates.append(lastDate)

    print()



    # print(str(pivots))
    # print(str(dates))
    timeD = dt.timedelta(days = 30)
    for index in range(len(pivots)):
        print(str(pivots[index]) + ": " + str(dates[index]))
        plt.plot_date([dates[index], dates[index] + timeD],
                      [pivots[index],pivots[index]], linestyle = "-"
                      , linewidth = 2, marker="none" )




    plt.show()

    stock = input("Enter the stock Symbol : ")
