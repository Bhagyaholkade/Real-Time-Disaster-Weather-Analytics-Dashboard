import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import folium
from streamlit_folium import st_folium

# Import page modules
from pages.executive_overview import executive_overview
from pages.disaster_map import live_disaster_map
from pages.weather_intelligence import weather_intelligence
from pages.impact_analytics import impact_analytics
from pages.alerts_notifications import alerts_notifications
from pages.ml_prediction import ml_risk_prediction

# Page configuration
st.set_page_config(
    page_title="🌪️ Disaster Analytics Dashboard",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and modern styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 10px 0;
    }
    
    .alert-high {
        background: rgba(220, 53, 69, 0.2);
        border-left: 4px solid #dc3545;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .alert-medium {
        background: rgba(255, 193, 7, 0.2);
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .alert-low {
        background: rgba(40, 167, 69, 0.2);
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'disaster_data' not in st.session_state:
    st.session_state.disaster_data = None
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None

def main():
    st.title("🌪️ Real-Time Disaster & Weather Analytics Dashboard")
    st.markdown("### *Advanced Risk Intelligence & Impact Analysis*")
    
    # Sidebar navigation
    st.sidebar.title("🎛️ Navigation")
    page = st.sidebar.selectbox(
        "Select Dashboard",
        ["🏠 Executive Overview", "🗺️ Live Disaster Map", "🌤️ Weather Intelligence", 
         "📊 Impact Analytics", "🚨 Alerts & Notifications", "🤖 ML Risk Prediction"]
    )
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=False)
    if auto_refresh:
        st.rerun()
    
    # Load data
    load_data()
    
    # Route to selected page
    if page == "🏠 Executive Overview":
        executive_overview()
    elif page == "🗺️ Live Disaster Map":
        live_disaster_map()
    elif page == "🌤️ Weather Intelligence":
        weather_intelligence()
    elif page == "📊 Impact Analytics":
        impact_analytics()
    elif page == "🚨 Alerts & Notifications":
        alerts_notifications()
    elif page == "🤖 ML Risk Prediction":
        ml_risk_prediction()

def load_data():
    """Load and cache disaster and weather data"""
    # Generate mock data for demonstration
    # In production, this would fetch from real APIs
    
    if st.session_state.disaster_data is None:
        st.session_state.disaster_data = generate_mock_disaster_data()
    
    if st.session_state.weather_data is None:
        st.session_state.weather_data = generate_mock_weather_data()

def generate_mock_disaster_data():
    """Generate realistic mock disaster data"""
    np.random.seed(42)
    
    disaster_types = ['Earthquake', 'Flood', 'Cyclone', 'Wildfire', 'Drought', 'Landslide']
    severities = ['Low', 'Medium', 'High', 'Critical']
    
    # Generate coordinates for various global locations
    locations = [
        {'name': 'California, USA', 'lat': 36.7783, 'lon': -119.4179},
        {'name': 'Tokyo, Japan', 'lat': 35.6762, 'lon': 139.6503},
        {'name': 'Mumbai, India', 'lat': 19.0760, 'lon': 72.8777},
        {'name': 'Sydney, Australia', 'lat': -33.8688, 'lon': 151.2093},
        {'name': 'London, UK', 'lat': 51.5074, 'lon': -0.1278},
        {'name': 'São Paulo, Brazil', 'lat': -23.5505, 'lon': -46.6333},
        {'name': 'Cairo, Egypt', 'lat': 30.0444, 'lon': 31.2357},
        {'name': 'Jakarta, Indonesia', 'lat': -6.2088, 'lon': 106.8456},
    ]
    
    data = []
    for i in range(50):
        location = np.random.choice(locations)
        disaster_type = np.random.choice(disaster_types)
        severity = np.random.choice(severities, p=[0.4, 0.3, 0.2, 0.1])
        
        # Add some noise to coordinates
        lat = location['lat'] + np.random.normal(0, 2)
        lon = location['lon'] + np.random.normal(0, 2)
        
        timestamp = datetime.now() - timedelta(
            hours=np.random.randint(0, 72),
            minutes=np.random.randint(0, 60)
        )
        
        data.append({
            'id': i,
            'type': disaster_type,
            'severity': severity,
            'latitude': lat,
            'longitude': lon,
            'location': location['name'],
            'timestamp': timestamp,
            'affected_population': np.random.randint(100, 50000),
            'magnitude': np.random.uniform(1.0, 9.0) if disaster_type == 'Earthquake' else np.random.uniform(1.0, 5.0)
        })
    
    return pd.DataFrame(data)

def generate_mock_weather_data():
    """Generate realistic mock weather data"""
    np.random.seed(42)
    
    # Generate weather data for the last 30 days
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    data = []
    for date in dates:
        data.append({
            'date': date,
            'temperature': np.random.normal(25, 10),
            'humidity': np.random.uniform(30, 90),
            'wind_speed': np.random.uniform(5, 50),
            'rainfall': np.random.exponential(2),
            'pressure': np.random.normal(1013, 20),
            'uv_index': np.random.uniform(1, 11)
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    main()