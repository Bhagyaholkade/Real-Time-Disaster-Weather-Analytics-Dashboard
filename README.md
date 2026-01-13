# 🌪️ Real-Time Disaster & Weather Analytics Dashboard

A comprehensive, interactive web-based analytics dashboard that tracks weather conditions and natural disasters, analyzes their impact severity, and provides visual insights and alerts to help users understand risk levels and trends.

## 🎯 Features

### 🏠 Executive Overview Dashboard
- Real-time KPI cards (Active disasters, High-risk regions, Weather severity index, Critical alerts)
- Interactive charts showing disaster frequency trends and type distribution
- Recent activity feed with severity-based alerts

### 🗺️ Live Disaster Map
- Interactive world map with disaster markers
- Color-coded severity indicators
- Heatmap overlay for high-risk zones
- Detailed popup information for each event
- Regional statistics and filtering options

### 🌤️ Weather Intelligence
- Current weather conditions with risk assessment
- 30-day weather trend analysis
- Extreme weather detection and alerts
- Comprehensive risk scoring system

### 📊 Impact Analytics
- Population impact analysis
- Regional comparison charts
- Economic impact estimation
- Historical vs current trend analysis
- Detailed impact metrics and insights

### 🚨 Alerts & Notifications
- Real-time critical and high-priority alerts
- Regional risk assessment
- Alert timeline and logging
- Customizable notification settings

### 🤖 ML Risk Prediction
- Machine learning models for risk classification
- Feature importance analysis
- Real-time risk prediction interface
- Model performance metrics and insights

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS styling
- **Visualization**: Plotly, Folium maps
- **Machine Learning**: Scikit-learn (Random Forest, Logistic Regression)
- **Data Processing**: Pandas, NumPy
- **Styling**: Dark theme with glassmorphism effects

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd disaster-analytics-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard**
   Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
disaster-analytics-dashboard/
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── pages/                          # Individual page components
│   ├── executive_overview.py       # Executive dashboard
│   ├── disaster_map.py            # Interactive map
│   ├── weather_intelligence.py    # Weather analysis
│   ├── impact_analytics.py        # Impact analysis
│   ├── alerts_notifications.py    # Alerts system
│   └── ml_prediction.py           # ML predictions
└── README.md                       # Project documentation
```

## 🎨 Design Features

- **Dark Theme**: Professional control-room style interface
- **Glassmorphism**: Modern translucent card designs
- **Color Coding**: Red/Amber/Green alert system
- **Responsive Layout**: Works on desktop and mobile
- **Smooth Animations**: Pulsing indicators and hover effects
- **Interactive Elements**: Clickable maps, filterable data

## 📊 Data Sources

Currently uses mock data for demonstration. In production, integrate with:
- Weather APIs (OpenWeatherMap, AccuWeather)
- Disaster databases (USGS, NOAA, UN OCHA)
- Government emergency services
- Satellite imagery services

## 🤖 Machine Learning Models

- **Random Forest Classifier**: Primary risk prediction model
- **Feature Engineering**: Weather patterns, historical data, location factors
- **Risk Classification**: Safe, Warning, Danger levels
- **Real-time Prediction**: Interactive parameter adjustment

## 🔧 Customization

### Adding New Data Sources
1. Modify the `load_data()` function in `app.py`
2. Update data generation functions for real API integration
3. Adjust feature engineering in ML models

### Styling Modifications
- Edit CSS in the `st.markdown()` sections
- Modify color schemes in the style variables
- Adjust card layouts and animations

### New Features
- Add new pages in the `pages/` directory
- Import and route in `app.py`
- Follow the existing pattern for consistency

## 📈 Performance Considerations

- Data caching with Streamlit's `@st.cache_data`
- Efficient data processing with Pandas
- Optimized visualizations with Plotly
- Lazy loading for large datasets

## 🔒 Security Notes

- Input validation for user parameters
- Secure API key management (use environment variables)
- Data sanitization for external sources
- Rate limiting for API calls

## 🚀 Deployment Options

### Streamlit Cloud
```bash
# Push to GitHub and deploy via Streamlit Cloud
streamlit run app.py
```

### Docker
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Heroku
```bash
# Add Procfile: web: streamlit run app.py --server.port=$PORT
git push heroku main
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Plotly for interactive visualizations
- OpenStreetMap for map data
- Scikit-learn for ML capabilities

## 📞 Support

For questions or support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for disaster preparedness and community safety**