import requests

# URL for the login endpoint
url = "http://127.0.0.1:5000/login"

# Replace these with the actual username and password
payload = {
    "username": "CapstoneUser",
    "password": "lewisuniversitysummer2024"
}

# Send a POST request to the login endpoint
response = requests.post(url, data=payload)

# Print the response
if response.status_code == 200:
    print("Login successful!")
else:
    print(f"Login failed: {response.status_code}")
    print(response.text)
