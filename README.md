# 🌾 Agricultural AI Orchestra - Multi-Agent ADK

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A sophisticated multi-agent AI system for agricultural optimization with agent-to-agent economy, intelligent chat capabilities, and robust offline functionality.

## 🚀 Features

### 🤖 Multi-Agent Architecture
- **5 Specialized Agents**: Orchestrator, Sensor, Prediction, Resource Allocation, Market Intelligence
- **Agent-to-Agent Economy**: Credit-based transaction system with negotiations
- **Swarm Intelligence**: Collaborative decision-making across agents
- **Real-time Coordination**: Dynamic agent interaction and response synthesis

### 💬 Intelligent Chat System
- **Priority-Based Responses**: Dataset-first, general knowledge fallback
- **Follow-up Questions**: Intelligent question generation for better problem understanding
- **Chain-of-Thought Reasoning**: Transparent step-by-step analysis
- **Multi-language Support**: Urdu and English with automatic language detection
- **Conversation History**: Complete interaction tracking and context management

### 🔄 Automatic Offline Mode
- **Bandwidth Detection**: Automatic monitoring of network connectivity
- **Seamless Degradation**: Transparent switch to offline mode when needed
- **Cached Data Utilization**: Historical data and pattern analysis
- **Rule-Based Decisions**: Conservative recommendations using predefined rules
- **Fallback Strategies**: Emergency protocols for critical situations

### 📊 Data-Driven Insights
- **40,000+ Records**: Comprehensive agricultural dataset
- **Real-time Analysis**: Live data processing and insights
- **Vector Embeddings**: Semantic search and context retrieval
- **RAG System**: Retrieval Augmented Generation for accurate responses

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agricultural AI Orchestra                    │
├─────────────────────────────────────────────────────────────────┤
│  🌐 Frontend Layer (Streamlit)                                 │
│  ├── Intelligent Chat Interface                                │
│  ├── Multi-Agent Dashboard                                     │
│  ├── Economy Visualization                                      │
│  └── Analytics Dashboard                                       │
├─────────────────────────────────────────────────────────────────┤
│  🤖 Agent Orchestration Layer                                  │
│  ├── Orchestrator Agent (Central Coordinator)                 │
│  ├── Sensor Agent (Environmental Data)                       │
│  ├── Prediction Agent (Forecasting)                           │
│  ├── Resource Agent (Allocation)                              │
│  └── Market Agent (Intelligence)                              │
├─────────────────────────────────────────────────────────────────┤
│  🧠 AI Processing Layer                                        │
│  ├── OpenAI Integration (GPT-3.5-turbo)                      │
│  ├── RAG System (Vector Embeddings)                           │
│  ├── Chain-of-Thought Reasoning                               │
│  └── Priority-Based Responses                              │
├─────────────────────────────────────────────────────────────────┤
│  💾 Data Layer                                                 │
│  ├── Farm Resources (1,400+ farms)                            │
│  ├── Sensor Data (36,000+ readings)                           │
│  ├── Market Data (1,800+ records)                             │
│  └── Weather Data (1,800+ records)                            │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- 4GB+ RAM recommended
- Internet connection (for online mode)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/agricultural-ai-orchestra.git
   cd agricultural-ai-orchestra
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

5. **Run the Application**:
   ```bash
   streamlit run multi_agent_adk.py --server.port 8503
   ```

6. **Access the Application**:
   Open your browser to `http://localhost:8503`

## 🤖 Multi-Agent System

### Agent Specifications

#### 🎯 Orchestrator Agent
- **Role**: Central coordinator and decision synthesizer
- **Responsibilities**: Query processing, agent coordination, response synthesis
- **Key Features**: Priority system management, follow-up question generation

#### 🌡️ Sensor Agent
- **Role**: Environmental data collection and analysis
- **Responsibilities**: Sensor data collection, validation, caching, and selling
- **Key Features**: Real-time environmental monitoring, data quality assurance

#### 🔮 Prediction Agent
- **Role**: Forecasting and predictive analytics
- **Responsibilities**: Weather prediction, pest outbreak forecasting, harvest timing
- **Key Features**: Machine learning models, pattern recognition, trend analysis

