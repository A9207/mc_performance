# =====================================================
# FUTURISTIC BAG FILTER PERFORMANCE MONITORING SYSTEM
# Python 3.13 + Streamlit
# =====================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import os
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.sidebar.markdown("---")
st.sidebar.subheader("🔒 Data Entry Login")

if not st.session_state.authenticated:

    password = st.sidebar.text_input(
        "Password",
        type="password"
    )

    if st.sidebar.button("Login"):

        if password == "PIC123":
            st.session_state.authenticated = True
            st.sidebar.success("Login Successful")

        else:
            st.sidebar.error("Wrong Password")

else:

    st.sidebar.success("Logged in as PIC")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
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
# CSS THEME
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color:#050816;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color:#0b1120;
    border-right:1px solid #00F5FF;
}

h1,h2,h3 {
    color:#00F5FF !important;
    text-shadow:0px 0px 10px #00F5FF;
}

.stNumberInput input,
.stDateInput input,
.stTextInput input {
    background-color:#111827 !important;
    color:white !important;
}

.stButton>button {
    background:linear-gradient(90deg,#00F5FF,#0066FF);
    color:black;
    border:none;
    border-radius:10px;
    font-weight:bold;
}

.metric-card {
    background-color:#111827;
    padding:20px;
    border-radius:15px;
    border:1px solid #00F5FF;
    box-shadow:0px 0px 15px rgba(0,245,255,0.3);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ MACHINE PANEL")

machine = st.sidebar.selectbox(
    "Select Machine",
    [f"Machine {i}" for i in range(1, 10)]
)

# =====================================================
# FILE SETUP
# =====================================================

os.makedirs("data", exist_ok=True)

DATA_FILE = f"data/{machine.replace(' ','_')}.xlsx"

# =====================================================
# REQUIRED COLUMNS
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
    "Any Abnormality",
    "Operator Signature",
    "Supervisor Signature"
]

# =====================================================
# LOAD DATA
# =====================================================

if os.path.exists(DATA_FILE):

    df = pd.read_excel(DATA_FILE)

    # Add missing columns
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

    # Force column order
    df = df[required_columns]

else:

    df = pd.DataFrame(columns=required_columns)

    df.to_excel(DATA_FILE, index=False)

# =====================================================
# FIX DATE TYPE
# =====================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

# =====================================================
# DATA TYPE FIX
# =====================================================

numeric_columns = [
    "Pressure (KPA)",
    "Temperature (°C)",
    "Air Flow Rate (CFM)",
    "Compressed Air Pressure (MPa)",
    "Motor Ampere (A)"
]

for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    ).fillna(0)

# =====================================================
# TITLE
# =====================================================

st.title(" BAG FILTER PERFORMANCE MONITORING SYSTEM")

