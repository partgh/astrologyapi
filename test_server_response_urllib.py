import urllib.request
import urllib.error
import json
import time
import sys

def run_verify():
    url = "http://127.0.0.1:8000/get_chart"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "year": 2023,
        "month": 1,
        "day": 17,
        "hour": 12,
        "minute": 0,
        "second": 0,
        "timezone": "Asia/Kolkata",
        "latitude": 28.6139,
        "longitude": 77.2090
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    
    # Retry loop to wait for server
    for i in range(10):
        try:
            print(f"Attempt {i+1}: Sending request...")
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    body = response.read().decode('utf-8')
                    json_data = json.loads(body)
                    
                    print("\n--- API Response Aspects ---")
                    aspects = json_data.get("aspects", [])
                    # Limit output
                    for aspect in aspects[:5]:
                        print(aspect)
                    if len(aspects) > 5:
                        print(f"... and {len(aspects)-5} more.")

                    if aspects:
                        first = aspects[0]
                        if "angle" in first and "orb" in first and "house_distance" not in first:
                            print("\nSUCCESS: Schema matches expected format.")
                            sys.exit(0)
                        else:
                            print("\nFAILURE: Schema does not match expected format.")
                            print("First aspect keys:", first.keys())
                            sys.exit(1)
                    else:
                        print("WARNING: No aspects found.")
                        sys.exit(0) 

        except urllib.error.URLError as e:
            print(f"Connection failed: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
            
    print("Could not connect to server after 10 attempts.")
    sys.exit(1)

if __name__ == "__main__":
    run_verify()
