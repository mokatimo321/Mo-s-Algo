# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 21:05:08 2022

@author: mohit
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime


#"""input_df = pd.read_csv(uploaded_file)      
    #fig = go.Figure(data=[go.Candlestick(x=input_df['date'],
                #open=input_df['open'],
                #high=input_df['high'],
                #low=input_df['low'],
                #close=input_df['close'])])
    
    #st.plotly_chart(fig)"""


st.write("""
# MO's ALGO -- Made by Mohit
""")


st.header('UPLOAD HERE!!!')

uploaded_file = st.file_uploader("UPLOAD THE BANK NIFTY OR NIFTY DATA FILE", type=["csv"])
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    if(st.button('Show Chart!!')):
        fig = go.Figure(data=[go.Candlestick(x=df['date'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])
        st.plotly_chart(fig)
        st.subheader("Stop Showing Chart")
        if(st.button('Stop Showing Chart!!')):
            st.button('Show Chart!!', disabled=True)

    option = st.selectbox(
     'Which Strategy would you like to use??',
     ('RSI BUY && RSI SELL', 'RSI BUY && CMO SELL', 'RSI & VWAP BUY && RSI SELL', 'RSI & VWAP BUY && CMO SELL'))
    
    just_rsi = False
    rsi_and_cmo = False
    rsi_and_vwap = False
    rsi_cmo_vwap = False

    if(option == "RSI BUY && RSI SELL"):
        just_rsi = True
    elif(option == "RSI BUY && CMO SELL"):
        rsi_and_cmo = True
    elif(option == "RSI & VWAP BUY && RSI SELL"):
        rsi_and_vwap = True
    else:
        rsi_cmo_vwap = True


    st.subheader("Choose the Value of RSI for Buying")
    rsi_buy = st.slider('RSI (0 to 100)', 0, 100, 30)

    if(just_rsi or rsi_and_vwap):
        st.subheader("Choose the Value of RSI for Selling")
        rsi_sell = st.slider('RSI (0 to 100)', 0, 100, 60)

    if(rsi_and_cmo or rsi_cmo_vwap):
        st.subheader("Choose the Value of CMO for Selling")
        cmo = st.slider('CMO (-1000 to 100)', -100, 100, 50)
          
    
    rsi_list = []
    cmo_list = []
    green_cond = []
    close = []
    date = []
    vwap_cond = []

    index_name = ""
    strike_type = ""
    lot = 0
    strike_name = ""


    for i in df['strike']:
        strike_name = str(i)
        break
    for i in df['instrument_type']:
        strike_type = str(i)
        break
    for i in df['name']:
        index_name = str(i)
    for i in df['lot_size']:
        lot = int(i)
        break

    for i in df['rsi']:
        rsi_list.append(i)
    for i in df['CMO']:
        cmo_list.append(i)
    for i in df['greencandle']:
        green_cond.append(i)
    for i in df['close']:
        close.append(i)
    for i in df['date']:
        date.append(i[11:19])
    for i in df['price_vs_vwap']:
        vwap_cond.append(i)

    buy_flag = 0
    buy_price = 0
    net = 0
    cnt = 0
    max_fund = 0
    rsi_cond = False
    Total = 0

    max_profit = 0
    max_loss = 0
    total_fund = 0

    #375 for 1min, 188 for 2 min, 126 for 3 min, 76 for 5 min, 38 for 10 min, 26 for 15 min, 13 for 30 
    cutoff_time = 0
    time_frame = 0

    rsi_cond = False

    if(len(rsi_list) == 375):
        cutoff_time = 365
        time_frame = 1
    elif(len(rsi_list) == 188):
        cutoff_time = 182
        time_frame = 2
    elif(len(rsi_list) == 126):
        cutoff_time = 121
        time_frame = 3
    elif(len(rsi_list) == 76):
        cutoff_time = 73
        time_frame = 5
    elif(len(rsi_list) == 38):
        cutoff_time = 36
        time_frame = 10
    elif(len(rsi_list) == 26):
        cutoff_time = 24
        time_frame = 15
    elif(len(rsi_list) == 13):
        cutoff_time = 12
        time_frame = 30

    if st.button('START TRADING!!'):

        st.title(index_name + "  " + strike_name + "  " + strike_type + " -- " + str(time_frame) + " minutes")

        st.header("DETAILS OF ALL TRADES")

        for i in range(len(rsi_list)):
            if(rsi_list[i] <= rsi_buy):
                rsi_cond = True
            if(just_rsi == True and i > 0 and i < cutoff_time and buy_flag == 0 and rsi_cond == True and green_cond[i] == True):
                buy_price = close[i]
                buy_flag = 1
                max_fund = max(max_fund, buy_price)
                total_fund += buy_price*lot
                st.write(str(date[i]) + " -> " + "Buy at " + str(buy_price))
            elif(rsi_and_cmo == True and i > 0 and i < cutoff_time and buy_flag == 0 and rsi_cond == True and green_cond[i] == True):
                buy_price = close[i]
                buy_flag = 1
                max_fund = max(max_fund, buy_price)
                total_fund += buy_price*lot
                st.write(str(date[i]) + " -> " + "Buy at " + str(buy_price))
            elif(rsi_cmo_vwap == True and i > 0 and i < cutoff_time and buy_flag == 0 and rsi_cond == True and green_cond[i] == True and vwap_cond[i] == True):
                buy_price = close[i]
                buy_flag = 1
                max_fund = max(max_fund, buy_price)
                total_fund += buy_price*lot
                st.write(str(date[i]) + " -> " + "Buy at " + str(buy_price))
            elif(rsi_and_vwap == True and i > 0 and i < cutoff_time and buy_flag == 0 and rsi_cond == True and green_cond[i] == True and vwap_cond[i] == True):
                buy_price = close[i]
                buy_flag = 1
                max_fund = max(max_fund, buy_price)
                total_fund += buy_price*lot
                st.write(str(date[i]) + " -> " + "Buy at " + str(buy_price))
            if(just_rsi == True and buy_flag == 1 and rsi_list[i] >= rsi_sell):
                cnt += 1
                net += close[i] - buy_price
                buy_flag = 0
                rsi_cond = False
                st.write(str(date[i]) + " -> " + "Sell at " + str(close[i]))
            elif(rsi_and_cmo == True and buy_flag == 1 and cmo_list[i] >= cmo):
                cnt += 1
                net += close[i] - buy_price
                buy_flag = 0
                rsi_cond = False
                st.write(str(date[i]) + " -> " + "Sell at " + str(close[i]))
            elif(rsi_and_vwap == True and buy_flag == 1 and rsi_list[i] >= rsi_sell):
                cnt += 1
                net += close[i] - buy_price
                buy_flag = 0
                rsi_cond = False
                st.write(str(date[i]) + " -> " + "Sell at " + str(close[i]))
            elif(rsi_cmo_vwap == True and buy_flag == 1 and cmo_list[i] >= cmo):
                cnt += 1
                net += close[i] - buy_price
                buy_flag = 0
                rsi_cond = False
                st.write(str(date[i]) + " -> " + "Sell at " + str(close[i]))
            if(buy_flag == 1 and i == cutoff_time):
                cnt += 1
                net += close[i] - buy_price
                buy_flag = 0
                st.write(str(date[i]) + " -> " + "Sell at " + str(close[i]) + " -- Sold bcoz of CutOff Time")

        max_profit = max(max_profit, net*lot - cnt*65)
        max_loss = min(max_loss, net*lot - cnt*65)
        Total += net*lot - cnt*65
        st.subheader("Total Trade Done is : " + str(cnt))
        if(cnt > 0):
            st.subheader("Net Profit : " + str(net*lot - cnt*65))
            st.subheader("Max Fund Required : " + str(max_fund*lot))
            st.subheader("Total Fund Required : " + str(total_fund))

    else:

        st.header("Thank You!!")


st.caption("Mo's ALGO Pvt. Ltd.")