# /code/create_subscription.py
# Paubox Marketing API
# Subscribes an existing subscriber to an existing subscription list.
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/subscriptions"

payload = { "subscription": {
        "subscription_list_id": "123e4567-e89b-12d3-a456-426614174000",
        "subscriber_id": 4821
    } }
headers = {
    "authorization": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

# 
# HTTP 200:
{
  "data": {
    "id": 123,
    "uuid": "<string>",
    "subscription_list_id": "<string>",
    "dynamic_list_id": 123,
    "subscriber_id": 123,
    "unsubscribed_at": "2023-11-07T05:31:56Z",
    "delete_at": "2023-11-07T05:31:56Z",
    "created_at": "2023-11-07T05:31:56Z",
    "updated_at": "2023-11-07T05:31:56Z"
  },
  "errors": [
    "<string>"
  ]
}

# 
# 
# 
