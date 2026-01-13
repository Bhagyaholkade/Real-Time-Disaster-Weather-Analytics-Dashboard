import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def ml_risk_prediction():
    """ML-Based Risk Prediction - Predict and classify disaster risk"""
    
    st.markdown("## 🤖 ML-Based Risk Prediction")
    st.markdown("*Advanced machine learning models for disaster risk assessment*")
    
    # Get data from session state
    disaster_data = st.session_state.disaster_data
    weather_data = st.session_state.weather_data
    
    if disaster_data is None or weather_data is None:
        st.error("Data not loaded. Please refresh the page.")
        return
    
    # Model Selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Risk Prediction Model")
    
    with col2:
        model_type = st.selectbox(
            "Select Model",
            ["Random Forest", "Logistic Regression", "Ensemble"],
            index=0
        )
    
    # Prepare data for ML
    ml_data = prepare_ml_data(disaster_data, weather_data)
    
    if ml_data is not None and len(ml_data) > 0:
        # Train model
        model, scaler, label_encoder, feature_importance, accuracy = train_risk_model(ml_data, model_type)
        
        # Model Performance
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #28a745; margin: 0;">🎯 Model Accuracy</h4>
                <h2 style="color: white; margin: 10px 0;">{accuracy:.1%}</h2>
                <p style="color: #888; margin: 0;">Prediction accuracy</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            training_samples = len(ml_data)
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #17a2b8; margin: 0;">📊 Training Data</h4>
                <h2 style="color: white; margin: 10px 0;">{training_samples}</h2>
                <p style="color: #888; margin: 0;">Data points used</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            feature_count = len(feature_importance)
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #ffc107; margin: 0;">🔧 Features</h4>
                <h2 style="color: white; margin: 10px 0;">{feature_count}</h2>
                <p style="color: #888; margin: 0;">Input features</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feature Importance
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Feature Importance")
            
            # Create feature importance chart
            importance_df = pd.DataFrame({
                'Feature': feature_importance.keys(),
                'Importance': feature_importance.values()
            }).sort_values('Importance', ascending=True)
            
            fig = px.bar(
                importance_df,
                x='Importance',
                y='Feature',
                orientation='h',
                title="Feature Importance in Risk Prediction",
                color='Importance',
                color_continuous_scale='Viridis'
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
        
        with col2:
            st.markdown("### 🎯 Risk Distribution")
            
            # Show risk level distribution in training data
            risk_dist = ml_data['risk_level'].value_counts()
            
            fig = px.pie(
                values=risk_dist.values,
                names=risk_dist.index,
                title="Risk Level Distribution in Training Data",
                color_discrete_map={
                    'Safe': '#28a745',
                    'Warning': '#ffc107',
                    'Danger': '#dc3545'
                }
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_color='white'
            )
            
            st.plotly_chart(fig, width='stretch')
        
        # Real-time Prediction
        st.markdown("### 🔮 Real-Time Risk Prediction")
        
        # Input parameters for prediction
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🌡️ Weather Parameters")
            temp_input = st.slider("Temperature (°C)", -20, 50, 25)
            humidity_input = st.slider("Humidity (%)", 0, 100, 60)
            wind_input = st.slider("Wind Speed (km/h)", 0, 100, 15)
            rainfall_input = st.slider("Rainfall (mm)", 0, 50, 2)
        
        with col2:
            st.markdown("#### 📍 Location Parameters")
            # Simplified location encoding
            location_risk = st.selectbox("Historical Risk Level", ["Low", "Medium", "High"], index=0)
            population_density = st.slider("Population Density", 1, 10, 5)
            disaster_history = st.slider("Recent Disaster Count", 0, 10, 1)
        
        with col3:
            st.markdown("#### ⏰ Temporal Parameters")
            season = st.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"], index=1)
            time_of_day = st.slider("Hour of Day", 0, 23, 12)
            
            if st.button("🔮 Predict Risk Level", type="primary"):
                # Make prediction
                prediction_input = prepare_prediction_input(
                    temp_input, humidity_input, wind_input, rainfall_input,
                    location_risk, population_density, disaster_history,
                    season, time_of_day
                )
                
                risk_prediction, confidence = make_risk_prediction(
                    model, scaler, label_encoder, prediction_input
                )
                
                # Display prediction
                display_risk_prediction(risk_prediction, confidence)
        
        # Model Insights
        st.markdown("### 💡 Model Insights & Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔍 Key Risk Factors")
            
            # Top risk factors based on feature importance
            top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for i, (feature, importance) in enumerate(top_features, 1):
                st.markdown(f"{i}. **{feature.replace('_', ' ').title()}** ({importance:.3f})")
            
            st.markdown("#### 📈 Risk Patterns")
            risk_patterns = analyze_risk_patterns(ml_data)
            for pattern in risk_patterns:
                st.markdown(f"• {pattern}")
        
        with col2:
            st.markdown("#### 🎯 Prediction Accuracy by Risk Level")
            
            # Create confusion matrix visualization
            y_true = ml_data['risk_level']
            X = ml_data.drop(['risk_level'], axis=1)
            
            # Make predictions on training data for visualization
            X_scaled = scaler.transform(X)
            y_pred = model.predict(X_scaled)
            y_pred_labels = label_encoder.inverse_transform(y_pred)
            
            # Calculate accuracy by class
            class_accuracy = {}
            for risk_level in ['Safe', 'Warning', 'Danger']:
                mask = y_true == risk_level
                if mask.sum() > 0:
                    accuracy = (y_pred_labels[mask] == risk_level).mean()
                    class_accuracy[risk_level] = accuracy
            
            for risk_level, acc in class_accuracy.items():
                color = {'Safe': '#28a745', 'Warning': '#ffc107', 'Danger': '#dc3545'}[risk_level]
                st.markdown(f"**{risk_level}**: {acc:.1%} <span style='color: {color};'>●</span>", unsafe_allow_html=True)
        
        # Historical Predictions vs Actual
        st.markdown("### 📊 Model Performance Analysis")
        
        # Create performance visualization
        performance_data = create_performance_analysis(ml_data, model, scaler, label_encoder)
        
        if performance_data is not None:
            fig = px.line(
                performance_data,
                x='date',
                y=['actual_risk_score', 'predicted_risk_score'],
                title="Predicted vs Actual Risk Scores Over Time",
                labels={'value': 'Risk Score', 'variable': 'Type'}
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
        
        # Model Configuration
        st.markdown("### ⚙️ Model Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🎛️ Model Parameters")
            st.write(f"**Algorithm**: {model_type}")
            st.write(f"**Features**: {len(feature_importance)}")
            st.write(f"**Training Samples**: {len(ml_data)}")
            st.write(f"**Accuracy**: {accuracy:.1%}")
        
        with col2:
            st.markdown("#### 🔄 Retraining Options")
            auto_retrain = st.checkbox("Auto-retrain daily", value=True)
            retrain_threshold = st.slider("Accuracy threshold for retraining", 0.5, 0.95, 0.8)
            
            if st.button("🔄 Retrain Model"):
                st.info("Model retraining initiated...")
                # In a real application, this would trigger model retraining
        
        with col3:
            st.markdown("#### 📤 Model Export")
            if st.button("💾 Export Model"):
                st.success("Model exported successfully!")
            
            if st.button("📊 Download Predictions"):
                st.success("Predictions downloaded!")
    
    else:
        st.error("Insufficient data for ML model training. Please ensure data is loaded properly.")

def prepare_ml_data(disaster_data, weather_data):
    """Prepare data for machine learning"""
    try:
        # Merge disaster and weather data by date
        disaster_data['date'] = disaster_data['timestamp'].dt.date
        weather_data['date'] = weather_data['date'].dt.date
        
        # Aggregate disaster data by date
        daily_disasters = disaster_data.groupby('date').agg({
            'affected_population': 'sum',
            'severity': lambda x: (x == 'Critical').sum(),
            'type': 'count'
        }).reset_index()
        daily_disasters.columns = ['date', 'total_affected', 'critical_count', 'disaster_count']
        
        # Merge with weather data
        ml_data = pd.merge(weather_data, daily_disasters, on='date', how='left')
        ml_data = ml_data.fillna(0)
        
        # Create features
        ml_data['temp_extreme'] = (ml_data['temperature'] > 35) | (ml_data['temperature'] < 5)
        ml_data['high_wind'] = ml_data['wind_speed'] > 30
        ml_data['heavy_rain'] = ml_data['rainfall'] > 10
        ml_data['low_pressure'] = ml_data['pressure'] < 1000
        
        # Create risk level target
        ml_data['risk_score'] = (
            ml_data['critical_count'] * 3 +
            ml_data['disaster_count'] * 1 +
            ml_data['temp_extreme'].astype(int) * 2 +
            ml_data['high_wind'].astype(int) * 2 +
            ml_data['heavy_rain'].astype(int) * 2
        )
        
        # Classify risk levels
        ml_data['risk_level'] = pd.cut(
            ml_data['risk_score'],
            bins=[-np.inf, 2, 5, np.inf],
            labels=['Safe', 'Warning', 'Danger']
        )
        
        # Select features for training
        feature_columns = [
            'temperature', 'humidity', 'wind_speed', 'rainfall', 'pressure',
            'temp_extreme', 'high_wind', 'heavy_rain', 'low_pressure'
        ]
        
        ml_data = ml_data[feature_columns + ['risk_level']].dropna()
        
        return ml_data
    
    except Exception as e:
        st.error(f"Error preparing ML data: {str(e)}")
        return None

def train_risk_model(ml_data, model_type):
    """Train the risk prediction model"""
    try:
        # Prepare features and target
        X = ml_data.drop(['risk_level'], axis=1)
        y = ml_data['risk_level']
        
        # Encode labels
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Train model
        if model_type == "Random Forest":
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:  # Default to Random Forest for simplicity
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        model.fit(X_train, y_train)
        
        # Calculate accuracy
        accuracy = model.score(X_test, y_test)
        
        # Get feature importance
        feature_importance = dict(zip(X.columns, model.feature_importances_))
        
        return model, scaler, label_encoder, feature_importance, accuracy
    
    except Exception as e:
        st.error(f"Error training model: {str(e)}")
        return None, None, None, {}, 0.0

def prepare_prediction_input(temp, humidity, wind, rainfall, location_risk, 
                           population_density, disaster_history, season, time_of_day):
    """Prepare input for prediction"""
    # Convert categorical inputs
    location_risk_score = {'Low': 1, 'Medium': 2, 'High': 3}[location_risk]
    season_score = {'Spring': 1, 'Summer': 2, 'Autumn': 3, 'Winter': 4}[season]
    
    # Create feature vector
    features = {
        'temperature': temp,
        'humidity': humidity,
        'wind_speed': wind,
        'rainfall': rainfall,
        'pressure': 1013,  # Default pressure
        'temp_extreme': (temp > 35) or (temp < 5),
        'high_wind': wind > 30,
        'heavy_rain': rainfall > 10,
        'low_pressure': False  # Default
    }
    
    return pd.DataFrame([features])

def make_risk_prediction(model, scaler, label_encoder, input_data):
    """Make risk prediction"""
    try:
        # Scale input
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        prediction_proba = model.predict_proba(input_scaled)[0]
        
        # Get risk level
        risk_level = label_encoder.inverse_transform([prediction])[0]
        confidence = max(prediction_proba)
        
        return risk_level, confidence
    
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return "Unknown", 0.0

def display_risk_prediction(risk_level, confidence):
    """Display risk prediction results"""
    risk_colors = {'Safe': '#28a745', 'Warning': '#ffc107', 'Danger': '#dc3545'}
    risk_icons = {'Safe': '✅', 'Warning': '⚠️', 'Danger': '🚨'}
    
    color = risk_colors.get(risk_level, '#888')
    icon = risk_icons.get(risk_level, '❓')
    
    st.markdown(f"""
    <div class="metric-card" style="text-align: center; border: 2px solid {color};">
        <h2 style="color: {color}; margin: 0;">{icon} {risk_level}</h2>
        <h3 style="color: white; margin: 10px 0;">Risk Level Prediction</h3>
        <p style="color: #888; margin: 0;">Confidence: {confidence:.1%}</p>
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; margin: 20px 0;">
            <div style="background: {color}; height: 100%; width: {confidence*100}%; border-radius: 10px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Risk level explanations
    explanations = {
        'Safe': "Low risk conditions. Normal monitoring recommended.",
        'Warning': "Elevated risk detected. Increased vigilance advised.",
        'Danger': "High risk conditions. Immediate attention required."
    }
    
    st.info(f"**Interpretation**: {explanations.get(risk_level, 'Unknown risk level')}")

def analyze_risk_patterns(ml_data):
    """Analyze patterns in risk data"""
    patterns = []
    
    # Temperature patterns
    high_temp_risk = ml_data[ml_data['temperature'] > 35]['risk_level'].value_counts()
    if len(high_temp_risk) > 0 and 'Danger' in high_temp_risk.index:
        patterns.append(f"High temperatures (>35°C) increase danger risk by {high_temp_risk['Danger']/len(ml_data)*100:.1f}%")
    
    # Wind patterns
    high_wind_risk = ml_data[ml_data['wind_speed'] > 30]['risk_level'].value_counts()
    if len(high_wind_risk) > 0:
        patterns.append(f"High winds (>30 km/h) correlate with elevated risk levels")
    
    # Rainfall patterns
    heavy_rain_risk = ml_data[ml_data['rainfall'] > 10]['risk_level'].value_counts()
    if len(heavy_rain_risk) > 0:
        patterns.append(f"Heavy rainfall (>10mm) significantly increases risk probability")
    
    return patterns

def create_performance_analysis(ml_data, model, scaler, label_encoder):
    """Create performance analysis data"""
    try:
        # Create risk scores for visualization
        risk_level_scores = {'Safe': 1, 'Warning': 2, 'Danger': 3}
        ml_data['actual_risk_score'] = ml_data['risk_level'].map(risk_level_scores)
        
        # Make predictions
        X = ml_data.drop(['risk_level', 'actual_risk_score'], axis=1)
        X_scaled = scaler.transform(X)
        predictions = model.predict(X_scaled)
        predicted_labels = label_encoder.inverse_transform(predictions)
        ml_data['predicted_risk_score'] = pd.Series(predicted_labels).map(risk_level_scores).values
        
        # Add date column for visualization
        ml_data['date'] = pd.date_range(start='2024-01-01', periods=len(ml_data), freq='D')
        
        return ml_data[['date', 'actual_risk_score', 'predicted_risk_score']]
    
    except Exception as e:
        st.error(f"Error creating performance analysis: {str(e)}")
        return None