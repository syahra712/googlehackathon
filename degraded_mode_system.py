"""
🌾 AGRICULTURAL AI ORCHESTRA - DEGRADED MODE SYSTEM
Offline operation with cached data and rule-based decisions
"""
import json
import pandas as pd
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any, Optional

class DegradedModeSystem:
    """Degraded mode system for offline operation"""
    
    def __init__(self):
        self.cached_data = {}
        self.rule_engine = RuleBasedEngine()
        self.offline_agents = {}
        self.fallback_strategies = {}
        self.initialize_offline_system()
    
    def initialize_offline_system(self):
        """Initialize offline system with cached data and rules"""
        # Load cached data
        self.cached_data = {
            'sensor_data': self.load_cached_sensor_data(),
            'market_data': self.load_cached_market_data(),
            'weather_data': self.load_cached_weather_data(),
            'farm_data': self.load_cached_farm_data()
        }
        
        # Initialize offline agents
        self.offline_agents = {
            'sensor_agent': OfflineSensorAgent(self.cached_data),
            'prediction_agent': OfflinePredictionAgent(self.cached_data),
            'resource_agent': OfflineResourceAgent(self.cached_data),
            'market_agent': OfflineMarketAgent(self.cached_data)
        }
        
        # Initialize fallback strategies
        self.fallback_strategies = {
            'irrigation': self.get_irrigation_fallback(),
            'pest_control': self.get_pest_control_fallback(),
            'harvest_timing': self.get_harvest_timing_fallback(),
            'market_timing': self.get_market_timing_fallback()
        }
    
    def load_cached_sensor_data(self):
        """Load cached sensor data for offline operation"""
        try:
            with open('farm_sensor_data_tehsil_with_date.json', 'r') as f:
                data = json.load(f)
            # Cache last 1000 records
            return data[-1000:] if len(data) > 1000 else data
        except:
            return []
    
    def load_cached_market_data(self):
        """Load cached market data for offline operation"""
        try:
            data = pd.read_csv('market_prices copy.csv')
            # Cache last 100 records
            return data.tail(100).to_dict('records')
        except:
            return []
    
    def load_cached_weather_data(self):
        """Load cached weather data for offline operation"""
        try:
            data = pd.read_csv('weather_data_tehsil copy.csv')
            # Cache last 100 records
            return data.tail(100).to_dict('records')
        except:
            return []
    
    def load_cached_farm_data(self):
        """Load cached farm data for offline operation"""
        try:
            with open('farm_resources.json', 'r') as f:
                data = json.load(f)
            # Cache first 100 farms
            return data[:100]
        except:
            return []
    
    def get_irrigation_fallback(self):
        """Get irrigation fallback strategy"""
        return {
            'soil_moisture_low': 'Increase irrigation by 20%',
            'soil_moisture_high': 'Reduce irrigation by 30%',
            'temperature_high': 'Increase irrigation by 15%',
            'temperature_low': 'Maintain current irrigation',
            'default': 'Follow standard irrigation schedule'
        }
    
    def get_pest_control_fallback(self):
        """Get pest control fallback strategy"""
        return {
            'pest_detected': 'Apply immediate treatment',
            'high_humidity': 'Monitor for pest development',
            'temperature_optimal': 'Check for pest activity',
            'default': 'Regular monitoring schedule'
        }
    
    def get_harvest_timing_fallback(self):
        """Get harvest timing fallback strategy"""
        return {
            'temperature_high': 'Harvest 1-2 weeks earlier',
            'temperature_low': 'Harvest 1-2 weeks later',
            'rainfall_high': 'Harvest before next rain',
            'default': 'Follow standard harvest schedule'
        }
    
    def get_market_timing_fallback(self):
        """Get market timing fallback strategy"""
        return {
            'price_trending_up': 'Hold for better prices',
            'price_trending_down': 'Sell immediately',
            'demand_high': 'Sell at current prices',
            'default': 'Follow standard market schedule'
        }
    
    def execute_offline_optimization(self, farm_id, scenario):
        """Execute offline optimization using cached data and rules"""
        results = {
            'timestamp': datetime.now(),
            'farm_id': farm_id,
            'mode': 'degraded',
            'recommendations': [],
            'data_sources': 'cached',
            'confidence': 'medium'
        }
        
        # Get farm data from cache
        farm_data = next((f for f in self.cached_data['farm_data'] if f['farm_id'] == farm_id), {})
        
        # Get sensor data from cache
        sensor_data = [s for s in self.cached_data['sensor_data'] if s['farm_id'] == farm_id]
        
        # Apply rule-based recommendations
        if sensor_data:
            latest_sensor = sensor_data[-1]
            
            # Irrigation recommendation
            if latest_sensor['soil_moisture_%'] < 40:
                results['recommendations'].append({
                    'type': 'irrigation',
                    'action': 'Increase irrigation',
                    'reason': 'Soil moisture below 40%',
                    'confidence': 'high'
                })
            elif latest_sensor['soil_moisture_%'] > 70:
                results['recommendations'].append({
                    'type': 'irrigation',
                    'action': 'Reduce irrigation',
                    'reason': 'Soil moisture above 70%',
                    'confidence': 'high'
                })
            
            # Pest control recommendation
            if latest_sensor['pest_detection'] != 'None':
                results['recommendations'].append({
                    'type': 'pest_control',
                    'action': 'Apply pest treatment',
                    'reason': f'Pest detected: {latest_sensor["pest_detection"]}',
                    'confidence': 'high'
                })
            
            # Temperature-based recommendations
            if latest_sensor['temperature_c'] > 35:
                results['recommendations'].append({
                    'type': 'temperature',
                    'action': 'Increase irrigation and monitor for heat stress',
                    'reason': 'High temperature detected',
                    'confidence': 'medium'
                })
        
        # Market recommendations using cached data
        market_data = self.cached_data['market_data']
        if market_data:
            # Get latest market data
            latest_market = market_data[-1]
            results['recommendations'].append({
                'type': 'market',
                'action': f'Consider selling {latest_market.get("commodity", "crops")}',
                'reason': f'Market price: {latest_market.get("avg_price_pkr_per_40kg", "N/A")} PKR',
                'confidence': 'low'
            })
        
        # Weather recommendations using cached data
        weather_data = self.cached_data['weather_data']
        if weather_data:
            latest_weather = weather_data[-1]
            if latest_weather['extreme_event'] != 'normal':
                results['recommendations'].append({
                    'type': 'weather',
                    'action': f'Prepare for {latest_weather["extreme_event"]}',
                    'reason': f'Extreme weather event: {latest_weather["extreme_event"]}',
                    'confidence': 'medium'
                })
        
        return results

