from typing import List
from .models import TripOption, UserPreference

def score_trips(trips: List[TripOption], preferences: UserPreference) -> List[TripOption]:
    """
    Scores trips based on user preferences.
    """
    scored_trips = []
    for trip in trips:
        score = 0.0
        
        # Budget match
        if preferences.budget_max:
            if trip.cost <= preferences.budget_max:
                score += 10.0
            else:
                score -= 5.0 # Penalty for over budget
        
        # Destination keywords match
        for keyword in preferences.destination_keywords:
            if keyword.lower() in trip.destination.lower() or keyword.lower() in trip.description.lower():
                score += 5.0
                
        # Duration match (if specified, exact match bonus, close match smaller bonus)
        if preferences.duration_days:
            if trip.duration_days == preferences.duration_days:
                score += 5.0
            elif abs(trip.duration_days - preferences.duration_days) <= 2:
                score += 2.0
                
        trip.score = score
        scored_trips.append(trip)
        
    # Sort by score descending
    scored_trips.sort(key=lambda x: x.score if x.score is not None else -float('inf'), reverse=True)
    return scored_trips
