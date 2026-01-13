import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="🌪️ Disaster Analytics Dashboard",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🌪️ Real-Time Disaster & Weather Analytics Dashboard")
    st.markdown("### *Advanced Risk Intelligence & Impact Analysis*")
    
    # Sidebar navigation
    st.sidebar.title("🎛️ Navigation")
    page = st.sidebar.selectbox(
        "Select Dashboard",
        ["🏠 Executive Overview", "📊 Simple Analytics", "🌤️ Weather Data"]
    )
    
    # Generate sample data
    @st.cache_data
    def load_sample_data():
        np.random.seed(42)
        
        # Disaster data
        disaster_data = pd.DataFrame({
            'type': np.random.choice(['Earthquake', 'Flood', 'Cyclone', 'Wildfire'], 20),
            'severity': np.random.choice(['Low', 'Medium', 'High', 'Critical'], 20),
            'affected_population': np.random.randint(100, 50000, 20),
            'timestamp': [datetime.now() - timedelta(hours=np.random.randint(1, 72)) for _ in range(20)]
        })
        
        # Weather data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        weather_data = pd.DataFrame({
            'date': dates,
            'temperature': np.random.normal(25, 10, len(dates)),
            'humidity': np.random.uniform(30, 90, len(dates)),
            'wind_speed': np.random.uniform(5, 50, len(dates)),
            'rainfall': np.random.exponential(2, len(dates))
        })
        
        return disaster_data, weather_data
    
    disaster_data, weather_data = load_sample_data()
    
    if page == "🏠 Executive Overview":
        show_executive_overview(disaster_data, weather_data)
    elif page == "📊 Simple Analytics":
        show_simple_analytics(disaster_data)
    elif page == "🌤️ Weather Data":
        show_weather_data(weather_data)

def show_executive_overview(disaster_data, weather_data):
    st.markdown("## 🏠 Executive Overview Dashboard")
    
    # KPI Cards
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
        critical_count = len(disaster_data[disaster_data['severity'] == 'Critical'])
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #dc3545; margin: 0;">🚨 Critical Events</h3>
            <h1 style="color: white; margin: 10px 0;">{critical_count}</h1>
            <p style="color: #888; margin: 0;">High priority</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_affected = disaster_data['affected_population'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #ffc107; margin: 0;">👥 Total Affected</h3>
            <h1 style="color: white; margin: 10px 0;">{total_affected:,}</h1>
            <p style="color: #888; margin: 0;">People impacted</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_temp = weather_data['temperature'].iloc[-1]
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #17a2b8; margin: 0;">🌡️ Current Temp</h3>
            <h1 style="color: white; margin: 10px 0;">{avg_temp:.1f}°C</h1>
            <p style="color: #888; margin: 0;">Current weather</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Disaster Type Distribution")
        type_counts = disaster_data['type'].value_counts()
        fig = px.bar(x=type_counts.index, y=type_counts.values, 
                    title="Disasters by Type", color=type_counts.values,
                    color_continuous_scale='Reds')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            showlegend=False
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("### ⚠️ Severity Levels")
        severity_counts = disaster_data['severity'].value_counts()
        colors = {'Low': '#28a745', 'Medium': '#ffc107', 'High': '#fd7e14', 'Critical': '#dc3545'}
        fig = px.pie(values=severity_counts.values, names=severity_counts.index,
                    title="Risk Level Distribution",
                    color_discrete_map=colors)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white'
        )
        st.plotly_chart(fig, width='stretch')

def show_simple_analytics(disaster_data):
    st.markdown("## 📊 Simple Analytics")
    
    # Data table
    st.markdown("### 📋 Recent Disasters")
    st.dataframe(disaster_data.sort_values('timestamp', ascending=False), width='stretch')
    
    # Summary stats
    st.markdown("### 📈 Summary Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Disaster Counts by Type:**")
        st.write(disaster_data['type'].value_counts())
    
    with col2:
        st.write("**Severity Distribution:**")
        st.write(disaster_data['severity'].value_counts())

def show_weather_data(weather_data):
    st.markdown("## 🌤️ Weather Data")
    
    # Weather trends
    st.markdown("### 📈 Temperature Trend")
    fig = px.line(weather_data, x='date', y='temperature', 
                 title="Temperature Over Time",
                 color_discrete_sequence=['#ff6b6b'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    st.plotly_chart(fig, width='stretch')
    
    # Weather data table
    st.markdown("### 📊 Weather Data Table")
    st.dataframe(weather_data, width='stretch')

if __name__ == "__main__":
    main()