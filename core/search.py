from typing import List, Optional
from .models import TripOption, UserPreference

# Mock database of trips
MOCK_TRIPS = [
    TripOption(id="1", destination="Paris, France", cost=1200.0, duration_days=7, description="Romantic getaway in Paris with Eiffel Tower tour."),
    TripOption(id="2", destination="Tokyo, Japan", cost=2000.0, duration_days=10, description="Tech and culture tour in Tokyo."),
    TripOption(id="3", destination="Bali, Indonesia", cost=800.0, duration_days=14, description="Relaxing beach vacation in Bali."),
    TripOption(id="4", destination="New York, USA", cost=1500.0, duration_days=5, description="City that never sleeps experience."),
    TripOption(id="5", destination="Rome, Italy", cost=1300.0, duration_days=8, description="Historical tour of Rome."),
]

def search_trips(query: str, max_price: Optional[float] = None) -> List[TripOption]:
    """
    Simulates searching for trips based on a query string and optional max price.
    """
    query = query.lower()
    results = []
    for trip in MOCK_TRIPS:
        if max_price and trip.cost > max_price:
            continue
        
        # Simple keyword matching
        if query in trip.destination.lower() or query in trip.description.lower():
            results.append(trip)
            
    return results

def get_all_trips() -> List[TripOption]:
    return MOCK_TRIPS