class RuleBasedEngine:
    """Rule-based decision engine for offline operation"""
    
    def __init__(self):
        self.rules = self.initialize_rules()
    
    def initialize_rules(self):
        """Initialize rule-based decision rules"""
        return {
            'irrigation_rules': {
                'soil_moisture_low': lambda x: x < 40,
                'soil_moisture_high': lambda x: x > 70,
                'temperature_high': lambda x: x > 35,
                'humidity_low': lambda x: x < 30
            },
            'pest_control_rules': {
                'pest_detected': lambda x: x != 'None',
                'high_humidity': lambda x: x > 80,
                'temperature_optimal': lambda x: 25 <= x <= 30
            },
            'harvest_rules': {
                'temperature_high': lambda x: x > 35,
                'temperature_low': lambda x: x < 20,
                'rainfall_high': lambda x: x > 50
            },
            'market_rules': {
                'price_trending_up': lambda x: x > 0,
                'demand_high': lambda x: x == 'High',
                'demand_low': lambda x: x == 'Low'
            }
        }
    
    def apply_rules(self, data, rule_type):
        """Apply rules to data and return recommendations"""
        rules = self.rules.get(rule_type, {})
        recommendations = []
        
        for rule_name, rule_func in rules.items():
            if rule_func(data):
                recommendations.append({
                    'rule': rule_name,
                    'condition': data,
                    'recommendation': self.get_rule_recommendation(rule_name, rule_type)
                })
        
        return recommendations
    
    def get_rule_recommendation(self, rule_name, rule_type):
        """Get recommendation for specific rule"""
        recommendations = {
            'irrigation_rules': {
                'soil_moisture_low': 'Increase irrigation by 20%',
                'soil_moisture_high': 'Reduce irrigation by 30%',
                'temperature_high': 'Increase irrigation by 15%',
                'humidity_low': 'Increase irrigation by 10%'
            },
            'pest_control_rules': {
                'pest_detected': 'Apply immediate treatment',
                'high_humidity': 'Monitor for pest development',
                'temperature_optimal': 'Check for pest activity'
            },
            'harvest_rules': {
                'temperature_high': 'Harvest 1-2 weeks earlier',
                'temperature_low': 'Harvest 1-2 weeks later',
                'rainfall_high': 'Harvest before next rain'
            },
            'market_rules': {
                'price_trending_up': 'Hold for better prices',
                'demand_high': 'Sell at current prices',
                'demand_low': 'Wait for better demand'
            }
        }
        
        return recommendations.get(rule_type, {}).get(rule_name, 'No specific recommendation')

