# =====================================================
# FUTURISTIC BAG FILTER PERFORMANCE MONITORING SYSTEM
# FIXED: Airflow calculator persistence (V1–V5)
# =====================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Bag Filter Performance Monitoring System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>
.stApp {background-color:#050816; color:white;}
section[data-testid="stSidebar"] {background-color:#0b1120;}
h1,h2,h3 {color:#00F5FF !important;}
.metric-card {
    background-color:#111827;
    padding:20px;
    border-radius:15px;
    border:1px solid #00F5FF;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ MACHINE PANEL")

machine = st.sidebar.selectbox(
    "Select Machine",
    ["Machine 1", "Machine 2", "Machine 3", "Machine 4"]
)

# =====================================================
# FILE
# =====================================================

os.makedirs("data", exist_ok=True)
DATA_FILE = f"data/{machine.replace(' ','_')}.xlsx"

# =====================================================
# REQUIRED COLUMNS (UPDATED)
# =====================================================

required_columns = [
    "Date",
    "Pressure (KPA)",
    "Temperature (°C)",
    "Air Flow Rate (CFM)",
    "Compressed Air Pressure (MPa)",
    "Chimney Condition",
    "Discharge Hopper Condition",
    "Motor Ampere (A)",
    "Operator Signature",
    "Supervisor Signature",
    "V1",
    "V2",
    "V3",
    "V4",
    "V5"
]

# =====================================================
# LOAD DATA
# =====================================================

if os.path.exists(DATA_FILE):
    df = pd.read_excel(DATA_FILE)
else:
    df = pd.DataFrame(columns=required_columns)
    df.to_excel(DATA_FILE, index=False)

# ensure columns exist
for col in required_columns:
    if col not in df.columns:
        df[col] = ""

df = df[required_columns]

# fix datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# numeric fix
num_cols = [
    "Pressure (KPA)",
    "Temperature (°C)",
    "Air Flow Rate (CFM)",
    "Compressed Air Pressure (MPa)",
    "Motor Ampere (A)",
    "V1","V2","V3","V4","V5"
]

for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# =====================================================
# TITLE
# =====================================================

st.title("BAG FILTER PERFORMANCE MONITORING SYSTEM")

# =====================================================
# DATE SELECT
# =====================================================

temp_date = st.date_input("Select Date To Edit/View", value=date.today())

existing_row = df[df["Date"].dt.date == temp_date]

if not existing_row.empty:
    existing_data = existing_row.iloc[0].to_dict()
else:
    existing_data = {
        "Pressure (KPA)": 0.0,
        "Temperature (°C)": 0.0,
        "Air Flow Rate (CFM)": 0.0,
        "Compressed Air Pressure (MPa)": 0.0,
        "Motor Ampere (A)": 0.0,
        "Chimney Condition": "",
        "Discharge Hopper Condition": "",
        "Operator Signature": "",
        "Supervisor Signature": "",
        "V1": 0.0,
        "V2": 0.0,
        "V3": 0.0,
        "V4": 0.0,
        "V5": 0.0,
    }

# =====================================================
# FORM
# =====================================================

with st.form("form"):

    input_date = st.date_input("Date", value=temp_date)

    pressure = st.number_input(
        "Pressure (KPA)",
        value=float(existing_data["Pressure (KPA)"])
    )

    temperature = st.number_input(
        "Temperature (°C)",
        value=float(existing_data["Temperature (°C)"])
    )

    compressed_air = st.number_input(
        "Compressed Air Pressure (MPa)",
        value=float(existing_data["Compressed Air Pressure (MPa)"])
    )

    motor_ampere = st.number_input(
        "Motor Ampere (A)",
        value=float(existing_data["Motor Ampere (A)"])
    )

    st.markdown("### 🌪️ Air Flow Calculator")

    v1 = st.number_input("V1", value=float(existing_data["V1"]))
    v2 = st.number_input("V2", value=float(existing_data["V2"]))
    v3 = st.number_input("V3", value=float(existing_data["V3"]))
    v4 = st.number_input("V4", value=float(existing_data["V4"]))
    v5 = st.number_input("V5", value=float(existing_data["V5"]))

    V = (v1 + v2 + v3 + v4 + v5) / 5

    circumference = 0.81
    import math
    D = circumference / math.pi
    A = (math.pi * D * D) / 4
    Q = (A * V * 3600) * 0.5886

    airflow = Q

    st.success(f"Calculated Air Flow Rate (CFM): {airflow:.2f}")

    chimney = st.text_input("Chimney Condition", value=str(existing_data["Chimney Condition"]))
    hopper = st.text_input("Hopper Condition", value=str(existing_data["Discharge Hopper Condition"]))
    operator_signature = st.text_input("Operator Signature", value=str(existing_data["Operator Signature"]))
    supervisor_signature = st.text_input("Supervisor Signature", value=str(existing_data["Supervisor Signature"]))

    submit = st.form_submit_button("💾 SAVE DATA")

# =====================================================
# SAVE
# =====================================================

if submit:

    df["Date"] = pd.to_datetime(df["Date"]).dt.date

    df = df[~(df["Date"] == input_date)]

    new_data = pd.DataFrame({
        "Date": [input_date],
        "Pressure (KPA)": [pressure],
        "Temperature (°C)": [temperature],
        "Air Flow Rate (CFM)": [airflow],
        "Compressed Air Pressure (MPa)": [compressed_air],
        "Chimney Condition": [chimney],
        "Discharge Hopper Condition": [hopper],
        "Motor Ampere (A)": [motor_ampere],
        "Operator Signature": [operator_signature],
        "Supervisor Signature": [supervisor_signature],
        "V1": [v1],
        "V2": [v2],
        "V3": [v3],
        "V4": [v4],
        "V5": [v5],
    })

    df = pd.concat([df, new_data], ignore_index=True)

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    df = df[required_columns]

    df.to_excel(DATA_FILE, index=False)

    st.success("✅ Data Saved Successfully")
