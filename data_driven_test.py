"""
Data-Driven Test Questions - Tests that responses are based on YOUR datasets
"""
import json
import pandas as pd

def load_test_data():
    """Load your actual data for testing"""
    try:
        # Load farm data
        with open('farm_resources.json', 'r') as f:
            farms = json.load(f)
        
        # Load sensor data
        with open('farm_sensor_data_tehsil_with_date.json', 'r') as f:
            sensors = json.load(f)
        
        # Load market data
        market = pd.read_csv('market_prices copy.csv')
        
        # Load weather data
        weather = pd.read_csv('weather_data_tehsil copy.csv')
        
        return {
            'farms': farms,
            'sensors': sensors,
            'market': market,
            'weather': weather
        }
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

def get_data_insights(data):
    """Get insights from your actual data"""
    insights = {}
    
    if 'farms' in data:
        farms = data['farms']
        insights['farms'] = {
            'total': len(farms),
            'avg_irrigation': sum(f['irrigation_hours_per_week'] for f in farms) / len(farms),
            'avg_fertilizer': sum(f['fertilizer_kg_available'] for f in farms) / len(farms),
            'total_tractor_hours': sum(f['equipment_availability']['tractor_hours'] for f in farms),
            'total_harvester_hours': sum(f['equipment_availability']['harvester_hours'] for f in farms)
        }
    
    if 'sensors' in data:
        sensors = data['sensors']
        insights['sensors'] = {
            'total': len(sensors),
            'avg_soil_moisture': sum(s['soil_moisture_%'] for s in sensors) / len(sensors),
            'avg_temperature': sum(s['temperature_c'] for s in sensors) / len(sensors),
            'pest_detections': len([s for s in sensors if s['pest_detection'] != 'None'])
        }
    
    if 'market' in data:
        market = data['market']
        insights['market'] = {
            'total': len(market),
            'commodities': market['commodity'].unique().tolist(),
            'locations': market['market_location'].unique().tolist(),
            'avg_wheat_price': market[market['commodity'] == 'Wheat']['avg_price_pkr_per_40kg'].mean(),
            'high_demand': len(market[market['demand_status'] == 'High'])
        }
    
    if 'weather' in data:
        weather = data['weather']
        insights['weather'] = {
            'total': len(weather),
            'provinces': weather['province'].unique().tolist(),
            'avg_rainfall': weather['rainfall_mm'].mean(),
            'avg_temperature': weather['temperature_c'].mean(),
            'extreme_events': weather['extreme_event'].value_counts().to_dict()
        }
    
    return insights