class OfflineSensorAgent:
    """Offline sensor agent using cached data"""
    
    def __init__(self, cached_data):
        self.cached_data = cached_data
        self.data_quality = 'cached'
    
    def get_sensor_data(self, farm_id, data_type):
        """Get sensor data from cache"""
        sensor_data = [s for s in self.cached_data['sensor_data'] if s['farm_id'] == farm_id]
        if data_type == 'environmental':
            return [s for s in sensor_data if 'soil_moisture' in s or 'temperature' in s]
        return sensor_data
    
    def validate_data_quality(self, data):
        """Validate data quality using cached patterns"""
        if not data:
            return 'low'
        
        # Check data consistency
        recent_data = data[-10:] if len(data) > 10 else data
        moisture_values = [d.get('soil_moisture_%', 0) for d in recent_data]
        
        if all(0 <= m <= 100 for m in moisture_values):
            return 'high'
        elif all(0 <= m <= 100 for m in moisture_values[-5:]):
            return 'medium'
        else:
            return 'low'

class OfflinePredictionAgent:
    """Offline prediction agent using cached models"""
    
    def __init__(self, cached_data):
        self.cached_data = cached_data
        self.prediction_models = 'cached'
    
    def generate_prediction(self, data, prediction_type):
        """Generate prediction using cached models"""
        if not data:
            return None
        
        # Use simple rule-based prediction
        if prediction_type == 'irrigation':
            avg_moisture = sum(d.get('soil_moisture_%', 50) for d in data) / len(data)
            if avg_moisture < 40:
                return 'High irrigation needed'
            elif avg_moisture > 70:
                return 'Reduce irrigation'
            else:
                return 'Maintain current irrigation'
        
        elif prediction_type == 'pest_outbreak':
            pest_count = len([d for d in data if d.get('pest_detection') != 'None'])
            if pest_count > len(data) * 0.3:
                return 'High pest risk'
            else:
                return 'Low pest risk'
        
        return 'No prediction available'

class OfflineResourceAgent:
    """Offline resource agent using cached allocations"""
    
    def __init__(self, cached_data):
        self.cached_data = cached_data
        self.allocation_patterns = 'cached'
    
    def allocate_resources(self, farm_id, resource_type, amount):
        """Allocate resources using cached patterns"""
        # Use cached farm data to determine allocation
        farm_data = next((f for f in self.cached_data['farm_data'] if f['farm_id'] == farm_id), {})
        
        if resource_type == 'irrigation':
            available_hours = farm_data.get('irrigation_hours_per_week', 0)
            if available_hours >= amount:
                return {
                    'status': 'allocated',
                    'amount': amount,
                    'source': 'local',
                    'cost': amount * 5
                }
            else:
                return {
                    'status': 'partial',
                    'amount': available_hours,
                    'source': 'local',
                    'cost': available_hours * 5
                }
        
        return {
            'status': 'unavailable',
            'amount': 0,
            'source': 'none',
            'cost': 0
        }

class OfflineMarketAgent:
    """Offline market agent using cached market data"""
    
    def __init__(self, cached_data):
        self.cached_data = cached_data
        self.market_trends = 'cached'
    
    def analyze_market(self, commodity, location):
        """Analyze market using cached data"""
        market_data = [m for m in self.cached_data['market_data'] 
                      if m.get('commodity') == commodity and m.get('market_location') == location]
        
        if not market_data:
            return {
                'status': 'no_data',
                'recommendation': 'No market data available',
                'confidence': 'low'
            }
        
        # Use latest cached data
        latest_data = market_data[-1]
        return {
            'status': 'cached',
            'price': latest_data.get('avg_price_pkr_per_40kg', 0),
            'demand': latest_data.get('demand_status', 'Unknown'),
            'recommendation': f'Use cached price: {latest_data.get("avg_price_pkr_per_40kg", 0)} PKR',
            'confidence': 'medium'
        }

def main():
    """Test degraded mode system"""
    print("🌾 AGRICULTURAL AI ORCHESTRA - DEGRADED MODE SYSTEM")
    print("=" * 60)
    
    # Initialize degraded mode system
    degraded_system = DegradedModeSystem()
    
    # Test offline optimization
    test_farm = 'F-001'
    test_scenario = {
        'sensor_data': {
            'soil_moisture_%': 35,
            'temperature_c': 32,
            'humidity_%': 45,
            'pest_detection': 'None'
        }
    }
    
    print(f"🧪 Testing offline optimization for {test_farm}")
    results = degraded_system.execute_offline_optimization(test_farm, test_scenario)
    
    print(f"📊 Results:")
    print(f"   Mode: {results['mode']}")
    print(f"   Data Sources: {results['data_sources']}")
    print(f"   Confidence: {results['confidence']}")
    print(f"   Recommendations: {len(results['recommendations'])}")
    
    for rec in results['recommendations']:
        print(f"   • {rec['type']}: {rec['action']} ({rec['confidence']} confidence)")
    
    print("\n✅ Degraded mode system operational!")
    print("🎯 System can operate offline with cached data and rule-based decisions")

if __name__ == "__main__":
    main()
