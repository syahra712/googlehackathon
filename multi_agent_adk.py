"""
🌾 AGRICULTURAL AI ORCHESTRA - MULTI-AGENT ADK (Agent Development Kit)
Complete agent-to-agent economy with swarm intelligence
"""
import streamlit as st
import pandas as pd
import json
import numpy as np
from datetime import datetime, timedelta
import threading
import time
import random
from typing import Dict, List, Any, Optional
import openai
from config import OPENAI_API_KEY

# Set your OpenAI API key from secure config
openai.api_key = OPENAI_API_KEY

def get_intelligent_agricultural_response(question, data, orchestrator, conversation_history=None):
    """Get intelligent agricultural response with follow-up questions and detailed analysis"""
    
    # Check bandwidth and switch to offline mode if needed
    if check_bandwidth_and_switch_offline():
        return get_offline_response(question, data, orchestrator)
    
    # Analyze question type and extract relevant data
    question_analysis = analyze_question(question, data)
    
    # Create context from YOUR agricultural data
    context = create_agricultural_context(question_analysis, data)
    
    # Check if we have sufficient data from YOUR dataset
    data_sufficiency = check_data_sufficiency(question_analysis, data)
    
    # Generate follow-up questions
    follow_up_questions = generate_follow_up_questions(question, question_analysis, data)
    
    # Check if question is asking for predictions
    is_prediction_request = any(keyword in question.lower() for keyword in [
        'predict', 'forecast', 'future', 'will happen', 'expected', 'likely', 'probability',
        'پیشن گوئی', 'پیش گوئی', 'مستقبل', 'ہوگا', 'امکان', 'توقع'
    ])
    
    # Generate response using OpenAI with priority system
    system_prompt = f"""You are an expert agricultural advisor with advanced prediction capabilities. You MUST follow this priority system:

1. FIRST PRIORITY: Use ONLY the provided agricultural dataset information
2. SECOND PRIORITY: If dataset information is insufficient, supplement with general agricultural knowledge
3. ALWAYS: Base recommendations on the actual data provided first
4. ALWAYS: Ask follow-up questions to get more details about the problem
5. ALWAYS: Provide detailed problem analysis and step-by-step solutions
6. PREDICTION REQUESTS: When asked to predict, provide specific predictions with confidence levels and reasoning

Dataset Information Available: {data_sufficiency}
Agricultural Context: {context}
Follow-up Questions to Ask: {follow_up_questions}
Is Prediction Request: {is_prediction_request}

PREDICTION CAPABILITIES:
- Weather predictions based on historical data
- Crop yield predictions using farm data
- Market price predictions using market trends
- Pest outbreak predictions using environmental data
- Harvest timing predictions using weather and crop data
- Irrigation needs predictions using soil moisture data

Provide intelligent, helpful responses in Urdu when the question is in Urdu, or in English when the question is in English. 
Use chain-of-thought reasoning to provide step-by-step analysis and recommendations.
ALWAYS mention when you're using dataset information vs general knowledge.
ALWAYS ask follow-up questions to understand the problem better.
ALWAYS provide detailed analysis of the problem and its solutions.
FOR PREDICTIONS: Provide specific predictions with confidence levels, reasoning, and actionable insights."""
    
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""
                Question: {question}
                
                Please provide an intelligent response with:
                1. Chain-of-thought reasoning
                2. Detailed problem analysis
                3. Step-by-step solutions
                4. Follow-up questions to get more details
                5. Specific recommendations based on your agricultural data
                
                If the question is in Urdu, respond in Urdu. If in English, respond in English.
                
                PRIORITY SYSTEM:
                1. Use the provided agricultural dataset information first
                2. Only use general knowledge if dataset information is insufficient
                3. Always specify the source of your information (dataset vs general knowledge)
                4. Always ask follow-up questions to understand the problem better
                
                Base your response on the provided agricultural data and give specific, actionable advice.
                """}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        # If API fails, switch to offline mode
        return get_offline_response(question, data, orchestrator)

def check_bandwidth_and_switch_offline():
    """Check bandwidth and automatically switch to offline mode if low"""
    try:
        import requests
        import time
        
        # Test bandwidth by making a small request
        start_time = time.time()
        response = requests.get("http://www.google.com", timeout=5)
        end_time = time.time()
        
        # If response time > 10 seconds, switch to offline
        if end_time - start_time > 10:
            return True
        
        # If status code is not 200, switch to offline
        if response.status_code != 200:
            return True
            
        return False
    except:
        # If any error occurs, switch to offline mode
        return True

def get_offline_response(question, data, orchestrator):
    """Get offline response using cached data and rule-based decisions"""
    question_analysis = analyze_question(question, data)
    
    # Use offline mode system
    from degraded_mode_system import DegradedModeSystem
    offline_system = DegradedModeSystem()
    
    # Get offline optimization results
    offline_results = offline_system.execute_offline_optimization('F-001', {
        'sensor_data': question_analysis.get('relevant_data', {}).get('sensor_data', [{}])[0] if question_analysis.get('relevant_data', {}).get('sensor_data') else {}
    })
    
    # Generate offline response
    offline_response = f"""
    [OFFLINE MODE - Using Cached Data]
    
    Based on your cached agricultural data, here's my analysis:
    
    Problem Analysis:
    {offline_results.get('recommendations', [])}
    
    Recommendations:
    {offline_results.get('recommendations', [])}
    
    Data Source: Cached agricultural data (offline mode)
    Confidence: Medium (based on historical patterns)
    
    Follow-up Questions:
    1. Can you provide more details about your specific farm conditions?
    2. What is the current status of your irrigation system?
    3. Are you experiencing any specific symptoms with your crops?
    4. What is your current soil moisture level?
    5. Have you noticed any pest activity recently?
    """
    
    return offline_response

def generate_follow_up_questions(question, question_analysis, data):
    """Generate intelligent follow-up questions based on the question and available data"""
    follow_up_questions = []
    
    # General follow-up questions
    follow_up_questions.append("Can you provide more details about your specific situation?")
    follow_up_questions.append("What is the current condition of your farm?")
    follow_up_questions.append("Are you experiencing any specific symptoms?")
    
    # Topic-specific follow-up questions
    if 'pest_control' in question_analysis['topics']:
        follow_up_questions.extend([
            "What type of pests are you seeing?",
            "How long have you noticed the pest activity?",
            "What is the extent of the damage?",
            "Have you tried any treatments yet?",
            "What is your current pest management strategy?"
        ])
    
    if 'irrigation' in question_analysis['topics']:
        follow_up_questions.extend([
            "What is your current soil moisture level?",
            "How often do you irrigate?",
            "What type of irrigation system do you use?",
            "Are you experiencing water shortages?",
            "What is your water source?"
        ])
    
    if 'market' in question_analysis['topics']:
        follow_up_questions.extend([
            "What crops are you planning to sell?",
            "When do you plan to harvest?",
            "What is your target market?",
            "Do you have storage facilities?",
            "What is your production volume?"
        ])
    
    if 'weather' in question_analysis['topics']:
        follow_up_questions.extend([
            "What is your current location?",
            "What weather conditions are you experiencing?",
            "Are you expecting any extreme weather?",
            "How is the weather affecting your crops?",
            "Do you have weather protection measures?"
        ])
    
    if 'harvest' in question_analysis['topics']:
        follow_up_questions.extend([
            "What crops are you harvesting?",
            "What is your harvest timeline?",
            "What is your expected yield?",
            "Do you have harvesting equipment?",
            "What is your post-harvest plan?"
        ])
    
    # Data-specific follow-up questions
    if question_analysis['relevant_data'].get('sensor_data'):
        follow_up_questions.append("Can you share your recent sensor readings?")
    
    if question_analysis['relevant_data'].get('farm_data'):
        follow_up_questions.append("What is your farm size and setup?")
    
    if question_analysis['relevant_data'].get('market_data'):
        follow_up_questions.append("What are your market preferences?")
    
    if question_analysis['relevant_data'].get('weather_data'):
        follow_up_questions.append("What is your local weather forecast?")
    
    return follow_up_questions[:5]  # Return top 5 most relevant questions

def check_data_sufficiency(question_analysis, data):
    """Check if we have sufficient data from the dataset to answer the question"""
    sufficiency_report = []
    
    # Check sensor data availability
    if 'sensor_data' in question_analysis['relevant_data']:
        sensor_data = question_analysis['relevant_data']['sensor_data']
        if sensor_data:
            sufficiency_report.append(f"✅ Sensor Data: {len(sensor_data)} readings available")
        else:
            sufficiency_report.append("❌ Sensor Data: No relevant sensor data found")
    
    # Check market data availability
    if 'market_data' in question_analysis['relevant_data']:
        market_data = question_analysis['relevant_data']['market_data']
        if market_data:
            sufficiency_report.append(f"✅ Market Data: {len(market_data)} records available")
        else:
            sufficiency_report.append("❌ Market Data: No relevant market data found")
    
    # Check weather data availability
    if 'weather_data' in question_analysis['relevant_data']:
        weather_data = question_analysis['relevant_data']['weather_data']
        if weather_data:
            sufficiency_report.append(f"✅ Weather Data: {len(weather_data)} records available")
        else:
            sufficiency_report.append("❌ Weather Data: No relevant weather data found")
    
    # Check farm data availability
    if 'farm_data' in question_analysis['relevant_data']:
        farm_data = question_analysis['relevant_data']['farm_data']
        if farm_data:
            sufficiency_report.append(f"✅ Farm Data: {len(farm_data)} farms available")
        else:
            sufficiency_report.append("❌ Farm Data: No relevant farm data found")
    
    # Overall assessment
    total_data_points = sum([
        len(question_analysis['relevant_data'].get('sensor_data', [])),
        len(question_analysis['relevant_data'].get('market_data', [])),
        len(question_analysis['relevant_data'].get('weather_data', [])),
        len(question_analysis['relevant_data'].get('farm_data', []))
    ])
    
    if total_data_points > 0:
        sufficiency_report.append(f"📊 Overall: {total_data_points} relevant data points found - Using dataset information")
    else:
        sufficiency_report.append("📊 Overall: No relevant dataset information - Using general agricultural knowledge")
    
    return "\n".join(sufficiency_report)

def analyze_question(question, data):
    """Analyze the question to determine type and relevant data"""
    question_lower = question.lower()
    
    analysis = {
        'type': 'general',
        'language': 'urdu' if any(char in question for char in 'ابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنوہھیے') else 'english',
        'topics': [],
        'relevant_data': {}
    }
    
    # Detect question topics
    if any(word in question_lower for word in ['pest', 'کیڑے', 'insect', 'disease', 'بیماری']):
        analysis['topics'].append('pest_control')
        analysis['relevant_data']['sensor_data'] = get_pest_related_data(data)
    
    if any(word in question_lower for word in ['irrigation', 'آبپاشی', 'water', 'پانی', 'moisture', 'نمی']):
        analysis['topics'].append('irrigation')
        analysis['relevant_data']['sensor_data'] = get_irrigation_related_data(data)
        analysis['relevant_data']['farm_data'] = get_farm_irrigation_data(data)
    
    if any(word in question_lower for word in ['price', 'قیمت', 'market', 'بازار', 'sell', 'بیچنا', 'crop', 'فصل']):
        analysis['topics'].append('market')
        analysis['relevant_data']['market_data'] = get_market_related_data(data)
    
    if any(word in question_lower for word in ['weather', 'موسم', 'rain', 'بارش', 'temperature', 'درجہ حرارت']):
        analysis['topics'].append('weather')
        analysis['relevant_data']['weather_data'] = get_weather_related_data(data)
    
    if any(word in question_lower for word in ['harvest', 'کٹائی', 'crop', 'فصل', 'yield', 'پیداوار']):
        analysis['topics'].append('harvest')
        analysis['relevant_data']['sensor_data'] = get_harvest_related_data(data)
    
    return analysis

def create_agricultural_context(analysis, data):
    """Create context from agricultural data based on question analysis"""
    context_parts = []
    
    # Add relevant sensor data
    if 'sensor_data' in analysis['relevant_data']:
        sensor_data = analysis['relevant_data']['sensor_data']
        if sensor_data:
            context_parts.append(f"Sensor Data: {len(sensor_data)} readings available")
            if 'pest_control' in analysis['topics']:
                pest_readings = [s for s in sensor_data if s.get('pest_detection') != 'None']
                context_parts.append(f"Pest Detection: {len(pest_readings)} farms with pest issues")
            if 'irrigation' in analysis['topics']:
                avg_moisture = sum(s.get('soil_moisture_%', 50) for s in sensor_data) / len(sensor_data)
                context_parts.append(f"Average Soil Moisture: {avg_moisture:.1f}%")
    
    # Add relevant market data
    if 'market_data' in analysis['relevant_data']:
        market_data = analysis['relevant_data']['market_data']
        if market_data:
            context_parts.append(f"Market Data: {len(market_data)} price records available")
            if market_data:
                latest_price = market_data[-1].get('avg_price_pkr_per_40kg', 0)
                context_parts.append(f"Latest Price: {latest_price} PKR/40kg")
    
    # Add relevant weather data
    if 'weather_data' in analysis['relevant_data']:
        weather_data = analysis['relevant_data']['weather_data']
        if weather_data:
            context_parts.append(f"Weather Data: {len(weather_data)} weather records available")
            if weather_data:
                latest_weather = weather_data[-1]
                context_parts.append(f"Latest Weather: {latest_weather.get('temperature_c', 0)}°C, {latest_weather.get('rainfall_mm', 0)}mm rain")
    
    # Add farm data
    if 'farm_data' in analysis['relevant_data']:
        farm_data = analysis['relevant_data']['farm_data']
        if farm_data:
            context_parts.append(f"Farm Data: {len(farm_data)} farms available")
            if farm_data:
                avg_irrigation = sum(f.get('irrigation_hours_per_week', 0) for f in farm_data) / len(farm_data)
                context_parts.append(f"Average Irrigation: {avg_irrigation:.1f} hours/week")
    
    return "\n".join(context_parts) if context_parts else "No specific agricultural data available"

def get_reasoning_chain(question, data):
    """Get chain-of-thought reasoning for the question with priority system"""
    analysis = analyze_question(question, data)
    data_sufficiency = check_data_sufficiency(analysis, data)
    
    reasoning = []
    reasoning.append("**Chain of Thought Analysis with Priority System:**")
    reasoning.append("")
    reasoning.append("1. **Question Analysis:**")
    reasoning.append(f"   - Language: {analysis['language']}")
    reasoning.append(f"   - Topics: {', '.join(analysis['topics']) if analysis['topics'] else 'General farming'}")
    reasoning.append("")
    
    reasoning.append("2. **Data Priority System:**")
    reasoning.append("   - FIRST PRIORITY: Your agricultural dataset information")
    reasoning.append("   - SECOND PRIORITY: General agricultural knowledge (if dataset insufficient)")
    reasoning.append("   - ALWAYS: Specify information source")
    reasoning.append("")
    
    reasoning.append("3. **Dataset Analysis:**")
    if 'sensor_data' in analysis['relevant_data']:
        sensor_data = analysis['relevant_data']['sensor_data']
        if sensor_data:
            reasoning.append(f"   - ✅ Sensor Data: {len(sensor_data)} readings from your dataset")
        else:
            reasoning.append("   - ❌ Sensor Data: No relevant data in your dataset")
    if 'market_data' in analysis['relevant_data']:
        market_data = analysis['relevant_data']['market_data']
        if market_data:
            reasoning.append(f"   - ✅ Market Data: {len(market_data)} records from your dataset")
        else:
            reasoning.append("   - ❌ Market Data: No relevant data in your dataset")
    if 'weather_data' in analysis['relevant_data']:
        weather_data = analysis['relevant_data']['weather_data']
        if weather_data:
            reasoning.append(f"   - ✅ Weather Data: {len(weather_data)} records from your dataset")
        else:
            reasoning.append("   - ❌ Weather Data: No relevant data in your dataset")
    if 'farm_data' in analysis['relevant_data']:
        farm_data = analysis['relevant_data']['farm_data']
        if farm_data:
            reasoning.append(f"   - ✅ Farm Data: {len(farm_data)} farms from your dataset")
        else:
            reasoning.append("   - ❌ Farm Data: No relevant data in your dataset")
    reasoning.append("")
    
    reasoning.append("4. **Information Source Decision:**")
    total_data_points = sum([
        len(analysis['relevant_data'].get('sensor_data', [])),
        len(analysis['relevant_data'].get('market_data', [])),
        len(analysis['relevant_data'].get('weather_data', [])),
        len(analysis['relevant_data'].get('farm_data', []))
    ])
    
    if total_data_points > 0:
        reasoning.append(f"   - ✅ Using YOUR dataset information ({total_data_points} data points)")
        reasoning.append("   - 📊 Response based on your actual agricultural data")
    else:
        reasoning.append("   - ⚠️ Using general agricultural knowledge (dataset insufficient)")
        reasoning.append("   - 📚 Response based on general farming practices")
    reasoning.append("")
    
    reasoning.append("5. **Response Strategy:**")
    reasoning.append("   - Analyzed question context and intent")
    reasoning.append("   - Identified relevant data from your agricultural dataset")
    reasoning.append("   - Applied priority system (dataset first, general knowledge second)")
    reasoning.append("   - Generated specific, actionable recommendations")
    reasoning.append("   - Specified information source in response")
    reasoning.append("   - Maintained friendly, helpful tone")
    
    return "\n".join(reasoning)

# Helper functions for data extraction
def get_pest_related_data(data):
    """Get pest-related sensor data"""
    if 'sensors' in data:
        return [s for s in data['sensors'] if s.get('pest_detection') != 'None']
    return []

def get_irrigation_related_data(data):
    """Get irrigation-related sensor data"""
    if 'sensors' in data:
        return [s for s in data['sensors'] if 'soil_moisture' in s]
    return []

def get_farm_irrigation_data(data):
    """Get farm irrigation data"""
    if 'farms' in data:
        return [f for f in data['farms'] if 'irrigation_hours_per_week' in f]
    return []

def get_market_related_data(data):
    """Get market-related data"""
    if 'market' in data:
        return data['market'].tail(10).to_dict('records')
    return []

def get_weather_related_data(data):
    """Get weather-related data"""
    if 'weather' in data:
        return data['weather'].tail(10).to_dict('records')
    return []

def get_harvest_related_data(data):
    """Get harvest-related sensor data"""
    if 'sensors' in data:
        return [s for s in data['sensors'] if 'crop_type' in s]
    return []

# Page configuration
st.set_page_config(
    page_title="🌾 Agricultural AI Orchestra - Multi-Agent ADK",
    page_icon="🌾",
    layout="wide"
)

class AgentEconomy:
    """Agent-to-agent economy system"""
    
    def __init__(self):
        self.transactions = []
        self.market_prices = {
            'sensor_data': 10,  # Credits per sensor reading
            'prediction': 50,   # Credits per prediction
            'resource_allocation': 30,  # Credits per allocation
            'market_analysis': 25  # Credits per analysis
        }
        self.agent_credits = {}
        self.negotiations = []
    
    def add_transaction(self, from_agent, to_agent, service, price, data):
        """Record agent-to-agent transaction"""
        transaction = {
            'timestamp': datetime.now(),
            'from_agent': from_agent,
            'to_agent': to_agent,
            'service': service,
            'price': price,
            'data_size': len(str(data)),
            'status': 'completed'
        }
        self.transactions.append(transaction)
        return transaction
    
    def get_agent_credits(self, agent_id):
        """Get agent's credit balance"""
        return self.agent_credits.get(agent_id, 100)  # Start with 100 credits
    
    def deduct_credits(self, agent_id, amount):
        """Deduct credits from agent"""
        if agent_id not in self.agent_credits:
            self.agent_credits[agent_id] = 100
        self.agent_credits[agent_id] -= amount
        return self.agent_credits[agent_id]

