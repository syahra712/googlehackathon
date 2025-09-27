"""
Multi-Agent Agricultural AI System - Main orchestrator
"""
import os
import logging
from typing import Dict, List, Any, Optional
from data_loader import DataLoader
from rag_system import RAGSystem
from agents import (
    FarmResourceAgent, 
    SensorDataAgent, 
    MarketIntelligenceAgent, 
    WeatherAgent, 
    OrchestratorAgent
)
from config import OPENAI_API_KEY, AGENT_CONFIG, SYSTEM_PROMPTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiAgentAgriculturalSystem:
    """Main multi-agent system for agricultural intelligence"""
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or OPENAI_API_KEY
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        # Initialize components
        self.data_loader = DataLoader()
        self.rag_system = RAGSystem()
        self.specialized_agents = {}
        self.orchestrator = None
        
        # Initialize the system
        self._initialize_agents()
        self._load_and_index_data()
    
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        try:
            self.specialized_agents = {
                'farm_resource_agent': FarmResourceAgent(self.openai_api_key),
                'sensor_data_agent': SensorDataAgent(self.openai_api_key),
                'market_intelligence_agent': MarketIntelligenceAgent(self.openai_api_key),
                'weather_agent': WeatherAgent(self.openai_api_key)
            }
            
            self.orchestrator = OrchestratorAgent(
                self.openai_api_key, 
                self.specialized_agents
            )
            
            logger.info("All agents initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing agents: {e}")
            raise
    
    def _load_and_index_data(self):
        """Load and index all data sources"""
        try:
            # Load data
            logger.info("Loading farm resources data...")
            farm_resources = self.data_loader.load_farm_resources("farm_resources.json")
            
            logger.info("Loading sensor data...")
            sensor_data = self.data_loader.load_sensor_data("farm_sensor_data_tehsil_with_date.json")
            
            logger.info("Loading market prices data...")
            market_prices = self.data_loader.load_market_prices("market_prices copy.csv")
            
            logger.info("Loading weather data...")
            weather_data = self.data_loader.load_weather_data("weather_data_tehsil copy.csv")
            
            # Index data in RAG system
            logger.info("Indexing data in RAG system...")
            if farm_resources:
                self.rag_system.index_farm_resources(farm_resources)
            if sensor_data:
                self.rag_system.index_sensor_data(sensor_data)
            if not market_prices.empty:
                self.rag_system.index_market_data(market_prices)
            if not weather_data.empty:
                self.rag_system.index_weather_data(weather_data)
            
            logger.info("Data loading and indexing completed successfully")
        except Exception as e:
            logger.error(f"Error loading and indexing data: {e}")
            raise
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query through the multi-agent system"""
        try:
            # Get relevant context from RAG system
            context = self.rag_system.get_context_for_query(query)
            
            # Process through orchestrator
            response = self.orchestrator.process_query(query, context)
            
            # Get data summary for additional context
            data_summary = self.data_loader.get_data_summary()
            
            return {
                "query": query,
                "response": response,
                "context_used": context[:500] + "..." if len(context) > 500 else context,
                "data_summary": data_summary,
                "agents_used": list(self.specialized_agents.keys()),
                "timestamp": self._get_timestamp()
            }
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "query": query,
                "response": f"Error processing query: {str(e)}",
                "error": True,
                "timestamp": self._get_timestamp()
            }
    
    def get_farm_analysis(self, farm_id: str) -> Dict[str, Any]:
        """Get comprehensive analysis for a specific farm"""
        try:
            # Get farm data
            farm_data = self.data_loader.get_farm_by_id(farm_id)
            if not farm_data:
                return {"error": f"Farm {farm_id} not found"}
            
            # Get sensor data for farm
            sensor_data = self.data_loader.get_sensor_data_by_farm(farm_id)
            
            # Get recent data
            recent_data = self.data_loader.get_recent_data(days=30)
            
            # Create analysis query
            analysis_query = f"""
            Provide a comprehensive analysis for Farm {farm_id} including:
            1. Resource utilization and optimization recommendations
            2. Recent sensor data analysis and crop health status
            3. Market opportunities for the farm's crops
            4. Weather impact and recommendations
            5. Overall farm performance and improvement suggestions
            """
            
            # Get context
            context = f"""
            Farm Data: {farm_data}
            Recent Sensor Data: {sensor_data[:5] if sensor_data else 'No recent data'}
            Recent Market Data: {recent_data.get('market', {}).head().to_dict() if 'market' in recent_data else 'No recent data'}
            Recent Weather Data: {recent_data.get('weather', {}).head().to_dict() if 'weather' in recent_data else 'No recent data'}
            """
            
            # Process through orchestrator
            response = self.orchestrator.process_query(analysis_query, context)
            
            return {
                "farm_id": farm_id,
                "analysis": response,
                "farm_data": farm_data,
                "sensor_data_count": len(sensor_data),
                "timestamp": self._get_timestamp()
            }
        except Exception as e:
            logger.error(f"Error analyzing farm {farm_id}: {e}")
            return {"error": f"Error analyzing farm: {str(e)}"}
    
    def get_market_insights(self, commodity: str = None, location: str = None) -> Dict[str, Any]:
        """Get market insights for specific commodity and/or location"""
        try:
            # Get market data
            if commodity:
                market_data = self.data_loader.get_market_data_by_commodity(commodity, location)
            else:
                market_data = self.data_loader.market_prices
            
            if market_data.empty:
                return {"error": "No market data available"}
            
            # Create insights query
            insights_query = f"""
            Provide market insights for {commodity or 'all commodities'} in {location or 'all locations'}:
            1. Price trends and patterns
            2. Demand analysis
            3. Market opportunities
            4. Trading recommendations
            5. Risk assessment
            """
            
            # Get context
            context = f"Market Data: {market_data.head(10).to_dict()}"
            
            # Process through market intelligence agent
            response = self.specialized_agents['market_intelligence_agent'].process_query(insights_query, context)
            
            return {
                "commodity": commodity,
                "location": location,
                "insights": response,
                "data_points": len(market_data),
                "timestamp": self._get_timestamp()
            }
        except Exception as e:
            logger.error(f"Error getting market insights: {e}")
            return {"error": f"Error getting market insights: {str(e)}"}
    
    def get_weather_forecast(self, location: str = None) -> Dict[str, Any]:
        """Get weather analysis and forecast"""
        try:
            # Get weather data
            if location:
                weather_data = self.data_loader.get_weather_data_by_location(tehsil=location)
            else:
                weather_data = self.data_loader.weather_data
            
            if weather_data.empty:
                return {"error": "No weather data available"}
            
            # Create weather query
            weather_query = f"""
            Provide weather analysis for {location or 'all locations'}:
            1. Current weather patterns
            2. Extreme weather events and risks
            3. Impact on agricultural operations
            4. Recommendations for farmers
            5. Climate trends and forecasts
            """
            
            # Get context
            context = f"Weather Data: {weather_data.head(10).to_dict()}"
            
            # Process through weather agent
            response = self.specialized_agents['weather_agent'].process_query(weather_query, context)
            
            return {
                "location": location,
                "forecast": response,
                "data_points": len(weather_data),
                "timestamp": self._get_timestamp()
            }
        except Exception as e:
            logger.error(f"Error getting weather forecast: {e}")
            return {"error": f"Error getting weather forecast: {str(e)}"}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and health"""
        return {
            "system_status": "operational",
            "agents_initialized": len(self.specialized_agents),
            "orchestrator_status": "active" if self.orchestrator else "inactive",
            "data_summary": self.data_loader.get_data_summary(),
            "rag_collections": list(self.rag_system.collections.keys()),
            "timestamp": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
