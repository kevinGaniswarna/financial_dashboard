## ACTIVATE VIRTUAL ENVIRONMENT

## Run in CMD
## .\myvenv\Scripts\activate

## Run in CMD
## deactivate


import streamlit as st
import os
import pandas as pd
import yfinance as yf
import datetime
import plotly.graph_objects as go
from pandas_datareader
import data as wb
import wbdata as wbank
import requests

st.title("Title")


st.header("Header")
st.subheader("Subheader")
st.writer("text")



## Require Application and requirement from BMEX
# def BMEX(BMXCODE, DateInit, DateFin, token):
#     url = "XXXX"
#     headers = {'BMX-Token':token}
#     response = requests.get(url, headers = headers)
#     status = response.status_code
#     data0 = response.json()
#     df = pd.dataFrame(data0)
#     return df

#
# Today = datetime.date.today()
# Start2023 = datetime.date(2023,1,1)
# diff = Start2023 - today
#
# Start = '2008-01-01'
# SStart2023 = str(Start2023)
# TToday = str(Today)
#
#
# ## SOURCE FROM YAHOO FINANCE
# VIX = wb.DataReader('^VIX', data_source = 'yahoo', start = Start)
# VIX['Returns'] = VIX['Close'].pct_change()
#
# SNP_IDX = wb.DataReader('^GSPC', data_source = 'yahoo', start = Start)
# SNP_IDX['Returns'] = SNP_IDX['Close'].pct_change()
#
# IPC_MX = wb.DataReader('^MXX', data_source = 'yahoo', start = Start)
# IPC_MX['Returns'] = IPC_MX['Close'].pct_change()
#
#
# ## Title for
#
# st.title('Economics Indicator Tracking')
#
# option = st.sidebar.selectbox("Select a Dashboard:", ('KEI', 'ITA', 'OA'),0)
#
# if option == 'KEI':
#     st.header('Key Economic Indicators')
#     st.writer('This Dashboard screens Key Economic Indicators')
#     Indicator_1 = st.selectbox("Select an Indicator:", ("VIX", "S&P Index", "IPC"), 0)
#
#     if indicator_1 == "VIX":
#         fig1 = go.figure()
#         fig1.add_trace(go.Scatter(x = VIX.index, y=VIX["Close"],
#                     mode= 'lines',
#                     name= 'VIX'))
#         fig1.update_xaxes(type = 'category')
#         fig1.update_layout(height = 600, width = 400)
#         st.plotly_chart(fig1, use_container_width = True)
#
#         st.dataframe(VIX)
#         st.write("Source: Yahoo Finance")
#
#
#     if indicator_1 == "VIX":
#         fig1 = go.figure()
#         fig1.add_trace(go.Scatter(x = VIX.index, y=VIX["Close"],
#                     mode= 'lines',
#                     name= 'VIX'))
#         fig1.update_xaxes(type = 'category')
#         fig1.update_layout(height = 600, width = 400)
#         st.plotly_chart(fig1, use_container_width = True)
#
#         st.dataframe(VIX)
#         st.write("Source: Yahoo Finance")
#
#     if indicator_1 == "S&P Index":
#         fig1 = go.figure()
#         fig1.add_trace(go.Scatter(x = SNP_IDX.index, y=SNP_IDX["Close"],
#                     mode= 'lines',
#                     name= 'SNP_IDX'))
#         fig1.update_xaxes(type = 'category')
#         fig1.update_layout(height = 600, width = 400)
#         st.plotly_chart(fig1, use_container_width = True)
#
#         st.dataframe(SNP_IDX)
#         st.write("Source: Yahoo Finance")
#
#
#     if indicator_1 == "IPC":
#         fig1 = go.figure()
#         fig1.add_trace(go.Scatter(x = IPC_MX.index, y=IPC_MX["Close"],
#                     mode= 'lines',
#                     name= 'IPC_MX'))
#         fig1.update_xaxes(type = 'category')
#         fig1.update_layout(height = 600, width = 400)
#         st.plotly_chart(fig1, use_container_width = True)
#
#         st.dataframe(IPC_MX)
#         st.write("Source: Yahoo Finance")
