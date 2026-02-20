NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# 7. Nakshatra & Pada Precision - Exact Constants
NAKSHATRA_SIZE = 13.333333333333334
PADA_SIZE = 3.3333333333333335

def get_nakshatra(longitude: float):
    """
    Calculates Nakshatra and Pada for a given longitude using exact precision constants.
    """
    # Normalize longitude 0-360
    longitude = longitude % 360.0
    
    # 6. Do NOT round Nakshatra degrees
    nak_index = int(longitude / NAKSHATRA_SIZE)
    nak_name = NAKSHATRAS[nak_index]
    
    # Degrees traversed in current nakshatra
    rem_deg = longitude % NAKSHATRA_SIZE
    
    pada = int(rem_deg / PADA_SIZE) + 1
    
    # Percentage traversal
    traversal_percentage = (rem_deg / NAKSHATRA_SIZE)
    
    return {
        "id": nak_index + 1,
        "name": nak_name,
        "pada": pada,
        "fraction_traversed": traversal_percentage, # Full precision
        "degrees_in_nakshatra": rem_deg # Full precision
    }
