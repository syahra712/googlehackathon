"""
Command-line interface for the Multi-Agent Agricultural AI System
"""
import os
import sys
from multi_agent_system import MultiAgentAgriculturalSystem
from config import OPENAI_API_KEY

def print_banner():
    """Print system banner"""
    print("=" * 80)
    print("🌾 AGRICULTURAL AI ORCHESTRA - Multi-Agent System")
    print("=" * 80)
    print("🤖 Specialized Agents:")
    print("   • Farm Resource Agent - Manages farm resources and equipment")
    print("   • Sensor Data Agent - Analyzes sensor readings and crop health")
    print("   • Market Intelligence Agent - Provides market analysis")
    print("   • Weather Agent - Processes weather and environmental data")
    print("   • Orchestrator Agent - Coordinates all agents")
    print("=" * 80)

def print_menu():
    """Print main menu"""
    print("\n📋 MAIN MENU:")
    print("1. 💬 Chat with AI Orchestra")
    print("2. 🏡 Analyze Specific Farm")
    print("3. 📈 Get Market Insights")
    print("4. 🌤️ Get Weather Forecast")
    print("5. 📊 View System Status")
    print("6. 🔧 View Data Summary")
    print("0. 🚪 Exit")
    print("-" * 50)

def chat_interface(system):
    """Interactive chat interface"""
    print("\n💬 CHAT INTERFACE")
    print("Type 'quit' to return to main menu")
    print("-" * 50)
    
    while True:
        query = input("\n🤔 Your question: ").strip()
        
        if query.lower() in ['quit', 'exit', 'back']:
            break
        
        if not query:
            continue
        
        print("\n🤖 AI Orchestra is thinking...")
        try:
            response = system.process_query(query)
            print(f"\n🤖 Response: {response['response']}")
            
            if 'context_used' in response and response['context_used']:
                print(f"\n📋 Context: {response['context_used'][:200]}...")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def farm_analysis(system):
    """Farm analysis interface"""
    print("\n🏡 FARM ANALYSIS")
    farm_id = input("Enter Farm ID (e.g., F-001): ").strip()
    
    if not farm_id:
        print("❌ Please enter a valid Farm ID")
        return
    
    print(f"\n🔍 Analyzing Farm {farm_id}...")
    try:
        analysis = system.get_farm_analysis(farm_id)
        
        if 'error' in analysis:
            print(f"❌ {analysis['error']}")
        else:
            print(f"\n📊 Analysis for Farm {farm_id}:")
            print(f"{analysis['analysis']}")
            print(f"\n📈 Metrics:")
            print(f"   • Sensor Records: {analysis['sensor_data_count']}")
            print(f"   • Analysis Time: {analysis['timestamp']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def market_insights(system):
    """Market insights interface"""
    print("\n📈 MARKET INSIGHTS")
    print("Available commodities: Wheat, Rice, Maize, Sugarcane, Cotton, Vegetables")
    commodity = input("Enter commodity (or press Enter for all): ").strip()
    
    print("Available locations: Lahore, Multan, Faisalabad, Karachi")
    location = input("Enter location (or press Enter for all): ").strip()
    
    print(f"\n📊 Analyzing market data...")
    try:
        insights = system.get_market_insights(
            commodity if commodity else None,
            location if location else None
        )
        
        if 'error' in insights:
            print(f"❌ {insights['error']}")
        else:
            print(f"\n📈 Market Analysis:")
            print(f"{insights['insights']}")
            print(f"\n📊 Metrics:")
            print(f"   • Commodity: {insights['commodity'] or 'All'}")
            print(f"   • Location: {insights['location'] or 'All'}")
            print(f"   • Data Points: {insights['data_points']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def weather_forecast(system):
    """Weather forecast interface"""
    print("\n🌤️ WEATHER FORECAST")
    location = input("Enter location/tehsil (or press Enter for all): ").strip()
    
    print(f"\n🌤️ Analyzing weather data...")
    try:
        forecast = system.get_weather_forecast(location if location else None)
        
        if 'error' in forecast:
            print(f"❌ {forecast['error']}")
        else:
            print(f"\n🌤️ Weather Analysis:")
            print(f"{forecast['forecast']}")
            print(f"\n📊 Metrics:")
            print(f"   • Location: {forecast['location'] or 'All'}")
            print(f"   • Data Points: {forecast['data_points']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def system_status(system):
    """Display system status"""
    print("\n📊 SYSTEM STATUS")
    try:
        status = system.get_system_status()
        
        print(f"🔧 System Status: {status['system_status']}")
        print(f"🤖 Agents Initialized: {status['agents_initialized']}")
        print(f"🎯 Orchestrator Status: {status['orchestrator_status']}")
        print(f"📚 RAG Collections: {', '.join(status['rag_collections'])}")
        
        if status['data_summary']:
            print(f"\n📊 Data Summary:")
            for data_type, summary in status['data_summary'].items():
                print(f"   • {data_type}: {summary}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def data_summary(system):
    """Display detailed data summary"""
    print("\n📊 DATA SUMMARY")
    try:
        status = system.get_system_status()
        data_summary = status['data_summary']
        
        if not data_summary:
            print("❌ No data summary available")
            return
        
        for data_type, summary in data_summary.items():
            print(f"\n📋 {data_type.upper()}:")
            for key, value in summary.items():
                if isinstance(value, list):
                    print(f"   • {key}: {', '.join(map(str, value[:5]))}{'...' if len(value) > 5 else ''}")
                else:
                    print(f"   • {key}: {value}")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main CLI function"""
    print_banner()
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY', OPENAI_API_KEY)
    if not api_key:
        print("❌ OpenAI API key not found!")
        print("Please set OPENAI_API_KEY environment variable or update config.py")
        return
    
    # Initialize system
    print("\n🚀 Initializing Multi-Agent System...")
    try:
        system = MultiAgentAgriculturalSystem(api_key)
        print("✅ System initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        return
    
    # Main loop
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (0-6): ").strip()
            
            if choice == '0':
                print("\n👋 Goodbye! Thank you for using Agricultural AI Orchestra!")
                break
            elif choice == '1':
                chat_interface(system)
            elif choice == '2':
                farm_analysis(system)
            elif choice == '3':
                market_insights(system)
            elif choice == '4':
                weather_forecast(system)
            elif choice == '5':
                system_status(system)
            elif choice == '6':
                data_summary(system)
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thank you for using Agricultural AI Orchestra!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
