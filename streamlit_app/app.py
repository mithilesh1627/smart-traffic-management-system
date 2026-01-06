import streamlit as st
import pandas as pd
from pymongo import MongoClient
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
st.set_page_config(page_title="Smart Traffic Dashboard", layout="wide")
from utils.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["traffic_system"]
collection = db["metrics"]

data = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)

st.title(" Smart Traffic Management Dashboard")

if df.empty:
    st.warning("No data available")
else:
    st.metric("Avg Flow", round(df["flow"].mean(), 2))
    st.metric("Avg Density", round(df["density"].mean(), 2))

    st.line_chart(df.set_index("timestamp")[["flow", "density"]])