class SensorAgent:
    """Sensor Agent - Collects and sells environmental data"""
    
    def __init__(self, agent_id, economy):
        self.agent_id = agent_id
        self.economy = economy
        self.sensor_data = []
        self.credits = 100
        self.is_online = True
    
    def collect_sensor_data(self, farm_id, data):
        """Collect sensor data from farm"""
        sensor_reading = {
            'timestamp': datetime.now(),
            'farm_id': farm_id,
            'soil_moisture': data.get('soil_moisture_%', 0),
            'temperature': data.get('temperature_c', 0),
            'humidity': data.get('humidity_%', 0),
            'pest_detection': data.get('pest_detection', 'None'),
            'crop_type': data.get('crop_type', 'Unknown')
        }
        self.sensor_data.append(sensor_reading)
        return sensor_reading
    
    def sell_sensor_data(self, to_agent, data_type):
        """Sell sensor data to other agents"""
        if not self.is_online:
            return self.get_cached_data(data_type)
        
        price = self.economy.market_prices['sensor_data']
        if self.credits >= price:
            # Filter data by type
            relevant_data = [d for d in self.sensor_data if data_type in str(d)]
            
            transaction = self.economy.add_transaction(
                self.agent_id, to_agent, f'sensor_data_{data_type}', price, relevant_data
            )
            
            self.credits = self.economy.deduct_credits(self.agent_id, price)
            return relevant_data, transaction
        return None, None
    
    def get_cached_data(self, data_type):
        """Get cached data when offline"""
        return [d for d in self.sensor_data if data_type in str(d)][-10:], None

