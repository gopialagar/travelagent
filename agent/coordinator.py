import google.generativeai as genai
import os
import sys

# Import tools directly
# In a real MCP setup, we would connect to the MCP server.
# Here we import the functions directly to simulate tool usage.
# We might need to mock or stub if dependencies are missing.
try:
    from tools.server import find_trips, score_and_recommend
except ImportError:
    # If fastmcp fails to import in this environment, define mocks
    print("Warning: Could not import tools.server. Using mocks.")
    def find_trips(query: str, max_price: float = None) -> str:
        return "Mock functionality for find_trips"
    def score_and_recommend(trip_ids: list, preferences: dict) -> str:
        return "Mock functionality for score_and_recommend"

# Configure the API key
# Ideally, this should be an environment variable.
if "GOOGLE_API_KEY" not in os.environ:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    # Assuming for now we can't run without key, we will exit or mock
    # sys.exit(1) 

def run_agent():
    print("Initializing Agent...")
    
    # Define tools for the model
    tools = [find_trips, score_and_recommend]
    
    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-pro-latest',
            tools=tools,
             system_instruction="""You are an expert travel agent. Your goal is to provide a personalized travel recommendation.
            
            Follow this process:
            1.  **Analyze the User's Request**: Is it specific enough? Do you know their budget, duration, and preferences?
            2.  **Gather Information**: If the request is vague, ask clarifying questions. 
            3.  **Search & Filter**: Use `find_trips` to find options based on their input.
            4.  **Score & Select**: Use `score_and_recommend` to rank the best options based on user preferences.
            5.  **Present Recommendation**: meaningful, detailed recommendation explaining WHY it's the best fit.
            
            Always be polite and helpful.
            """
        )
        chat = model.start_chat(enable_automatic_function_calling=True)
        
        print("Agent ready. Type 'quit' to exit.")
        while True:
            user_input = input("User: ")
            if user_input.lower() in ['quit', 'exit']:
                break
            
            response = chat.send_message(user_input)
            print(f"Agent: {response.text}")
            
    except Exception as e:
        print(f"Error running agent: {e}")

if __name__ == "__main__":
    run_agent()
