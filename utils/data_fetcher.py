"""
Data fetching utilities for real API integration
This module provides functions to fetch real-time data from various APIs
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional
import json

class WeatherDataFetcher:
    """Fetch weather data from various APIs"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, lat: float, lon: float) -> Dict:
        """Get current weather for coordinates"""
        if not self.api_key:
            return self._mock_weather_data()
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_weather_data(data)
        
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return self._mock_weather_data()
    
    def get_weather_forecast(self, lat: float, lon: float, days: int = 5) -> List[Dict]:
        """Get weather forecast for coordinates"""
        if not self.api_key:
            return self._mock_forecast_data(days)
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_forecast_data(data)
        
        except Exception as e:
            print(f"Error fetching forecast data: {e}")
            return self._mock_forecast_data(days)
    
    def _parse_weather_data(self, data: Dict) -> Dict:
        """Parse OpenWeatherMap current weather response"""
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data.get('wind', {}).get('speed', 0) * 3.6,  # Convert m/s to km/h
            'rainfall': data.get('rain', {}).get('1h', 0),
            'description': data['weather'][0]['description'],
            'timestamp': datetime.now()
        }
    
    def _parse_forecast_data(self, data: Dict) -> List[Dict]:
        """Parse OpenWeatherMap forecast response"""
        forecast_list = []
        
        for item in data['list']:
            forecast_list.append({
                'timestamp': datetime.fromtimestamp(item['dt']),
                'temperature': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item.get('wind', {}).get('speed', 0) * 3.6,
                'rainfall': item.get('rain', {}).get('3h', 0),
                'description': item['weather'][0]['description']
            })
        
        return forecast_list
    
    def _mock_weather_data(self) -> Dict:
        """Generate mock weather data when API is not available"""
        return {
            'temperature': np.random.normal(25, 10),
            'humidity': np.random.uniform(30, 90),
            'pressure': np.random.normal(1013, 20),
            'wind_speed': np.random.uniform(5, 50),
            'rainfall': np.random.exponential(2),
            'description': 'Mock weather data',
            'timestamp': datetime.now()
        }
    
    def _mock_forecast_data(self, days: int) -> List[Dict]:
        """Generate mock forecast data"""
        forecast = []
        for i in range(days * 8):  # 8 forecasts per day (3-hour intervals)
            forecast.append({
                'timestamp': datetime.now() + timedelta(hours=i*3),
                'temperature': np.random.normal(25, 10),
                'humidity': np.random.uniform(30, 90),
                'pressure': np.random.normal(1013, 20),
                'wind_speed': np.random.uniform(5, 50),
                'rainfall': np.random.exponential(2),
                'description': 'Mock forecast data'
            })
        return forecast