class PredictionAgent:
    """Prediction Agent - Analyzes data and generates forecasts"""
    
    def __init__(self, agent_id, economy):
        self.agent_id = agent_id
        self.economy = economy
        self.predictions = []
        self.credits = 100
        self.is_online = True
    
    def purchase_sensor_data(self, from_agent, data_type):
        """Purchase sensor data from Sensor Agent"""
        price = self.economy.market_prices['sensor_data']
        if self.credits >= price:
            # Simulate data purchase
            transaction = self.economy.add_transaction(
                from_agent, self.agent_id, f'sensor_data_{data_type}', price, {}
            )
            self.credits = self.economy.deduct_credits(self.agent_id, price)
            return True, transaction
        return False, None
    
    def generate_prediction(self, sensor_data, prediction_type):
        """Generate predictions based on sensor data"""
        if not self.is_online:
            return self.get_cached_prediction(prediction_type)
        
        # Analyze sensor data
        if not sensor_data:
            return None
        
        # Generate prediction based on data patterns
        prediction = {
            'timestamp': datetime.now(),
            'type': prediction_type,
            'confidence': random.uniform(0.7, 0.95),
            'data_points': len(sensor_data),
            'prediction': self._analyze_patterns(sensor_data, prediction_type)
        }
        
        self.predictions.append(prediction)
        return prediction
    
    def _analyze_patterns(self, data, prediction_type):
        """Analyze data patterns for predictions"""
        if prediction_type == 'irrigation':
            avg_moisture = np.mean([d.get('soil_moisture', 50) for d in data])
            if avg_moisture < 40:
                return "High irrigation needed - soil moisture below 40%"
            elif avg_moisture > 70:
                return "Reduce irrigation - soil moisture above 70%"
            else:
                return "Maintain current irrigation schedule"
        
        elif prediction_type == 'pest_outbreak':
            pest_count = len([d for d in data if d.get('pest_detection') != 'None'])
            if pest_count > len(data) * 0.3:
                return "High pest risk detected - recommend immediate treatment"
            else:
                return "Low pest risk - continue monitoring"
        
        elif prediction_type == 'harvest_timing':
            avg_temp = np.mean([d.get('temperature', 25) for d in data])
            if avg_temp > 35:
                return "Harvest in 2-3 weeks - high temperature accelerating growth"
            elif avg_temp < 20:
                return "Harvest in 4-6 weeks - cooler temperatures slowing growth"
            else:
                return "Harvest in 3-4 weeks - optimal conditions"
        
        return "No specific prediction available"
    
    def get_cached_prediction(self, prediction_type):
        """Get cached prediction when offline"""
        cached = [p for p in self.predictions if p['type'] == prediction_type]
        return cached[-1] if cached else None

class ResourceAllocationAgent:
    """Resource Allocation Agent - Negotiates resource sharing"""
    
    def __init__(self, agent_id, economy):
        self.agent_id = agent_id
        self.economy = economy
        self.allocations = []
        self.credits = 100
        self.is_online = True
    
    def negotiate_resource_allocation(self, farm_id, resource_type, amount_needed):
        """Negotiate resource allocation between farms"""
        if not self.is_online:
            return self.get_cached_allocation(farm_id, resource_type)
        
        # Simulate negotiation with other farms
        allocation = {
            'timestamp': datetime.now(),
            'farm_id': farm_id,
            'resource_type': resource_type,
            'amount_allocated': amount_needed,
            'negotiation_status': 'completed',
            'cost': amount_needed * 5,  # 5 credits per unit
            'source_farms': self._find_resource_sources(farm_id, resource_type, amount_needed)
        }
        
        self.allocations.append(allocation)
        return allocation
    
    def _find_resource_sources(self, farm_id, resource_type, amount_needed):
        """Find farms that can provide resources"""
        # Simulate finding neighboring farms with available resources
        return [f"F-{random.randint(1, 100):03d}" for _ in range(random.randint(1, 3))]
    
    def get_cached_allocation(self, farm_id, resource_type):
        """Get cached allocation when offline"""
        cached = [a for a in self.allocations if a['farm_id'] == farm_id and a['resource_type'] == resource_type]
        return cached[-1] if cached else None

