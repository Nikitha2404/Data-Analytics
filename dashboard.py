from pyspark.sql import SparkSession
import streamlit as st

from FAnalysis import fundamental_analysis
from TAnalysis import technical_analysis
from init import load_model

PAGE_HOME = "Home"
PAGE_SECOND = "Fundamental Analysis"
PAGE_THIRD = "Technical Analysis"

pages = [
    PAGE_HOME,
    PAGE_SECOND,
    PAGE_THIRD
]

def main():
    selected_page = st.sidebar.selectbox("Select a Page", pages)
    if selected_page=="Home":
        st.write(load_model())
    elif selected_page=="Fundamental Analysis":
        fundamental_analysis()
    elif selected_page=="Technical Analysis":
        technical_analysis()

if __name__ == "__main__":
    main()