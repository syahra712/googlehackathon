"""
Streamlit-based chatbot interface for the Multi-Agent Agricultural AI System
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from multi_agent_system import MultiAgentAgriculturalSystem
from config import OPENAI_API_KEY

# Page configuration
st.set_page_config(
    page_title="Agricultural AI Orchestra",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
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
    .agent-card {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2E8B57;
    }
    .response-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_system():
    """Initialize the multi-agent system with caching"""
    try:
        api_key = st.session_state.get('openai_api_key', OPENAI_API_KEY)
        if not api_key:
            return None
        return MultiAgentAgriculturalSystem(api_key)
    except Exception as e:
        st.error(f"Error initializing system: {e}")
        return None

def main():
    """Main application function"""
    st.markdown('<h1 class="main-header">🌾 Agricultural AI Orchestra</h1>', unsafe_allow_html=True)
    st.markdown("### Multi-Agent AI System for Agricultural Intelligence")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.get('openai_api_key', ''),
            type="password",
            help="Enter your OpenAI API key"
        )
        
        if api_key:
            st.session_state['openai_api_key'] = api_key
        
        st.divider()
        
        # System status
        st.header("📊 System Status")
        if 'system' in st.session_state and st.session_state['system']:
            status = st.session_state['system'].get_system_status()
            st.success("✅ System Operational")
            st.metric("Agents", status['agents_initialized'])
            st.metric("Collections", len(status['rag_collections']))
        else:
            st.error("❌ System Not Initialized")
        
        st.divider()
        
        # Quick actions
        st.header("🚀 Quick Actions")
        if st.button("🔄 Refresh System"):
            st.cache_resource.clear()
            st.rerun()
        
        if st.button("📊 View Data Summary"):
            st.session_state['show_data_summary'] = True

    # Initialize system
    if 'system' not in st.session_state or st.session_state['system'] is None:
        if api_key:
            with st.spinner("Initializing Multi-Agent System..."):
                st.session_state['system'] = initialize_system()
            if st.session_state['system']:
                st.success("System initialized successfully!")
            else:
                st.error("Failed to initialize system. Please check your API key.")
                return
        else:
            st.warning("Please enter your OpenAI API key in the sidebar to continue.")
            return

    # Main interface
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Chat Interface", 
        "🏡 Farm Analysis", 
        "📈 Market Insights", 
        "🌤️ Weather Forecast", 
        "📊 Data Dashboard"
    ])

    with tab1:
        chat_interface()

    with tab2:
        farm_analysis_interface()

    with tab3:
        market_insights_interface()

    with tab4:
        weather_forecast_interface()

    with tab5:
        data_dashboard()

def chat_interface():
    """Chat interface for general queries"""
    st.header("💬 Chat with Agricultural AI Orchestra")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    # Chat input
    user_input = st.text_area(
        "Ask me anything about agriculture, farming, markets, weather, or farm management:",
        height=100,
        placeholder="e.g., What are the best irrigation practices for wheat farming? How is the rice market performing? What weather conditions should I watch for?"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("🚀 Send", type="primary")
    
    # Process query
    if send_button and user_input:
        with st.spinner("Processing your query..."):
            try:
                response = st.session_state['system'].process_query(user_input)
                
                # Add to chat history
                st.session_state['chat_history'].append({
                    'query': user_input,
                    'response': response['response'],
                    'timestamp': response['timestamp']
                })
                
                # Display response
                st.markdown('<div class="response-box">', unsafe_allow_html=True)
                st.markdown("**🤖 AI Response:**")
                st.markdown(response['response'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show context if available
                if 'context_used' in response and response['context_used']:
                    with st.expander("📋 Context Used"):
                        st.text(response['context_used'])
                
            except Exception as e:
                st.error(f"Error processing query: {e}")
    
    # Display chat history
    if st.session_state['chat_history']:
        st.header("💭 Chat History")
        for i, chat in enumerate(reversed(st.session_state['chat_history'][-5:])):
            with st.expander(f"💬 Query {len(st.session_state['chat_history'])-i}: {chat['query'][:50]}..."):
                st.markdown(f"**Query:** {chat['query']}")
                st.markdown(f"**Response:** {chat['response']}")
                st.caption(f"Time: {chat['timestamp']}")

def farm_analysis_interface():
    """Farm-specific analysis interface"""
    st.header("🏡 Farm Analysis")
    
    # Farm ID input
    farm_id = st.text_input("Enter Farm ID (e.g., F-001):", placeholder="F-001")
    
    if st.button("🔍 Analyze Farm") and farm_id:
        with st.spinner("Analyzing farm data..."):
            try:
                analysis = st.session_state['system'].get_farm_analysis(farm_id)
                
                if 'error' in analysis:
                    st.error(analysis['error'])
                else:
                    # Display analysis
                    st.markdown("### 📊 Farm Analysis Results")
                    st.markdown(analysis['analysis'])
                    
                    # Show farm data
                    with st.expander("🏡 Farm Details"):
                        st.json(analysis['farm_data'])
                    
                    # Show metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Farm ID", analysis['farm_id'])
                    with col2:
                        st.metric("Sensor Records", analysis['sensor_data_count'])
                    with col3:
                        st.metric("Analysis Time", analysis['timestamp'])
                        
            except Exception as e:
                st.error(f"Error analyzing farm: {e}")

def market_insights_interface():
    """Market insights interface"""
    st.header("📈 Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        commodity = st.selectbox(
            "Select Commodity:",
            ["Wheat", "Rice", "Maize", "Sugarcane", "Cotton", "Vegetables"],
            index=0
        )
    
    with col2:
        location = st.selectbox(
            "Select Location:",
            ["Lahore", "Multan", "Faisalabad", "Karachi", "All"],
            index=0
        )
    
    if st.button("📊 Get Market Insights"):
        with st.spinner("Analyzing market data..."):
            try:
                insights = st.session_state['system'].get_market_insights(
                    commodity if commodity != "All" else None,
                    location if location != "All" else None
                )
                
                if 'error' in insights:
                    st.error(insights['error'])
                else:
                    st.markdown("### 📈 Market Analysis")
                    st.markdown(insights['insights'])
                    
                    # Show metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Commodity", insights['commodity'] or "All")
                    with col2:
                        st.metric("Location", insights['location'] or "All")
                    with col3:
                        st.metric("Data Points", insights['data_points'])
                        
            except Exception as e:
                st.error(f"Error getting market insights: {e}")

def weather_forecast_interface():
    """Weather forecast interface"""
    st.header("🌤️ Weather Forecast")
    
    location = st.text_input("Enter Location (Tehsil):", placeholder="Depalpur")
    
    if st.button("🌤️ Get Weather Analysis"):
        with st.spinner("Analyzing weather data..."):
            try:
                forecast = st.session_state['system'].get_weather_forecast(
                    location if location else None
                )
                
                if 'error' in forecast:
                    st.error(forecast['error'])
                else:
                    st.markdown("### 🌤️ Weather Analysis")
                    st.markdown(forecast['forecast'])
                    
                    # Show metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Location", forecast['location'] or "All")
                    with col2:
                        st.metric("Data Points", forecast['data_points'])
                        
            except Exception as e:
                st.error(f"Error getting weather forecast: {e}")

def data_dashboard():
    """Data dashboard interface"""
    st.header("📊 Data Dashboard")
    
    try:
        status = st.session_state['system'].get_system_status()
        data_summary = status['data_summary']
        
        # System metrics
        st.subheader("🔧 System Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Agents", status['agents_initialized'])
        with col2:
            st.metric("Collections", len(status['rag_collections']))
        with col3:
            st.metric("Status", "Operational" if status['system_status'] == 'operational' else "Error")
        with col4:
            st.metric("Orchestrator", "Active" if status['orchestrator_status'] == 'active' else "Inactive")
        
        # Data summary
        if data_summary:
            st.subheader("📊 Data Summary")
            
            if 'farm_resources' in data_summary:
                st.subheader("🏡 Farm Resources")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Farms", data_summary['farm_resources']['total_farms'])
                with col2:
                    st.metric("Avg Irrigation Hours", f"{data_summary['farm_resources']['avg_irrigation_hours']:.1f}")
                with col3:
                    st.metric("Avg Fertilizer (kg)", f"{data_summary['farm_resources']['avg_fertilizer']:.1f}")
            
            if 'sensor_data' in data_summary:
                st.subheader("📡 Sensor Data")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Records", data_summary['sensor_data']['total_records'])
                with col2:
                    st.metric("Unique Farms", data_summary['sensor_data']['unique_farms'])
            
            if 'market_prices' in data_summary:
                st.subheader("💰 Market Data")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Records", data_summary['market_prices']['total_records'])
                with col2:
                    st.metric("Commodities", len(data_summary['market_prices']['commodities']))
            
            if 'weather_data' in data_summary:
                st.subheader("🌤️ Weather Data")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Records", data_summary['weather_data']['total_records'])
                with col2:
                    st.metric("Provinces", len(data_summary['weather_data']['provinces']))
        
        # Agent information
        st.subheader("🤖 Agent Information")
        agents_info = [
            {"name": "Farm Resource Agent", "description": "Manages farm resources and equipment"},
            {"name": "Sensor Data Agent", "description": "Analyzes sensor readings and crop health"},
            {"name": "Market Intelligence Agent", "description": "Provides market analysis and insights"},
            {"name": "Weather Agent", "description": "Processes weather and environmental data"},
            {"name": "Orchestrator Agent", "description": "Coordinates all specialized agents"}
        ]
        
        for agent in agents_info:
            st.markdown(f"""
            <div class="agent-card">
                <strong>{agent['name']}</strong><br>
                {agent['description']}
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

if __name__ == "__main__":
    main()
