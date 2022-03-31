import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from deta import Deta
import json
import requests

def unique(list1):
    x = np.array(list1)
    return np.unique(x)

log = alert = Deta("c0vidk60_8unssenvnHkuZmQfqhZ4jW49o5hRMvwG").Base('superhero_log')

res = log.fetch(query=None, limit=None, last=None)
unique_mbr = unique([x['mbr_id'] for x in res.items])
unique_endpoints = unique([x['endpoint'] for x in res.items])
unique_dates = unique([x['datetime'][0:10] for x in res.items])

if 'saved_mbr_num' not in st.session_state or  'saved_end_num' not in st.session_state or 'saved_req_num' not in st.session_state:
    st.session_state['saved_mbr_num'] = len(unique_mbr)
    st.session_state['saved_end_num'] = len(unique_endpoints)
    st.session_state['saved_req_num'] = len(res.items)

st.title('7 Day Superhero Dashboard')

st.header('Metrics')
col1, col2, col3, col4= st.columns(4)
col1.metric(label="Days", value=len(unique_dates))
col2.metric(label="Active Members", value=len(unique_mbr), delta = (len(unique_mbr)-st.session_state['save_mbr_num']))
col3.metric(label="Active Endpoints", value=len(unique_endpoints), delta = (len(unique_endpoints)-st.session_state['save_end_num']))
col4.metric(label="All Requests", value=len(res.items), delta = (len(res.items)-st.session_state['save_req_num']) )

st.session_state['saved_mbr_num'] = len(unique_mbr)
st.session_state['saved_end_num'] = len(unique_endpoints)
st.session_state['saved_req_num'] = len(res.items)
dd = {}
##Start
for row in unique_mbr :
    if row not in dd.keys():
        dd[row] = {}
    for y in unique_dates:
        dd[row][y] = 0

for z in res.items :
    dd[z['mbr_id']][z['datetime'][0:10]] = dd[z['mbr_id']][z['datetime'][0:10]] + 1
d_mbr = pd.DataFrame.from_dict(dd)
st.header('Daily usage by member')
st.dataframe(d_mbr)
st.bar_chart(d_mbr)

##Start
dd = {}
for row in unique_endpoints :
    if row not in dd.keys():
        dd[row] = {}
    for y in unique_dates:
        dd[row][y] = 0

for z in res.items :
    dd[z['endpoint']][z['datetime'][0:10]] = dd[z['endpoint']][z['datetime'][0:10]] + 1
d_endpoint = pd.DataFrame.from_dict(dd)
st.header('Daily usage by endpoint')
st.dataframe(d_endpoint)
st.bar_chart(d_endpoint)