class DisasterDataFetcher:
    """Fetch disaster data from various APIs"""
    
    def __init__(self):
        self.usgs_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    
    def get_earthquake_data(self, days: int = 7) -> List[Dict]:
        """Get earthquake data from USGS"""
        try:
            start_time = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            params = {
                'format': 'geojson',
                'starttime': start_time,
                'minmagnitude': 4.0,
                'limit': 100
            }
            
            response = requests.get(self.usgs_url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_earthquake_data(data)
        
        except Exception as e:
            print(f"Error fetching earthquake data: {e}")
            return self._mock_earthquake_data()
    
    def _parse_earthquake_data(self, data: Dict) -> List[Dict]:
        """Parse USGS earthquake data"""
        earthquakes = []
        
        for feature in data['features']:
            props = feature['properties']
            coords = feature['geometry']['coordinates']
            
            earthquakes.append({
                'id': feature['id'],
                'type': 'Earthquake',
                'magnitude': props['mag'],
                'location': props['place'],
                'latitude': coords[1],
                'longitude': coords[0],
                'timestamp': datetime.fromtimestamp(props['time'] / 1000),
                'severity': self._classify_earthquake_severity(props['mag']),
                'affected_population': self._estimate_earthquake_impact(props['mag'])
            })
        
        return earthquakes
    
    def _classify_earthquake_severity(self, magnitude: float) -> str:
        """Classify earthquake severity based on magnitude"""
        if magnitude >= 7.0:
            return 'Critical'
        elif magnitude >= 6.0:
            return 'High'
        elif magnitude >= 5.0:
            return 'Medium'
        else:
            return 'Low'
    
    def _estimate_earthquake_impact(self, magnitude: float) -> int:
        """Estimate affected population based on magnitude"""
        # Simplified estimation
        if magnitude >= 7.0:
            return np.random.randint(10000, 100000)
        elif magnitude >= 6.0:
            return np.random.randint(1000, 10000)
        elif magnitude >= 5.0:
            return np.random.randint(100, 1000)
        else:
            return np.random.randint(10, 100)
    
    def _mock_earthquake_data(self) -> List[Dict]:
        """Generate mock earthquake data"""
        earthquakes = []
        
        for i in range(10):
            magnitude = np.random.uniform(4.0, 8.0)
            earthquakes.append({
                'id': f'mock_eq_{i}',
                'type': 'Earthquake',
                'magnitude': magnitude,
                'location': f'Mock Location {i}',
                'latitude': np.random.uniform(-90, 90),
                'longitude': np.random.uniform(-180, 180),
                'timestamp': datetime.now() - timedelta(hours=np.random.randint(1, 168)),
                'severity': self._classify_earthquake_severity(magnitude),
                'affected_population': self._estimate_earthquake_impact(magnitude)
            })
        
        return earthquakes

class DataIntegrator:
    """Integrate data from multiple sources"""
    
    def __init__(self):
        self.weather_fetcher = WeatherDataFetcher()
        self.disaster_fetcher = DisasterDataFetcher()
    
    def get_integrated_data(self, locations: List[Dict]) -> Dict:
        """Get integrated weather and disaster data for multiple locations"""
        integrated_data = {
            'weather_data': [],
            'disaster_data': [],
            'last_updated': datetime.now()
        }
        
        # Fetch weather data for each location
        for location in locations:
            weather = self.weather_fetcher.get_current_weather(
                location['lat'], location['lon']
            )
            weather['location'] = location['name']
            integrated_data['weather_data'].append(weather)
        
        # Fetch disaster data
        disasters = self.disaster_fetcher.get_earthquake_data()
        integrated_data['disaster_data'].extend(disasters)
        
        return integrated_data
    
    def save_data_to_cache(self, data: Dict, filename: str = 'cache_data.json'):
        """Save data to cache file"""
        try:
            # Convert datetime objects to strings for JSON serialization
            cache_data = self._serialize_datetime(data)
            
            with open(filename, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            print(f"Data cached to {filename}")
        
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def load_data_from_cache(self, filename: str = 'cache_data.json') -> Optional[Dict]:
        """Load data from cache file"""
        try:
            if not os.path.exists(filename):
                return None
            
            with open(filename, 'r') as f:
                cache_data = json.load(f)
            
            # Convert string timestamps back to datetime objects
            return self._deserialize_datetime(cache_data)
        
        except Exception as e:
            print(f"Error loading cache: {e}")
            return None
    
    def _serialize_datetime(self, obj):
        """Convert datetime objects to strings for JSON serialization"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: self._serialize_datetime(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_datetime(item) for item in obj]
        else:
            return obj
    
    def _deserialize_datetime(self, obj):
        """Convert string timestamps back to datetime objects"""
        if isinstance(obj, str):
            try:
                return datetime.fromisoformat(obj)
            except ValueError:
                return obj
        elif isinstance(obj, dict):
            return {key: self._deserialize_datetime(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._deserialize_datetime(item) for item in obj]
        else:
            return obj

# Example usage
if __name__ == "__main__":
    # Example locations
    locations = [
        {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060},
        {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503},
        {'name': 'London', 'lat': 51.5074, 'lon': -0.1278}
    ]
    
    # Initialize data integrator
    integrator = DataIntegrator()
    
    # Get integrated data
    data = integrator.get_integrated_data(locations)
    
    # Save to cache
    integrator.save_data_to_cache(data)
    
    print("Data integration example completed!")
    print(f"Weather data points: {len(data['weather_data'])}")
    print(f"Disaster data points: {len(data['disaster_data'])}")