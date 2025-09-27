# 🚀 Agricultural AI Orchestra - Deployment Guide

## 🌐 Streamlit Cloud Deployment

### **Step 1: Create GitHub Repository**
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `agricultural-ai-orchestra`
3. Make it public
4. Upload all files from this directory

### **Step 2: Deploy to Streamlit Cloud**
1. Go to [Streamlit Cloud](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Select the repository: `agricultural-ai-orchestra`
5. Main file path: `multi_agent_adk.py`
6. Click "Deploy"

### **Step 3: Environment Variables**
In Streamlit Cloud, add these environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `STREAMLIT_SERVER_PORT`: 8503
- `STREAMLIT_SERVER_HEADLESS`: true

### **Step 4: Access Your Live App**
Once deployed, you'll get a URL like:
`https://agricultural-ai-orchestra.streamlit.app`

## 🔧 Local Development

### **Run Locally:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export OPENAI_API_KEY="your_api_key_here"

# Run the app
streamlit run multi_agent_adk.py --server.port 8503
```

### **Access Locally:**
- URL: `http://localhost:8503`

## 📊 Features Available

### **💬 Intelligent Chat**
- Ask questions in Urdu or English
- Get priority-based responses
- Follow-up questions
- Chain-of-thought reasoning

### **🤖 Multi-Agent System**
- 5 specialized agents
- Agent-to-agent economy
- Real-time coordination
- Swarm intelligence

### **🔮 Prediction Capabilities**
- Weather predictions
- Market price forecasts
- Crop yield predictions
- Pest outbreak predictions
- Irrigation needs predictions

### **🎯 Demo Scenarios**
- Complete Farm Optimization
- Pest Control & Management
- Irrigation Planning
- Market Analysis & Trading
- Weather Impact Assessment
- Farm-to-Farm Resource Sharing
- Multi-Agent Economy Simulation
- Real-time Agent Coordination

## 🌾 Test Questions

### **Urdu Questions:**
- "میری فصل میں کیڑے لگ گئے ہیں، کیا کروں؟"
- "کیا اگلے ہفتے بارش ہوگی؟"
- "گندم کی قیمت کیا ہوگی؟"

### **English Questions:**
- "What will my crop yield be this season?"
- "When should I harvest for maximum profit?"
- "How can I optimize my irrigation?"

## 🎬 Demo Video Questions

1. **Complex Pest Management**: "میرے کھیت میں گندم کی فصل میں مختلف قسم کے کیڑے لگ گئے ہیں..."
2. **Farm Optimization**: "I have a 10-acre wheat farm and I'm facing serious irrigation challenges..."
3. **Market Intelligence**: "میں نے 500 40kg گندم کے بوریوں کی فصل کاٹی ہے..."
4. **Weather Risk Management**: "I'm concerned about the upcoming monsoon season..."

## 🚀 Your Agricultural AI Orchestra is Ready!

**Features:**
- ✅ Multi-agent coordination
- ✅ Prediction capabilities
- ✅ Priority-based responses
- ✅ Multi-language support
- ✅ Offline mode
- ✅ Comprehensive demos
- ✅ Real-time agent economy

**Perfect for:**
- Farmers and agricultural professionals
- Agricultural research and development
- Educational purposes
- Agricultural technology demonstrations
