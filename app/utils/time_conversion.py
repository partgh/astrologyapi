import swisseph as swe
from datetime import datetime
import pytz

def get_julian_day(year: int, month: int, day: int, hour: int, minute: int, second: int, timezone_str: str) -> float:
    """
    Converts local date and time to Julian Day (ET/UT).
    """
    try:
        local_tz = pytz.timezone(timezone_str)
    except pytz.UnknownTimeZoneError:
        raise ValueError(f"Unknown timezone: {timezone_str}")

    # Create timezone-aware datetime object
    dt_local = local_tz.localize(datetime(year, month, day, hour, minute, second))
    
    # Convert to UTC
    dt_utc = dt_local.astimezone(pytz.UTC)
    
    # Calculate fractional hour for Swiss Ephemeris
    # swe.julday expects UT time
    hour_utc = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    
    julian_day = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_utc)
    
    return julian_day
