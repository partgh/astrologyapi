# Vedic Astrology Calculation Engine API

A professional, high-precision Vedic Astrology API using `pyswisseph`.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ephemeris Files**:
    Download Swiss Ephemeris files (ext `.se1`) and place them in the `ephemeris/` directory.
    You can get them from [astro.com](ftp://ftp.astro.com/pub/swisseph/ephe/).
    (Note: `pyswisseph` may work with internal defaults for 3000BC-3000AD without external files, but for high precision and speed, external files are recommended).
    
    *Important*: The application is configured to look for ephemeris files in the `ephemeris/` directory relative to the project root.

3.  **Run the API**:
    ```bash
    uvicorn app.main:app --reload
    ```

## Features

-   **Sidereal Zodiac**: Lahiri Ayanamsa.
-   **Planetary Positions**: Sun to Pluto, True Rahu, Ketu.
-   **Houses**: Sripati House System (Ascendant based).
-   **Nakshatras**: Accurate 27 Nakshatra division with Pada.
-   **Vimshottari Dasha**: Classic 120-year cycle.
-   **Aspects**: Vedic aspects including special aspects for Mars, Jupiter, Saturn.

## API Usage

**POST /get_chart**

```json
{
  "year": 2023,
  "month": 10,
  "day": 25,
  "hour": 14,
  "minute": 30,
  "second": 0,
  "timezone": "Asia/Kolkata",
  "latitude": 28.6139,
  "longitude": 77.2090
}
```
