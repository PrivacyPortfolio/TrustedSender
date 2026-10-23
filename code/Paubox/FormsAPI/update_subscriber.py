# /code/update_subscriber.py
# Paubox Marketing API
# Updates a subscriber record
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/subscribers/{subscriber_id}"

payload = { "subscriber": {
        "email": "jsmith@example.com",
        "phone_number": "<string>",
        "first_name": "<string>",
        "last_name": "<string>"
    } }
headers = {
    "authorization": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)

# 
# HTTP 200:
# {
  "data": {
    "id": "<string>",
    "type": "subscriber",
    "attributes": {
      "email": "jsmith@example.com",
      "unsubscribed": true,
      "first_name": "<string>",
      "last_name": "<string>"
    }
  }
}

# 
