# 🔧 Troubleshooting Guide - Disaster Analytics Dashboard

## Common Issues and Solutions

### 🌐 **Dashboard Not Loading Properly**

#### **Issue**: Browser shows file explorer instead of dashboard
**Solution**: 
1. Make sure you're running the correct command: `streamlit run app.py`
2. Check that you're accessing the correct URL (usually http://localhost:8501)
3. Try refreshing the browser or opening in incognito mode
4. Clear browser cache if needed

#### **Issue**: "Port already in use" error
**Solution**:
```bash
# Try a different port
streamlit run app.py --server.port 8503

# Or kill existing processes
# Windows:
netstat -ano | findstr :8501
taskkill /PID <process_id> /F

# Unix/Linux/Mac:
lsof -ti:8501 | xargs kill -9
```

### 📦 **Package Installation Issues**

#### **Issue**: Import errors or missing packages
**Solution**:
```bash
# Install all requirements
pip install -r requirements.txt

# Or install individually
pip install streamlit plotly pandas numpy scikit-learn folium streamlit-folium
```

#### **Issue**: Version conflicts
**Solution**:
```bash
# Create virtual environment
python -m venv dashboard_env
# Windows:
dashboard_env\Scripts\activate
# Unix/Linux/Mac:
source dashboard_env/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 🗺️ **Map Not Displaying**

#### **Issue**: Folium map appears blank
**Solution**:
1. Check internet connection (maps need to load tiles)
2. Try refreshing the page
3. Check browser console for JavaScript errors
4. Ensure folium and streamlit-folium are properly installed

### 📊 **Charts Not Rendering**

#### **Issue**: Plotly charts not showing
**Solution**:
1. Update Plotly: `pip install --upgrade plotly`
2. Check browser JavaScript is enabled
3. Try different browser
4. Clear browser cache

### 🤖 **ML Model Issues**

#### **Issue**: Model training fails
**Solution**:
1. Check scikit-learn version: `pip install --upgrade scikit-learn`
2. Ensure sufficient data is available
3. Check for data type issues in the dataset

### 🎨 **Styling Issues**

#### **Issue**: Dark theme not applying
**Solution**:
1. Hard refresh the browser (Ctrl+F5 or Cmd+Shift+R)
2. Check if custom CSS is being blocked
3. Try different browser

### 🔄 **Auto-refresh Problems**

#### **Issue**: Auto-refresh causing errors
**Solution**:
1. Disable auto-refresh if causing issues
2. Check for session state conflicts
3. Restart the dashboard

## 🚀 **Quick Fixes**

### **Complete Reset**
```bash
# Stop all Streamlit processes
# Windows:
taskkill /f /im streamlit.exe

# Unix/Linux/Mac:
pkill -f streamlit

# Restart dashboard
streamlit run app.py
```

### **Clean Installation**
```bash
# Remove and reinstall packages
pip uninstall streamlit plotly pandas numpy scikit-learn folium streamlit-folium
pip install -r requirements.txt
```

### **Browser Issues**
1. Try different browser (Chrome, Firefox, Safari, Edge)
2. Disable browser extensions
3. Clear cache and cookies
4. Try incognito/private mode

## 📞 **Getting Help**

### **Check Dashboard Status**
```bash
python verify_functionality.py
```

### **Run Tests**
```bash
python test_dashboard.py
```

### **View Logs**
- Check terminal output for error messages
- Look for Python tracebacks
- Note any warning messages

## 🔍 **Debug Mode**

To run in debug mode with more verbose output:
```bash
streamlit run app.py --logger.level debug
```

## 📋 **System Requirements**

### **Minimum Requirements**
- Python 3.7+
- 4GB RAM
- Modern web browser
- Internet connection (for map tiles)

### **Recommended**
- Python 3.9+
- 8GB RAM
- Chrome or Firefox browser
- Stable internet connection

## ✅ **Verification Checklist**

Before reporting issues, verify:
- [ ] Python version is 3.7+
- [ ] All packages installed correctly
- [ ] No firewall blocking localhost
- [ ] Browser JavaScript enabled
- [ ] Sufficient disk space
- [ ] No antivirus blocking Python

## 🆘 **Emergency Reset**

If nothing works, try this complete reset:

```bash
# 1. Stop all processes
pkill -f streamlit  # Unix/Linux/Mac
# or
taskkill /f /im streamlit.exe  # Windows

# 2. Clean Python cache
find . -type d -name "__pycache__" -delete  # Unix/Linux/Mac
# or manually delete __pycache__ folders on Windows

# 3. Reinstall everything
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# 4. Restart
streamlit run app.py
```

---

**Still having issues?** 
- Check the error messages in terminal
- Run the verification script: `python verify_functionality.py`
- Ensure all files are present and not corrupted