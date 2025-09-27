"""
RAG (Retrieval Augmented Generation) system for the Multi-Agent Agricultural AI System
"""
import os
import json
import pandas as pd
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGSystem:
    """RAG system for document retrieval and generation"""
    
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        self.collections = {}
        self._initialize_collections()
    
    def _initialize_collections(self):
        """Initialize ChromaDB collections for different data types"""
        collections_config = {
            "farm_resources": "Farm resource and equipment data",
            "sensor_data": "Sensor readings and crop monitoring data", 
            "market_data": "Market prices and commodity data",
            "weather_data": "Weather and environmental data"
        }
        
        for collection_name, description in collections_config.items():
            try:
                self.collections[collection_name] = self.chroma_client.get_or_create_collection(
                    name=collection_name,
                    metadata={"description": description}
                )
                logger.info(f"Initialized collection: {collection_name}")
            except Exception as e:
                logger.error(f"Error initializing collection {collection_name}: {e}")
    
    def _chunk_data(self, data: List[Dict], chunk_size: int = 1000) -> List[Dict]:
        """Split data into chunks for embedding"""
        chunks = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            chunks.append({
                'data': chunk,
                'chunk_id': f"chunk_{i//chunk_size}",
                'size': len(chunk)
            })
        return chunks
    
    def _create_document_text(self, record: Dict, data_type: str) -> str:
        """Convert data record to searchable text"""
        if data_type == "farm_resources":
            return f"""
            Farm ID: {record.get('farm_id', 'N/A')}
            Irrigation Hours per Week: {record.get('irrigation_hours_per_week', 'N/A')}
            Fertilizer Available (kg): {record.get('fertilizer_kg_available', 'N/A')}
            Tractor Hours: {record.get('equipment_availability', {}).get('tractor_hours', 'N/A')}
            Harvester Hours: {record.get('equipment_availability', {}).get('harvester_hours', 'N/A')}
            Neighboring Farms: {', '.join(record.get('neighboring_farms', []))}
            """
        
        elif data_type == "sensor_data":
            return f"""
            Date: {record.get('date', 'N/A')}
            Farm ID: {record.get('farm_id', 'N/A')}
            Location: {record.get('tehsil', 'N/A')}, {record.get('district', 'N/A')}, {record.get('province', 'N/A')}
            Crop Type: {record.get('crop_type', 'N/A')}
            Soil Moisture: {record.get('soil_moisture_%', 'N/A')}%
            Temperature: {record.get('temperature_c', 'N/A')}°C
            Humidity: {record.get('humidity_%', 'N/A')}%
            Pest Detection: {record.get('pest_detection', 'N/A')}
            """
        
        elif data_type == "market_data":
            return f"""
            Date: {record.get('date', 'N/A')}
            Market Location: {record.get('market_location', 'N/A')}
            Commodity: {record.get('commodity', 'N/A')}
            Min Price (PKR/40kg): {record.get('min_price_pkr_per_40kg', 'N/A')}
            Max Price (PKR/40kg): {record.get('max_price_pkr_per_40kg', 'N/A')}
            Avg Price (PKR/40kg): {record.get('avg_price_pkr_per_40kg', 'N/A')}
            Demand Status: {record.get('demand_status', 'N/A')}
            """
        
        elif data_type == "weather_data":
            return f"""
            Date: {record.get('date', 'N/A')}
            Location: {record.get('tehsil', 'N/A')}, {record.get('district', 'N/A')}, {record.get('province', 'N/A')}
            Rainfall: {record.get('rainfall_mm', 'N/A')}mm
            Temperature: {record.get('temperature_c', 'N/A')}°C
            Humidity: {record.get('humidity_%', 'N/A')}%
            Extreme Event: {record.get('extreme_event', 'N/A')}
            """
        
        return str(record)
    
    def index_farm_resources(self, farm_data: List[Dict]):
        """Index farm resources data"""
        try:
            collection = self.collections["farm_resources"]
            documents = []
            metadatas = []
            ids = []
            
            for i, record in enumerate(farm_data):
                doc_text = self._create_document_text(record, "farm_resources")
                documents.append(doc_text)
                metadatas.append({
                    "farm_id": record.get('farm_id', ''),
                    "data_type": "farm_resources"
                })
                ids.append(f"farm_{i}")
            
            if documents:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Indexed {len(documents)} farm resource records")
        except Exception as e:
            logger.error(f"Error indexing farm resources: {e}")
    
    def index_sensor_data(self, sensor_data: List[Dict]):
        """Index sensor data"""
        try:
            collection = self.collections["sensor_data"]
            documents = []
            metadatas = []
            ids = []
            
            for i, record in enumerate(sensor_data):
                doc_text = self._create_document_text(record, "sensor_data")
                documents.append(doc_text)
                metadatas.append({
                    "farm_id": record.get('farm_id', ''),
                    "date": record.get('date', ''),
                    "crop_type": record.get('crop_type', ''),
                    "data_type": "sensor_data"
                })
                ids.append(f"sensor_{i}")
            
            if documents:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Indexed {len(documents)} sensor data records")
        except Exception as e:
            logger.error(f"Error indexing sensor data: {e}")
    
    def index_market_data(self, market_data: pd.DataFrame):
        """Index market data"""
        try:
            collection = self.collections["market_data"]
            documents = []
            metadatas = []
            ids = []
            
            for i, (_, record) in enumerate(market_data.iterrows()):
                doc_text = self._create_document_text(record.to_dict(), "market_data")
                documents.append(doc_text)
                metadatas.append({
                    "commodity": record.get('commodity', ''),
                    "market_location": record.get('market_location', ''),
                    "date": str(record.get('date', '')),
                    "data_type": "market_data"
                })
                ids.append(f"market_{i}")
            
            if documents:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Indexed {len(documents)} market data records")
        except Exception as e:
            logger.error(f"Error indexing market data: {e}")
    
    def index_weather_data(self, weather_data: pd.DataFrame):
        """Index weather data"""
        try:
            collection = self.collections["weather_data"]
            documents = []
            metadatas = []
            ids = []
            
            for i, (_, record) in enumerate(weather_data.iterrows()):
                doc_text = self._create_document_text(record.to_dict(), "weather_data")
                documents.append(doc_text)
                metadatas.append({
                    "tehsil": record.get('tehsil', ''),
                    "district": record.get('district', ''),
                    "province": record.get('province', ''),
                    "date": str(record.get('date', '')),
                    "data_type": "weather_data"
                })
                ids.append(f"weather_{i}")
            
            if documents:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Indexed {len(documents)} weather data records")
        except Exception as e:
            logger.error(f"Error indexing weather data: {e}")
    
    def search(self, query: str, collection_name: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant documents"""
        try:
            if collection_name not in self.collections:
                logger.error(f"Collection {collection_name} not found")
                return []
            
            collection = self.collections[collection_name]
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            return results
        except Exception as e:
            logger.error(f"Error searching collection {collection_name}: {e}")
            return []
    
    def search_all_collections(self, query: str, n_results: int = 3) -> Dict[str, List[Dict]]:
        """Search across all collections"""
        results = {}
        for collection_name in self.collections.keys():
            results[collection_name] = self.search(query, collection_name, n_results)
        return results
    
    def get_context_for_query(self, query: str, max_results: int = 10) -> str:
        """Get relevant context for a query from all collections"""
        all_results = self.search_all_collections(query, max_results // len(self.collections))
        
        context_parts = []
        for collection_name, results in all_results.items():
            if results and 'documents' in results:
                for doc in results['documents'][0]:
                    context_parts.append(doc)
        
        return "\n\n".join(context_parts)