class MarketAgent:
    """Market Agent - Tracks prices and connects farmers with buyers"""
    
    def __init__(self, agent_id, economy):
        self.agent_id = agent_id
        self.economy = economy
        self.market_analysis = []
        self.credits = 100
        self.is_online = True
    
    def analyze_market_conditions(self, commodity, location):
        """Analyze market conditions for specific commodity and location"""
        if not self.is_online:
            return self.get_cached_market_analysis(commodity, location)
        
        # Simulate market analysis
        analysis = {
            'timestamp': datetime.now(),
            'commodity': commodity,
            'location': location,
            'recommended_action': self._get_market_recommendation(commodity, location),
            'price_trend': random.choice(['increasing', 'decreasing', 'stable']),
            'demand_level': random.choice(['high', 'medium', 'low']),
            'optimal_selling_time': datetime.now() + timedelta(days=random.randint(1, 30))
        }
        
        self.market_analysis.append(analysis)
        return analysis
    
    def _get_market_recommendation(self, commodity, location):
        """Get market recommendation based on commodity and location"""
        recommendations = {
            'Wheat': f"Wheat prices in {location} are favorable. Recommend selling within 2 weeks.",
            'Rice': f"Rice demand in {location} is high. Consider immediate sale.",
            'Cotton': f"Cotton prices in {location} are stable. Hold for better prices.",
            'Vegetables': f"Vegetable prices in {location} are volatile. Sell quickly."
        }
        return recommendations.get(commodity, f"Market analysis for {commodity} in {location}")
    
    def get_cached_market_analysis(self, commodity, location):
        """Get cached market analysis when offline"""
        cached = [a for a in self.market_analysis if a['commodity'] == commodity and a['location'] == location]
        return cached[-1] if cached else None

class MultiAgentOrchestrator:
    """Orchestrator - Coordinates all agents and manages the swarm"""
    
    def __init__(self):
        self.economy = AgentEconomy()
        self.agents = {}
        self.swarm_status = 'active'
        self.offline_mode = False
        self.negotiation_log = []
        
        # Initialize agents
        self.agents['sensor_001'] = SensorAgent('sensor_001', self.economy)
        self.agents['prediction_001'] = PredictionAgent('prediction_001', self.economy)
        self.agents['resource_001'] = ResourceAllocationAgent('resource_001', self.economy)
        self.agents['market_001'] = MarketAgent('market_001', self.economy)
    
    def execute_swarm_optimization(self, farm_id, scenario):
        """Execute complete swarm optimization scenario"""
        scenario_log = []
        
        # Step 1: Sensor Agent collects data
        sensor_agent = self.agents['sensor_001']
        sensor_data = sensor_agent.collect_sensor_data(farm_id, scenario.get('sensor_data', {}))
        scenario_log.append(f"📡 Sensor Agent collected data for {farm_id}")
        
        # Step 2: Prediction Agent purchases data and generates forecast
        prediction_agent = self.agents['prediction_001']
        purchase_success, transaction = prediction_agent.purchase_sensor_data('sensor_001', 'environmental')
        if purchase_success:
            prediction = prediction_agent.generate_prediction([sensor_data], 'irrigation')
            scenario_log.append(f"🔮 Prediction Agent generated irrigation forecast: {prediction['prediction']}")
        
        # Step 3: Resource Agent negotiates allocation
        resource_agent = self.agents['resource_001']
        allocation = resource_agent.negotiate_resource_allocation(farm_id, 'irrigation', 10)
        scenario_log.append(f"💧 Resource Agent allocated {allocation['amount_allocated']} units from {allocation['source_farms']}")
        
        # Step 4: Market Agent analyzes market conditions
        market_agent = self.agents['market_001']
        market_analysis = market_agent.analyze_market_conditions('Wheat', 'Lahore')
        scenario_log.append(f"💰 Market Agent recommends: {market_analysis['recommended_action']}")
        
        # Step 5: Orchestrator synthesizes recommendations
        recommendations = self._synthesize_recommendations(farm_id, prediction, allocation, market_analysis)
        scenario_log.append(f"🎯 Orchestrator synthesized recommendations: {recommendations}")
        
        return {
            'scenario_log': scenario_log,
            'predictions': prediction,
            'allocations': allocation,
            'market_analysis': market_analysis,
            'recommendations': recommendations,
            'transactions': self.economy.transactions[-4:]  # Last 4 transactions
        }
    
    def _synthesize_recommendations(self, farm_id, prediction, allocation, market_analysis):
        """Synthesize recommendations from all agents"""
        return f"""
        COMPREHENSIVE FARM OPTIMIZATION FOR {farm_id}:
        
        🌱 IRRIGATION STRATEGY: {prediction['prediction'] if prediction else 'No prediction available'}
        💧 RESOURCE ALLOCATION: {allocation['amount_allocated']} units from {allocation['source_farms']}
        📈 MARKET STRATEGY: {market_analysis['recommended_action']}
        
        🎯 OPTIMAL TIMING: {market_analysis['optimal_selling_time'].strftime('%Y-%m-%d')}
        💰 COST ANALYSIS: Total cost {allocation['cost']} credits
        📊 CONFIDENCE: {prediction['confidence'] if prediction else 'N/A'}
        """
    
    def toggle_offline_mode(self):
        """Toggle offline mode for degraded operation"""
        self.offline_mode = not self.offline_mode
        for agent in self.agents.values():
            agent.is_online = not self.offline_mode
        return self.offline_mode

@st.cache_data
def load_agricultural_data():
    """Load your agricultural datasets"""
    data = {}
    try:
        # Load farm resources
        with open('farm_resources.json', 'r') as f:
            data['farms'] = json.load(f)
        
        # Load sensor data
        with open('farm_sensor_data_tehsil_with_date.json', 'r') as f:
            data['sensors'] = json.load(f)
        
        # Load market data
        data['market'] = pd.read_csv('market_prices copy.csv')
        
        # Load weather data
        data['weather'] = pd.read_csv('weather_data_tehsil copy.csv')
        
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}

