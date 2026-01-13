@echo off
echo 🌪️ Starting Disaster Analytics Dashboard...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import streamlit, plotly, pandas, numpy, sklearn, folium" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Some packages are missing. Installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install packages
        pause
        exit /b 1
    )
)

echo ✅ All dependencies are ready!
echo.
echo 🚀 Starting dashboard...
echo 📍 Dashboard will be available at: http://localhost:8501
echo 🔄 Press Ctrl+C to stop the dashboard
echo.

streamlit run app.py

pause