def print_data_driven_tests():
    """Print test questions that verify data-driven responses"""
    
    print("🌾 DATA-DRIVEN AGRICULTURAL AI ORCHESTRA - TEST SUITE")
    print("=" * 80)
    print("🎯 GOAL: Verify that ALL responses are based on YOUR actual datasets")
    print("=" * 80)
    
    # Load your data
    data = load_test_data()
    if not data:
        print("❌ Could not load your data files")
        return
    
    # Get insights from your data
    insights = get_data_insights(data)
    
    print("\n📊 YOUR DATASET INSIGHTS:")
    print("-" * 40)
    if 'farms' in insights:
        print(f"🏡 FARMS: {insights['farms']['total']} farms")
        print(f"   • Avg Irrigation: {insights['farms']['avg_irrigation']:.1f} hours/week")
        print(f"   • Avg Fertilizer: {insights['farms']['avg_fertilizer']:.1f} kg")
        print(f"   • Total Tractor Hours: {insights['farms']['total_tractor_hours']}")
        print(f"   • Total Harvester Hours: {insights['farms']['total_harvester_hours']}")
    
    if 'sensors' in insights:
        print(f"📡 SENSORS: {insights['sensors']['total']} readings")
        print(f"   • Avg Soil Moisture: {insights['sensors']['avg_soil_moisture']:.1f}%")
        print(f"   • Avg Temperature: {insights['sensors']['avg_temperature']:.1f}°C")
        print(f"   • Pest Detections: {insights['sensors']['pest_detections']}")
    
    if 'market' in insights:
        print(f"💰 MARKET: {insights['market']['total']} records")
        print(f"   • Commodities: {', '.join(insights['market']['commodities'])}")
        print(f"   • Locations: {', '.join(insights['market']['locations'])}")
        print(f"   • Avg Wheat Price: {insights['market']['avg_wheat_price']:.2f} PKR/40kg")
        print(f"   • High Demand Records: {insights['market']['high_demand']}")
    
    if 'weather' in insights:
        print(f"🌤️ WEATHER: {insights['weather']['total']} records")
        print(f"   • Provinces: {', '.join(insights['weather']['provinces'])}")
        print(f"   • Avg Rainfall: {insights['weather']['avg_rainfall']:.1f}mm")
        print(f"   • Avg Temperature: {insights['weather']['avg_temperature']:.1f}°C")
        print(f"   • Extreme Events: {insights['weather']['extreme_events']}")
    
    print("\n" + "=" * 80)
    print("🧪 DATA-DRIVEN TEST QUESTIONS")
    print("=" * 80)
    
    test_questions = {
        "🏡 FARM RESOURCE TESTS (Must reference YOUR farm data)": [
            f"Analyze farm F-001 from my dataset. What are its specific irrigation hours, fertilizer amount, and equipment availability?",
            f"Which farms in my dataset have the highest irrigation hours? Show me the actual numbers.",
            f"Compare the equipment utilization across my farms. Which ones have the most tractor hours available?",
            f"What's the fertilizer distribution pattern in my dataset? Which farms need more nutrients?",
            f"Show me the neighboring farm relationships in my dataset. How are farms connected?"
        ],
        
        "📡 SENSOR DATA TESTS (Must reference YOUR sensor data)": [
            f"What's the average soil moisture level in my sensor data? Show me the actual percentage.",
            f"Which farms in my dataset have pest detection issues? Show me the specific records.",
            f"Analyze the temperature patterns in my sensor data. What's the range and average?",
            f"Show me the humidity levels affecting crops in my dataset. Which farms have optimal conditions?",
            f"What crop types are monitored in my sensor data? Show me the distribution."
        ],
        
        "💰 MARKET DATA TESTS (Must reference YOUR market data)": [
            f"What's the current wheat price in Lahore according to my market data? Show me the exact numbers.",
            f"Which commodities in my dataset have the highest demand? Show me the actual demand status counts.",
            f"Compare rice prices across different locations in my market data. Where are prices highest?",
            f"What's the price range for cotton in my dataset? Show me min, max, and average prices.",
            f"Which market locations in my data have the most trading activity? Show me the record counts."
        ],
        
        "🌤️ WEATHER DATA TESTS (Must reference YOUR weather data)": [
            f"What extreme weather events are recorded in my weather data? Show me the actual counts.",
            f"Which provinces in my dataset have the most rainfall? Show me the specific amounts.",
            f"Analyze the temperature patterns in my weather data. What's the range across provinces?",
            f"Show me the drought and flood risk areas in my weather dataset. Which regions are affected?",
            f"What's the humidity distribution in my weather data? Which areas have optimal conditions?"
        ],
        
        "🔄 MULTI-AGENT COORDINATION TESTS (Must use ALL your data)": [
            f"Give me a comprehensive analysis using ALL my datasets: farms, sensors, markets, and weather. Show me the actual data points.",
            f"Analyze farm F-001 using my sensor data, market opportunities, and weather conditions. Use my actual data.",
            f"Which farms in my dataset are performing best overall? Consider my resource data, sensor readings, market access, and weather impact.",
            f"Show me the correlation between my weather data and market prices. Use my actual datasets.",
            f"Provide strategic recommendations based on my complete agricultural dataset. Use real numbers and patterns."
        ],
        
        "📊 SPECIFIC DATA POINT TESTS (Must show exact values)": [
            f"What's the exact irrigation hours for farm F-001 in my dataset?",
            f"Show me the precise soil moisture reading for farm F-002 on the most recent date in my sensor data.",
            f"What's the exact wheat price in Lahore on the latest date in my market data?",
            f"Show me the specific rainfall amount for Punjab on the most recent date in my weather data.",
            f"What's the exact fertilizer amount available for farm F-003 in my dataset?"
        ]
    }
    
    for category, questions in test_questions.items():
        print(f"\n{category}")
        print("-" * 60)
        for i, question in enumerate(questions, 1):
            print(f"{i:2d}. {question}")
    
    print("\n" + "=" * 80)
    print("✅ SUCCESS CRITERIA - Responses MUST include:")
    print("=" * 80)
    print("• Specific numbers from YOUR datasets")
    print("• Actual farm IDs from your data (F-001, F-002, etc.)")
    print("• Real commodity prices from your market data")
    print("• Actual weather readings from your weather data")
    print("• Precise sensor readings from your sensor data")
    print("• References to your specific locations (Lahore, Multan, Punjab, etc.)")
    print("• Data-driven insights based on YOUR patterns and trends")
    print("• NO generic agricultural advice - ONLY your data analysis")
    
    print("\n🚀 HOW TO TEST:")
    print("1. Open: http://localhost:8501")
    print("2. Use the 'Data-Driven Chat' tab")
    print("3. Ask questions from the test suite above")
    print("4. Verify responses contain YOUR actual data points")
    print("5. Ensure AI analyzes YOUR datasets, not generic information")
    
    print("\n🎯 EXPECTED RESPONSE FORMAT:")
    print("✅ 'Based on your dataset of 1,400 farms...'")
    print("✅ 'Farm F-001 in your data has 16 irrigation hours...'")
    print("✅ 'Your wheat prices in Lahore average 1,955 PKR...'")
    print("✅ 'Your sensor data shows 53% soil moisture...'")
    print("❌ 'Generally, farms need irrigation...' (Generic advice)")
    print("❌ 'Wheat prices are typically...' (Generic information)")

if __name__ == "__main__":
    print_data_driven_tests()