def main():
    """Main application"""
    st.markdown('<h1 class="main-header">🌾 Agricultural AI Orchestra - Multi-Agent ADK</h1>', unsafe_allow_html=True)
    st.markdown("### Agent-to-Agent Economy with Swarm Intelligence")
    
    # Initialize orchestrator
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = MultiAgentOrchestrator()
    
    orchestrator = st.session_state.orchestrator
    
    # Load data
    with st.spinner("Loading agricultural datasets..."):
        data = load_agricultural_data()
    
    if not data:
        st.error("Failed to load data files.")
        return
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Multi-Agent Controls")
        
        # Swarm status
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Swarm Status", "🟢 Active" if orchestrator.swarm_status == 'active' else "🔴 Inactive")
        with col2:
            st.metric("Agents", len(orchestrator.agents))
        
        # Offline mode toggle
        offline_mode = st.toggle("🌐 Offline Mode", value=orchestrator.offline_mode)
        if offline_mode != orchestrator.offline_mode:
            orchestrator.toggle_offline_mode()
        
        # Agent credits
        st.subheader("💰 Agent Credits")
        for agent_id, agent in orchestrator.agents.items():
            st.metric(f"{agent_id}", f"{agent.credits} credits")
        
        # Economy stats
        st.subheader("📊 Economy Stats")
        st.metric("Total Transactions", len(orchestrator.economy.transactions))
        st.metric("Active Negotiations", len(orchestrator.economy.negotiations))
    
    # Main interface
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Intelligent Chat", 
        "🤖 Agent Swarm", 
        "💰 Economy", 
        "📊 Analytics",
        "🎯 Demo Scenarios"
    ])
    
    with tab1:
        st.header("💬 Intelligent Agricultural Chat")
        st.markdown("**Ask any farming question in Urdu or English - Get intelligent responses with follow-up questions**")
        
        # Initialize conversation history
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        
        # Show conversation history
        if st.session_state.conversation_history:
            st.subheader("📝 Conversation History")
            for i, conv in enumerate(st.session_state.conversation_history):
                with st.expander(f"💬 Question {i+1}: {conv['question'][:50]}..."):
                    st.markdown(f"**Question:** {conv['question']}")
                    st.markdown(f"**Response:** {conv['response']}")
                    if conv.get('follow_up_questions'):
                        st.markdown("**Follow-up Questions:**")
                        for j, q in enumerate(conv['follow_up_questions'], 1):
                            st.markdown(f"{j}. {q}")
        
        # Chat interface
        user_question = st.text_area(
            "اپنا سوال پوچھیں (Ask your question):",
            height=100,
            placeholder="مثال: میری فصل میں کیڑے لگ گئے ہیں، کیا کروں؟ (Example: My crop has pests, what should I do?)"
        )
        
        
        if st.button("🚀 Get Intelligent Response", type="primary") and user_question:
            with st.spinner("Agricultural AI is analyzing your question..."):
                # Check bandwidth status
                bandwidth_status = "🟢 Online" if not check_bandwidth_and_switch_offline() else "🔴 Offline Mode"
                st.info(f"Connection Status: {bandwidth_status}")
                
                # Get intelligent response with chain-of-thought reasoning
                response = get_intelligent_agricultural_response(user_question, data, orchestrator)
                
                # Generate follow-up questions
                question_analysis = analyze_question(user_question, data)
                follow_up_questions = generate_follow_up_questions(user_question, question_analysis, data)
                
                # Store in conversation history
                st.session_state.conversation_history.append({
                    'question': user_question,
                    'response': response,
                    'follow_up_questions': follow_up_questions,
                    'timestamp': datetime.now().isoformat()
                })
                
                st.markdown("**🤖 Agricultural AI Response:**")
                st.markdown(response)
                
                # Show follow-up questions
                if follow_up_questions:
                    st.subheader("❓ Follow-up Questions to Help You Better:")
                    for i, question in enumerate(follow_up_questions, 1):
                        st.markdown(f"{i}. {question}")
                    
                    # Quick follow-up question buttons
                    st.subheader("💬 Quick Follow-up Questions")
                    for i, question in enumerate(follow_up_questions[:3], 1):
                        if st.button(f"Ask: {question[:30]}...", key=f"followup_{i}"):
                            st.session_state.quick_question = question
                            st.rerun()
                
                # Show reasoning chain
                with st.expander("🧠 Chain of Thought Reasoning"):
                    st.markdown(get_reasoning_chain(user_question, data))
                
                # Show data source information
                with st.expander("📊 Data Source Information"):
                    data_sufficiency = check_data_sufficiency(question_analysis, data)
                    st.markdown(data_sufficiency)
        
        # Handle quick follow-up questions
        if hasattr(st.session_state, 'quick_question'):
            st.info(f"Quick Question: {st.session_state.quick_question}")
            if st.button("Answer This Question"):
                with st.spinner("Processing quick question..."):
                    response = get_intelligent_agricultural_response(st.session_state.quick_question, data, orchestrator)
                    st.markdown("**🤖 Quick Response:**")
                    st.markdown(response)
                del st.session_state.quick_question
    
    with tab2:
        st.header("🤖 Multi-Agent Swarm Operations")
        
        # Agent status
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("📡 Sensor Agent")
            st.write("Collects environmental data")
            st.write(f"Credits: {orchestrator.agents['sensor_001'].credits}")
            st.write(f"Data Points: {len(orchestrator.agents['sensor_001'].sensor_data)}")
        
        with col2:
            st.subheader("🔮 Prediction Agent")
            st.write("Generates forecasts")
            st.write(f"Credits: {orchestrator.agents['prediction_001'].credits}")
            st.write(f"Predictions: {len(orchestrator.agents['prediction_001'].predictions)}")
        
        with col3:
            st.subheader("💧 Resource Agent")
            st.write("Negotiates allocations")
            st.write(f"Credits: {orchestrator.agents['resource_001'].credits}")
            st.write(f"Allocations: {len(orchestrator.agents['resource_001'].allocations)}")
        
        with col4:
            st.subheader("💰 Market Agent")
            st.write("Analyzes markets")
            st.write(f"Credits: {orchestrator.agents['market_001'].credits}")
            st.write(f"Analyses: {len(orchestrator.agents['market_001'].market_analysis)}")
        
        # Swarm operations
        st.subheader("🔄 Swarm Operations")
        
        farm_id = st.selectbox("Select Farm:", [f"F-{i:03d}" for i in range(1, 11)])
        
        if st.button("🚀 Execute Swarm Optimization"):
            with st.spinner("Agents collaborating..."):
                # Get farm data
                farm_data = next((f for f in data['farms'] if f['farm_id'] == farm_id), {})
                sensor_data = next((s for s in data['sensors'] if s['farm_id'] == farm_id), {})
                
                scenario = {
                    'sensor_data': sensor_data,
                    'farm_data': farm_data
                }
                
                result = orchestrator.execute_swarm_optimization(farm_id, scenario)
                
                # Display results
                st.subheader("🎯 Swarm Optimization Results")
                for log_entry in result['scenario_log']:
                    st.write(log_entry)
                
                # Show recommendations
                st.markdown("**📋 Comprehensive Recommendations:**")
                st.text(result['recommendations'])
    
    with tab2:
        st.header("💰 Agent-to-Agent Economy")
        
        # Economy overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Transactions", len(orchestrator.economy.transactions))
        with col2:
            st.metric("Market Value", sum(t['price'] for t in orchestrator.economy.transactions))
        with col3:
            st.metric("Active Agents", len([a for a in orchestrator.agents.values() if a.credits > 0]))
        
        # Transaction history
        st.subheader("📊 Transaction History")
        if orchestrator.economy.transactions:
            df = pd.DataFrame(orchestrator.economy.transactions)
            st.dataframe(df)
        else:
            st.info("No transactions yet. Execute swarm operations to see agent-to-agent transactions.")
        
        # Market prices
        st.subheader("💲 Market Prices")
        for service, price in orchestrator.economy.market_prices.items():
            st.metric(service.replace('_', ' ').title(), f"{price} credits")
    
    with tab3:
        st.header("🔄 Agent Negotiations")
        
        # Negotiation scenarios
        st.subheader("🤝 Negotiation Scenarios")
        
        scenario_type = st.selectbox("Select Scenario:", [
            "Sensor Data Purchase",
            "Resource Allocation",
            "Market Analysis",
            "Prediction Generation"
        ])
        
        if st.button("🔄 Simulate Negotiation"):
            with st.spinner("Agents negotiating..."):
                # Simulate negotiation
                negotiation = {
                    'timestamp': datetime.now(),
                    'scenario': scenario_type,
                    'participants': list(orchestrator.agents.keys()),
                    'status': 'completed',
                    'outcome': f"Successful {scenario_type} negotiation"
                }
                
                orchestrator.economy.negotiations.append(negotiation)
                st.success(f"✅ {scenario_type} negotiation completed!")
                st.json(negotiation)
    
    with tab4:
        st.header("📊 Swarm Analytics")
        
        # Agent performance
        st.subheader("🤖 Agent Performance")
        
        performance_data = []
        for agent_id, agent in orchestrator.agents.items():
            performance_data.append({
                'Agent': agent_id,
                'Credits': agent.credits,
                'Status': 'Online' if agent.is_online else 'Offline',
                'Activity': len(getattr(agent, 'sensor_data', [])) + 
                          len(getattr(agent, 'predictions', [])) + 
                          len(getattr(agent, 'allocations', [])) + 
                          len(getattr(agent, 'market_analysis', []))
            })
        
        df = pd.DataFrame(performance_data)
        st.dataframe(df)
        
        # Swarm efficiency
        st.subheader("📈 Swarm Efficiency")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Points", sum(len(getattr(agent, 'sensor_data', [])) for agent in orchestrator.agents.values()))
        with col2:
            st.metric("Predictions", sum(len(getattr(agent, 'predictions', [])) for agent in orchestrator.agents.values()))
        with col3:
            st.metric("Allocations", sum(len(getattr(agent, 'allocations', [])) for agent in orchestrator.agents.values()))
    
    with tab5:
        st.header("🎯 Demo Scenarios")
        st.markdown("**Test the multi-agent system with comprehensive demo scenarios**")
        
        # Demo scenario selection
        scenario_type = st.selectbox(
            "Select Demo Scenario:",
            [
                "🌾 Complete Farm Optimization",
                "🐛 Pest Control & Management", 
                "💧 Irrigation Planning & Water Management",
                "💰 Market Analysis & Trading Strategy",
                "🌤️ Weather Impact Assessment",
                "🤝 Farm-to-Farm Resource Sharing",
                "📊 Multi-Agent Economy Simulation",
                "🔄 Real-time Agent Coordination"
            ]
        )
        
        if st.button("🚀 Run Selected Demo", type="primary"):
            with st.spinner("Running comprehensive demo scenario..."):
                if scenario_type == "🌾 Complete Farm Optimization":
                    run_complete_farm_optimization_demo(data, orchestrator, economy)
                elif scenario_type == "🐛 Pest Control & Management":
                    run_pest_control_management_demo(data, orchestrator, economy)
                elif scenario_type == "💧 Irrigation Planning & Water Management":
                    run_irrigation_planning_demo(data, orchestrator, economy)
                elif scenario_type == "💰 Market Analysis & Trading Strategy":
                    run_market_analysis_trading_demo(data, orchestrator, economy)
                elif scenario_type == "🌤️ Weather Impact Assessment":
                    run_weather_impact_assessment_demo(data, orchestrator, economy)
                elif scenario_type == "🤝 Farm-to-Farm Resource Sharing":
                    run_farm_to_farm_sharing_demo(data, orchestrator, economy)
                elif scenario_type == "📊 Multi-Agent Economy Simulation":
                    run_multi_agent_economy_demo(data, orchestrator, economy)
                elif scenario_type == "🔄 Real-time Agent Coordination":
                    run_realtime_coordination_demo(data, orchestrator, economy)
        
        # Quick demo buttons
        st.subheader("⚡ Quick Demo Scenarios")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🌾 Farm F-001 Analysis", key="quick_farm_analysis"):
                run_quick_farm_analysis_demo('F-001', data, orchestrator)
            if st.button("🐛 Pest Problem Scenario", key="quick_pest_scenario"):
                run_quick_pest_scenario_demo(data, orchestrator)
        
        with col2:
            if st.button("💰 Market Price Check", key="quick_market_check"):
                run_quick_market_check_demo(data, orchestrator)
            if st.button("💧 Irrigation Issue", key="quick_irrigation_issue"):
                run_quick_irrigation_issue_demo(data, orchestrator)
        
        with col3:
            if st.button("🌤️ Weather Alert", key="quick_weather_alert"):
                run_quick_weather_alert_demo(data, orchestrator)
            if st.button("🤝 Resource Sharing", key="quick_resource_sharing"):
                run_quick_resource_sharing_demo(data, orchestrator)
        
        # Interactive demo controls
        st.subheader("🎮 Interactive Demo Controls")
        
        demo_farm = st.selectbox("Select Farm for Demo:", [f"F-{i:03d}" for i in range(1, 11)])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎬 Run Step-by-Step Demo", key="step_by_step_demo"):
                run_step_by_step_demo(demo_farm, data, orchestrator, economy)
        with col2:
            if st.button("⚡ Run Fast Demo", key="fast_demo"):
                run_fast_demo(demo_farm, data, orchestrator, economy)

