"""
Data loading and preprocessing utilities for the Multi-Agent Agricultural AI System
"""
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Handles loading and preprocessing of agricultural datasets"""
    
    def __init__(self):
        self.farm_resources = None
        self.sensor_data = None
        self.market_prices = None
        self.weather_data = None
        
    def load_farm_resources(self, file_path: str) -> List[Dict]:
        """Load farm resources data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                self.farm_resources = json.load(f)
            logger.info(f"Loaded {len(self.farm_resources)} farm resource records")
            return self.farm_resources
        except Exception as e:
            logger.error(f"Error loading farm resources: {e}")
            return []
    
    def load_sensor_data(self, file_path: str) -> List[Dict]:
        """Load sensor data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                self.sensor_data = json.load(f)
            logger.info(f"Loaded {len(self.sensor_data)} sensor data records")
            return self.sensor_data
        except Exception as e:
            logger.error(f"Error loading sensor data: {e}")
            return []
    
    def load_market_prices(self, file_path: str) -> pd.DataFrame:
        """Load market prices data from CSV file"""
        try:
            self.market_prices = pd.read_csv(file_path)
            self.market_prices['date'] = pd.to_datetime(self.market_prices['date'])
            logger.info(f"Loaded {len(self.market_prices)} market price records")
            return self.market_prices
        except Exception as e:
            logger.error(f"Error loading market prices: {e}")
            return pd.DataFrame()
    
    def load_weather_data(self, file_path: str) -> pd.DataFrame:
        """Load weather data from CSV file"""
        try:
            self.weather_data = pd.read_csv(file_path)
            self.weather_data['date'] = pd.to_datetime(self.weather_data['date'])
            logger.info(f"Loaded {len(self.weather_data)} weather data records")
            return self.weather_data
        except Exception as e:
            logger.error(f"Error loading weather data: {e}")
            return pd.DataFrame()
    
    def get_farm_by_id(self, farm_id: str) -> Optional[Dict]:
        """Get specific farm resource data by farm ID"""
        if not self.farm_resources:
            return None
        return next((farm for farm in self.farm_resources if farm['farm_id'] == farm_id), None)
    
    def get_sensor_data_by_farm(self, farm_id: str) -> List[Dict]:
        """Get sensor data for a specific farm"""
        if not self.sensor_data:
            return []
        return [record for record in self.sensor_data if record['farm_id'] == farm_id]
    
    def get_market_data_by_commodity(self, commodity: str, location: str = None) -> pd.DataFrame:
        """Get market data for specific commodity and optional location"""
        if self.market_prices is None or self.market_prices.empty:
            return pd.DataFrame()
        
        filtered_data = self.market_prices[self.market_prices['commodity'] == commodity]
        if location:
            filtered_data = filtered_data[filtered_data['market_location'] == location]
        return filtered_data
    
    def get_weather_data_by_location(self, tehsil: str = None, district: str = None, province: str = None) -> pd.DataFrame:
        """Get weather data filtered by location"""
        if self.weather_data is None or self.weather_data.empty:
            return pd.DataFrame()
        
        filtered_data = self.weather_data.copy()
        if tehsil:
            filtered_data = filtered_data[filtered_data['tehsil'] == tehsil]
        if district:
            filtered_data = filtered_data[filtered_data['district'] == district]
        if province:
            filtered_data = filtered_data[filtered_data['province'] == province]
        return filtered_data
    
    def get_recent_data(self, days: int = 30) -> Dict[str, Any]:
        """Get recent data from all sources (last N days)"""
        recent_data = {}
        
        # Get recent sensor data
        if self.sensor_data:
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_sensor = [
                record for record in self.sensor_data 
                if datetime.strptime(record['date'], '%Y-%m-%d') >= cutoff_date
            ]
            recent_data['sensor'] = recent_sensor
        
        # Get recent market data
        if not self.market_prices.empty:
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_market = self.market_prices[self.market_prices['date'] >= cutoff_date]
            recent_data['market'] = recent_market
        
        # Get recent weather data
        if not self.weather_data.empty:
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_weather = self.weather_data[self.weather_data['date'] >= cutoff_date]
            recent_data['weather'] = recent_weather
        
        return recent_data
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary statistics of all loaded data"""
        summary = {}
        
        if self.farm_resources:
            summary['farm_resources'] = {
                'total_farms': len(self.farm_resources),
                'avg_irrigation_hours': np.mean([f['irrigation_hours_per_week'] for f in self.farm_resources]),
                'avg_fertilizer': np.mean([f['fertilizer_kg_available'] for f in self.farm_resources])
            }
        
        if self.sensor_data:
            summary['sensor_data'] = {
                'total_records': len(self.sensor_data),
                'unique_farms': len(set(record['farm_id'] for record in self.sensor_data)),
                'date_range': {
                    'start': min(record['date'] for record in self.sensor_data),
                    'end': max(record['date'] for record in self.sensor_data)
                }
            }
        
        if not self.market_prices.empty:
            summary['market_prices'] = {
                'total_records': len(self.market_prices),
                'commodities': self.market_prices['commodity'].unique().tolist(),
                'locations': self.market_prices['market_location'].unique().tolist()
            }
        
        if not self.weather_data.empty:
            summary['weather_data'] = {
                'total_records': len(self.weather_data),
                'provinces': self.weather_data['province'].unique().tolist(),
                'extreme_events': self.weather_data['extreme_event'].value_counts().to_dict()
            }
        
        return summary