#### 🔧 Resource Allocation Agent
- **Role**: Resource optimization and sharing
- **Responsibilities**: Irrigation scheduling, fertilizer distribution, equipment sharing
- **Key Features**: Optimization algorithms, resource negotiation, farm-to-farm exchange

#### 💰 Market Intelligence Agent
- **Role**: Market analysis and trading recommendations
- **Responsibilities**: Price tracking, demand analysis, trading recommendations
- **Key Features**: Market trend analysis, price forecasting, trading strategies

## 💬 Intelligent Chat System

### Priority-Based Response System

1. **FIRST PRIORITY**: Your agricultural dataset information
2. **SECOND PRIORITY**: General agricultural knowledge (only when dataset is insufficient)
3. **ALWAYS**: Specifies information source in responses

### Follow-up Question Generation

The system automatically generates intelligent follow-up questions based on:
- **Question Topic**: Pest control, irrigation, market, weather, harvest
- **Available Data**: Sensor data, market data, weather data, farm data
- **Problem Complexity**: Simple queries vs. complex multi-faceted problems
- **User Context**: Previous questions and conversation history

### Chain-of-Thought Reasoning

Every response includes:
- **Question Analysis**: Language detection, topic identification
- **Data Priority System**: Dataset vs. general knowledge decision
- **Dataset Analysis**: Available data sources and sufficiency
- **Information Source Decision**: Clear specification of data source
- **Response Strategy**: Step-by-step reasoning process

## 🔄 Offline Mode System

### Automatic Bandwidth Detection

The system continuously monitors:
- **Connection Speed**: Response time analysis
- **Network Stability**: Error rate monitoring
- **API Availability**: Service health checks
- **Auto-Switch Logic**: Seamless transition to offline mode

### Offline Capabilities

When offline, the system provides:
- **Cached Data**: Historical agricultural data and patterns
- **Rule-Based Decisions**: Predefined decision rules for common scenarios
- **Pattern Recognition**: Historical trend analysis and recommendations
- **Fallback Strategies**: Conservative recommendations for critical situations

### Rule-Based Engine

The offline mode includes rules for:
- **Irrigation Management**: Soil moisture, temperature, humidity rules
- **Pest Control**: Pest detection, environmental condition rules
- **Harvest Planning**: Weather, temperature, rainfall rules
- **Market Analysis**: Price trend, demand pattern rules

## 📊 Data Sources

### Farm Resources (1,400+ farms)
- Farm ID and location information
- Irrigation hours per week
- Fertilizer availability (kg)
- Equipment availability (tractor, harvester hours)
- Neighboring farm networks

### Sensor Data (36,000+ readings)
- Environmental monitoring (soil moisture, temperature, humidity)
- Pest detection and monitoring
- Crop health indicators
- Time-series data for trend analysis

### Market Data (1,800+ records)
- Commodity prices (Wheat, Rice, Cotton, Sugarcane)
- Location-based pricing (Lahore, Multan, Punjab)
- Demand status and market trends
- Historical price analysis

### Weather Data (1,800+ records)
- Rainfall measurements
- Temperature and humidity data
- Extreme weather events
- Climate pattern analysis

## 🛠️ Technology Stack

### Backend Technologies
- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **OpenAI GPT-3.5-turbo**: AI language model
- **ChromaDB**: Vector database for embeddings
- **SentenceTransformers**: Text embeddings
- **Pandas**: Data processing and analysis
- **NumPy**: Numerical computing

### AI/ML Technologies
- **RAG System**: Retrieval Augmented Generation
- **Vector Embeddings**: Semantic search and similarity
- **Chain-of-Thought**: Transparent reasoning process
- **Multi-Agent Systems**: Distributed AI coordination
- **Swarm Intelligence**: Collaborative decision-making

### Data Processing
- **JSON/CSV Parsing**: Data ingestion and processing
- **Vector Indexing**: Embedding generation and storage
- **Semantic Search**: Context-aware information retrieval
- **Real-time Processing**: Live data analysis and insights

## 📚 Documentation

### Comprehensive Documentation
- **[COMPREHENSIVE_DOCUMENTATION.md](COMPREHENSIVE_DOCUMENTATION.md)**: Complete system documentation
- **[SOFTWARE_ARCHITECTURE.md](SOFTWARE_ARCHITECTURE.md)**: Detailed architecture diagrams
- **[agent_documentation.md](agent_documentation.md)**: Agent-specific documentation

