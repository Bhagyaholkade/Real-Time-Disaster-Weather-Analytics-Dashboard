import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from folium.plugins import HeatMap

def live_disaster_map():
    """Live Disaster Map - Visualize disasters geographically"""
    
    st.markdown("## 🗺️ Live Disaster Map")
    st.markdown("*Interactive visualization of global disaster events*")
    
    # Get data from session state
    disaster_data = st.session_state.disaster_data
    
    if disaster_data is None:
        st.error("Disaster data not loaded. Please refresh the page.")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        disaster_types = st.multiselect(
            "🎯 Filter by Disaster Type",
            options=disaster_data['type'].unique(),
            default=disaster_data['type'].unique()
        )
    
    with col2:
        severity_levels = st.multiselect(
            "⚠️ Filter by Severity",
            options=['Low', 'Medium', 'High', 'Critical'],
            default=['Medium', 'High', 'Critical']
        )
    
    with col3:
        time_range = st.selectbox(
            "⏰ Time Range",
            options=['Last 24 hours', 'Last 7 days', 'Last 30 days', 'All time'],
            index=1
        )
    
    # Apply filters
    filtered_data = disaster_data[
        (disaster_data['type'].isin(disaster_types)) &
        (disaster_data['severity'].isin(severity_levels))
    ]
    
    # Apply time filter
    if time_range == 'Last 24 hours':
        cutoff = datetime.now() - timedelta(hours=24)
    elif time_range == 'Last 7 days':
        cutoff = datetime.now() - timedelta(days=7)
    elif time_range == 'Last 30 days':
        cutoff = datetime.now() - timedelta(days=30)
    else:
        cutoff = datetime.min
    
    filtered_data = filtered_data[filtered_data['timestamp'] >= cutoff]
    
    # Create the map
    if len(filtered_data) > 0:
        # Center map on mean coordinates
        center_lat = filtered_data['latitude'].mean()
        center_lon = filtered_data['longitude'].mean()
    else:
        center_lat, center_lon = 20, 0
    
    # Create folium map with dark theme
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=2,
        tiles=None
    )
    
    # Add dark tile layer
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name='Dark Theme',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Color mapping for severity
    severity_colors = {
        'Low': '#28a745',
        'Medium': '#ffc107', 
        'High': '#fd7e14',
        'Critical': '#dc3545'
    }
    
    # Icon mapping for disaster types
    disaster_icons = {
        'Earthquake': 'flash',
        'Flood': 'tint',
        'Cyclone': 'wind',
        'Wildfire': 'fire',
        'Drought': 'sun',
        'Landslide': 'mountain'
    }
    
    # Add markers for each disaster
    for _, disaster in filtered_data.iterrows():
        # Ensure coordinates are valid
        lat = float(disaster['latitude'])
        lon = float(disaster['longitude'])
        
        # Skip invalid coordinates
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            continue
            
        # Create popup content
        popup_html = f"""
        <div style="width: 200px;">
            <h4 style="color: {severity_colors[disaster['severity']]}; margin: 0;">
                {disaster['type']}
            </h4>
            <hr style="margin: 5px 0;">
            <p><strong>Location:</strong> {disaster['location']}</p>
            <p><strong>Severity:</strong> 
                <span style="color: {severity_colors[disaster['severity']]};">
                    {disaster['severity']}
                </span>
            </p>
            <p><strong>Time:</strong> {disaster['timestamp'].strftime('%Y-%m-%d %H:%M')}</p>
            <p><strong>Affected:</strong> {int(disaster['affected_population']):,} people</p>
            {f"<p><strong>Magnitude:</strong> {disaster['magnitude']:.1f}</p>" if disaster['type'] == 'Earthquake' else ""}
        </div>
        """
        
        # Add marker
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{disaster['type']} - {disaster['severity']}",
            icon=folium.Icon(
                color='red' if disaster['severity'] in ['High', 'Critical'] else 'orange' if disaster['severity'] == 'Medium' else 'green',
                icon=disaster_icons.get(disaster['type'], 'exclamation-sign'),
                prefix='fa'
            )
        ).add_to(m)
    
    # Add heatmap layer for high-risk zones
    if len(filtered_data) > 0:
        # Create heatmap data (lat, lon, weight)
        heat_data = []
        for _, disaster in filtered_data.iterrows():
            # Ensure all values are properly formatted
            lat = float(disaster['latitude'])
            lon = float(disaster['longitude'])
            weight = {'Low': 0.3, 'Medium': 0.6, 'High': 0.8, 'Critical': 1.0}[disaster['severity']]
            
            # Only add valid coordinates
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                heat_data.append([lat, lon, weight])
        
        # Add heatmap only if we have valid data
        if heat_data:
            HeatMap(
                heat_data,
                radius=20,
                blur=15,
                max_zoom=1,
                gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}
            ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Display the map
    map_data = st_folium(m, width=1200, height=600)
    
    # Statistics below the map
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Current View Statistics")
        st.metric("Total Events", len(filtered_data))
        st.metric("Critical Events", len(filtered_data[filtered_data['severity'] == 'Critical']))
        st.metric("Affected Population", f"{filtered_data['affected_population'].sum():,}")
    
    with col2:
        st.markdown("### 🎯 Most Affected Regions")
        if len(filtered_data) > 0:
            region_stats = filtered_data.groupby('location').agg({
                'affected_population': 'sum',
                'severity': lambda x: (x == 'Critical').sum()
            }).sort_values('affected_population', ascending=False).head(5)
            
            for region, stats in region_stats.iterrows():
                st.write(f"**{region}**")
                st.write(f"Population: {stats['affected_population']:,}")
                st.write(f"Critical events: {stats['severity']}")
                st.write("---")
    
    with col3:
        st.markdown("### 🔥 Recent High-Severity Events")
        recent_critical = filtered_data[
            filtered_data['severity'].isin(['High', 'Critical'])
        ].sort_values('timestamp', ascending=False).head(5)
        
        for _, event in recent_critical.iterrows():
            hours_ago = int((datetime.now() - event['timestamp']).total_seconds() / 3600)
            st.write(f"**{event['type']}** - {event['location']}")
            st.write(f"Severity: {event['severity']} | {hours_ago}h ago")
            st.write("---")
    
    # Legend
    st.markdown("### 🗂️ Map Legend")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Severity Colors:**
        - 🟢 Low Risk
        - 🟡 Medium Risk  
        - 🟠 High Risk
        - 🔴 Critical Risk
        """)
    
    with col2:
        st.markdown("""
        **Disaster Types:**
        - ⚡ Earthquake
        - 💧 Flood
        - 🌪️ Cyclone
        - 🔥 Wildfire
        - ☀️ Drought
        - ⛰️ Landslide
        """)