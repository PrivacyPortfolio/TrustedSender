# /code/create_subscription_list.py
# Paubox Marketing API
# Creates a subscription list record
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/subscription_lists"

payload = { "name": "Newsletter Subscribers" }
headers = {
    "authorization": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

# 
# 
# HTTP 200:
{
  "data": {
    "id": "<string>",
    "type": "subscription_list",
    "attributes": {
      "name": "<string>",
      "is_default": true,
      "subscriber_count": 123,
      "form_id": "<string>"
    }
  }
}

# 
