import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Ethiopia FI Consortium", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_and_clean_data():
    # Load the primary data and the impact links
    file_path = "../data/raw/ethiopia_fi_unified_data.xlsx"
    df_main = pd.read_excel(file_path, sheet_name="ethiopia_fi_unified_data")
    df_impact = pd.read_excel(file_path, sheet_name="Impact_sheet")
    
    # Clean data types to avoid the "Object" errors
    df_main['value_numeric'] = pd.to_numeric(df_main['value_numeric'], errors='coerce')
    df_impact['impact_magnitude'] = pd.to_numeric(df_impact['impact_magnitude'], errors='coerce')
    
    return df_main, df_impact

try:
    df_main, df_impact = load_and_clean_data()
except Exception as e:
    st.error(f"Could not load data. Check file path. Error: {e}")
    st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Trends", "2026 Projections"])

# --- PAGE 1: OVERVIEW ---
if page == "Overview":
    st.header("🇪🇹 Ethiopia Financial Inclusion Overview")
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    latest_ownership = df_main[df_main['indicator_code'] == 'ACC_OWNERSHIP']['value_numeric'].iloc[-1]
    col1.metric("Account Ownership", f"{latest_ownership}%", "Target: 60%")
    col2.metric("Digital Usage", "19.7%", "Target: 35%")
    col3.metric("P2P/ATM Ratio", "1.42", "Crossover: 2024")

    # Simple Trend Chart
    st.subheader("Account Ownership Trend")
    trend_data = df_main[df_main['indicator_code'] == 'ACC_OWNERSHIP']
    fig = px.line(trend_data, x='observation_date', y='value_numeric', markers=True, 
                  labels={'value_numeric': 'Ownership %', 'observation_date': 'Year'})
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: 2026 PROJECTIONS ---
elif page == "2026 Projections":
    st.header("Road to 60%: Scenario Modeling")
    
    scenario = st.select_slider("Select Growth Scenario", 
                               options=["Pessimistic", "Base", "Optimistic"])
    
    # Simple logic for scenario visualization
    base_val = 49.8
    if scenario == "Optimistic":
        proj_val = 62.5
        msg = "Fayda Digital ID adoption is mandatory and universal."
    elif scenario == "Pessimistic":
        proj_val = 51.2
        msg = "Connectivity issues and slow rural rollout."
    else:
        proj_val = 56.4
        msg = "Current growth rates continue steadily."

    st.write(f"**Scenario Outcome:** {msg}")

    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = proj_val,
        title = {'text': f"Projected 2026 Ownership ({scenario})"},
        delta = {'reference': 60},
        gauge = {'axis': {'range': [None, 100]},
                 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 60}}
    ))
    st.plotly_chart(fig)