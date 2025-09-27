"""
Data-Driven Agricultural AI Orchestra - Uses YOUR datasets as primary source
"""
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import openai           
from config import OPENAI_API_KEY

# Set your OpenAI API key
openai.api_key = OPENAI_API_KEY

# Page configuration
st.set_page_config(
    page_title="🌾 Agricultural AI Orchestra - Data-Driven",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .response-box {
        background-color: #f0f8f0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
    }
    .data-highlight {
        background-color: #e8f5e8;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_data():
    """Load ALL your agricultural data"""
    data = {}
    
    try:
        # Load farm resources (1,400+ farms)
        with open('farm_resources.json', 'r') as f:
            data['farms'] = json.load(f)
        
        # Load sensor data (36,000+ records)
        with open('farm_sensor_data_tehsil_with_date.json', 'r') as f:
            data['sensors'] = json.load(f)
        
        # Load market data (1,800+ records)
        data['market'] = pd.read_csv('market_prices copy.csv')
        
        # Load weather data (1,800+ records)
        data['weather'] = pd.read_csv('weather_data_tehsil copy.csv')
        
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}

def get_relevant_data(query, data):
    """Extract relevant data based on query"""
    relevant_data = {}
    query_lower = query.lower()
    
    # Farm Resource Agent - Extract farm data
    if any(word in query_lower for word in ['farm', 'resource', 'equipment', 'irrigation', 'fertilizer', 'tractor', 'harvester']):
        if 'farms' in data:
            relevant_data['farms'] = data['farms']
    
    # Sensor Data Agent - Extract sensor data
    if any(word in query_lower for word in ['sensor', 'soil', 'moisture', 'pest', 'crop', 'temperature', 'humidity']):
        if 'sensors' in data:
            relevant_data['sensors'] = data['sensors']
    
    # Market Intelligence Agent - Extract market data
    if any(word in query_lower for word in ['price', 'market', 'commodity', 'demand', 'trading', 'wheat', 'rice', 'cotton']):
        if 'market' in data:
            relevant_data['market'] = data['market']
    
    # Weather Agent - Extract weather data
    if any(word in query_lower for word in ['weather', 'rain', 'rainfall', 'climate', 'extreme', 'flood', 'drought']):
        if 'weather' in data:
            relevant_data['weather'] = data['weather']
    
    # If no specific keywords, include all data
    if not relevant_data:
        relevant_data = data
    
    return relevant_data

def analyze_farm_data(farm_id, data):
    """Analyze specific farm using YOUR data"""
    if 'farms' not in data:
        return "No farm data available"
    
    farm = next((f for f in data['farms'] if f['farm_id'] == farm_id), None)
    if not farm:
        return f"Farm {farm_id} not found in your dataset"
    
    # Get sensor data for this farm
    sensor_data = [s for s in data.get('sensors', []) if s['farm_id'] == farm_id]
    
    analysis = f"""
    FARM ANALYSIS FOR {farm_id} (FROM YOUR DATASET):
    
    📊 RESOURCE DATA:
    • Irrigation Hours/Week: {farm['irrigation_hours_per_week']}
    • Fertilizer Available: {farm['fertilizer_kg_available']} kg
    • Tractor Hours: {farm['equipment_availability']['tractor_hours']}
    • Harvester Hours: {farm['equipment_availability']['harvester_hours']}
    • Neighboring Farms: {', '.join(farm['neighboring_farms'])}
    
    📡 SENSOR DATA ({len(sensor_data)} records):
    """
    
    if sensor_data:
        recent_sensors = sensor_data[-5:]  # Last 5 readings
        for sensor in recent_sensors:
            analysis += f"""
    • Date: {sensor['date']} | Soil: {sensor['soil_moisture_%']}% | Temp: {sensor['temperature_c']}°C | Humidity: {sensor['humidity_%']}% | Pest: {sensor['pest_detection']}
    """
    
    return analysis

def analyze_market_data(commodity, location, data):
    """Analyze market data using YOUR data"""
    if 'market' not in data:
        return "No market data available"
    
    market_data = data['market']
    
    # Filter by commodity and location
    if commodity and commodity != 'All':
        market_data = market_data[market_data['commodity'] == commodity]
    if location and location != 'All':
        market_data = market_data[market_data['market_location'] == location]
    
    if market_data.empty:
        return f"No market data found for {commodity} in {location}"
    
    analysis = f"""
    MARKET ANALYSIS (FROM YOUR DATASET):
    
    📈 COMMODITY: {commodity or 'All'}
    📍 LOCATION: {location or 'All'}
    📊 RECORDS: {len(market_data)} data points
    
    💰 PRICE ANALYSIS:
    • Average Price: {market_data['avg_price_pkr_per_40kg'].mean():.2f} PKR/40kg
    • Min Price: {market_data['min_price_pkr_per_40kg'].min():.2f} PKR/40kg
    • Max Price: {market_data['max_price_pkr_per_40kg'].max():.2f} PKR/40kg
    
    📊 DEMAND STATUS:
    """
    
    demand_counts = market_data['demand_status'].value_counts()
    for status, count in demand_counts.items():
        analysis += f"    • {status}: {count} records\n"
    
    # Show recent data
    recent_data = market_data.tail(5)
    analysis += f"\n📅 RECENT DATA:\n"
    for _, row in recent_data.iterrows():
        analysis += f"    • {row['date']}: {row['commodity']} in {row['market_location']} - {row['avg_price_pkr_per_40kg']:.2f} PKR (Demand: {row['demand_status']})\n"
    
    return analysis

def analyze_weather_data(province, data):
    """Analyze weather data using YOUR data"""
    if 'weather' not in data:
        return "No weather data available"
    
    weather_data = data['weather']
    
    if province and province != 'All':
        weather_data = weather_data[weather_data['province'] == province]
    
    if weather_data.empty:
        return f"No weather data found for {province}"
    
    analysis = f"""
    WEATHER ANALYSIS (FROM YOUR DATASET):
    
    🌤️ PROVINCE: {province or 'All'}
    📊 RECORDS: {len(weather_data)} data points
    
    🌡️ TEMPERATURE:
    • Average: {weather_data['temperature_c'].mean():.1f}°C
    • Min: {weather_data['temperature_c'].min():.1f}°C
    • Max: {weather_data['temperature_c'].max():.1f}°C
    
    🌧️ RAINFALL:
    • Average: {weather_data['rainfall_mm'].mean():.1f}mm
    • Total: {weather_data['rainfall_mm'].sum():.1f}mm
    
    💧 HUMIDITY:
    • Average: {weather_data['humidity_%'].mean():.1f}%
    
    ⚠️ EXTREME EVENTS:
    """
    
    extreme_events = weather_data['extreme_event'].value_counts()
    for event, count in extreme_events.items():
        analysis += f"    • {event}: {count} occurrences\n"
    
    return analysis

def call_openai_with_data(query, data_context):
    """Call OpenAI with YOUR data as primary context"""
    system_prompt = f"""You are an Agricultural AI Assistant. You MUST base your responses ONLY on the provided dataset. 
    Do NOT provide generic agricultural advice. Use ONLY the specific data provided to give insights and analysis.
    
    Your role is to analyze the provided agricultural data and give insights based on the actual numbers, patterns, and trends in the dataset.
    Always reference specific data points, statistics, and patterns from the provided dataset."""
    
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Dataset Context: {data_context}\n\nQuery: {query}\n\nPlease analyze the provided data and give insights based on the actual data points."}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main application"""
    st.markdown('<h1 class="main-header">🌾 Agricultural AI Orchestra - Data-Driven</h1>', unsafe_allow_html=True)
    st.markdown("### Multi-Agent AI System Using YOUR Agricultural Datasets")
    
    # Load data
    with st.spinner("Loading YOUR agricultural datasets..."):
        data = load_all_data()
    
    if not data:
        st.error("Failed to load your data files.")
        return
    
    # Show data summary
    st.sidebar.header("📊 Your Dataset Summary")
    st.sidebar.metric("Farms", len(data.get('farms', [])))
    st.sidebar.metric("Sensor Records", len(data.get('sensors', [])))
    st.sidebar.metric("Market Records", len(data.get('market', [])))
    st.sidebar.metric("Weather Records", len(data.get('weather', [])))
    
    # Main interface
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Data-Driven Chat", 
        "🏡 Farm Analysis", 
        "📈 Market Analysis", 
        "🌤️ Weather Analysis",
        "📊 Data Explorer"
    ])
    
    with tab1:
        st.header("💬 Chat with YOUR Data")
        st.info("🤖 All responses are based on YOUR actual agricultural datasets")
        
        user_input = st.text_area(
            "Ask questions about YOUR agricultural data:",
            height=100,
            placeholder="e.g., Analyze farm F-001 using my data, What are the wheat prices in my dataset?, Show me weather patterns from my data"
        )
        
        if st.button("🚀 Analyze My Data", type="primary") and user_input:
            with st.spinner("Analyzing YOUR data..."):
                # Get relevant data based on query
                relevant_data = get_relevant_data(user_input, data)
                
                # Create data context
                data_context = ""
                if 'farms' in relevant_data:
                    data_context += f"FARM DATA: {len(relevant_data['farms'])} farms with resources, equipment, irrigation data\n"
                if 'sensors' in relevant_data:
                    data_context += f"SENSOR DATA: {len(relevant_data['sensors'])} sensor readings with soil moisture, temperature, pest detection\n"
                if 'market' in relevant_data:
                    data_context += f"MARKET DATA: {len(relevant_data['market'])} market records with commodity prices and demand\n"
                if 'weather' in relevant_data:
                    data_context += f"WEATHER DATA: {len(relevant_data['weather'])} weather records with rainfall, temperature, extreme events\n"
                
                # Get AI analysis based on YOUR data
                response = call_openai_with_data(user_input, data_context)
                
                st.markdown('<div class="response-box">', unsafe_allow_html=True)
                st.markdown("**🤖 Analysis of YOUR Data:****")
                st.markdown(response)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show data context used
                with st.expander("📋 Data Context Used"):
                    st.text(data_context)
    
    with tab2:
        st.header("🏡 Farm Analysis - YOUR Data")
        
        # Farm selection from YOUR data
        farm_ids = [farm['farm_id'] for farm in data['farms'][:20]]
        selected_farm = st.selectbox("Select Farm from YOUR dataset:", farm_ids)
        
        if selected_farm:
            # Analyze using YOUR data
            analysis = analyze_farm_data(selected_farm, data)
            
            st.markdown("**📊 Farm Analysis from YOUR Dataset:**")
            st.markdown(f'<div class="data-highlight">{analysis}</div>', unsafe_allow_html=True)
            
            # Get AI insights based on YOUR data
            if st.button("🤖 Get AI Insights"):
                with st.spinner("AI analyzing YOUR farm data..."):
                    ai_response = call_openai_with_data(f"Analyze farm {selected_farm}", analysis)
                    st.markdown("**🤖 AI Insights:**")
                    st.markdown(ai_response)
    
    with tab3:
        st.header("📈 Market Analysis - YOUR Data")
        
        col1, col2 = st.columns(2)
        with col1:
            commodities = ['All'] + list(data['market']['commodity'].unique())
            selected_commodity = st.selectbox("Commodity:", commodities)
        with col2:
            locations = ['All'] + list(data['market']['market_location'].unique())
            selected_location = st.selectbox("Location:", locations)
        
        if st.button("📊 Analyze Market"):
            analysis = analyze_market_data(selected_commodity, selected_location, data)
            st.markdown("**📈 Market Analysis from YOUR Dataset:**")
            st.markdown(f'<div class="data-highlight">{analysis}</div>', unsafe_allow_html=True)
            
            # Get AI insights
            if st.button("🤖 Get AI Market Insights"):
                with st.spinner("AI analyzing YOUR market data..."):
                    ai_response = call_openai_with_data(f"Analyze market for {selected_commodity} in {selected_location}", analysis)
                    st.markdown("**🤖 AI Market Insights:**")
                    st.markdown(ai_response)
    
    with tab4:
        st.header("🌤️ Weather Analysis - YOUR Data")
        
        provinces = ['All'] + list(data['weather']['province'].unique())
        selected_province = st.selectbox("Province:", provinces)
        
        if st.button("🌤️ Analyze Weather"):
            analysis = analyze_weather_data(selected_province, data)
            st.markdown("**🌤️ Weather Analysis from YOUR Dataset:**")
            st.markdown(f'<div class="data-highlight">{analysis}</div>', unsafe_allow_html=True)
            
            # Get AI insights
            if st.button("🤖 Get AI Weather Insights"):
                with st.spinner("AI analyzing YOUR weather data..."):
                    ai_response = call_openai_with_data(f"Analyze weather for {selected_province}", analysis)
                    st.markdown("**🤖 AI Weather Insights:**")
                    st.markdown(ai_response)
    
    with tab5:
        st.header("📊 Explore YOUR Data")
        
        # Show actual data from your datasets
        if st.button("Show Farm Data"):
            st.dataframe(pd.DataFrame(data['farms'][:10]))
        
        if st.button("Show Market Data"):
            st.dataframe(data['market'].head(10))
        
        if st.button("Show Weather Data"):
            st.dataframe(data['weather'].head(10))
        
        if st.button("Show Sensor Data"):
            st.dataframe(pd.DataFrame(data['sensors'][:10]))

if __name__ == "__main__":
    main()
