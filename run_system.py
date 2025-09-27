#!/usr/bin/env python3
"""
Startup script for the Agricultural AI Orchestra
"""
import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import openai
        import pandas
        import numpy
        import streamlit
        import chromadb
        import sentence_transformers
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_data_files():
    """Check if all data files exist"""
    required_files = [
        "farm_resources.json",
        "farm_sensor_data_tehsil_with_date.json", 
        "market_prices copy.csv",
        "weather_data_tehsil copy.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing data files: {', '.join(missing_files)}")
        return False
    
    print("✅ All data files found")
    return True

def check_api_key():
    """Check if OpenAI API key is configured"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key not found")
        print("Please set OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY='your_key_here'")
        return False
    
    print("✅ OpenAI API key configured")
    return True

def main():
    """Main startup function"""
    print("🌾 Agricultural AI Orchestra - Startup Check")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check data files
    if not check_data_files():
        sys.exit(1)
    
    # Check API key
    if not check_api_key():
        sys.exit(1)
    
    print("\n🚀 All checks passed! Starting system...")
    print("\nChoose your interface:")
    print("1. 🌐 Web Interface (Streamlit)")
    print("2. 💻 Command Line Interface")
    print("3. 🔧 System Test")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        print("\n🌐 Starting Streamlit web interface...")
        subprocess.run(["streamlit", "run", "chatbot_interface.py"])
    elif choice == '2':
        print("\n💻 Starting command line interface...")
        subprocess.run([sys.executable, "cli_interface.py"])
    elif choice == '3':
        print("\n🔧 Running system test...")
        try:
            from multi_agent_system import MultiAgentAgriculturalSystem
            system = MultiAgentAgriculturalSystem()
            status = system.get_system_status()
            print("✅ System test passed!")
            print(f"Status: {status}")
        except Exception as e:
            print(f"❌ System test failed: {e}")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