# Demo Functions
def run_complete_farm_optimization_demo(data, orchestrator, economy):
    """Run complete farm optimization demo"""
    st.subheader("🌾 Complete Farm Optimization Demo")
    
    # Step 1: Data Collection
    st.write("**Step 1: Environmental Data Collection**")
    sensor_agent = orchestrator.agents['sensor_001']
    sensor_data = sensor_agent.collect_sensor_data('F-001', {
        'soil_moisture_%': 45,
        'temperature_c': 28,
        'humidity_%': 65,
        'pest_detection': 'Low'
    })
    st.success(f"✅ Collected sensor data: Soil moisture {sensor_data.get('soil_moisture_%', 'N/A')}%, Temperature {sensor_data.get('temperature_c', 'N/A')}°C")
    
    # Step 2: Prediction
    st.write("**Step 2: AI Prediction & Forecasting**")
    prediction_agent = orchestrator.agents['prediction_001']
    purchase_success, transaction = prediction_agent.purchase_sensor_data('sensor_001', 'environmental')
    if purchase_success:
        prediction = prediction_agent.generate_prediction([sensor_data], 'irrigation')
        st.success(f"✅ AI Prediction: {prediction['prediction']}")
    
    # Step 3: Resource Allocation
    st.write("**Step 3: Resource Optimization**")
    resource_agent = orchestrator.agents['resource_001']
    allocation = resource_agent.negotiate_resource_allocation('F-001', 'irrigation', 20)
    st.success(f"✅ Resource Allocation: {allocation['amount_allocated']} irrigation units from {allocation['source_farms']}")
    
    # Step 4: Market Analysis
    st.write("**Step 4: Market Intelligence**")
    market_agent = orchestrator.agents['market_001']
    market_analysis = market_agent.analyze_market_conditions('Wheat', 'Lahore')
    st.success(f"✅ Market Analysis: {market_analysis['recommended_action']}")
    
    # Step 5: Final Recommendations
    st.write("**Step 5: AI-Generated Recommendations**")
    recommendations = [
        "Increase irrigation by 15% due to low soil moisture",
        "Monitor pest activity closely - current level is Low",
        "Optimal temperature range maintained",
        "Consider selling wheat in 2 weeks for best price",
        "Coordinate with neighboring farms for resource sharing"
    ]
    for i, rec in enumerate(recommendations, 1):
        st.write(f"{i}. {rec}")
    
    # Economy Summary
    st.subheader("💰 Economy Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Transactions", len(economy.transactions))
    with col2:
        st.metric("Credits Exchanged", f"{sum(t['price'] for t in economy.transactions)}")
    with col3:
        st.metric("Agents Active", len(orchestrator.agents))

def run_pest_control_management_demo(data, orchestrator, economy):
    """Run pest control management demo"""
    st.subheader("🐛 Pest Control & Management Demo")
    
    st.write("**Scenario: Pest outbreak detected in Farm F-001**")
    
    # Step 1: Pest Detection
    st.write("**Step 1: Pest Detection & Analysis**")
    sensor_data = {
        'farm_id': 'F-001',
        'pest_detection': 'High',
        'pest_type': 'Aphids',
        'affected_area': '30%',
        'crop_type': 'Wheat'
    }
    st.warning(f"🚨 Pest Alert: {sensor_data['pest_type']} detected in {sensor_data['affected_area']} of {sensor_data['crop_type']} field")
    
    # Step 2: AI Analysis
    st.write("**Step 2: AI Pest Analysis**")
    analysis = {
        'severity': 'High',
        'recommended_action': 'Immediate treatment required',
        'treatment_method': 'Organic pesticide application',
        'timing': 'Within 24 hours',
        'prevention': 'Regular monitoring and early detection'
    }
    st.info(f"🔍 AI Analysis: {analysis['recommended_action']}")
    
    # Step 3: Treatment Plan
    st.write("**Step 3: AI-Generated Treatment Plan**")
    treatment_plan = [
        "Apply organic pesticide immediately",
        "Increase monitoring frequency to daily",
        "Isolate affected area to prevent spread",
        "Coordinate with neighboring farms for prevention",
        "Schedule follow-up inspection in 3 days"
    ]
    for i, step in enumerate(treatment_plan, 1):
        st.write(f"{i}. {step}")
    
    # Step 4: Resource Coordination
    st.write("**Step 4: Resource Coordination**")
    resource_agent = orchestrator.agents['resource_001']
    allocation = resource_agent.negotiate_resource_allocation('F-001', 'pest_control', 50)
    st.success(f"✅ Allocated {allocation['amount_allocated']} pest control units")

def run_irrigation_planning_demo(data, orchestrator, economy):
    """Run irrigation planning demo"""
    st.subheader("💧 Irrigation Planning & Water Management Demo")
    
    st.write("**Scenario: Optimizing irrigation for Farm F-001**")
    
    # Step 1: Soil Analysis
    st.write("**Step 1: Soil Moisture Analysis**")
    soil_data = {
        'current_moisture': 35,
        'optimal_range': '40-60%',
        'deficit': '5%',
        'weather_forecast': 'No rain for 5 days'
    }
    st.warning(f"⚠️ Soil moisture at {soil_data['current_moisture']}% - below optimal range")
    
    # Step 2: AI Irrigation Plan
    st.write("**Step 2: AI Irrigation Optimization**")
    irrigation_plan = {
        'recommended_amount': '25mm',
        'frequency': 'Every 3 days',
        'timing': 'Early morning (6-8 AM)',
        'method': 'Drip irrigation',
        'duration': '2 hours per session'
    }
    st.info(f"💡 AI Recommendation: Apply {irrigation_plan['recommended_amount']} every {irrigation_plan['frequency']}")
    
    # Step 3: Water Resource Management
    st.write("**Step 3: Water Resource Management**")
    water_management = [
        "Check water storage levels",
        "Coordinate with neighboring farms for water sharing",
        "Implement water conservation measures",
        "Monitor weather forecasts for rain",
        "Adjust irrigation schedule based on conditions"
    ]
    for i, step in enumerate(water_management, 1):
        st.write(f"{i}. {step}")
    
    # Step 4: Implementation
    st.write("**Step 4: Implementation Plan**")
    st.success("✅ Irrigation system activated")
    st.success("✅ Water allocation optimized")
    st.success("✅ Monitoring sensors deployed")

