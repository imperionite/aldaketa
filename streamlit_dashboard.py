import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# Load latest data
df = pd.read_csv("cleaned_iot_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

st.title("📊 Smart Water Quality Monitoring Dashboard")

# Sidebar filter
sensor_type = st.sidebar.multiselect(
    "Select Sensor Type", df["data_type"].unique(), default=df["data_type"].unique()
)

filtered_df = df[df["data_type"].isin(sensor_type)]

# Latest timestamp
latest = filtered_df["timestamp"].max()
st.markdown(f"⏱️ **Latest Data Timestamp:** `{latest}`")

# Show summary metrics
st.metric("Total Records", len(filtered_df))
st.metric("Unique Sensors", filtered_df["sensor_id"].nunique())

# Line chart
st.subheader("📈 Sensor Values Over Time")
for sensor in sensor_type:
    data = filtered_df[filtered_df["data_type"] == sensor]
    st.line_chart(data.set_index("timestamp")["numeric_value"], height=300)


# Raw data
with st.expander("🧾 Show Raw Data"):
    st.dataframe(filtered_df)
