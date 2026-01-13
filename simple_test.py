#!/usr/bin/env python3
"""
Simple test to verify core functionality without complex components
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="🌪️ Dashboard Test",
    page_icon="🌪️",
    layout="wide"
)

st.title("🌪️ Dashboard Functionality Test")

# Test data generation
@st.cache_data
def generate_test_data():
    np.random.seed(42)
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    data = []
    for date in dates:
        data.append({
            'date': date,
            'disasters': np.random.randint(0, 5),
            'severity_score': np.random.uniform(1, 10),
            'affected_population': np.random.randint(100, 10000)
        })
    
    return pd.DataFrame(data)

# Generate test data
df = generate_test_data()

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Disasters", df['disasters'].sum())

with col2:
    st.metric("Avg Severity", f"{df['severity_score'].mean():.1f}")

with col3:
    st.metric("Total Affected", f"{df['affected_population'].sum():,}")

# Display chart
st.subheader("📈 Disaster Trends")
fig = px.line(df, x='date', y='disasters', title="Daily Disaster Count")
st.plotly_chart(fig, width='stretch')

# Display data table
st.subheader("📊 Data Table")
st.dataframe(df, width='stretch')

st.success("✅ Core functionality is working!")
st.info("If you see this page properly, the basic dashboard components are functional.")