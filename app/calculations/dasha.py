from datetime import datetime, timedelta, timezone

# Dasha Sequence and Duration (Years)
DASHA_SYSTEM = [
    ("Ketu", 7),
    ("Venus", 20),
    ("Sun", 6),
    ("Moon", 10),
    ("Mars", 7),
    ("Rahu", 18),
    ("Jupiter", 16),
    ("Saturn", 19),
    ("Mercury", 17)
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

# Constants
NAKSHATRA_SIZE = 13.333333333333334

def get_vimshottari_dasha(moon_longitude: float, birth_date: datetime):
    """
    Calculates the Vimshottari Dasha balance and current operating dasha.
    8. Vimshottari Dasha Precision:
    - Exact fractional remaining
    - Exact multiplication
    - No integer rounding
    - UTC arithmetic
    """
    moon_longitude = moon_longitude % 360.0
    
    nak_index = int(moon_longitude / NAKSHATRA_SIZE)
    rem_deg = moon_longitude % NAKSHATRA_SIZE
    fraction_traversed = rem_deg / NAKSHATRA_SIZE
    
    # 8. Exact fractional remaining
    fraction_remaining = 1.0 - fraction_traversed
    
    lord_name = NAKSHATRA_LORDS[nak_index]
    
    total_years = 0
    for name, years in DASHA_SYSTEM:
        if name == lord_name:
            total_years = years
            break
            
    # 8. Exact multiplication
    balance_years = total_years * fraction_remaining
    
    # 8. All date arithmetic must use UTC internally
    # We assume birth_date is already UTC or aware. 
    # If naive, we treat as UTC or rely on external conversion.
    # Best practice: convert days to seconds for precision or use timedelta.
    
    # 1 year = 365.25 days (Julian Year) or 365.2425?
    # Swiss Ephemeris uses Julian Days (365.25 avg).
    # Common Practice: 365.25 days.
    days_balance = balance_years * 365.25
    
    # Current dasha end date
    # Ensure birth_date is aware
    if birth_date.tzinfo is None:
        birth_date = birth_date.replace(tzinfo=timezone.utc)
    
    current_dasha_end_date = birth_date + timedelta(days=days_balance)
    
    return {
        "birth_nakshatra_index": nak_index + 1,
        "birth_dasha_lord": lord_name,
        "total_dasha_years": total_years,
        "fraction_left": fraction_remaining, # Full Float
        "balance_years": balance_years, # Full Float
        "current_dasha_end_date": current_dasha_end_date.isoformat(),
    }
