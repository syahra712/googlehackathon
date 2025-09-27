#!/bin/bash

echo "🚀 Pushing Agricultural AI Orchestra to GitHub..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Initializing..."
    git init
fi

# Add all files
echo "📁 Adding all files..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "🌾 Agricultural AI Orchestra - Multi-Agent ADK with Prediction Capabilities

✨ Features:
- Multi-agent coordination with 5 specialized agents
- Agent-to-agent economy with credit system
- Intelligent chat with follow-up questions
- Prediction capabilities for weather, market, crops, pests, irrigation
- Priority-based responses (dataset first, general knowledge second)
- Chain-of-thought reasoning
- Multi-language support (Urdu/English)
- Automatic offline mode
- Comprehensive demo scenarios
- Real-time agent coordination

📊 Data Sources:
- 1,400+ farms with resource data
- 36,000+ sensor readings
- 1,800+ market records
- 1,800+ weather records

🎯 Ready for Streamlit Cloud deployment!"

# Set up remote (you'll need to replace with your actual GitHub username)
echo "🔗 Setting up remote repository..."
echo "Please create a repository on GitHub first:"
echo "1. Go to https://github.com/new"
echo "2. Repository name: agricultural-ai-orchestra"
echo "3. Make it public"
echo "4. Don't initialize with README"
echo "5. Click Create repository"
echo ""
echo "Then run:"
echo "git remote add origin https://github.com/YOUR_USERNAME/agricultural-ai-orchestra.git"
echo "git push -u origin master"

echo "✅ Ready to push to GitHub!"
