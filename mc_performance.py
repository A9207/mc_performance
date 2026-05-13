# =====================================================
# FUTURISTIC BAG FILTER PERFORMANCE MONITORING SYSTEM
# Python 3.13 + Streamlit
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
    ["Machine 1", "Machine 2", "Machine 3", "Machine 4"]
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
    "Operator Signature",
    "Supervisor Signature"
]

# =====================================================
# LOAD DATA
# =====================================================

if os.path.exists(DATA_FILE):

    df = pd.read_excel(DATA_FILE)

    # Add missing columns for old Excel files
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

else:

    df = pd.DataFrame(columns=required_columns)

    df.to_excel(DATA_FILE, index=False)

# =====================================================
# DATA TYPE FIX
# =====================================================

numeric_columns = [
    "Pressure (KPA)",
    "Temperature (°C)",
    "Air Flow Rate (CFM)",
    "Compressed Air Pressure (MPa)"
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
# INPUT FORM
# =====================================================

st.subheader("📥 DAILY DATA ENTRY")

with st.form("form"):

    col1, col2 = st.columns(2)

    # =================================================
    # LEFT COLUMN
    # =================================================

    with col1:

        input_date = st.date_input(
            "Date",
            value=date.today()
        )

        pressure = st.number_input(
            "Pressure (KPA)",
            min_value=0.0,
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
            step=0.1,
            format="%.2f"
        )

        compressed_air = st.number_input(
            "Compressed Air Pressure (MPa)",
            min_value=0.0,
            step=0.01,
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

        D = 0.81 / 3.142

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
        "Chimney Condition (OK / NOT OK)"
    )

    hopper = st.text_input(
        "Discharge Hopper Condition (OK / NOT OK)"
    )

    operator_signature = st.text_input(
        "Operator Signature"
    )

    supervisor_signature = st.text_input(
        "Supervisor Signature"
    )

    submit = st.form_submit_button(
        " SAVE DATA"
    )

# =====================================================
# SAVE DATA
# =====================================================

if submit:

    if not df.empty:
        df["Date"] = pd.to_datetime(
            df["Date"]
        ).dt.date

    # Replace same date entry
    df = df[~(df["Date"] == input_date)]

    new_data = pd.DataFrame({

        "Date": [input_date],
        "Pressure (KPA)": [pressure],
        "Temperature (°C)": [temperature],
        "Air Flow Rate (CFM)": [airflow],
        "Compressed Air Pressure (MPa)": [compressed_air],
        "Chimney Condition": [chimney],
        "Discharge Hopper Condition": [hopper],
        "Operator Signature": [operator_signature],
        "Supervisor Signature": [supervisor_signature]

    })

    df = pd.concat(
        [df, new_data],
        ignore_index=True
    )

    df.to_excel(DATA_FILE, index=False)

    st.success("✅ Data Saved Successfully")

# =====================================================
# DATAFRAME
# =====================================================

machine_df = df.copy()

# =====================================================
# KPI SUMMARY
# =====================================================

if not machine_df.empty:

    machine_df["Date"] = pd.to_datetime(
        machine_df["Date"]
    )

    latest = machine_df.sort_values(
        "Date"
    ).iloc[-1]

    st.subheader("📊 MACHINE SUMMARY")

    c1, c2, c3, c4 = st.columns(4)

    # PRESSURE

    with c1:

        st.markdown(f"""
        <div class="metric-card">
        <h3>Pressure</h3>
        <h1>{latest['Pressure (KPA)']:.2f} KPA</h1>
        </div>
        """, unsafe_allow_html=True)

    # TEMPERATURE

    with c2:

        st.markdown(f"""
        <div class="metric-card">
        <h3>Temperature</h3>
        <h1>{latest['Temperature (°C)']:.2f} °C</h1>
        </div>
        """, unsafe_allow_html=True)

    # AIR FLOW

    with c3:

        st.markdown(f"""
        <div class="metric-card">
        <h3>Air Flow</h3>
        <h1>{latest['Air Flow Rate (CFM)']:.2f} CFM</h1>
        </div>
        """, unsafe_allow_html=True)

    # COMPRESSED AIR

    with c4:

        st.markdown(f"""
        <div class="metric-card">
        <h3>Compressed Air</h3>
        <h1>{latest['Compressed Air Pressure (MPa)']:.2f} MPa</h1>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# DATA TABLE
# =====================================================

st.subheader("🗂️ RECORDED DATA")

if not machine_df.empty:

    machine_df["Date"] = pd.to_datetime(
        machine_df["Date"]
    )

    machine_df = machine_df.sort_values(
        "Date",
        ascending=False
    )

    display_df = machine_df.copy()

    display_df["Date"] = display_df[
        "Date"
    ].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df,
        use_container_width=True
    )

else:

    st.info("No data available.")

# =====================================================
# GRAPH SECTION
# =====================================================

if not machine_df.empty:

    graph_df = machine_df.copy()

    graph_df["Day"] = graph_df["Date"].dt.day

    st.subheader("📈 PERFORMANCE ANALYTICS")

    # =================================================
    # PRESSURE GRAPH
    # =================================================

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=graph_df["Day"],
        y=graph_df["Pressure (KPA)"],
        mode="lines+markers",
        line=dict(color="#00F5FF", width=4),
        marker=dict(size=8)
    ))

    fig1.update_layout(
        title="Pressure Trend (KPA)",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white"),
        hovermode="x unified",
        xaxis=dict(
            title="Day",
            dtick=1,
            range=[1, 31]
        ),
        yaxis_title="KPA"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # =================================================
    # TEMPERATURE GRAPH
    # =================================================

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=graph_df["Day"],
        y=graph_df["Temperature (°C)"],
        mode="lines+markers",
        line=dict(color="#FF00FF", width=4),
        marker=dict(size=8)
    ))

    fig2.update_layout(
        title="Temperature Trend (°C)",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white"),
        hovermode="x unified",
        xaxis=dict(
            title="Day",
            dtick=1,
            range=[1, 31]
        ),
        yaxis_title="°C"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # =================================================
    # AIR FLOW GRAPH
    # =================================================

    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(
        x=graph_df["Day"],
        y=graph_df["Air Flow Rate (CFM)"],
        mode="lines+markers",
        line=dict(color="#00FF88", width=4),
        marker=dict(size=8)
    ))

    fig3.update_layout(
        title="Air Flow Trend (CFM)",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white"),
        hovermode="x unified",
        xaxis=dict(
            title="Day",
            dtick=1,
            range=[1, 31]
        ),
        yaxis_title="CFM"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # =================================================
    # COMPRESSED AIR GRAPH
    # =================================================

    fig4 = go.Figure()

    fig4.add_trace(go.Scatter(
        x=graph_df["Day"],
        y=graph_df["Compressed Air Pressure (MPa)"],
        mode="lines+markers",
        line=dict(color="#FFD700", width=4),
        marker=dict(size=8)
    ))

    fig4.update_layout(
        title="Compressed Air Pressure Trend (MPa)",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white"),
        hovermode="x unified",
        xaxis=dict(
            title="Day",
            dtick=1,
            range=[1, 31]
        ),
        yaxis_title="MPa"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =====================================================
# EXPORT
# =====================================================

st.subheader("📥 EXPORT")

if os.path.exists(DATA_FILE):

    with open(DATA_FILE, "rb") as f:

        st.download_button(
            "⬇️ Download Excel",
            f,
            file_name=f"{machine}_data.xlsx"
        )
