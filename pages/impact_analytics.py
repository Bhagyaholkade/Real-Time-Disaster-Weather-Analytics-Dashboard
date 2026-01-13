import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def impact_analytics():
    """Disaster Impact Analytics - Turn data into insights"""
    
    st.markdown("## 📊 Disaster Impact Analytics")
    st.markdown("*Advanced impact analysis and population risk assessment*")
    
    # Get data from session state
    disaster_data = st.session_state.disaster_data
    
    if disaster_data is None:
        st.error("Disaster data not loaded. Please refresh the page.")
        return
    
    # Calculate impact metrics
    total_affected = disaster_data['affected_population'].sum()
    avg_severity = calculate_severity_index(disaster_data)
    most_affected_region = disaster_data.groupby('location')['affected_population'].sum().idxmax()
    
    # Impact Overview Cards
    st.markdown("### 🎯 Impact Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #ff6b6b; margin: 0;">👥 Total Affected</h4>
            <h2 style="color: white; margin: 10px 0;">{total_affected:,}</h2>
            <p style="color: #888; margin: 0;">People impacted</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #ffc107; margin: 0;">📈 Severity Index</h4>
            <h2 style="color: white; margin: 10px 0;">{avg_severity:.1f}/10</h2>
            <p style="color: #888; margin: 0;">Average severity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        economic_impact = estimate_economic_impact(disaster_data)
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #17a2b8; margin: 0;">💰 Economic Impact</h4>
            <h2 style="color: white; margin: 10px 0;">${economic_impact:.1f}M</h2>
            <p style="color: #888; margin: 0;">Estimated losses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #28a745; margin: 0;">🏆 Most Affected</h4>
            <h2 style="color: white; margin: 10px 0; font-size: 1.2em;">{most_affected_region.split(',')[0]}</h2>
            <p style="color: #888; margin: 0;">Region</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Impact Analysis Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Regional Impact Comparison")
        
        # Group by region and calculate impact metrics
        regional_impact = disaster_data.groupby('location').agg({
            'affected_population': 'sum',
            'severity': lambda x: calculate_severity_score(x),
            'type': 'count'
        }).reset_index()
        regional_impact.columns = ['Region', 'Affected_Population', 'Severity_Score', 'Event_Count']
        
        # Create bubble chart
        fig = px.scatter(
            regional_impact,
            x='Event_Count',
            y='Affected_Population',
            size='Severity_Score',
            color='Severity_Score',
            hover_name='Region',
            title="Regional Impact Analysis",
            labels={
                'Event_Count': 'Number of Events',
                'Affected_Population': 'Affected Population',
                'Severity_Score': 'Severity Score'
            },
            color_continuous_scale='Reds'
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
        st.markdown("### 📊 Disaster Type Impact")
        
        # Impact by disaster type
        type_impact = disaster_data.groupby('type').agg({
            'affected_population': 'sum',
            'severity': lambda x: calculate_severity_score(x)
        }).reset_index()
        
        fig = px.bar(
            type_impact,
            x='type',
            y='affected_population',
            color='severity',
            title="Population Impact by Disaster Type",
            labels={
                'type': 'Disaster Type',
                'affected_population': 'Affected Population',
                'severity': 'Avg Severity'
            },
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
    
    # Historical vs Current Trends
    st.markdown("### 📈 Historical vs Current Disaster Trends")
    
    # Create time-based analysis
    disaster_data['date'] = disaster_data['timestamp'].dt.date
    daily_impact = disaster_data.groupby('date').agg({
        'affected_population': 'sum',
        'type': 'count',
        'severity': lambda x: calculate_severity_score(x)
    }).reset_index()
    daily_impact.columns = ['Date', 'Affected_Population', 'Event_Count', 'Severity_Score']
    
    # Create subplot with multiple metrics
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Daily Affected Population', 'Event Frequency', 'Severity Trend', 'Cumulative Impact'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Daily affected population
    fig.add_trace(
        go.Scatter(
            x=daily_impact['Date'],
            y=daily_impact['Affected_Population'],
            mode='lines+markers',
            name='Affected Population',
            line=dict(color='#ff6b6b', width=2),
            fill='tonexty'
        ),
        row=1, col=1
    )
    
    # Event frequency
    fig.add_trace(
        go.Bar(
            x=daily_impact['Date'],
            y=daily_impact['Event_Count'],
            name='Event Count',
            marker_color='#17a2b8',
            opacity=0.7
        ),
        row=1, col=2
    )
    
    # Severity trend
    fig.add_trace(
        go.Scatter(
            x=daily_impact['Date'],
            y=daily_impact['Severity_Score'],
            mode='lines+markers',
            name='Severity Score',
            line=dict(color='#ffc107', width=2)
        ),
        row=2, col=1
    )
    
    # Cumulative impact
    daily_impact['Cumulative_Impact'] = daily_impact['Affected_Population'].cumsum()
    fig.add_trace(
        go.Scatter(
            x=daily_impact['Date'],
            y=daily_impact['Cumulative_Impact'],
            mode='lines',
            name='Cumulative Impact',
            line=dict(color='#28a745', width=3),
            fill='tonexty'
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
    
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig, width='stretch')
    
    # Detailed Impact Table
    st.markdown("### 📋 Detailed Impact Analysis")
    
    # Create detailed analysis table
    detailed_analysis = disaster_data.groupby(['location', 'type']).agg({
        'affected_population': ['sum', 'mean'],
        'severity': lambda x: calculate_severity_score(x),
        'timestamp': 'count'
    }).round(2)
    
    # Flatten column names
    detailed_analysis.columns = ['Total_Affected', 'Avg_Affected', 'Severity_Score', 'Event_Count']
    detailed_analysis = detailed_analysis.reset_index()
    
    # Add risk classification
    detailed_analysis['Risk_Level'] = detailed_analysis['Severity_Score'].apply(classify_risk_level)
    detailed_analysis['Economic_Impact'] = detailed_analysis['Total_Affected'] * 0.001  # Simplified calculation
    
    # Style the dataframe
    styled_df = detailed_analysis.style.format({
        'Total_Affected': '{:,.0f}',
        'Avg_Affected': '{:,.0f}',
        'Severity_Score': '{:.1f}',
        'Economic_Impact': '${:.1f}M'
    }).background_gradient(subset=['Severity_Score'], cmap='Reds')
    
    st.dataframe(styled_df, width='stretch')
    
    # Impact Insights
    st.markdown("### 💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔍 Critical Findings")
        
        # Generate insights
        insights = generate_impact_insights(disaster_data)
        for insight in insights:
            st.markdown(f"• {insight}")
    
    with col2:
        st.markdown("#### 📊 Statistical Summary")
        
        stats = {
            'Most Common Disaster': disaster_data['type'].mode().iloc[0],
            'Highest Single Impact': f"{disaster_data['affected_population'].max():,} people",
            'Average Event Severity': f"{avg_severity:.1f}/10",
            'Most Vulnerable Region': most_affected_region,
            'Peak Activity Period': disaster_data.groupby(disaster_data['timestamp'].dt.hour)['type'].count().idxmax()
        }
        
        for key, value in stats.items():
            st.markdown(f"**{key}:** {value}")

def calculate_severity_index(disaster_data):
    """Calculate average severity index (0-10 scale)"""
    severity_map = {'Low': 2, 'Medium': 5, 'High': 8, 'Critical': 10}
    return disaster_data['severity'].map(severity_map).mean()

def calculate_severity_score(severity_series):
    """Calculate severity score for a series"""
    severity_map = {'Low': 2, 'Medium': 5, 'High': 8, 'Critical': 10}
    return severity_series.map(severity_map).mean()

def estimate_economic_impact(disaster_data):
    """Estimate economic impact in millions USD"""
    # Simplified calculation based on affected population and severity
    severity_multiplier = {'Low': 0.001, 'Medium': 0.005, 'High': 0.01, 'Critical': 0.02}
    
    total_impact = 0
    for _, row in disaster_data.iterrows():
        multiplier = severity_multiplier[row['severity']]
        impact = row['affected_population'] * multiplier
        total_impact += impact
    
    return total_impact

def classify_risk_level(severity_score):
    """Classify risk level based on severity score"""
    if severity_score < 3:
        return 'Low'
    elif severity_score < 6:
        return 'Medium'
    elif severity_score < 8:
        return 'High'
    else:
        return 'Critical'

def generate_impact_insights(disaster_data):
    """Generate key insights from disaster data"""
    insights = []
    
    # Most affected disaster type
    most_common = disaster_data['type'].value_counts().iloc[0]
    most_common_type = disaster_data['type'].value_counts().index[0]
    insights.append(f"{most_common_type}s are the most frequent disasters ({most_common} events)")
    
    # Severity distribution
    critical_pct = (disaster_data['severity'] == 'Critical').mean() * 100
    insights.append(f"{critical_pct:.1f}% of disasters are classified as Critical severity")
    
    # Population impact
    total_affected = disaster_data['affected_population'].sum()
    insights.append(f"Total of {total_affected:,} people affected across all events")
    
    # Regional concentration
    top_region = disaster_data.groupby('location')['affected_population'].sum().idxmax()
    insights.append(f"{top_region} shows highest population impact concentration")
    
    # Temporal pattern
    recent_trend = len(disaster_data[disaster_data['timestamp'] > datetime.now() - timedelta(days=7)])
    insights.append(f"{recent_trend} disasters occurred in the past week")
    
    return insights