"""
Demo queries for the Agricultural AI Orchestra
"""
import openai

# Set your OpenAI API key

def demo_queries():
    """Demo some example queries"""
    
    demo_questions = [
        "What are the best irrigation practices for wheat farming?",
        "How is the rice market performing in Lahore?",
        "What weather conditions should I watch for this season?",
        "Analyze farm F-001 and provide optimization recommendations",
        "What are the current wheat prices and demand trends?",
        "How is the weather affecting crop yields in Punjab?",
        "What equipment should I prioritize for my farm?",
        "Which crops are most profitable in the current market?",
        "How can I optimize my irrigation schedule?",
        "What pest management strategies should I use?"
    ]
    
    print("🌾 Agricultural AI Orchestra - Demo Queries")
    print("=" * 50)
    print("\nHere are some example questions you can ask:")
    
    for i, question in enumerate(demo_questions, 1):
        print(f"{i:2d}. {question}")
    
    print("\n" + "=" * 50)
    print("🚀 Your app is running at: http://localhost:8501")
    print("💡 Try these questions in the web interface!")
    print("=" * 50)

if __name__ == "__main__":
    demo_queries()