### Key Documentation Sections
1. **System Overview**: High-level system description
2. **Architecture Design**: Component interactions and data flow
3. **Multi-Agent System**: Agent specifications and responsibilities
4. **Data Processing Pipeline**: Data ingestion and processing
5. **Intelligent Chat System**: Priority-based responses and follow-up questions
6. **Offline Mode System**: Bandwidth detection and fallback strategies
7. **Agent-to-Agent Economy**: Credit system and negotiations
8. **RAG Implementation**: Vector embeddings and semantic search
9. **API Integration**: OpenAI integration and error handling
10. **Deployment Guide**: Local and production deployment
11. **Testing Framework**: Unit and integration tests
12. **Performance Metrics**: System performance and scalability

## 🧪 Testing

### Unit Tests
```bash
# Run unit tests
python -m pytest tests/unit/

# Test specific components
python -m pytest tests/unit/test_agents.py
python -m pytest tests/unit/test_economy.py
```

### Integration Tests
```bash
# Run integration tests
python -m pytest tests/integration/

# Test complete workflow
python -m pytest tests/integration/test_workflow.py
```

### Offline Mode Tests
```bash
# Test offline capabilities
python offline_capabilities_test.py
python offline_mode_demo.py
python offline_mode_live_test.py
```

## 🚀 Deployment

### Local Development
```bash
# Development server
streamlit run multi_agent_adk.py --server.port 8503

# With specific configuration
streamlit run multi_agent_adk.py --server.port 8503 --server.headless true
```

### Production Deployment
```bash
# Docker deployment
docker build -t agricultural-ai-orchestra .
docker run -p 8503:8503 agricultural-ai-orchestra

# Streamlit Cloud deployment
# Connect your GitHub repository to Streamlit Cloud
# Set environment variables in Streamlit Cloud dashboard
```

### Environment Variables
```bash
# Required environment variables
OPENAI_API_KEY=your_openai_api_key
STREAMLIT_SERVER_PORT=8503
STREAMLIT_SERVER_HEADLESS=true
```

## 📈 Performance Metrics

### System Performance
- **Response Time**: < 3 seconds for complex queries
- **Offline Mode**: < 1 second for cached responses
- **Agent Coordination**: < 2 seconds for multi-agent responses
- **RAG Retrieval**: < 500ms for semantic search

### Data Processing
- **Data Loading**: < 10 seconds for 40,000+ records
- **Vector Indexing**: < 30 seconds for full dataset
- **Semantic Search**: < 200ms per query
- **Agent Transactions**: < 100ms per transaction

### Resource Utilization
- **Memory Usage**: ~2GB for full dataset
- **CPU Usage**: < 50% during normal operation
- **Storage**: ~500MB for vector database
- **Network**: Minimal (offline mode available)

## 🔮 Future Enhancements

### Short-term (3-6 months)
- **Advanced Analytics**: Machine learning models for crop yield prediction
- **Mobile Application**: Native mobile app for field operations
- **Voice Interface**: Voice-activated agricultural assistant
- **Real-time Monitoring**: Live sensor data integration

### Medium-term (6-12 months)
- **IoT Integration**: Direct integration with IoT sensors
- **Computer Vision**: Image analysis for crop health assessment
- **Automated Systems**: Integration with irrigation and pest control systems
- **Federated Learning**: Distributed learning across farms

### Long-term (1-2 years)
- **Blockchain Integration**: Transparent and secure transactions
- **Edge Computing**: Distributed computing for remote areas
- **Quantum Computing**: Advanced optimization algorithms
- **5G Integration**: High-speed connectivity for real-time operations

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for all functions
- Include unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI**: For providing the GPT-3.5-turbo API
- **Streamlit**: For the excellent web framework
- **ChromaDB**: For vector database capabilities
- **SentenceTransformers**: For text embedding models
- **Agricultural Community**: For providing valuable feedback and requirements

## 📞 Support

For support and questions:
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/agricultural-ai-orchestra/issues)
- **Documentation**: Check the comprehensive documentation
- **Community**: Join our agricultural AI community discussions

## 🌟 Star the Repository

If you find this project helpful, please give it a star! ⭐

---

**Agricultural AI Orchestra** - Revolutionizing agriculture through intelligent multi-agent systems and advanced AI technology.
