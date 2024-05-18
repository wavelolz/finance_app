import pandas as pd
import numpy as np
from google.cloud import firestore
import json
from datetime import datetime
import os
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go


db = firestore.Client.from_service_account_json("testing.json")

def upload_to_firestore(data, doc_id):
    doc_ref = db.collection('test').document(doc_id)
    doc_ref.set({'data': data})

def delete_document(collection_name, doc_id):
    doc_ref = db.collection(collection_name).document(doc_id)
    doc_ref.delete()

def FetchDatasetList(collection_name):
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()
    stock_ids = []
    for doc in docs:
        stock_ids.append(doc.id)
    return stock_ids

def FetchData(collection_name, stock_id):
    doc_ref = db.collection(collection_name).document(stock_id)
    doc = doc_ref.get()
    data = doc.to_dict()["data"]
    df = pd.DataFrame(data)
    return df

def CleanData(data):
    filter_data = data.loc[data["close"] != 0]
    return filter_data

def PrepareData(data):
    candle = data[["date", "Trading_Volume", "open", "close", "max", "min"]]
    candle.columns = ["date", "volume", "open", "close", "high", "low"]
    return candle

def ExtractMarketCloseDate(data):
    date_l = data["date"].to_list()
    start_date = datetime.strptime(date_l[0], "%Y-%m-%d")
    end_date = datetime.strptime(date_l[-1], "%Y-%m-%d")
    diff = (end_date-start_date).days
    all_days = [str(start_date+timedelta(days=i)).split(" ")[0] for i in range(diff)]
    close_days = sorted(set(all_days)-set(date_l))
    return close_days


def FilterDate(candle_data, code):
    if code == 0:
        filter_candle_data = candle_data[-30:]
    elif code == 1:
        filter_candle_data = candle_data[-90:]
    elif code == 2:
        filter_candle_data = candle_data[-150:]
    elif code == 3:
        filter_candle_data = candle_data[-365:]
    elif code == 4:
        filter_candle_data = candle_data[-1825:]
    else:
        return candle_data
    return filter_candle_data

tab_graph, tab_dollar_cost_averaging, tab_random_strategy = st.tabs(["個股走勢", "定期定額實驗", "隨機選股實驗"])

with tab_graph:
    stock_id_l = FetchDatasetList()

    option = st.selectbox(
        "Stock List",
        stock_id_l
    )

    data = FetchData(option)
    data = CleanData(data)
    candle_data_all = PrepareData(data)
    close_days = ExtractMarketCloseDate(candle_data_all)
    

    
    genre_duration = st.radio(
        "請選擇繪圖日期長度",
        ["1月", "3月", "5月", "1年", "5年", "全部時間"],
        horizontal=True
        )

    if genre_duration == '1月':
        candle_data_part = FilterDate(candle_data_all, 0)
    elif genre_duration == '3月':
        candle_data_part = FilterDate(candle_data_all, 1)
    elif genre_duration == '5月':
        candle_data_part = FilterDate(candle_data_all, 2)
    elif genre_duration == '1年':
        candle_data_part = FilterDate(candle_data_all, 3)
    elif genre_duration == '5年':
        candle_data_part = FilterDate(candle_data_all, 4)
    else:
        candle_data_part = FilterDate(candle_data_all, 5)


    candle = go.Candlestick(
        x=candle_data_part["date"], 
        open=candle_data_part["open"], 
        high=candle_data_part["high"], 
        low=candle_data_part["low"], 
        close=candle_data_part["close"]
        )

    fig = go.Figure(data=candle)
    fig.update_xaxes(rangebreaks=[dict(values=close_days)])
    st.plotly_chart(fig, use_container_width=True)
