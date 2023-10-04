import os
import smtplib, ssl
import imghdr
from email.message import EmailMessage

import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr


sender_email = os.environ.get('EMAIL_USER')
receiver_email = 'kevin.ganiswarna@hotmail.com'
password = os.environ.get('EMAIL_PASSWORD')
port = 587  # For starttls
smtp_server = "smtp.gmail.com"


msg = EmailMessage()
yf.pdr_override()

start = dt.datetime(2018,12,1)
now = dt.datetime.now()

stock = "QQQ"
TargetPrice = 180

msg["Subject"] = "Alert on " + stock
msg["From"] = sender_email
msg["To"] = receiver_email

alerted = False

while 1:
        df = pdr.get_data_yahoo(stock, start, now)
        currentClose = df["Adj Close"][-1]
        condition = currentClose > TargetPrice
        if (condition and alerted  == False ):
            alerted = True;
            message = stock + "Has Activated the alerted price of " + str(TargetPrice) +\
            "\nCurrent Price : " + str(currentClose)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)

                print("completed")
        else:
            print("no new alerts")
        time.sleep(60)
