"""
Specialized AI agents for the Multi-Agent Agricultural AI System
"""
import openai
from typing import Dict, List, Any, Optional
import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all specialized agents"""
    
    def __init__(self, name: str, description: str, openai_api_key: str):
        self.name = name
        self.description = description
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        self.conversation_history = []
    
    @abstractmethod
    def process_query(self, query: str, context: str = "") -> str:
        """Process a query and return a response"""
        pass
    
    def add_to_history(self, query: str, response: str):
        """Add interaction to conversation history"""
        self.conversation_history.append({
            "query": query,
            "response": response,
            "timestamp": self._get_timestamp()
        })
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _call_openai(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo") -> str:
        """Make API call to OpenAI"""
        try:
            client = openai.OpenAI(api_key=self.openai_api_key)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return f"Error processing request: {str(e)}"

class FarmResourceAgent(BaseAgent):
    """Agent specialized in farm resource management"""
    
    def __init__(self, openai_api_key: str):
        super().__init__(
            name="Farm Resource Agent",
            description="Manages farm resources, equipment, and irrigation data",
            openai_api_key=openai_api_key
        )
    
    def process_query(self, query: str, context: str = "") -> str:
        """Process farm resource related queries"""
        system_prompt = """You are a Farm Resource Agent specialized in managing agricultural resources. 
        You have access to farm resource data including irrigation hours, fertilizer availability, 
        equipment hours (tractor and harvester), and neighboring farm relationships. 
        Your role is to provide insights on resource optimization, equipment scheduling, 
        and resource sharing recommendations."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ]
        
        response = self._call_openai(messages)
        self.add_to_history(query, response)
        return response

class SensorDataAgent(BaseAgent):
    """Agent specialized in sensor data analysis"""
    
    def __init__(self, openai_api_key: str):
        super().__init__(
            name="Sensor Data Agent",
            description="Handles sensor readings, crop monitoring, and pest detection",
            openai_api_key=openai_api_key
        )
    
    def process_query(self, query: str, context: str = "") -> str:
        """Process sensor data related queries"""
        system_prompt = """You are a Sensor Data Agent specialized in analyzing agricultural sensor data. 
        You have access to soil moisture, temperature, humidity, pest detection, and crop type data. 
        Your role is to provide insights on crop health, irrigation needs, pest management, 
        and environmental monitoring recommendations."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ]
        
        response = self._call_openai(messages)
        self.add_to_history(query, response)
        return response

class MarketIntelligenceAgent(BaseAgent):
    """Agent specialized in market analysis"""
    
    def __init__(self, openai_api_key: str):
        super().__init__(
            name="Market Intelligence Agent",
            description="Analyzes market prices, demand trends, and commodity data",
            openai_api_key=openai_api_key
        )
    
    def process_query(self, query: str, context: str = "") -> str:
        """Process market intelligence related queries"""
        system_prompt = """You are a Market Intelligence Agent specialized in agricultural market analysis. 
        You have access to commodity prices, demand status, and market trends across different locations. 
        Your role is to provide insights on pricing strategies, market opportunities, 
        and demand forecasting for agricultural products."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ]
        
        response = self._call_openai(messages)
        self.add_to_history(query, response)
        return response

class WeatherAgent(BaseAgent):
    """Agent specialized in weather analysis"""
    
    def __init__(self, openai_api_key: str):
        super().__init__(
            name="Weather Agent",
            description="Processes weather data, rainfall, temperature, and extreme events",
            openai_api_key=openai_api_key
        )
    
    def process_query(self, query: str, context: str = "") -> str:
        """Process weather related queries"""
        system_prompt = """You are a Weather Agent specialized in environmental and weather analysis. 
        You have access to rainfall, temperature, humidity, and extreme weather event data. 
        Your role is to provide insights on weather patterns, climate risks, 
        and environmental impact on agricultural operations."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ]
        
        response = self._call_openai(messages)
        self.add_to_history(query, response)
        return response

class OrchestratorAgent(BaseAgent):
    """Orchestrator agent that coordinates all specialized agents"""
    
    def __init__(self, openai_api_key: str, specialized_agents: Dict[str, BaseAgent]):
        super().__init__(
            name="Orchestrator Agent",
            description="Coordinates all agents and provides unified responses",
            openai_api_key=openai_api_key
        )
        self.specialized_agents = specialized_agents
    
    def process_query(self, query: str, context: str = "") -> str:
        """Process queries by coordinating with specialized agents"""
        # Determine which agents are relevant for the query
        relevant_agents = self._identify_relevant_agents(query)
        
        # Get responses from relevant agents
        agent_responses = {}
        for agent_name in relevant_agents:
            if agent_name in self.specialized_agents:
                agent = self.specialized_agents[agent_name]
                response = agent.process_query(query, context)
                agent_responses[agent_name] = response
        
        # Synthesize responses
        synthesized_response = self._synthesize_responses(query, agent_responses, context)
        self.add_to_history(query, synthesized_response)
        return synthesized_response
    
    def _identify_relevant_agents(self, query: str) -> List[str]:
        """Identify which agents are relevant for the query"""
        query_lower = query.lower()
        relevant_agents = []
        
        # Keywords for different agent types
        farm_keywords = ['farm', 'resource', 'equipment', 'irrigation', 'fertilizer', 'tractor', 'harvester']
        sensor_keywords = ['sensor', 'soil', 'moisture', 'pest', 'crop', 'temperature', 'humidity']
        market_keywords = ['price', 'market', 'commodity', 'demand', 'trading', 'economic']
        weather_keywords = ['weather', 'rain', 'rainfall', 'climate', 'extreme', 'flood', 'drought']
        
        if any(keyword in query_lower for keyword in farm_keywords):
            relevant_agents.append('farm_resource_agent')
        if any(keyword in query_lower for keyword in sensor_keywords):
            relevant_agents.append('sensor_data_agent')
        if any(keyword in query_lower for keyword in market_keywords):
            relevant_agents.append('market_intelligence_agent')
        if any(keyword in query_lower for keyword in weather_keywords):
            relevant_agents.append('weather_agent')
        
        # If no specific keywords found, use all agents
        if not relevant_agents:
            relevant_agents = list(self.specialized_agents.keys())
        
        return relevant_agents
    
    def _synthesize_responses(self, query: str, agent_responses: Dict[str, str], context: str) -> str:
        """Synthesize responses from multiple agents"""
        system_prompt = """You are the Orchestrator Agent, the central coordinator of the agricultural AI system. 
        You coordinate between specialized agents to provide comprehensive agricultural insights. 
        You synthesize information from farm resources, sensor data, market intelligence, and weather analysis 
        to provide holistic recommendations for agricultural decision-making."""
        
        # Prepare agent responses for synthesis
        agent_summary = "\n\n".join([
            f"{agent_name}: {response}" 
            for agent_name, response in agent_responses.items()
        ])
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""
            Original Query: {query}
            
            Context Data: {context}
            
            Specialized Agent Responses:
            {agent_summary}
            
            Please synthesize these responses into a comprehensive, coherent answer that addresses the user's query.
            """}
        ]
        
        return self._call_openai(messages)
