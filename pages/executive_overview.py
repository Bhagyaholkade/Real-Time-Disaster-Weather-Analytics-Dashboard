import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def executive_overview():
    """Executive Overview Dashboard - High-level situation awareness"""
    
    st.markdown("## 🏠 Executive Overview Dashboard")
    st.markdown("*Real-time situation awareness and key performance indicators*")
    
    # Get data from session state
    disaster_data = st.session_state.disaster_data
    weather_data = st.session_state.weather_data
    
    if disaster_data is None or weather_data is None:
        st.error("Data not loaded. Please refresh the page.")
        return
    
    # KPI Cards Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_disasters = len(disaster_data[disaster_data['timestamp'] > datetime.now() - timedelta(hours=24)])
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #ff6b6b; margin: 0;">🌪️ Active Disasters</h3>
            <h1 style="color: white; margin: 10px 0;">{active_disasters}</h1>
            <p style="color: #888; margin: 0;">Last 24 hours</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        high_risk_regions = len(disaster_data[disaster_data['severity'].isin(['High', 'Critical'])]['location'].unique())
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #ffc107; margin: 0;">⚠️ High-Risk Regions</h3>
            <h1 style="color: white; margin: 10px 0;">{high_risk_regions}</h1>
            <p style="color: #888; margin: 0;">Regions affected</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Weather severity index (0-100)
        current_weather = weather_data.iloc[-1]
        severity_index = calculate_weather_severity_index(current_weather)
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #17a2b8; margin: 0;">🌡️ Weather Severity</h3>
            <h1 style="color: white; margin: 10px 0;">{severity_index:.0f}/100</h1>
            <p style="color: #888; margin: 0;">Current index</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        critical_alerts = len(disaster_data[disaster_data['severity'] == 'Critical'])
        st.markdown(f"""
        <div class="metric-card pulse">
            <h3 style="color: #dc3545; margin: 0;">🚨 Critical Alerts</h3>
            <h1 style="color: white; margin: 10px 0;">{critical_alerts}</h1>
            <p style="color: #888; margin: 0;">Immediate attention</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Disaster Frequency Trend")
        
        # Group disasters by date
        disaster_data['date'] = disaster_data['timestamp'].dt.date
        daily_counts = disaster_data.groupby('date').size().reset_index(name='count')
        
        fig = px.line(
            daily_counts, 
            x='date', 
            y='count',
            title="Daily Disaster Occurrences",
            color_discrete_sequence=['#ff6b6b']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("### 🎯 Disaster Type Distribution")
        
        type_counts = disaster_data['type'].value_counts()
        
        fig = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="Disasters by Type",
            color=type_counts.values,
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            showlegend=False
        )
        
        st.plotly_chart(fig, width='stretch')
    
    # Severity Distribution
    st.markdown("### 🎚️ Risk Level Distribution")
    
    severity_counts = disaster_data['severity'].value_counts()
    colors = {'Low': '#28a745', 'Medium': '#ffc107', 'High': '#fd7e14', 'Critical': '#dc3545'}
    
    fig = go.Figure(data=[
        go.Pie(
            labels=severity_counts.index,
            values=severity_counts.values,
            hole=0.4,
            marker_colors=[colors.get(x, '#888') for x in severity_counts.index]
        )
    ])
    
    fig.update_layout(
        title="Current Risk Level Distribution",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    
    st.plotly_chart(fig, width='stretch')
    
    # Recent Activity Feed
    st.markdown("### 📋 Recent Activity Feed")
    
    recent_disasters = disaster_data.sort_values('timestamp', ascending=False).head(10)
    
    for _, disaster in recent_disasters.iterrows():
        severity_class = f"alert-{disaster['severity'].lower()}"
        time_ago = datetime.now() - disaster['timestamp']
        hours_ago = int(time_ago.total_seconds() / 3600)
        
        st.markdown(f"""
        <div class="{severity_class}">
            <strong>{disaster['type']}</strong> - {disaster['location']}<br>
            <small>Severity: {disaster['severity']} | {hours_ago}h ago | Population affected: {disaster['affected_population']:,}</small>
        </div>
        """, unsafe_allow_html=True)

def calculate_weather_severity_index(weather_row):
    """Calculate weather severity index (0-100)"""
    # Normalize different weather parameters and combine
    temp_score = min(abs(weather_row['temperature'] - 25) / 25 * 100, 100)
    wind_score = min(weather_row['wind_speed'] / 50 * 100, 100)
    rain_score = min(weather_row['rainfall'] / 10 * 100, 100)
    
    # Weighted average
    severity = (temp_score * 0.3 + wind_score * 0.4 + rain_score * 0.3)
    return min(severity, 100)