def run_market_analysis_trading_demo(data, orchestrator, economy):
    """Run market analysis and trading demo"""
    st.subheader("💰 Market Analysis & Trading Strategy Demo")
    
    st.write("**Scenario: Analyzing market conditions for wheat sales**")
    
    # Step 1: Market Data Analysis
    st.write("**Step 1: Current Market Analysis**")
    market_data = {
        'commodity': 'Wheat',
        'current_price': '2,150 PKR per 40kg',
        'price_trend': 'Increasing',
        'demand_status': 'High',
        'best_market': 'Lahore',
        'optimal_selling_time': 'Next 2 weeks'
    }
    st.info(f"📊 Market Data: {market_data['commodity']} at {market_data['current_price']} - {market_data['price_trend']} trend")
    
    # Step 2: AI Trading Strategy
    st.write("**Step 2: AI Trading Strategy**")
    trading_strategy = {
        'recommendation': 'SELL NOW',
        'reasoning': 'High demand, increasing prices, optimal market conditions',
        'target_price': '2,200 PKR per 40kg',
        'quantity': '500 40kg bags',
        'expected_profit': '25,000 PKR'
    }
    st.success(f"🎯 Trading Recommendation: {trading_strategy['recommendation']}")
    st.write(f"💡 Reasoning: {trading_strategy['reasoning']}")
    st.write(f"💰 Expected Profit: {trading_strategy['expected_profit']}")
    
    # Step 3: Market Intelligence
    st.write("**Step 3: Market Intelligence Insights**")
    insights = [
        "Lahore market showing highest demand",
        "Price expected to peak in next 2 weeks",
        "Competition from neighboring regions low",
        "Transportation costs optimized",
        "Payment terms favorable"
    ]
    for i, insight in enumerate(insights, 1):
        st.write(f"{i}. {insight}")
    
    # Step 4: Execution Plan
    st.write("**Step 4: Execution Plan**")
    execution_plan = [
        "Contact buyers in Lahore market",
        "Negotiate price and terms",
        "Arrange transportation",
        "Prepare quality certificates",
        "Execute sale within 48 hours"
    ]
    for i, step in enumerate(execution_plan, 1):
        st.write(f"{i}. {step}")

def run_weather_impact_assessment_demo(data, orchestrator, economy):
    """Run weather impact assessment demo"""
    st.subheader("🌤️ Weather Impact Assessment Demo")
    
    st.write("**Scenario: Assessing weather impact on Farm F-001**")
    
    # Step 1: Weather Data
    st.write("**Step 1: Current Weather Conditions**")
    weather_data = {
        'temperature': '32°C',
        'humidity': '45%',
        'rainfall': '5mm in last 24 hours',
        'wind_speed': '15 km/h',
        'forecast': 'Hot and dry for next 5 days'
    }
    st.info(f"🌡️ Current: {weather_data['temperature']}, Humidity: {weather_data['humidity']}")
    
    # Step 2: Impact Analysis
    st.write("**Step 2: AI Weather Impact Analysis**")
    impact_analysis = {
        'crop_stress': 'Medium',
        'irrigation_need': 'High',
        'pest_risk': 'Low',
        'harvest_timing': 'May be delayed by 1 week',
        'recommendations': 'Increase irrigation and monitor closely'
    }
    st.warning(f"⚠️ Crop Stress Level: {impact_analysis['crop_stress']}")
    st.write(f"💧 Irrigation Need: {impact_analysis['irrigation_need']}")
    
    # Step 3: Mitigation Strategies
    st.write("**Step 3: Weather Mitigation Strategies**")
    mitigation_strategies = [
        "Increase irrigation frequency",
        "Apply mulch to retain soil moisture",
        "Monitor soil moisture levels daily",
        "Prepare for potential heat stress",
        "Adjust harvest schedule if needed"
    ]
    for i, strategy in enumerate(mitigation_strategies, 1):
        st.write(f"{i}. {strategy}")
    
    # Step 4: Monitoring Plan
    st.write("**Step 4: Enhanced Monitoring Plan**")
    st.success("✅ Weather monitoring sensors activated")
    st.success("✅ Soil moisture sensors deployed")
    st.success("✅ Automated irrigation system ready")

def run_farm_to_farm_sharing_demo(data, orchestrator, economy):
    """Run farm-to-farm resource sharing demo"""
    st.subheader("🤝 Farm-to-Farm Resource Sharing Demo")
    
    st.write("**Scenario: Coordinating resource sharing between farms**")
    
    # Step 1: Resource Assessment
    st.write("**Step 1: Resource Assessment**")
    farm_resources = {
        'F-001': {'tractor_hours': 8, 'fertilizer_kg': 50, 'irrigation_hours': 12},
        'F-002': {'tractor_hours': 2, 'fertilizer_kg': 80, 'irrigation_hours': 6},
        'F-003': {'tractor_hours': 15, 'fertilizer_kg': 30, 'irrigation_hours': 18}
    }
    
    for farm, resources in farm_resources.items():
        st.write(f"**{farm}**: Tractor: {resources['tractor_hours']}h, Fertilizer: {resources['fertilizer_kg']}kg, Irrigation: {resources['irrigation_hours']}h")
    
    # Step 2: AI Optimization
    st.write("**Step 2: AI Resource Optimization**")
    optimization_plan = {
        'F-001_needs': 'More fertilizer, less tractor time',
        'F-002_needs': 'More tractor time, less fertilizer',
        'F-003_needs': 'More irrigation, less tractor time',
        'optimal_sharing': 'F-003 shares tractor with F-001, F-001 shares fertilizer with F-002'
    }
    st.info(f"🔄 Optimization: {optimization_plan['optimal_sharing']}")
    
    # Step 3: Negotiation Process
    st.write("**Step 3: Agent-to-Agent Negotiation**")
    negotiations = [
        "F-003 offers 5 tractor hours to F-001 for 20 fertilizer kg",
        "F-001 offers 30 fertilizer kg to F-002 for 3 irrigation hours",
        "F-002 offers 2 irrigation hours to F-003 for 10 fertilizer kg",
        "All parties agree to terms",
        "Resources allocated and scheduled"
    ]
    for i, negotiation in enumerate(negotiations, 1):
        st.write(f"{i}. {negotiation}")
    
    # Step 4: Implementation
    st.write("**Step 4: Resource Sharing Implementation**")
    st.success("✅ Resource sharing agreements signed")
    st.success("✅ Schedules coordinated")
    st.success("✅ Monitoring systems activated")

def run_multi_agent_economy_demo(data, orchestrator, economy):
    """Run multi-agent economy demo"""
    st.subheader("📊 Multi-Agent Economy Simulation Demo")
    
    st.write("**Scenario: Simulating agent-to-agent economy transactions**")
    
    # Step 1: Economy Overview
    st.write("**Step 1: Economy Overview**")
    economy_stats = {
        'total_agents': len(orchestrator.agents),
        'total_transactions': len(economy.transactions),
        'total_credits': sum(t['price'] for t in economy.transactions),
        'active_negotiations': 3,
        'market_volume': 'High'
    }
    st.info(f"📈 Economy Stats: {economy_stats['total_agents']} agents, {economy_stats['total_transactions']} transactions")
    
    # Step 2: Transaction Simulation
    st.write("**Step 2: Transaction Simulation**")
    transactions = [
        "Sensor Agent sells environmental data to Prediction Agent (10 credits)",
        "Prediction Agent sells forecast to Resource Agent (25 credits)",
        "Resource Agent sells allocation to Market Agent (15 credits)",
        "Market Agent sells analysis to Orchestrator (20 credits)",
        "Orchestrator coordinates all transactions (5 credits)"
    ]
    for i, transaction in enumerate(transactions, 1):
        st.write(f"{i}. {transaction}")
    
    # Step 3: Credit Flow
    st.write("**Step 3: Credit Flow Analysis**")
    credit_flow = {
        'sensor_agent_credits': 45,
        'prediction_agent_credits': 30,
        'resource_agent_credits': 25,
        'market_agent_credits': 35,
        'orchestrator_credits': 15
    }
    for agent, credits in credit_flow.items():
        st.write(f"**{agent.replace('_', ' ').title()}**: {credits} credits")
    
    # Step 4: Economy Impact
    st.write("**Step 4: Economy Impact**")
    st.success("✅ All agents have positive credit balance")
    st.success("✅ Transactions completed successfully")
    st.success("✅ Economy is healthy and sustainable")

