#!/usr/bin/env python3
"""
Test script for the Disaster Analytics Dashboard
Run this to verify all components are working correctly
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import pandas as pd
        import numpy as np
        print("✅ Pandas and NumPy imported successfully")
    except ImportError as e:
        print(f"❌ Pandas/NumPy import failed: {e}")
        return False
    
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler
        print("✅ Scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ Scikit-learn import failed: {e}")
        return False
    
    try:
        import folium
        from streamlit_folium import st_folium
        print("✅ Folium imported successfully")
    except ImportError as e:
        print(f"❌ Folium import failed: {e}")
        return False
    
    return True

def test_data_generation():
    """Test data generation functions"""
    print("\n🧪 Testing data generation...")
    
    try:
        # Import the main app module
        sys.path.append('.')
        from app import generate_mock_disaster_data, generate_mock_weather_data
        
        # Test disaster data generation
        disaster_data = generate_mock_disaster_data()
        assert isinstance(disaster_data, pd.DataFrame), "Disaster data should be a DataFrame"
        assert len(disaster_data) > 0, "Disaster data should not be empty"
        assert 'type' in disaster_data.columns, "Disaster data should have 'type' column"
        assert 'severity' in disaster_data.columns, "Disaster data should have 'severity' column"
        print(f"✅ Disaster data generated: {len(disaster_data)} records")
        
        # Test weather data generation
        weather_data = generate_mock_weather_data()
        assert isinstance(weather_data, pd.DataFrame), "Weather data should be a DataFrame"
        assert len(weather_data) > 0, "Weather data should not be empty"
        assert 'temperature' in weather_data.columns, "Weather data should have 'temperature' column"
        assert 'humidity' in weather_data.columns, "Weather data should have 'humidity' column"
        print(f"✅ Weather data generated: {len(weather_data)} records")
        
        return True
    
    except Exception as e:
        print(f"❌ Data generation test failed: {e}")
        return False

def test_page_imports():
    """Test if all page modules can be imported"""
    print("\n🧪 Testing page imports...")
    
    try:
        from pages.executive_overview import executive_overview
        print("✅ Executive overview page imported")
    except ImportError as e:
        print(f"❌ Executive overview import failed: {e}")
        return False
    
    try:
        from pages.disaster_map import live_disaster_map
        print("✅ Disaster map page imported")
    except ImportError as e:
        print(f"❌ Disaster map import failed: {e}")
        return False
    
    try:
        from pages.weather_intelligence import weather_intelligence
        print("✅ Weather intelligence page imported")
    except ImportError as e:
        print(f"❌ Weather intelligence import failed: {e}")
        return False
    
    try:
        from pages.impact_analytics import impact_analytics
        print("✅ Impact analytics page imported")
    except ImportError as e:
        print(f"❌ Impact analytics import failed: {e}")
        return False
    
    try:
        from pages.alerts_notifications import alerts_notifications
        print("✅ Alerts notifications page imported")
    except ImportError as e:
        print(f"❌ Alerts notifications import failed: {e}")
        return False
    
    try:
        from pages.ml_prediction import ml_risk_prediction
        print("✅ ML prediction page imported")
    except ImportError as e:
        print(f"❌ ML prediction import failed: {e}")
        return False
    
    return True

def test_ml_functionality():
    """Test ML model functionality"""
    print("\n🧪 Testing ML functionality...")
    
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        
        # Create sample data
        np.random.seed(42)
        X = np.random.rand(100, 5)
        y = np.random.choice(['Safe', 'Warning', 'Danger'], 100)
        
        # Test label encoding
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        print("✅ Label encoding works")
        
        # Test scaling
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        print("✅ Feature scaling works")
        
        # Test model training
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_scaled, y_encoded)
        print("✅ Model training works")
        
        # Test prediction
        prediction = model.predict(X_scaled[:1])
        print("✅ Model prediction works")
        
        return True
    
    except Exception as e:
        print(f"❌ ML functionality test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'pages/executive_overview.py',
        'pages/disaster_map.py',
        'pages/weather_intelligence.py',
        'pages/impact_analytics.py',
        'pages/alerts_notifications.py',
        'pages/ml_prediction.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def run_all_tests():
    """Run all tests"""
    print("🌪️ Disaster Analytics Dashboard - Test Suite")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Package Imports", test_imports),
        ("Page Imports", test_page_imports),
        ("Data Generation", test_data_generation),
        ("ML Functionality", test_ml_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The dashboard is ready to run.")
        print("🚀 Run 'streamlit run app.py' to start the dashboard.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)