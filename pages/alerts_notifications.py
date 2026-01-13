import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def alerts_notifications():
    """Alerts & Notifications - Action-oriented insights"""
    
    st.markdown("## 🚨 Alerts & Notifications")
    st.markdown("*Real-time alerts and risk-based notifications*")
    
    # Get data from session state
    disaster_data = st.session_state.disaster_data
    weather_data = st.session_state.weather_data
    
    if disaster_data is None or weather_data is None:
        st.error("Data not loaded. Please refresh the page.")
        return
    
    # Generate alerts
    disaster_alerts = generate_disaster_alerts(disaster_data)
    weather_alerts = generate_weather_alerts(weather_data)
    
    # Alert Summary
    st.markdown("### 🎯 Alert Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    critical_alerts = len([a for a in disaster_alerts if a['priority'] == 'Critical'])
    high_alerts = len([a for a in disaster_alerts if a['priority'] == 'High'])
    weather_warnings = len([a for a in weather_alerts if a['priority'] in ['High', 'Critical']])
    total_alerts = len(disaster_alerts) + len(weather_alerts)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card pulse">
            <h4 style="color: #dc3545; margin: 0;">🔴 Critical</h4>
            <h2 style="color: white; margin: 10px 0;">{critical_alerts}</h2>
            <p style="color: #888; margin: 0;">Immediate action</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #fd7e14; margin: 0;">🟠 High Priority</h4>
            <h2 style="color: white; margin: 10px 0;">{high_alerts}</h2>
            <p style="color: #888; margin: 0;">Urgent attention</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #ffc107; margin: 0;">🌤️ Weather Warnings</h4>
            <h2 style="color: white; margin: 10px 0;">{weather_warnings}</h2>
            <p style="color: #888; margin: 0;">Weather-related</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #17a2b8; margin: 0;">📊 Total Alerts</h4>
            <h2 style="color: white; margin: 10px 0;">{total_alerts}</h2>
            <p style="color: #888; margin: 0;">All active alerts</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Active Alerts Section
    st.markdown("### 🚨 Active Critical Alerts")
    
    # Filter and display critical alerts
    critical_disaster_alerts = [a for a in disaster_alerts if a['priority'] == 'Critical']
    critical_weather_alerts = [a for a in weather_alerts if a['priority'] == 'Critical']
    
    if critical_disaster_alerts or critical_weather_alerts:
        for alert in critical_disaster_alerts + critical_weather_alerts:
            display_alert_card(alert, 'critical')
    else:
        st.success("✅ No critical alerts at this time")
    
    # High Priority Alerts
    st.markdown("### ⚠️ High Priority Alerts")
    
    high_disaster_alerts = [a for a in disaster_alerts if a['priority'] == 'High']
    high_weather_alerts = [a for a in weather_alerts if a['priority'] == 'High']
    
    if high_disaster_alerts or high_weather_alerts:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌪️ Disaster Alerts")
            for alert in high_disaster_alerts:
                display_alert_card(alert, 'high')
        
        with col2:
            st.markdown("#### 🌤️ Weather Alerts")
            for alert in high_weather_alerts:
                display_alert_card(alert, 'high')
    else:
        st.info("ℹ️ No high priority alerts")
    
    # Regional Risk Assessment
    st.markdown("### 🗺️ Regional Risk Assessment")
    
    regional_risks = calculate_regional_risks(disaster_data, weather_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk level distribution
        risk_counts = pd.Series([r['risk_level'] for r in regional_risks]).value_counts()
        
        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Regional Risk Distribution",
            color_discrete_map={
                'Low': '#28a745',
                'Medium': '#ffc107',
                'High': '#fd7e14',
                'Critical': '#dc3545'
            }
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white'
        )
        
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("#### 🎯 High-Risk Regions")
        
        high_risk_regions = [r for r in regional_risks if r['risk_level'] in ['High', 'Critical']]
        high_risk_regions.sort(key=lambda x: x['risk_score'], reverse=True)
        
        for region in high_risk_regions[:5]:
            risk_color = {'High': '#fd7e14', 'Critical': '#dc3545'}[region['risk_level']]
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin: 5px 0; border-left: 4px solid {risk_color};">
                <strong>{region['location']}</strong><br>
                <small>Risk Level: <span style="color: {risk_color};">{region['risk_level']}</span> | Score: {region['risk_score']:.1f}/10</small><br>
                <small>Active Events: {region['active_events']} | Population at Risk: {region['population_at_risk']:,}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Alert Timeline
    st.markdown("### 📅 Alert Timeline")
    
    # Create timeline data
    timeline_data = []
    
    for alert in disaster_alerts + weather_alerts:
        timeline_data.append({
            'timestamp': alert['timestamp'],
            'type': alert['type'],
            'priority': alert['priority'],
            'message': alert['message'][:50] + '...' if len(alert['message']) > 50 else alert['message']
        })
    
    if timeline_data:
        timeline_df = pd.DataFrame(timeline_data)
        timeline_df = timeline_df.sort_values('timestamp', ascending=False)
        
        # Create timeline chart
        priority_colors = {'Critical': '#dc3545', 'High': '#fd7e14', 'Medium': '#ffc107', 'Low': '#28a745'}
        
        fig = px.scatter(
            timeline_df,
            x='timestamp',
            y='type',
            color='priority',
            size=[10] * len(timeline_df),
            hover_data=['message'],
            title="Alert Timeline",
            color_discrete_map=priority_colors
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
    
    # Alert Log
    st.markdown("### 📋 Alert Log")
    
    # Create detailed alert log
    if timeline_data:
        log_df = pd.DataFrame(timeline_data)
        log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])
        log_df = log_df.sort_values('timestamp', ascending=False)
        
        # Style the dataframe
        def style_priority(val):
            colors = {'Critical': 'background-color: rgba(220, 53, 69, 0.3)',
                     'High': 'background-color: rgba(253, 126, 20, 0.3)',
                     'Medium': 'background-color: rgba(255, 193, 7, 0.3)',
                     'Low': 'background-color: rgba(40, 167, 69, 0.3)'}
            return colors.get(val, '')
        
        styled_log = log_df.style.map(style_priority, subset=['priority'])
        st.dataframe(styled_log, width='stretch')
    
    # Alert Settings
    st.markdown("### ⚙️ Alert Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔔 Notification Preferences")
        enable_critical = st.checkbox("Critical Alerts", value=True)
        enable_high = st.checkbox("High Priority Alerts", value=True)
        enable_weather = st.checkbox("Weather Warnings", value=True)
        enable_regional = st.checkbox("Regional Updates", value=False)
    
    with col2:
        st.markdown("#### 🎯 Alert Thresholds")
        population_threshold = st.slider("Population Impact Threshold", 1000, 50000, 10000)
        severity_threshold = st.selectbox("Minimum Severity Level", ['Low', 'Medium', 'High', 'Critical'], index=1)
    
    with col3:
        st.markdown("#### 📱 Delivery Methods")
        email_alerts = st.checkbox("Email Notifications", value=True)
        sms_alerts = st.checkbox("SMS Alerts", value=False)
        push_notifications = st.checkbox("Push Notifications", value=True)
        
        if st.button("💾 Save Settings"):
            st.success("Alert settings saved successfully!")

