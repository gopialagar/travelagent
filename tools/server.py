try:
    from fastmcp import FastMCP
except ImportError:
    # Mock FastMCP for environments without it installed
    class FastMCP:
        def __init__(self, name):
             self.name = name
        def tool(self):
            def decorator(func):
                return func
            return decorator
    print("Warning: FastMCP not installed. Using mock.")

from typing import List, Dict, Any, Optional
from core.models import UserPreference, TripOption, Recommendation
from core.search import search_trips, get_all_trips
from core.scoring import score_trips
from datetime import datetime

# Initialize FastMCP Server
mcp = FastMCP("TravelAgent")

@mcp.tool()
def find_trips(query: str, max_price: Optional[float] = None) -> str:
    """
    Search for trips based on a destination or interest query.
    Args:
        query: Destination name or keyword (e.g., "Paris", "beach")
        max_price: Optional maximum price per person
    """
    results = search_trips(query, max_price)
    if not results:
        return "No trips found matching your criteria."
    
    # Format as string for the model
    output = "Found the following trips:\n"
    for r in results:
        output += f"- [ID: {r.id}] {r.destination} (${r.cost}): {r.description}\n"
    return output

@mcp.tool()
def score_and_recommend(trip_ids: List[str], preferences: Dict[str, Any]) -> str:
    """
    Score a list of trips against user preferences and return the top recommendations.
    Args:
        trip_ids: List of trip IDs to score (e.g., ["1", "3"])
        preferences: Dictionary of user preferences. Keys should match UserPreference model:
                     - destination_keywords: List[str]
                     - budget_max: float
                     - start_date: str (ISO format)
                     - duration_days: int
    """
    # 1. Fetch trips
    all_trips = get_all_trips()
    target_trips = [t for t in all_trips if t.id in trip_ids]
    
    if not target_trips:
        return "No valid trips found for the provided IDs."

    # 2. Parse preferences
    try:
        # Handle date parsing if needed, for now assuming string or None
        # In a real app, we'd parse ISO strings to datetime
        prefs = UserPreference(**preferences)
    except Exception as e:
        return f"Error parsing preferences: {str(e)}"

    # 3. Score
    scored = score_trips(target_trips, prefs)
    
    # 4. Format Output
    output = "Ranked Recommendations:\n"
    for trip in scored:
        output += f"1. {trip.destination} (Score: {trip.score})\n   Cost: ${trip.cost}, Duration: {trip.duration_days} days\n   Description: {trip.description}\n"
        
    return output

if __name__ == "__main__":
    mcp.run()