st.markdown(f"""
<div class="metric-card">
<h2>{machine}</h2>
<p>Daily Monitoring Dashboard</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# LOAD EXISTING DATA FOR SELECTED DATE
# =====================================================
if st.session_state.authenticated:
st.subheader("📥 DAILY DATA ENTRY")

existing_data = {}

temp_date = st.date_input(
    "Select Date To Edit/View",
    value=date.today(),
    key="top_date_selector"
)

existing_row = df[
    df["Date"].dt.date == temp_date
]

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
        "Any Abnormality": "",
        "Operator Signature": "",
        "Supervisor Signature": ""
    }

# =====================================================
# INPUT FORM
# =====================================================

with st.form("form"):

    col1, col2 = st.columns(2)

    # =================================================
    # LEFT COLUMN
    # =================================================

    with col1:

        input_date = st.date_input(
            "Date",
            value=temp_date
        )

        pressure = st.number_input(
            "Pressure (KPA)",
            min_value=0.0,
            value=float(existing_data["Pressure (KPA)"]),
            step=0.1,
            format="%.2f"
        )

    # =================================================
    # RIGHT COLUMN
    # =================================================

    with col2:

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            value=float(existing_data["Temperature (°C)"]),
            step=0.1,
            format="%.2f"
        )

        compressed_air = st.number_input(
            "Compressed Air Pressure (MPa)",
            min_value=0.0,
            value=float(existing_data["Compressed Air Pressure (MPa)"]),
            step=0.01,
            format="%.2f"
        )

        motor_ampere = st.number_input(
            "Motor Ampere (A)",
            min_value=0.0,
            value=float(existing_data["Motor Ampere (A)"]),
            step=0.1,
            format="%.2f"
        )

        st.markdown("### 🌪️ Air Flow Calculator")

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            v1 = st.number_input(
                "V1",
                min_value=0.0,
                step=0.1,
                format="%.2f"
            )

        with c2:
            v2 = st.number_input(
                "V2",
                min_value=0.0,
                step=0.1,
                format="%.2f"
            )

        with c3:
            v3 = st.number_input(
                "V3",
                min_value=0.0,
                step=0.1,
                format="%.2f"
            )

        with c4:
            v4 = st.number_input(
                "V4",
                min_value=0.0,
                step=0.1,
                format="%.2f"
            )

        with c5:
            v5 = st.number_input(
                "V5",
                min_value=0.0,
                step=0.1,
                format="%.2f"
            )

        # =================================================
        # AIR FLOW CALCULATION
        # =================================================

        V = (v1 + v2 + v3 + v4 + v5) / 5

        circumference = 0.81

        D = circumference / 3.142

        A = (3.142 * D * D) / 4

        Q = (A * V * 3600) * 0.5886

        airflow = Q

        st.success(
            f"Calculated Air Flow Rate (CFM): {airflow:.2f}"
        )

    # =================================================
    # EXTRA INPUTS
    # =================================================

    chimney = st.text_input(
        "Chimney Condition (OK / NOT OK)",
        value=str(existing_data["Chimney Condition"])
    )

    hopper = st.text_input(
        "Discharge Hopper Condition (OK / NOT OK)",
        value=str(existing_data["Discharge Hopper Condition"])
    )

    abnormality = st.text_input(
    "Any Abnormality",
    value=str(existing_data["Any Abnormality"]),
    placeholder="Describe any abnormal condition observed..."
    )
    operator_signature = st.text_input(
        "Operator Signature",
        value=str(existing_data["Operator Signature"])
    )

    supervisor_signature = st.text_input(
        "Supervisor Signature",
        value=str(existing_data["Supervisor Signature"])
    )

    submit = st.form_submit_button(
        "💾 SAVE DATA"
    )
    

# =====================================================
# SAVE DATA
# =====================================================

if submit:

    df["Date"] = pd.to_datetime(df["Date"]).dt.date

    # Remove same date entry
    df = df[~(df["Date"] == input_date)]

    # New Data
    new_data = pd.DataFrame({

        "Date": [input_date],
        "Pressure (KPA)": [pressure],
        "Temperature (°C)": [temperature],
        "Air Flow Rate (CFM)": [airflow],
        "Compressed Air Pressure (MPa)": [compressed_air],
        "Chimney Condition": [chimney],
        "Discharge Hopper Condition": [hopper],
        "Motor Ampere (A)": [motor_ampere],
        "Any Abnormality": [abnormality],
        "Operator Signature": [operator_signature],
        "Supervisor Signature": [supervisor_signature]

    })

    # Add Data
    df = pd.concat(
        [df, new_data],
        ignore_index=True
    )

    # Sort
    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values(
        by="Date",
        ascending=True
    ).reset_index(drop=True)

    # Force column order
    df = df[required_columns]

    # Save
    df.to_excel(DATA_FILE, index=False)

    st.success("✅ Data Saved Successfully")

# =====================================================
# MACHINE DATAFRAME
# =====================================================

machine_df = df.copy()

# =====================================================
# MONTH FILTER
# =====================================================

st.sidebar.markdown("## 📅 FILTER")

if not machine_df.empty:

    available_years = sorted(
        machine_df["Date"].dt.year.dropna().unique()
    )

else:

    available_years = [date.today().year]

selected_year = st.sidebar.selectbox(
    "Select Year",
    available_years
)

selected_month = st.sidebar.selectbox(
    "Select Month",
    range(1, 13),
    format_func=lambda x:
    date(1900, x, 1).strftime("%B")
)

# =====================================================
# FILTER DATAFRAME
# =====================================================

if not machine_df.empty:

    filtered_df = machine_df[
        (machine_df["Date"].dt.year == selected_year) &
        (machine_df["Date"].dt.month == selected_month)
    ]

else:

    filtered_df = machine_df.copy()

# =====================================================
# FILTER INFO
# =====================================================

st.info(
    f"Showing data for "
    f"{date(1900, selected_month, 1).strftime('%B')} "
    f"{selected_year}"
)

# =====================================================
# KPI SUMMARY
# =====================================================

if not filtered_df.empty:

    latest = filtered_df.sort_values(
        "Date"
    ).iloc[-1]

    st.subheader("📊 MACHINE SUMMARY")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Pressure</h3>
        <h1>{latest['Pressure (KPA)']:.2f} KPA</h1>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Temperature</h3>
        <h1>{latest['Temperature (°C)']:.2f} °C</h1>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Air Flow</h3>
        <h1>{latest['Air Flow Rate (CFM)']:.2f} CFM</h1>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Compressed Air</h3>
        <h1>{latest['Compressed Air Pressure (MPa)']:.2f} MPa</h1>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Motor Ampere</h3>
        <h1>{latest['Motor Ampere (A)']:.2f} A</h1>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# DATA TABLE
# =====================================================

st.subheader("🗂️ RECORDED DATA")

if not filtered_df.empty:

    filtered_df = filtered_df.sort_values(
        "Date",
        ascending=False
    )

    display_df = filtered_df.copy()

    display_df["Date"] = display_df[
        "Date"
    ].dt.strftime("%Y-%m-%d")

    display_df = display_df[required_columns]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No data available.")

# =====================================================
# GRAPH SECTION
# =====================================================

if not filtered_df.empty:

    graph_df = filtered_df.sort_values(
        "Date"
    ).copy()

    graph_df["Day"] = graph_df["Date"].dt.day

    st.subheader("📈 PERFORMANCE ANALYTICS")

    graphs = [
        ("Pressure (KPA)", "#00F5FF", "KPA"),
        ("Temperature (°C)", "#FF00FF", "°C"),
        ("Air Flow Rate (CFM)", "#00FF88", "CFM"),
        ("Compressed Air Pressure (MPa)", "#FFD700", "MPa"),
        ("Motor Ampere (A)", "#FF4444", "Ampere (A)")
    ]

    for column, color, ylabel in graphs:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=graph_df["Day"],
            y=graph_df[column],
            mode="lines+markers",
            line=dict(color=color, width=4),
            marker=dict(size=8)

        ))

        if column == "Pressure (KPA)":
            fig.add_hline(
            y=2.0,
            line_color="red",
            line_dash="dash",
            line_width=3,
            annotation_text="MAX LIMIT = 2.0 KPA",
            annotation_position="top right"
        )  
        if column == "Pressure (KPA)":
            fig.add_hline(
            y=0.05,
            line_color="yellow",
            line_dash="dash",
            line_width=3,
            annotation_text="MIN LIMIT = 0.05 KPA",
            annotation_position="bottom right"
        ) 
        if column == "Temperature (°C)":
            fig.add_hline(
            y=60,
            line_color="red",
            line_dash="dash",
            line_width=3,
            annotation_text="MAX LIMIT = 60 °C",
            annotation_position="top right"
        )
        if column == "Air Flow Rate (CFM)":
            fig.add_hline(
            y=3500,
            line_color="red",
            line_dash="dash",
            line_width=3,
            annotation_text="MAX LIMIT = 3500 CFM",
            annotation_position="top right"
        )
        if column == "Air Flow Rate (CFM)":
            fig.add_hline(
            y=1000,
            line_color="yellow",
            line_dash="dash",
            line_width=3,
            annotation_text="MIN LIMIT = 1000 CFM",
            annotation_position="bottom right"
        )
        if column == "Compressed Air Pressure (MPa)":
            fig.add_hline(
            y=0.4,
            line_color="red",
            line_dash="dash",
            line_width=3,
            annotation_text="MAX LIMIT = 0.4 MPa",
            annotation_position="top right"
        )
        if column == "Compressed Air Pressure (MPa)":
            fig.add_hline(
            y=0.2,
            line_color="yellow",
            line_dash="dash",
            line_width=3,
            annotation_text="MIN LIMIT = 0.2 MPa",
            annotation_position="bottom right"
        )
        if column == "Motor Ampere (A)":
            fig.add_hline(
            y=8,
            line_color="red",
            line_dash="dash",
            line_width=3,
            annotation_text="MAX LIMIT = 8 A",
            annotation_position="top right"
        )
        if column == "Motor Ampere (A)":
            fig.add_hline(
            y=3,
            line_color="yellow",
            line_dash="dash",
            line_width=3,
            annotation_text="MIN LIMIT = 3 A",
            annotation_position="bottom right"
        )



        fig.update_layout(
            title=f"{column} Trend",
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            hovermode="x unified",
            xaxis=dict(
                title="Day",
                dtick=1,
                range=[1, 31]
            ),
            yaxis_title=ylabel
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =====================================================
# EXPORT FILTERED DATA
# =====================================================

st.subheader("📥 EXPORT")

if not filtered_df.empty:

    export_file = (
        f"{machine}_"
        f"{selected_year}_"
        f"{selected_month}.xlsx"
    )

    export_df = filtered_df[required_columns]

    export_df.to_excel(
        export_file,
        index=False
    )

    with open(export_file, "rb") as f:

        st.download_button(
            "⬇️ Download Filtered Excel",
            f,
            file_name=export_file
        )
