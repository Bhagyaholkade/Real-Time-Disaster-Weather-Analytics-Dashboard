#!/bin/bash

echo "🌪️ Starting Disaster Analytics Dashboard..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    echo "Please install Python and try again"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import streamlit, plotly, pandas, numpy, sklearn, folium" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ Some packages are missing. Installing..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install packages"
        exit 1
    fi
fi

echo "✅ All dependencies are ready!"
echo
echo "🚀 Starting dashboard..."
echo "📍 Dashboard will be available at: http://localhost:8501"
echo "🔄 Press Ctrl+C to stop the dashboard"
echo

streamlit run app.py