def generate_disaster_alerts(disaster_data):
    """Generate disaster-based alerts"""
    alerts = []
    
    # Recent critical disasters
    recent_critical = disaster_data[
        (disaster_data['severity'] == 'Critical') &
        (disaster_data['timestamp'] > datetime.now() - timedelta(hours=24))
    ]
    
    for _, disaster in recent_critical.iterrows():
        alerts.append({
            'id': f"DISASTER_{disaster['id']}",
            'type': 'Disaster Alert',
            'priority': 'Critical',
            'timestamp': disaster['timestamp'],
            'location': disaster['location'],
            'message': f"Critical {disaster['type']} affecting {disaster['affected_population']:,} people in {disaster['location']}",
            'action_required': True,
            'estimated_duration': '6-12 hours'
        })
    
    # High severity disasters
    recent_high = disaster_data[
        (disaster_data['severity'] == 'High') &
        (disaster_data['timestamp'] > datetime.now() - timedelta(hours=48))
    ]
    
    for _, disaster in recent_high.iterrows():
        alerts.append({
            'id': f"DISASTER_{disaster['id']}",
            'type': 'Disaster Alert',
            'priority': 'High',
            'timestamp': disaster['timestamp'],
            'location': disaster['location'],
            'message': f"High severity {disaster['type']} in {disaster['location']} - {disaster['affected_population']:,} people affected",
            'action_required': False,
            'estimated_duration': '2-4 hours'
        })
    
    return alerts

