import subprocess
import time
import requests
import sys
import json

def run_test():
    # Start the server
    print("Starting server...")
    process = subprocess.Popen(
        [sys.executable, "-m", "app.main"],
        cwd="c:/Users/lenovo/Desktop/self made kundli engine",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is not None:
            print("Server failed to start!")
            stdout, stderr = process.communicate()
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            return

        # Prepare request
        payload = {
            "year": 2023,
            "month": 1,
            "day": 17, # Saturn in Aquarius, Moon in Libra/Scorpio? Let's use a date where Saturn aspects Moon. 
            # Actually just any date to see the format is fine.
            # User example: Saturn aspects Moon (3rd). 
            # Saturn in Aquarius (approx Jan 2023+). Moon in Aries/Pisces?
            # Let's just use the date 2023-01-17 12:00
            "hour": 12,
            "minute": 0,
            "second": 0,
            "timezone": "Asia/Kolkata",
            "latitude": 28.6139,
            "longitude": 77.2090
        }
        
        print("Sending request to http://127.0.0.1:8000/get_chart ...")
        try:
            response = requests.post("http://127.0.0.1:8000/get_chart", json=payload)
            response.raise_for_status()
            data = response.json()
            
            print("\n--- API Response Aspects ---")
            aspects = data.get("aspects", [])
            for aspect in aspects:
                print(aspect)
                
            print("\n--- Check for expected fields ---")
            if aspects:
                first = aspects[0]
                if "angle" in first and "orb" in first and "house_distance" not in first:
                    print("SUCCESS: Schema matches expected format.")
                else:
                    print("FAILURE: Schema does not match expected format.")
            else:
                 print("WARNING: No aspects found for this date. Try another date.")

        except requests.exceptions.ConnectionError:
            print("Failed to connect to server.")
        except Exception as e:
            print(f"Request failed: {e}")
            if response:
                print(response.text)

    finally:
        print("Stopping server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        
        # Print logs if any specific error occurred or just to see
        # stdout, stderr = process.communicate()
        # print("Server Output:", stdout)

if __name__ == "__main__":
    run_test()
