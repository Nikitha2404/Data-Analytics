import streamlit as st
import pyspark.sql.functions as Func
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

from init import load_model,load_pandas,load_news

def fundamental_analysis():
    st.header("Fundamental Analysis")
    model=load_model()
    df=load_pandas()
    company_list=df['Ticker']
    add_selectbox = st.sidebar.selectbox("Select Ticker",company_list)   
    
    filter_cond=Func.col("Ticker")==add_selectbox
    filtered_rdd_row = model.filter(filter_cond).first()
    ticker = filtered_rdd_row['Ticker']
    st.subheader(filtered_rdd_row['Company Name'])

    st.write('TOP NEWS')
    news_df=load_news(ticker)
    column_headings=["DATE","NEWS"]
    df=pd.DataFrame(news_df,columns=column_headings)

    vader=SentimentIntensityAnalyzer()
    f=lambda title:vader.polarity_scores(title)['pos']
    df['pos']=df['NEWS'].apply(f)
    f=lambda title:vader.polarity_scores(title)['neg']
    df['neg']=df['NEWS'].apply(f)
    f=lambda title:vader.polarity_scores(title)['compound']
    df['compound']=df['NEWS'].apply(f)

    mean_compound=df['compound'].mean()
    formatted_mean_compound = round(mean_compound * 100, 2)
    st.write("Overall score {:.2f}%".format(formatted_mean_compound))

    median_pos = df[df['pos'] > 0]['pos'].median()
    median_neg = df[df['neg'] > 0]['neg'].median()
    median_compound = df[df['compound'] != 0]['compound'].median()

    df['pos'] = df['pos'].replace(0, median_pos)
    df['neg'] = df['neg'].replace(0, median_neg)
    df['compound'] = df['compound'].replace(0,median_compound)

    st.data_editor(df,hide_index=True,column_config={
        "pos":st.column_config.BarChartColumn(width=40,y_min=0.00,y_max=1.00),
        "neg":st.column_config.BarChartColumn(width=40,y_min=0.00,y_max=1.00),
        "compound":st.column_config.BarChartColumn(width=40,y_min=-1.00,y_max=1.00),
    })

    st.bar_chart(df[['pos','neg','compound']],use_container_width=True)

    