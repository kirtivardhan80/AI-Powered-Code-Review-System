import requests

# FastAPI server URL
url = "http://127.0.0.1:8000/review"

# Payload you want to test
payload = {
    "code": "def add(a, b): return a+b"
}

# Send POST request
response = requests.post(url, json=payload)

# Print status and result
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