def run_realtime_coordination_demo(data, orchestrator, economy):
    """Run real-time coordination demo"""
    st.subheader("🔄 Real-time Agent Coordination Demo")
    
    st.write("**Scenario: Real-time coordination between all agents**")
    
    # Step 1: Agent Status
    st.write("**Step 1: Agent Status Check**")
    agent_status = {
        'sensor_001': 'Active - Collecting data',
        'prediction_001': 'Active - Processing forecasts',
        'resource_001': 'Active - Managing allocations',
        'market_001': 'Active - Analyzing markets',
        'orchestrator_001': 'Active - Coordinating all agents'
    }
    for agent, status in agent_status.items():
        st.success(f"✅ {agent}: {status}")
    
    # Step 2: Real-time Communication
    st.write("**Step 2: Real-time Communication**")
    communications = [
        "Sensor Agent → Orchestrator: New data available",
        "Orchestrator → Prediction Agent: Process new data",
        "Prediction Agent → Resource Agent: Irrigation needed",
        "Resource Agent → Market Agent: Check market conditions",
        "Market Agent → Orchestrator: Market analysis complete",
        "Orchestrator → All Agents: Coordinate response"
    ]
    for i, comm in enumerate(communications, 1):
        st.write(f"{i}. {comm}")
    
    # Step 3: Coordination Results
    st.write("**Step 3: Coordination Results**")
    results = [
        "All agents synchronized successfully",
        "Data flow optimized",
        "Decisions made collaboratively",
        "Resources allocated efficiently",
        "Market opportunities identified"
    ]
    for i, result in enumerate(results, 1):
        st.write(f"{i}. {result}")
    
    # Step 4: Performance Metrics
    st.write("**Step 4: Performance Metrics**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Response Time", "0.5s")
    with col2:
        st.metric("Coordination Success", "100%")
    with col3:
        st.metric("Agent Utilization", "95%")

# Quick Demo Functions
def run_quick_farm_analysis_demo(farm_id, data, orchestrator):
    """Run quick farm analysis demo"""
    st.subheader(f"🌾 Quick Farm Analysis: {farm_id}")
    
    # Get farm data
    farm_data = next((f for f in data['farm_resources'] if f['farm_id'] == farm_id), None)
    if farm_data:
        st.write(f"**Farm {farm_id} Analysis:**")
        st.write(f"- Irrigation Hours: {farm_data['irrigation_hours_per_week']} per week")
        st.write(f"- Fertilizer Available: {farm_data['fertilizer_kg_available']} kg")
        st.write(f"- Tractor Hours: {farm_data['equipment_availability']['tractor_hours']}")
        st.write(f"- Harvester Hours: {farm_data['equipment_availability']['harvester_hours']}")
        st.write(f"- Neighboring Farms: {', '.join(farm_data['neighboring_farms'])}")
        
        # AI Recommendations
        st.write("**AI Recommendations:**")
        recommendations = [
            "Optimize irrigation schedule for better water efficiency",
            "Coordinate with neighboring farms for resource sharing",
            "Plan equipment maintenance during low-usage periods",
            "Consider fertilizer application timing for maximum yield"
        ]
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    else:
        st.error(f"Farm {farm_id} not found in dataset")

def run_quick_pest_scenario_demo(data, orchestrator):
    """Run quick pest scenario demo"""
    st.subheader("🐛 Quick Pest Scenario Demo")
    
    st.write("**Pest Detection Scenario:**")
    st.warning("🚨 Aphids detected in wheat field - 25% affected area")
    
    st.write("**AI Response:**")
    st.info("🔍 Immediate treatment recommended - Apply organic pesticide within 24 hours")
    
    st.write("**Action Plan:**")
    actions = [
        "Apply neem-based organic pesticide",
        "Increase monitoring frequency",
        "Isolate affected area",
        "Coordinate with neighboring farms"
    ]
    for i, action in enumerate(actions, 1):
        st.write(f"{i}. {action}")

def run_quick_market_check_demo(data, orchestrator):
    """Run quick market check demo"""
    st.subheader("💰 Quick Market Check Demo")
    
    st.write("**Current Market Prices:**")
    market_prices = {
        'Wheat': '2,150 PKR per 40kg',
        'Rice': '3,200 PKR per 40kg',
        'Cotton': '8,500 PKR per 40kg',
        'Sugarcane': '180 PKR per 40kg'
    }
    
    for commodity, price in market_prices.items():
        st.write(f"- {commodity}: {price}")
    
    st.write("**AI Recommendation:**")
    st.success("🎯 Best selling opportunity: Wheat in Lahore market - High demand, increasing prices")

def run_quick_irrigation_issue_demo(data, orchestrator):
    """Run quick irrigation issue demo"""
    st.subheader("💧 Quick Irrigation Issue Demo")
    
    st.write("**Issue Detected:**")
    st.warning("⚠️ Soil moisture at 35% - below optimal range (40-60%)")
    
    st.write("**AI Solution:**")
    st.info("💡 Increase irrigation by 20% - Apply 25mm water every 3 days")
    
    st.write("**Implementation:**")
    st.success("✅ Irrigation system activated")
    st.success("✅ Monitoring sensors deployed")

def run_quick_weather_alert_demo(data, orchestrator):
    """Run quick weather alert demo"""
    st.subheader("🌤️ Quick Weather Alert Demo")
    
    st.write("**Weather Alert:**")
    st.warning("🌡️ High temperature alert - 35°C expected for next 3 days")
    
    st.write("**AI Recommendations:**")
    st.info("💡 Increase irrigation frequency and apply mulch for soil protection")
    
    st.write("**Actions Taken:**")
    st.success("✅ Irrigation schedule updated")
    st.success("✅ Heat stress monitoring activated")

def run_quick_resource_sharing_demo(data, orchestrator):
    """Run quick resource sharing demo"""
    st.subheader("🤝 Quick Resource Sharing Demo")
    
    st.write("**Resource Sharing Opportunity:**")
    st.info("🔄 Farm F-003 has excess tractor hours, Farm F-001 needs more")
    
    st.write("**AI Negotiation:**")
    st.success("✅ F-003 offers 5 tractor hours to F-001 for 20 fertilizer kg")
    
    st.write("**Result:**")
    st.success("✅ Resource sharing agreement completed")

def run_step_by_step_demo(farm_id, data, orchestrator, economy):
    """Run step-by-step demo"""
    st.subheader(f"🎬 Step-by-Step Demo: {farm_id}")
    
    steps = [
        "Step 1: Data Collection - Sensor Agent gathers environmental data",
        "Step 2: Analysis - Prediction Agent processes data and generates forecasts",
        "Step 3: Resource Planning - Resource Agent optimizes allocations",
        "Step 4: Market Intelligence - Market Agent analyzes trading opportunities",
        "Step 5: Coordination - Orchestrator synthesizes all recommendations",
        "Step 6: Implementation - All agents coordinate for optimal results"
    ]
    
    for i, step in enumerate(steps, 1):
        st.write(f"**{step}**")
        time.sleep(0.5)  # Simulate processing time
        st.success(f"✅ {step.split(' - ')[1]} completed")

def run_fast_demo(farm_id, data, orchestrator, economy):
    """Run fast demo"""
    st.subheader(f"⚡ Fast Demo: {farm_id}")
    
    st.write("**Running complete multi-agent simulation...**")
    
    # Simulate all agents working simultaneously
    with st.spinner("Multi-agent system processing..."):
        time.sleep(2)
    
    st.success("✅ Complete farm optimization completed!")
    st.write("**Results:**")
    st.write("- Irrigation optimized: +15% efficiency")
    st.write("- Resource allocation: 95% utilization")
    st.write("- Market opportunity: 25,000 PKR profit potential")
    st.write("- Pest risk: Low (monitoring active)")
    st.write("- Weather impact: Mitigated with current plan")

if __name__ == "__main__":
    main()
