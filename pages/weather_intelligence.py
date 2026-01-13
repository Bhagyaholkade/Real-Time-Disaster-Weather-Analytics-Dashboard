import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def weather_intelligence():
    """Weather Intelligence Page - Analyze weather patterns and risks"""
    
    st.markdown("## 🌤️ Weather Intelligence")
    st.markdown("*Advanced weather pattern analysis and risk assessment*")
    
    # Get weather data from session state
    weather_data = st.session_state.weather_data
    
    if weather_data is None:
        st.error("Weather data not loaded. Please refresh the page.")
        return
    
    # Current weather metrics
    current_weather = weather_data.iloc[-1]
    
    st.markdown("### 🌡️ Current Weather Conditions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp_color = get_temperature_color(current_weather['temperature'])
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {temp_color}; margin: 0;">🌡️ Temperature</h4>
            <h2 style="color: white; margin: 10px 0;">{current_weather['temperature']:.1f}°C</h2>
            <p style="color: #888; margin: 0;">{get_temperature_status(current_weather['temperature'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        humidity_color = get_humidity_color(current_weather['humidity'])
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {humidity_color}; margin: 0;">💧 Humidity</h4>
            <h2 style="color: white; margin: 10px 0;">{current_weather['humidity']:.1f}%</h2>
            <p style="color: #888; margin: 0;">{get_humidity_status(current_weather['humidity'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        wind_color = get_wind_color(current_weather['wind_speed'])
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {wind_color}; margin: 0;">💨 Wind Speed</h4>
            <h2 style="color: white; margin: 10px 0;">{current_weather['wind_speed']:.1f} km/h</h2>
            <p style="color: #888; margin: 0;">{get_wind_status(current_weather['wind_speed'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        rain_color = get_rainfall_color(current_weather['rainfall'])
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {rain_color}; margin: 0;">🌧️ Rainfall</h4>
            <h2 style="color: white; margin: 10px 0;">{current_weather['rainfall']:.1f} mm</h2>
            <p style="color: #888; margin: 0;">{get_rainfall_status(current_weather['rainfall'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Weather trends
    st.markdown("### 📈 Weather Trends (30 Days)")
    
    # Create subplots for multiple weather parameters
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Temperature Trend', 'Rainfall Pattern', 'Wind Speed', 'Atmospheric Pressure'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Temperature trend
    fig.add_trace(
        go.Scatter(
            x=weather_data['date'],
            y=weather_data['temperature'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#ff6b6b', width=2),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    
    # Rainfall pattern
    fig.add_trace(
        go.Bar(
            x=weather_data['date'],
            y=weather_data['rainfall'],
            name='Rainfall',
            marker_color='#17a2b8',
            opacity=0.7
        ),
        row=1, col=2
    )
    
    # Wind speed
    fig.add_trace(
        go.Scatter(
            x=weather_data['date'],
            y=weather_data['wind_speed'],
            mode='lines',
            name='Wind Speed',
            line=dict(color='#28a745', width=2),
            fill='tonexty'
        ),
        row=2, col=1
    )
    
    # Atmospheric pressure
    fig.add_trace(
        go.Scatter(
            x=weather_data['date'],
            y=weather_data['pressure'],
            mode='lines+markers',
            name='Pressure',
            line=dict(color='#ffc107', width=2),
            marker=dict(size=3)
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    
    # Update axes
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig, width='stretch')
    
    # Extreme weather indicators
    st.markdown("### ⚠️ Extreme Weather Indicators")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature extremes
        temp_extremes = detect_temperature_extremes(weather_data)
        if temp_extremes:
            st.markdown("#### 🌡️ Temperature Alerts")
            for extreme in temp_extremes:
                alert_class = "alert-high" if extreme['severity'] == 'High' else "alert-medium"
                st.markdown(f"""
                <div class="{alert_class}">
                    <strong>{extreme['type']}</strong><br>
                    <small>{extreme['date'].strftime('%Y-%m-%d')}: {extreme['value']:.1f}°C</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Wind alerts
        wind_extremes = detect_wind_extremes(weather_data)
        if wind_extremes:
            st.markdown("#### 💨 Wind Alerts")
            for extreme in wind_extremes:
                alert_class = "alert-high" if extreme['severity'] == 'High' else "alert-medium"
                st.markdown(f"""
                <div class="{alert_class}">
                    <strong>{extreme['type']}</strong><br>
                    <small>{extreme['date'].strftime('%Y-%m-%d')}: {extreme['value']:.1f} km/h</small>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # Rainfall extremes
        rain_extremes = detect_rainfall_extremes(weather_data)
        if rain_extremes:
            st.markdown("#### 🌧️ Rainfall Alerts")
            for extreme in rain_extremes:
                alert_class = "alert-high" if extreme['severity'] == 'High' else "alert-medium"
                st.markdown(f"""
                <div class="{alert_class}">
                    <strong>{extreme['type']}</strong><br>
                    <small>{extreme['date'].strftime('%Y-%m-%d')}: {extreme['value']:.1f} mm</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Pressure alerts
        pressure_extremes = detect_pressure_extremes(weather_data)
        if pressure_extremes:
            st.markdown("#### 🔽 Pressure Alerts")
            for extreme in pressure_extremes:
                alert_class = "alert-high" if extreme['severity'] == 'High' else "alert-medium"
                st.markdown(f"""
                <div class="{alert_class}">
                    <strong>{extreme['type']}</strong><br>
                    <small>{extreme['date'].strftime('%Y-%m-%d')}: {extreme['value']:.1f} hPa</small>
                </div>
                """, unsafe_allow_html=True)
    
    # Weather risk assessment
    st.markdown("### 🎯 Weather Risk Assessment")
    
    risk_score = calculate_weather_risk_score(current_weather)
    risk_level = get_risk_level(risk_score)
    risk_color = {'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'}[risk_level]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <h3 style="color: {risk_color}; margin: 0;">Overall Weather Risk</h3>
            <h1 style="color: {risk_color}; margin: 20px 0; font-size: 3em;">{risk_level}</h1>
            <p style="color: white; margin: 0;">Risk Score: {risk_score:.1f}/100</p>
            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; margin: 20px 0;">
                <div style="background: {risk_color}; height: 100%; width: {risk_score}%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Helper functions for weather analysis

def get_temperature_color(temp):
    if temp < 0: return '#87ceeb'  # Light blue for freezing
    elif temp < 10: return '#4169e1'  # Blue for cold
    elif temp < 25: return '#28a745'  # Green for comfortable
    elif temp < 35: return '#ffc107'  # Yellow for warm
    else: return '#dc3545'  # Red for hot

def get_temperature_status(temp):
    if temp < 0: return 'Freezing'
    elif temp < 10: return 'Cold'
    elif temp < 25: return 'Comfortable'
    elif temp < 35: return 'Warm'
    else: return 'Hot'

def get_humidity_color(humidity):
    if humidity < 30: return '#ffc107'  # Yellow for dry
    elif humidity < 70: return '#28a745'  # Green for comfortable
    else: return '#17a2b8'  # Blue for humid

def get_humidity_status(humidity):
    if humidity < 30: return 'Dry'
    elif humidity < 70: return 'Comfortable'
    else: return 'Humid'

def get_wind_color(wind_speed):
    if wind_speed < 10: return '#28a745'  # Green for calm
    elif wind_speed < 25: return '#ffc107'  # Yellow for breezy
    elif wind_speed < 40: return '#fd7e14'  # Orange for windy
    else: return '#dc3545'  # Red for strong winds

def get_wind_status(wind_speed):
    if wind_speed < 10: return 'Calm'
    elif wind_speed < 25: return 'Breezy'
    elif wind_speed < 40: return 'Windy'
    else: return 'Strong Winds'

def get_rainfall_color(rainfall):
    if rainfall < 1: return '#28a745'  # Green for light
    elif rainfall < 5: return '#ffc107'  # Yellow for moderate
    elif rainfall < 10: return '#fd7e14'  # Orange for heavy
    else: return '#dc3545'  # Red for extreme

def get_rainfall_status(rainfall):
    if rainfall < 1: return 'Light'
    elif rainfall < 5: return 'Moderate'
    elif rainfall < 10: return 'Heavy'
    else: return 'Extreme'

def detect_temperature_extremes(weather_data):
    extremes = []
    for _, row in weather_data.iterrows():
        if row['temperature'] > 40:
            extremes.append({
                'type': 'Extreme Heat Warning',
                'date': row['date'],
                'value': row['temperature'],
                'severity': 'High'
            })
        elif row['temperature'] < -10:
            extremes.append({
                'type': 'Extreme Cold Warning',
                'date': row['date'],
                'value': row['temperature'],
                'severity': 'High'
            })
    return extremes[-5:]  # Return last 5

def detect_wind_extremes(weather_data):
    extremes = []
    for _, row in weather_data.iterrows():
        if row['wind_speed'] > 40:
            extremes.append({
                'type': 'High Wind Warning',
                'date': row['date'],
                'value': row['wind_speed'],
                'severity': 'High'
            })
    return extremes[-5:]

def detect_rainfall_extremes(weather_data):
    extremes = []
    for _, row in weather_data.iterrows():
        if row['rainfall'] > 10:
            extremes.append({
                'type': 'Heavy Rainfall Warning',
                'date': row['date'],
                'value': row['rainfall'],
                'severity': 'High'
            })
    return extremes[-5:]

def detect_pressure_extremes(weather_data):
    extremes = []
    for _, row in weather_data.iterrows():
        if row['pressure'] < 980:
            extremes.append({
                'type': 'Low Pressure System',
                'date': row['date'],
                'value': row['pressure'],
                'severity': 'High'
            })
    return extremes[-5:]

def calculate_weather_risk_score(weather_row):
    """Calculate overall weather risk score (0-100)"""
    temp_risk = 0
    if weather_row['temperature'] > 35 or weather_row['temperature'] < 0:
        temp_risk = 30
    elif weather_row['temperature'] > 30 or weather_row['temperature'] < 5:
        temp_risk = 15
    
    wind_risk = min(weather_row['wind_speed'] / 50 * 40, 40)
    rain_risk = min(weather_row['rainfall'] / 15 * 30, 30)
    
    return temp_risk + wind_risk + rain_risk

def get_risk_level(score):
    if score < 30: return 'Low'
    elif score < 60: return 'Medium'
    else: return 'High'