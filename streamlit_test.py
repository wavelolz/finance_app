
import time
import streamlit as st
# st.set_page_config(layout="wide")
import numpy as np
import pandas as pd
from FinMind.data import DataLoader
import ta
from ta.utils import dropna
import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import mplfinance as mpf
import plotly.graph_objects as go
import os
import json
import random
import plotly.express as px


import streamlit as st

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from s0050;', ttl=600)
