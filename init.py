from pyspark.sql import SparkSession
import streamlit as st
import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from pyspark.ml.feature import Imputer
import pandas_datareader as pdr
import datetime as dt
 
@st.cache_resource
def load_model():
    spark=SparkSession.builder.appName('StockDetails').getOrCreate()
    model=spark.read.option('header','true').csv('stock_data.csv',inferSchema=True)
    return model

@st.cache_resource
def load_pandas():
    df=pd.read_csv('stock_data.csv')
    return df

@st.cache_data
def load_news(ticker):
    fin_url='https://finviz.com/quote.ashx?t='+ticker+"&p=d"
    req=Request(fin_url,headers={'user-agent':'my-app'})
    response=urlopen(req)
    html=BeautifulSoup(response, 'html')
    news_table=html.find(id="news-table")
    parsed_data=[]
    for row in news_table.findAll('tr'):
        title=row.a.text
        date_time=row.td.text.replace('\r','').replace('\n','').strip().split(' ')

        if(len(date_time)==1):
            time=date_time[0]
        else:
            date = date_time[0]
    
        parsed_data.append([date,title])
    return parsed_data



