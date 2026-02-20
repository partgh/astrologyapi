import json
import urllib.error
import urllib.request


def main():
    payload = {
        "year": 2009,
        "month": 4,
        "day": 12,
        "hour": 7,
        "minute": 23,
        "second": 0,
        "timezone": "Asia/Kolkata",
        "latitude": 28.4089,
        "longitude": 77.3178
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "http://127.0.0.1:8000/get_chart",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            print("status_code:", response.status)
            print("response:")
            print(body)
    except urllib.error.HTTPError as err:
        print("status_code:", err.code)
        print("response:")
        print(err.read().decode("utf-8"))
    except urllib.error.URLError as err:
        print("request_error:", str(err))


if __name__ == "__main__":
    main()