def generate_weather_alerts(weather_data):
    """Generate weather-based alerts"""
    alerts = []
    current_weather = weather_data.iloc[-1]
    
    # Temperature alerts
    if current_weather['temperature'] > 40:
        alerts.append({
            'id': 'WEATHER_TEMP_HIGH',
            'type': 'Weather Alert',
            'priority': 'High',
            'timestamp': current_weather['date'],
            'location': 'Current Region',
            'message': f"Extreme heat warning: {current_weather['temperature']:.1f}°C - Heat stroke risk",
            'action_required': True,
            'estimated_duration': '4-8 hours'
        })
    elif current_weather['temperature'] < -5:
        alerts.append({
            'id': 'WEATHER_TEMP_LOW',
            'type': 'Weather Alert',
            'priority': 'High',
            'timestamp': current_weather['date'],
            'location': 'Current Region',
            'message': f"Extreme cold warning: {current_weather['temperature']:.1f}°C - Hypothermia risk",
            'action_required': True,
            'estimated_duration': '6-12 hours'
        })
    
    # Wind alerts
    if current_weather['wind_speed'] > 40:
        priority = 'Critical' if current_weather['wind_speed'] > 60 else 'High'
        alerts.append({
            'id': 'WEATHER_WIND',
            'type': 'Weather Alert',
            'priority': priority,
            'timestamp': current_weather['date'],
            'location': 'Current Region',
            'message': f"High wind warning: {current_weather['wind_speed']:.1f} km/h - Structural damage risk",
            'action_required': True,
            'estimated_duration': '2-6 hours'
        })
    
    # Rainfall alerts
    if current_weather['rainfall'] > 10:
        priority = 'Critical' if current_weather['rainfall'] > 20 else 'High'
        alerts.append({
            'id': 'WEATHER_RAIN',
            'type': 'Weather Alert',
            'priority': priority,
            'timestamp': current_weather['date'],
            'location': 'Current Region',
            'message': f"Heavy rainfall warning: {current_weather['rainfall']:.1f} mm - Flooding risk",
            'action_required': True,
            'estimated_duration': '3-8 hours'
        })
    
    return alerts

def calculate_regional_risks(disaster_data, weather_data):
    """Calculate risk levels for different regions"""
    regional_risks = []
    
    for location in disaster_data['location'].unique():
        location_data = disaster_data[disaster_data['location'] == location]
        
        # Calculate risk factors
        recent_events = len(location_data[location_data['timestamp'] > datetime.now() - timedelta(days=7)])
        critical_events = len(location_data[location_data['severity'] == 'Critical'])
        total_affected = location_data['affected_population'].sum()
        
        # Risk score calculation (0-10)
        risk_score = min(
            (recent_events * 2) + 
            (critical_events * 3) + 
            (total_affected / 10000), 
            10
        )
        
        # Risk level classification
        if risk_score >= 8:
            risk_level = 'Critical'
        elif risk_score >= 6:
            risk_level = 'High'
        elif risk_score >= 3:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        regional_risks.append({
            'location': location,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'active_events': recent_events,
            'population_at_risk': total_affected
        })
    
    return regional_risks

def display_alert_card(alert, alert_type):
    """Display an alert card with appropriate styling"""
    
    if alert_type == 'critical':
        card_class = 'alert-high pulse'
        icon = '🔴'
    elif alert_type == 'high':
        card_class = 'alert-medium'
        icon = '🟠'
    else:
        card_class = 'alert-low'
        icon = '🟡'
    
    action_text = "⚡ IMMEDIATE ACTION REQUIRED" if alert.get('action_required') else "ℹ️ Monitor situation"
    
    st.markdown(f"""
    <div class="{card_class}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0;">{icon} {alert['type']} - {alert['priority']} Priority</h4>
                <p style="margin: 5px 0;"><strong>{alert['message']}</strong></p>
                <small>📍 {alert['location']} | ⏰ {alert['timestamp'].strftime('%Y-%m-%d %H:%M')}</small><br>
                <small>⏱️ Duration: {alert.get('estimated_duration', 'Unknown')}</small>
            </div>
            <div style="text-align: right;">
                <small style="color: {'#dc3545' if alert.get('action_required') else '#17a2b8'};">{action_text}</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)