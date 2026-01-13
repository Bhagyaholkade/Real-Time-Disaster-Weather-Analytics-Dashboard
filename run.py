#!/usr/bin/env python3
"""
Quick start script for the Disaster Analytics Dashboard
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import plotly
        import pandas
        import numpy
        import sklearn
        import folium
        print("✅ All required packages are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        return False

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        return False

def run_dashboard():
    """Run the Streamlit dashboard"""
    print("🚀 Starting the Disaster Analytics Dashboard...")
    print("📍 Dashboard will be available at: http://localhost:8501")
    print("🔄 Press Ctrl+C to stop the dashboard")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped. Thank you for using the Disaster Analytics Dashboard!")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install requirements first.")

def main():
    """Main function"""
    print("🌪️ Disaster Analytics Dashboard - Quick Start")
    print("=" * 50)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ app.py not found!")
        return
    
    # Check requirements
    if not check_requirements():
        print("\n📦 Installing missing packages...")
        if not install_requirements():
            print("❌ Failed to install requirements. Please run: pip install -r requirements.txt")
            return
    
    # Run the dashboard
    print("\n" + "=" * 50)
    run_dashboard()

if __name__ == "__main__":
    main()