from core.models import UserPreference, TripOption
from core.search import search_trips, get_all_trips
from core.scoring import score_trips
from datetime import datetime

def test_core_logic():
    # 1. Test Search
    print("Testing Search...")
    paris_trips = search_trips("Paris")
    assert len(paris_trips) >= 1
    assert "Paris" in paris_trips[0].destination
    print(f"Found {len(paris_trips)} trips for 'Paris'. Check passed.")

    # 2. Test Scoring
    print("\nTesting Scoring...")
    all_trips = get_all_trips()
    prefs = UserPreference(
        destination_keywords=["beach", "relaxing"],
        budget_max=1000.0,
        duration_days=14
    )
    
    scored = score_trips(all_trips, prefs)
    top_pick = scored[0]
    print(f"Top pick: {top_pick.destination} (Score: {top_pick.score})")
    
    # Bali should be top because it matches 'beach', is under 1000, and is 14 days
    assert "Bali" in top_pick.destination
    print("Scoring logic Check passed.")

if __name__ == "__main__":
    test_core_logic()
