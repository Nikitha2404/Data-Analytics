import streamlit as st
import pyspark.sql.functions as Func
import yfinance as yf
import numpy as np
import datetime as dt

from init import load_model, load_pandas
from functions import execute_indicator

def technical_analysis():

    technical_indicators=['SMA','ATR','Fibonnaci Retracement','Stochastic','RSI','MACD','Bollinger bands','rate of change']

    st.title("Technical Analysis")
    model=load_model()
    df=load_pandas()
    company_list=df['Ticker']
    add_selectbox = st.sidebar.selectbox("Select Ticker",company_list)  
    select_indicator = st.sidebar.selectbox("Select Indicator",technical_indicators) 
    
    filter_cond=Func.col("Ticker")==add_selectbox
    filtered_rdd_row = model.filter(filter_cond).first()
    ticker = filtered_rdd_row['Ticker']
    st.subheader(filtered_rdd_row['Company Name'])
    
    #Getting the historical data for the ticker 
    tickerobj=yf.Ticker(ticker)
    data=tickerobj.history(period='1d',start='2022-1-1',end=dt.datetime.today())
    data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
    st.dataframe(data,column_order=['Date','Open','High','Low','Close','Log_Returns'])

    execute_indicator(select_indicator , data)
    

    