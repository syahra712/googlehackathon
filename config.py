"""
Configuration settings for the Multi-Agent Agricultural AI System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate API key
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required. Please set it in your .env file or environment.")

# Data file paths
FARM_RESOURCES_FILE = "farm_resources.json"
SENSOR_DATA_FILE = "farm_sensor_data_tehsil_with_date.json"
MARKET_PRICES_FILE = "market_prices copy.csv"
WEATHER_DATA_FILE = "weather_data_tehsil copy.csv"

# Agent Configuration
AGENT_CONFIG = {
    "farm_resource_agent": {
        "name": "Farm Resource Agent",
        "description": "Manages farm resources, equipment, and irrigation data",
        "specialization": "resource_management"
    },
    "sensor_data_agent": {
        "name": "Sensor Data Agent", 
        "description": "Handles sensor readings, crop monitoring, and pest detection",
        "specialization": "sensor_analysis"
    },
    "market_intelligence_agent": {
        "name": "Market Intelligence Agent",
        "description": "Analyzes market prices, demand trends, and commodity data",
        "specialization": "market_analysis"
    },
    "weather_agent": {
        "name": "Weather Agent",
        "description": "Processes weather data, rainfall, temperature, and extreme events",
        "specialization": "weather_analysis"
    },
    "orchestrator_agent": {
        "name": "Orchestrator Agent",
        "description": "Coordinates all agents and provides unified responses",
        "specialization": "coordination"
    }
}

# RAG Configuration
RAG_CONFIG = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "vector_store": "chroma"
}

# System prompts for each agent
SYSTEM_PROMPTS = {
    "farm_resource_agent": """You are a Farm Resource Agent specialized in managing agricultural resources. 
    You have access to farm resource data including irrigation hours, fertilizer availability, 
    equipment hours (tractor and harvester), and neighboring farm relationships. 
    Your role is to provide insights on resource optimization, equipment scheduling, 
    and resource sharing recommendations.""",
    
    "sensor_data_agent": """You are a Sensor Data Agent specialized in analyzing agricultural sensor data. 
    You have access to soil moisture, temperature, humidity, pest detection, and crop type data. 
    Your role is to provide insights on crop health, irrigation needs, pest management, 
    and environmental monitoring recommendations.""",
    
    "market_intelligence_agent": """You are a Market Intelligence Agent specialized in agricultural market analysis. 
    You have access to commodity prices, demand status, and market trends across different locations. 
    Your role is to provide insights on pricing strategies, market opportunities, 
    and demand forecasting for agricultural products.""",
    
    "weather_agent": """You are a Weather Agent specialized in environmental and weather analysis. 
    You have access to rainfall, temperature, humidity, and extreme weather event data. 
    Your role is to provide insights on weather patterns, climate risks, 
    and environmental impact on agricultural operations.""",
    
    "orchestrator_agent": """You are the Orchestrator Agent, the central coordinator of the agricultural AI system. 
    You coordinate between specialized agents to provide comprehensive agricultural insights. 
    You synthesize information from farm resources, sensor data, market intelligence, and weather analysis 
    to provide holistic recommendations for agricultural decision-making."""
}
